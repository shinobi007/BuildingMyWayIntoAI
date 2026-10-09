#!/usr/bin/env python3
"""
ProofLoop Role Deep Analysis v0.16

Consumes the v0.15 transparency report plus proofloop_enriched.db and performs
requirement-level analysis for the roles most relevant to Application #001.

This script deliberately does NOT choose the final top five. It produces a
transparent decision-review pool that can be compared with the v0.15 report.

Inputs (defaults):
    proofloop_role_analysis_report_v0_15.json
    proofloop_enriched.db

Outputs:
    proofloop_role_deep_analysis_report_v0_16.md
    proofloop_role_deep_analysis_report_v0_16.json

Design principles:
- database is opened read-only
- v0.15 role IDs/counts are cross-checked against the database
- strong sales roles are excluded from the actual candidate pool
- US-remote, ambiguous remote, and relocation-supported paths remain distinct
- qualifications are parsed line-by-line instead of matching arbitrary words
  such as "requirements" inside ordinary prose
- posted expectations are compared against evidence tiers:
    DIRECT_WORK_EVIDENCE
    RESUME_SKILL_CLAIM
    ADJACENT_EVIDENCE
    NOT_EVIDENCED
    UNKNOWN
- a requirement can be tagged as a major gap without declaring the user
  incapable of learning it; it means the current evidence does not establish it
- no opaque fit score is used
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


VERSION = "ProofLoop Role Deep Analysis v0.16"
EXPECTED_BASELINE = "ProofLoop Role Selection Transparency Battery v0.15"

# ---------------------------------------------------------------------------
# User evidence model
# ---------------------------------------------------------------------------
# This is intentionally conservative. "DIRECT_WORK_EVIDENCE" means the resume
# describes real work in the area. "RESUME_SKILL_CLAIM" means the skill is listed
# but the resume does not by itself prove years of production depth.

EVIDENCE_TIER_ORDER = {
    "DIRECT_WORK_EVIDENCE": 0,
    "RESUME_SKILL_CLAIM": 1,
    "ADJACENT_EVIDENCE": 2,
    "NOT_EVIDENCED": 3,
    "UNKNOWN": 4,
}

DOMAIN_EVIDENCE_TIERS: dict[str, str] = {
    # Strongly documented work history.
    "technical_support": "DIRECT_WORK_EVIDENCE",
    "troubleshooting_incidents": "DIRECT_WORK_EVIDENCE",
    "api_integrations": "DIRECT_WORK_EVIDENCE",
    "automation_workflows": "DIRECT_WORK_EVIDENCE",
    "ticketing_itsm": "DIRECT_WORK_EVIDENCE",
    "documentation_training": "DIRECT_WORK_EVIDENCE",
    "uat_qa_bug": "DIRECT_WORK_EVIDENCE",
    "crm_saas": "DIRECT_WORK_EVIDENCE",
    "basic_network_dns": "DIRECT_WORK_EVIDENCE",
    "process_improvement": "DIRECT_WORK_EVIDENCE",
    "technical_customer_communication": "DIRECT_WORK_EVIDENCE",

    # Listed as skills, but not treated as proof of professional production depth.
    "python_scripting": "RESUME_SKILL_CLAIM",
    "javascript_scripting": "RESUME_SKILL_CLAIM",
    "sql_data": "RESUME_SKILL_CLAIM",
    "powershell_bash": "RESUME_SKILL_CLAIM",
    "web_frontend": "RESUME_SKILL_CLAIM",

    # Related background, but the current resume does not establish the full domain.
    "systems_operations": "ADJACENT_EVIDENCE",
    "identity_device_management": "ADJACENT_EVIDENCE",
    "technical_program_delivery": "ADJACENT_EVIDENCE",
    "enterprise_customer_delivery": "ADJACENT_EVIDENCE",
    "vendor_management": "ADJACENT_EVIDENCE",

    # Current evidence does not establish the specialized depth these usually imply.
    "professional_software_engineering": "NOT_EVIDENCED",
    "production_system_ownership": "NOT_EVIDENCED",
    "distributed_systems": "NOT_EVIDENCED",
    "cloud_infrastructure": "NOT_EVIDENCED",
    "security_engineering": "NOT_EVIDENCED",
    "threat_intelligence_ir": "NOT_EVIDENCED",
    "offensive_security": "NOT_EVIDENCED",
    "fraud_abuse_investigations": "NOT_EVIDENCED",
    "data_science_statistics": "NOT_EVIDENCED",
    "ml_ai_engineering": "NOT_EVIDENCED",
    "datacenter_facilities": "NOT_EVIDENCED",
    "hardware_electrical": "NOT_EVIDENCED",
    "audiovisual_event_technology": "NOT_EVIDENCED",
    "people_management": "NOT_EVIDENCED",
    "security_vendor_risk": "NOT_EVIDENCED",
    "product_management": "NOT_EVIDENCED",
    "mergers_acquisitions": "NOT_EVIDENCED",
    "government_clearance": "NOT_EVIDENCED",
}

DOMAIN_PATTERNS: dict[str, tuple[str, ...]] = {
    "technical_support": (
        r"\btechnical support\b", r"\bsupport engineering\b",
        r"\bit support\b", r"\bservice desk\b", r"\buser operations\b",
        r"\bcustomer support\b",
    ),
    "troubleshooting_incidents": (
        r"\btroubleshoot", r"\bdebug", r"\bdiagnos",
        r"\broot cause\b", r"\bincident(?:s)?\b", r"\breproduc",
        r"\blogs?\b", r"\btelemetry\b",
    ),
    "api_integrations": (
        r"\bapi(?:s)?\b", r"\bintegration(?:s)?\b", r"\bwebhook",
        r"\bauthentication\b", r"\brest\b",
    ),
    "automation_workflows": (
        r"\bautomat", r"\bworkflow",
        r"\borchestrat(?:e|ed|es|ing|ion).{0,60}workflow",
        r"\bworkflow.{0,60}orchestrat(?:e|ed|es|ing|ion)",
        r"\blow[- ]code\b", r"\bzapier\b",
    ),
    "ticketing_itsm": (
        r"\bjira\b", r"\bitsm\b", r"\bservice desk\b",
        r"\bticket(?:s|ing)?\b", r"\bservicenow\b", r"\bzendesk\b",
    ),
    "documentation_training": (
        r"\bdocumentation\b", r"\bknowledge base\b", r"\bsop(?:s)?\b",
        r"\brunbook", r"\bplaybook", r"\btraining\b",
        r"\btechnical writing\b",
    ),
    "uat_qa_bug": (
        r"\buat\b", r"\buser acceptance\b", r"\bquality assurance\b",
        r"\bqa\b", r"\bbug(?:s)?\b", r"\btest(?:ing|ed|s)?\b",
        r"\bevaluation(?:s)?\b",
    ),
    "crm_saas": (
        r"\bcrm\b", r"\bsalesforce\b", r"\bsaas\b",
        r"\bmicrosoft 365\b", r"\boffice 365\b", r"\batlassian\b",
        r"\bgoogle workspace\b",
    ),
    "basic_network_dns": (
        r"\bdns\b", r"\brouter(?:s)?\b", r"\bnetwork troubleshooting\b",
        r"\bnetwork connectivity\b",
    ),
    "process_improvement": (
        r"\bprocess improvement\b", r"\bcontinuous improvement\b",
        r"\boperational improvement\b", r"\bimprove .*process",
        r"\brepeatable workflow",
    ),
    "technical_customer_communication": (
        r"\bcustomer[- ]facing\b", r"\bcustomer technical teams?\b",
        r"\btechnical communication\b", r"\bstakeholder communication\b",
        r"\bcommunicat(?:e|ion).*technical",
    ),
    "python_scripting": (r"\bpython\b", r"\bscript(?:s|ing)?\b"),
    "javascript_scripting": (r"\bjavascript\b", r"\btypescript\b", r"\bnode\.?js\b"),
    "sql_data": (r"\bsql\b", r"\bquery(?:ing|ies)?\b", r"\bdatabase(?:s)?\b"),
    "powershell_bash": (r"\bpowershell\b", r"\bbash\b", r"\bshell scripting\b"),
    "web_frontend": (r"\bhtml\b", r"\bcss\b", r"\bfront[- ]end\b"),
    "systems_operations": (
        r"\bsystems? operations\b", r"\benterprise systems?\b",
        r"\bsystem administration\b", r"\bsystems? support\b",
    ),
    "identity_device_management": (
        r"\bidentity\b", r"\bdevice management\b", r"\bjamf\b",
        r"\bintune\b", r"\bazure ad\b", r"\bentra\b", r"\bmacos\b",
    ),
    "technical_program_delivery": (
        r"\btechnical program", r"\bprogram management\b",
        r"\bcross[- ]functional (?:initiatives?|programs?)\b", r"\bdelivery plans?\b",
        r"\bmilestones?\b",
    ),
    "enterprise_customer_delivery": (
        r"\benterprise customers?\b", r"\bcustomer delivery\b",
        r"\btechnical engagements?\b", r"\bdeployment(?:s)?\b",
        r"\btechnical account\b",
    ),
    "vendor_management": (
        r"\bvendor management\b", r"\bvendors?\b", r"\bthird[- ]party\b",
    ),
    "professional_software_engineering": (
        r"\bsoftware engineer(?:ing)?\b", r"\bfull[- ]stack\b",
        r"\bbackend\b", r"\bfront[- ]end development\b",
        r"\bproduction code\b",
    ),
    "production_system_ownership": (
        r"\bproduction systems?\b", r"\bproduction environment",
        r"\boperate(?:d|s|ing)? .*production", r"\bon[- ]call\b",
        r"\bproduction launch\b",
    ),
    "distributed_systems": (
        r"\bdistributed systems?\b", r"\blarge[- ]scale systems?\b",
        r"\bhighly available\b", r"\bfault tolerance\b",
    ),
    "cloud_infrastructure": (
        r"\bcloud infrastructure\b", r"\baws\b", r"\bgcp\b",
        r"\bazure (?:cloud|services?|infrastructure)\b", r"\bkubernetes\b", r"\bdocker\b",
        r"\bcloud deployment\b",
    ),
    "security_engineering": (
        r"\bapplication security\b", r"\binfrastructure security\b",
        r"\bsecurity engineering\b", r"\bsecurity controls?\b",
        r"\bdetection engineering\b", r"\bsiem\b", r"\bedr\b",
    ),
    "threat_intelligence_ir": (
        r"\bthreat intelligence\b", r"\bincident response\b",
        r"\bthreat actor", r"\badversar(?:y|ies|ial)\b",
        r"\bthreat hunting\b", r"\btelemetry .*investigat",
    ),
    "offensive_security": (
        r"\boffensive security\b", r"\bpenetration test",
        r"\bred team", r"\bexploit development\b",
    ),
    "fraud_abuse_investigations": (
        r"\bfraud\b", r"\bscams?\b", r"\babuse investigations?\b",
        r"\bcybercrime\b", r"\btrust and safety investigations?\b",
    ),
    "data_science_statistics": (
        r"\bdata science\b", r"\bstatistics?\b", r"\bstatistical\b",
        r"\bexperimentation\b", r"\bquantitative field\b",
    ),
    "ml_ai_engineering": (
        r"\bmachine learning\b", r"\bml engineer", r"\bllm(?:s)?\b",
        r"\bmodel behavior\b", r"\bmodel evaluation", r"\bpytorch\b",
        r"\btensorflow\b", r"\bai applications?\b",
    ),
    "datacenter_facilities": (
        r"\bdata center\b", r"\bdatacenter\b", r"\bcritical facilities\b",
        r"\bcommissioning\b", r"\bpower projects?\b",
    ),
    "hardware_electrical": (
        r"\bhardware\b", r"\belectrical engineer", r"\bpcba\b",
        r"\bmechanical engineer", r"\bfirmware\b",
    ),
    "audiovisual_event_technology": (
        r"\baudiovisual\b", r"\baudio[- ]visual\b", r"\bav (?:systems?|technology|production)\b",
        r"\ball[- ]hands events?\b", r"\bevent technical production\b",
    ),
    "people_management": (
        r"\bpeople management\b", r"\bpeople manager\b",
        r"\bmanag(?:e|ed|ing) (?:a |the )?(?:team|people|engineers|staff)\b",
        r"\bled (?:a |the )?(?:team|organization|org)\b",
        r"\bleading (?:a |the )?(?:team|organization|org)\b",
        r"\bhir(?:e|ed|es|ing) (?:and |a |the )?(?:team|people|engineers|staff)\b",
        r"\bcoach(?:ed|ing)? (?:a |the )?(?:team|people|engineers|staff)\b",
        r"\bdirect reports?\b",
    ),
    "security_vendor_risk": (
        r"\bvendor security\b", r"\bthird[- ]party risk\b",
        r"\bthird[- ]party.{0,80}security risk",
        r"\bsupply[- ]chain risk\b", r"\bsupply[- ]chain.{0,80}security risk",
        r"\bsecurity addenda\b", r"\bvendor risk\b",
        r"\biso 27001\b", r"\bnist 800[- ]53\b", r"\bsoc 2\b",
    ),
    "product_management": (
        r"\bproduct management\b", r"\bproduct manager\b",
        r"\bproduct strategy\b", r"\bproduct roadmap\b",
    ),
    "mergers_acquisitions": (
        r"\bmergers? (?:&|and) acquisitions?\b", r"\bm&a\b",
        r"\bmerger integration\b",
    ),
    "government_clearance": (
        r"\bsecurity clearance\b", r"\btop secret\b", r"\bts/sci\b",
        r"\bpolygraph\b", r"\bus citizenship required\b",
    ),
}

# Known technologies/skills worth surfacing verbatim when they appear in
# qualifications. Presence here does not imply the user has them.
TECH_PATTERNS: dict[str, tuple[str, ...]] = {
    "Python": (r"\bpython\b",),
    "JavaScript/TypeScript": (r"\bjavascript\b", r"\btypescript\b"),
    "SQL": (r"\bsql\b",),
    "PowerShell": (r"\bpowershell\b",),
    "Bash": (r"\bbash\b",),
    "REST APIs": (r"\brest(?:ful)? api", r"\bapi(?:s)?\b"),
    "AWS": (r"\baws\b", r"\bamazon web services\b"),
    "GCP": (r"\bgcp\b", r"\bgoogle cloud\b"),
    "Azure": (r"\bazure\b",),
    "Kubernetes": (r"\bkubernetes\b", r"\bk8s\b"),
    "Docker": (r"\bdocker\b",),
    "Jira": (r"\bjira\b",),
    "Salesforce": (r"\bsalesforce\b",),
    "ServiceNow": (r"\bservicenow\b",),
    "Zendesk": (r"\bzendesk\b",),
    "Jamf": (r"\bjamf\b",),
    "Intune": (r"\bintune\b",),
    "Microsoft 365": (r"\bmicrosoft 365\b", r"\boffice 365\b"),
    "Google Workspace": (r"\bgoogle workspace\b",),
    "macOS": (r"\bmacos\b", r"\bmac os\b"),
    "Windows": (r"\bwindows\b",),
    "Linux": (r"\blinux\b",),
}

DIRECT_TARGET_TEAMS = {
    "Support Delivery", "Support Operations", "Support Automation", "IT", "User Operations"
}
ADJACENT_TARGET_TEAMS = {
    "Technical Success", "Technical Program Management", "Trust & Safety",
    "Intelligence & Investigations", "Security"
}

# ---------------------------------------------------------------------------
# Text / markdown helpers
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def trunc(value: Any, limit: int = 240) -> str:
    text = norm("" if value is None else str(value))
    return text if len(text) <= limit else text[: limit - 1] + "…"


def md_escape(value: Any) -> str:
    return str("" if value is None else value).replace("|", r"\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], max_cell: int = 240) -> str:
    if not rows:
        return "_No rows._\n"
    cols = list(rows[0].keys())
    out = [
        "| " + " | ".join(md_escape(c) for c in cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for row in rows:
        out.append(
            "| " + " | ".join(md_escape(trunc(row.get(c), max_cell)) for c in cols) + " |"
        )
    return "\n".join(out) + "\n"


def details(title: str, body: str) -> str:
    return f"<details>\n<summary>{md_escape(title)}</summary>\n\n{body}\n</details>\n"


def compile_patterns(patterns: Iterable[str]) -> list[re.Pattern[str]]:
    return [re.compile(p, re.I | re.S) for p in patterns]


def pattern_hits(text: str, patterns: Iterable[str]) -> list[str]:
    hits: list[str] = []
    for p in compile_patterns(patterns):
        m = p.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def grouped_hits(text: str, groups: dict[str, tuple[str, ...]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for name, pats in groups.items():
        hits = pattern_hits(text, pats)
        if hits:
            out[name] = hits
    return out


# ---------------------------------------------------------------------------
# Line-aware section parsing
# ---------------------------------------------------------------------------

RESPONSIBILITY_HEADINGS = (
    "in this role, you will:",
    "in this role you will:",
    "in this role, you will",
    "in this role you will",
    "responsibilities:",
    "responsibilities",
    "what you’ll do:",
    "what you'll do:",
    "what you’ll do",
    "what you'll do",
)

QUALIFICATION_HEADINGS = (
    "you might thrive in this role if you have:",
    "you might thrive in this role if you have",
    "you might thrive in this role if you:",
    "you might thrive in this role if you",
    "you might thrive in this role if:",
    "you might thrive in this role if",
    "you’ll thrive in this role if you have:",
    "you'll thrive in this role if you have:",
    "you’ll thrive in this role if you have",
    "you'll thrive in this role if you have",
    "you’ll thrive in this role if you:",
    "you'll thrive in this role if you:",
    "you’ll thrive in this role if you",
    "you'll thrive in this role if you",
    "you’ll thrive in this role if:",
    "you'll thrive in this role if:",
    "you may be a fit if:",
    "you may be a fit if",
    "you are a good fit if:",
    "you are a good fit if",
    "qualifications:",
    "qualifications",
    "requirements:",
    "requirements",
    "what we’re looking for:",
    "what we're looking for:",
    "what we’re looking for",
    "what we're looking for",
)

PREFERRED_HEADINGS = (
    "nice to have:", "nice to have", "preferred qualifications:",
    "preferred qualifications", "bonus:", "bonus", "preferred:", "preferred",
)

END_HEADINGS = (
    "about openai", "compensation", "benefits", "equal opportunity",
    "background checks", "application and accommodations",
    "additional information", "openai global applicant privacy policy",
)


def clean_lines(text: str) -> list[str]:
    return [line.strip() for line in (text or "").replace("\r\n", "\n").split("\n")]


def heading_key(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip().lower())


def find_heading(lines: list[str], headings: Iterable[str], start: int = 0) -> tuple[int | None, str | None]:
    wanted = {heading_key(h) for h in headings}
    for i in range(start, len(lines)):
        if heading_key(lines[i]) in wanted:
            return i, lines[i]
    return None, None


def next_heading_index(lines: list[str], start: int, heading_sets: Iterable[Iterable[str]]) -> int:
    wanted = set()
    for hs in heading_sets:
        wanted.update(heading_key(h) for h in hs)
    for i in range(start, len(lines)):
        if heading_key(lines[i]) in wanted:
            return i
    return len(lines)


def extract_sections(description: str) -> dict[str, Any]:
    lines = clean_lines(description)
    r_idx, r_head = find_heading(lines, RESPONSIBILITY_HEADINGS)
    q_idx, q_head = find_heading(lines, QUALIFICATION_HEADINGS)

    # Responsibilities end at qualifications/preferred/about section.
    if r_idx is not None:
        r_end = next_heading_index(
            lines, r_idx + 1,
            (QUALIFICATION_HEADINGS, PREFERRED_HEADINGS, END_HEADINGS),
        )
        resp_lines = lines[r_idx + 1:r_end]
        r_method = f"line_heading:{r_head}"
    else:
        resp_lines = []
        r_method = "not_found"

    if q_idx is not None:
        q_end = next_heading_index(lines, q_idx + 1, (PREFERRED_HEADINGS, END_HEADINGS))
        qual_lines = lines[q_idx + 1:q_end]
        q_method = f"line_heading:{q_head}"
    else:
        qual_lines = []
        q_method = "not_found"

    # Preferred section separately.
    p_idx, p_head = find_heading(lines, PREFERRED_HEADINGS, start=(q_idx + 1 if q_idx is not None else 0))
    if p_idx is not None:
        p_end = next_heading_index(lines, p_idx + 1, (END_HEADINGS,))
        pref_lines = lines[p_idx + 1:p_end]
        p_method = f"line_heading:{p_head}"
    else:
        pref_lines = []
        p_method = "not_found"

    def section_text(section_lines: list[str]) -> str:
        return "\n".join(line for line in section_lines if line).strip()

    return {
        "responsibilities_text": section_text(resp_lines),
        "qualifications_text": section_text(qual_lines),
        "preferred_text": section_text(pref_lines),
        "responsibility_method": r_method,
        "qualification_method": q_method,
        "preferred_method": p_method,
    }


def split_items(section: str) -> list[str]:
    """Split a section into bullets/expectations while preserving meaningful clauses."""
    if not section:
        return []
    lines = [x.strip() for x in section.splitlines() if x.strip()]
    items: list[str] = []
    current = ""
    for line in lines:
        is_bullet = bool(re.match(r"^[\-•*]\s*", line))
        cleaned = re.sub(r"^[\-•*]\s*", "", line).strip()
        if is_bullet:
            if current:
                items.append(norm(current))
            current = cleaned
        else:
            if current:
                current += " " + cleaned
            else:
                # Some Ashby plain text sections are paragraph-based.
                current = cleaned
    if current:
        items.append(norm(current))

    # If a parser found one huge paragraph, split conservatively on sentence
    # boundaries only when it clearly contains multiple expectation-style starts.
    if len(items) == 1 and len(items[0]) > 900:
        chunks = re.split(
            r"(?<=[.!?])\s+(?=(?:Have|Are|Can|Bring|Demonstrate|Possess|Experience|Strong|Proven|Ability|Comfort|Knowledge)\b)",
            items[0], flags=re.I,
        )
        if len(chunks) > 1:
            items = [norm(x) for x in chunks if norm(x)]
    return items


# ---------------------------------------------------------------------------
# Requirement interpretation
# ---------------------------------------------------------------------------

YEAR_PATTERNS = (
    re.compile(r"\b(?:at least|minimum(?: of)?|min\.?)[ ]+(\d{1,2})\s*\+?\s*(?:years?|yrs?)\b", re.I),
    re.compile(r"\b(\d{1,2})\s*\+\s*(?:years?|yrs?)\b", re.I),
    re.compile(r"\b(\d{1,2})\s*(?:-|–|—|to)\s*(\d{1,2})\s+(?:years?|yrs?)\b", re.I),
    re.compile(r"\b(\d{1,2})\s+(?:years?|yrs?)\s+of\b", re.I),
)


def years_in_text(text: str) -> list[int]:
    out: list[int] = []
    for pat in YEAR_PATTERNS:
        for m in pat.finditer(text):
            for g in m.groups():
                if g and g.isdigit():
                    out.append(int(g))
    return out


def expectation_strength(item: str, preferred: bool = False) -> str:
    low = item.lower()
    if preferred or re.search(r"\b(preferred|nice to have|bonus|ideally)\b", low):
        return "PREFERRED"
    if re.search(r"\b(required|must|minimum|at least|need to|needs to)\b", low):
        return "EXPLICIT_REQUIREMENT"
    # OpenAI commonly uses "You might thrive ... Have X". Treat this as a
    # posted expectation, not as a legal hard requirement.
    return "POSTED_EXPECTATION"


def domain_evidence_tier(domain: str) -> str:
    return DOMAIN_EVIDENCE_TIERS.get(domain, "UNKNOWN")


def classify_requirement_item(item: str, preferred: bool = False) -> dict[str, Any]:
    domains = grouped_hits(item, DOMAIN_PATTERNS)
    technologies = grouped_hits(item, TECH_PATTERNS)
    years = years_in_text(item)
    strength = expectation_strength(item, preferred=preferred)

    domain_rows = []
    for domain in domains:
        tier = domain_evidence_tier(domain)
        domain_rows.append({"domain": domain, "evidence_tier": tier})

    # Gap severity is conservative and visible. A NOT_EVIDENCED domain only
    # becomes MAJOR when the posting is explicitly asking for experience/depth,
    # or the item names years. Otherwise it is MODERATE.
    strongest_tier = min(
        (EVIDENCE_TIER_ORDER[r["evidence_tier"]] for r in domain_rows),
        default=EVIDENCE_TIER_ORDER["UNKNOWN"],
    )
    weakest_tier = max(
        (EVIDENCE_TIER_ORDER[r["evidence_tier"]] for r in domain_rows),
        default=EVIDENCE_TIER_ORDER["UNKNOWN"],
    )

    asks_depth = bool(re.search(
        r"\b(expert(?:ise)?|deep(?:ly)?|substantial depth|strong (?:experience|understanding|knowledge)|"
        r"proven experience|track record|significant experience|professional .* experience|"
        r"experience\b|proficient|hands[- ]on|have led|has led|working literacy|"
        r"demonstrated ability|independently assessed|independently delivered|"
        r"can reason credibly|understand .*principles|knowledge of)\b",
        item, re.I,
    )) or bool(years)

    if any(r["evidence_tier"] == "NOT_EVIDENCED" for r in domain_rows):
        gap = "MAJOR_GAP" if asks_depth and strength != "PREFERRED" else "MODERATE_GAP"
    elif any(r["evidence_tier"] == "RESUME_SKILL_CLAIM" for r in domain_rows):
        gap = "MODERATE_GAP" if asks_depth else "CLAIMED_SKILL_MATCH"
    elif any(r["evidence_tier"] == "ADJACENT_EVIDENCE" for r in domain_rows):
        gap = "ADJACENT_MATCH"
    elif any(r["evidence_tier"] == "DIRECT_WORK_EVIDENCE" for r in domain_rows):
        gap = "DIRECT_MATCH"
    else:
        gap = "UNCLASSIFIED_REQUIREMENT"

    return {
        "text": item,
        "strength": strength,
        "years": years,
        "domains": domain_rows,
        "technologies": sorted(technologies.keys()),
        "classification": gap,
        "strongest_evidence_tier_index": strongest_tier,
        "weakest_evidence_tier_index": weakest_tier,
    }


def seniority_burden(requirements: list[dict[str, Any]]) -> tuple[str, int | None]:
    years = [y for r in requirements for y in r.get("years", [])]
    maximum = max(years) if years else None
    if maximum is None:
        return "UNKNOWN", None
    if maximum <= 3:
        return "LOW", maximum
    if maximum <= 5:
        return "MODERATE", maximum
    if maximum <= 7:
        return "HIGH", maximum
    return "VERY_HIGH", maximum


def career_lane(role: dict[str, Any]) -> str:
    team = role.get("team") or ""
    title = (role.get("title") or "").lower()
    if team in DIRECT_TARGET_TEAMS or re.search(r"\b(it support|support engineer|support operations|user operations)\b", title):
        return "PRIMARY_SUPPORT_IT"
    if team in ADJACENT_TARGET_TEAMS or re.search(r"\b(deployment engineer|technical program|technical operations)\b", title):
        return "ADJACENT_TECHNICAL"
    return "STRETCH_TECHNICAL"




def title_alignment(role: dict[str, Any]) -> str:
    title = (role.get("title") or "").lower()
    if re.search(r"\b(support engineer|it support|support specialist|support operations|user operations|product engagement)\b", title):
        return "DIRECT_ROLE_FAMILY"
    if re.search(
        r"\b(software engineer|research engineer|research scientist|data scientist|applied ai engineer|"
        r"security engineer|red team|threat investigator|deployment engineer|demo experience engineer|"
        r"network engineer|infrastructure engineer|engineering manager)\b",
        title, re.I,
    ):
        return "SPECIALIST_ENGINEERING_STRETCH"
    if re.search(r"\btechnical program manager\b|\bprogram manager\b", title, re.I):
        return "ADJACENT_PROGRAM_ROLE"
    return "OTHER_TECHNICAL_ROLE"

def location_path(role: dict[str, Any]) -> str:
    cat = role.get("location_category") or ""
    if cat == "A_US_REMOTE_STRONG":
        return "REMOTE_NOW_STRONG"
    if cat in {"B_US_REMOTE_AMBIGUOUS", "B_REMOTE_US_LOCATION_AMBIGUOUS"}:
        return "REMOTE_NEEDS_CONFIRMATION"
    if cat == "C_US_RELOCATION_SUPPORTED":
        return "RELOCATION_SUPPORTED"
    if cat in {"D_US_ONSITE_OR_HYBRID", "D_US_LOCATION_UNCLEAR"}:
        return "US_LOCATION_DEPENDENCY"
    return "JURISDICTION_BARRIER"


def evidence_summary(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(r["classification"] for r in requirements)
    major_items = [r for r in requirements if r["classification"] == "MAJOR_GAP"]
    moderate_items = [r for r in requirements if r["classification"] == "MODERATE_GAP"]
    direct_items = [r for r in requirements if r["classification"] == "DIRECT_MATCH"]
    adjacent_items = [r for r in requirements if r["classification"] == "ADJACENT_MATCH"]
    claimed_items = [r for r in requirements if r["classification"] == "CLAIMED_SKILL_MATCH"]
    return {
        "classification_counts": dict(counts),
        "major_gap_count": len(major_items),
        "moderate_gap_count": len(moderate_items),
        "direct_match_count": len(direct_items),
        "adjacent_match_count": len(adjacent_items),
        "claimed_skill_match_count": len(claimed_items),
        "major_gap_items": [r["text"] for r in major_items],
        "moderate_gap_items": [r["text"] for r in moderate_items],
        "direct_match_items": [r["text"] for r in direct_items],
    }


def decision_band(role: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    sales = role.get("sales_classification")
    if sales == "EXCLUDE_STRONG_SALES":
        return "X_EXCLUDED_SALES", ["Violates hard NO SALES constraint"]

    if not role.get("qualification_parse_complete"):
        return "C_REQUIREMENTS_INCOMPLETE", ["No clean qualification section was extracted; do not reward apparent zero gaps"]

    if role.get("location_path") == "JURISDICTION_BARRIER":
        return "D_BACKGROUND", ["No practical US/Utah path established in current posting"]

    if role.get("technical_core_level") not in {"HIGH", "MEDIUM"} and role.get("career_lane") != "PRIMARY_SUPPORT_IT":
        return "D_BACKGROUND", ["Technical-core evidence is too weak for the stated target"]

    title_fit = role.get("title_alignment")

    ev = role["requirement_evidence_summary"]
    major = ev["major_gap_count"]
    moderate = ev["moderate_gap_count"]
    direct = ev["direct_match_count"]
    seniority = role["seniority_burden"]
    lane = role["career_lane"]
    loc = role["location_path"]

    if seniority == "VERY_HIGH":
        reasons.append("Very high posted seniority burden")
    if major:
        reasons.append(f"{major} major currently-unproven requirement area(s)")
    if direct:
        reasons.append(f"{direct} qualification item(s) map to direct work evidence")
    if loc == "REMOTE_NOW_STRONG":
        reasons.append("Strong current US-remote path")
    elif loc == "REMOTE_NEEDS_CONFIRMATION":
        reasons.append("Potential US-remote path needs confirmation")
    elif loc == "RELOCATION_SUPPORTED":
        reasons.append("Explicit relocation assistance")
    else:
        reasons.append("Location remains a material dependency")

    # Specialist engineering/research/security titles are kept visible, but the
    # current resume does not establish the professional depth implied by those
    # job families. They therefore cannot rise above stretch review here.
    if title_fit == "SPECIALIST_ENGINEERING_STRETCH":
        reasons.append("Specialist engineering/research/security title is outside the strongest documented work-history lane")
        if major <= 3 and role.get("technical_core_level") in {"HIGH", "MEDIUM"}:
            return "C_STRETCH_REVIEW", reasons
        return "D_BACKGROUND", reasons

    # A is deliberately difficult to reach. It means serious top-five review,
    # not that the role is already a final top-five selection.
    if (
        sales == "NO_SALES_SIGNAL_FOUND"
        and seniority in {"UNKNOWN", "LOW", "MODERATE"}
        and loc in {"REMOTE_NOW_STRONG", "REMOTE_NEEDS_CONFIRMATION", "RELOCATION_SUPPORTED"}
        and (
            (lane == "PRIMARY_SUPPORT_IT" and major <= 1 and direct >= 2)
            or (lane == "ADJACENT_TECHNICAL" and major == 0 and direct >= 3)
        )
    ):
        return "A_TOP5_REVIEW", reasons

    if (
        major <= 1
        and seniority != "VERY_HIGH"
        and (direct >= 1 or role.get("resume_evidence_overlap_count", 0) >= 5)
        and loc in {"REMOTE_NOW_STRONG", "REMOTE_NEEDS_CONFIRMATION", "RELOCATION_SUPPORTED", "US_LOCATION_DEPENDENCY"}
    ):
        return "B_SERIOUS_REVIEW", reasons

    if major <= 3 and role.get("technical_core_level") in {"HIGH", "MEDIUM"}:
        return "C_STRETCH_REVIEW", reasons

    return "D_BACKGROUND", reasons


# ---------------------------------------------------------------------------
# Candidate selection and report formatting
# ---------------------------------------------------------------------------

def candidate_seed(baseline_role: dict[str, Any]) -> bool:
    if baseline_role.get("sales_classification") == "EXCLUDE_STRONG_SALES":
        return False
    if baseline_role.get("location_category") == "E_NON_US_OR_JURISDICTION_MISMATCH":
        return False

    team = baseline_role.get("team") or ""
    tech = baseline_role.get("technical_core_level")
    priority = baseline_role.get("review_priority")
    overlap = baseline_role.get("resume_evidence_overlap_count", 0)
    loc = baseline_role.get("location_category")

    return bool(
        priority in {"P1_DEEP_REVIEW", "P2_REVIEW"}
        or team in DIRECT_TARGET_TEAMS
        or (team in ADJACENT_TARGET_TEAMS and overlap >= 3)
        or (loc == "A_US_REMOTE_STRONG" and tech in {"HIGH", "MEDIUM"})
    )


def salary_summary(role: dict[str, Any]) -> str:
    parts = []
    for c in role.get("salary_components") or []:
        if (c.get("compensation_type") or "").lower() != "salary":
            continue
        parts.append(
            f"{c.get('currency_code') or ''} {c.get('min_value')}–{c.get('max_value')} / {c.get('interval') or '?'}"
        )
    return "; ".join(parts)


def review_sort_key(role: dict[str, Any]) -> tuple[Any, ...]:
    band_order = {"A_TOP5_REVIEW": 0, "B_SERIOUS_REVIEW": 1, "C_STRETCH_REVIEW": 2, "C_REQUIREMENTS_INCOMPLETE": 3, "D_BACKGROUND": 4, "X_EXCLUDED_SALES": 5}
    lane_order = {"PRIMARY_SUPPORT_IT": 0, "ADJACENT_TECHNICAL": 1, "STRETCH_TECHNICAL": 2}
    loc_order = {"REMOTE_NOW_STRONG": 0, "REMOTE_NEEDS_CONFIRMATION": 1, "RELOCATION_SUPPORTED": 2, "US_LOCATION_DEPENDENCY": 3, "JURISDICTION_BARRIER": 4}
    seniority_order = {"LOW": 0, "UNKNOWN": 1, "MODERATE": 2, "HIGH": 3, "VERY_HIGH": 4}
    ev = role["requirement_evidence_summary"]
    return (
        band_order.get(role["decision_band"], 9),
        lane_order.get(role["career_lane"], 9),
        loc_order.get(role["location_path"], 9),
        ev["major_gap_count"],
        ev["moderate_gap_count"],
        seniority_order.get(role["seniority_burden"], 9),
        -ev["direct_match_count"],
        -role.get("resume_evidence_overlap_count", 0),
        role.get("team") or "",
        role.get("title") or "",
    )


def report_row(role: dict[str, Any]) -> dict[str, Any]:
    ev = role["requirement_evidence_summary"]
    return {
        "title": role["title"],
        "team": role["team"],
        "lane": role["career_lane"],
        "title_alignment": role["title_alignment"],
        "location_path": role["location_path"],
        "workplace": role.get("workplace_type"),
        "relocation": "YES" if role.get("relocation_assistance") else "NO",
        "office_days": role.get("office_days_per_week"),
        "sales": role.get("sales_classification"),
        "technical": role.get("technical_core_level"),
        "seniority": role.get("seniority_burden"),
        "max_years": role.get("max_years_mentioned"),
        "direct_req": ev["direct_match_count"],
        "claimed_req": ev["claimed_skill_match_count"],
        "adjacent_req": ev["adjacent_match_count"],
        "major_gaps": ev["major_gap_count"],
        "moderate_gaps": ev["moderate_gap_count"],
        "gap_domains": "; ".join(role.get("major_gap_domains", [])),
        "salary": salary_summary(role),
        "decision_band": role["decision_band"],
    }


def dossier_markdown(role: dict[str, Any]) -> str:
    ev = role["requirement_evidence_summary"]
    out = []
    out.append(f"### {role['title']} — {role['team']}\n\n")
    out.append(f"- **Decision band:** `{role['decision_band']}`\n")
    out.append(f"- **Career lane:** `{role['career_lane']}`; title alignment: `{role['title_alignment']}`\n")
    out.append(f"- **Location path:** `{role['location_path']}` — {role.get('location_reason','')}\n")
    out.append(f"- **Primary / secondary:** {role.get('primary_location')} / {', '.join(role.get('secondary_locations') or []) or 'none'}\n")
    out.append(f"- **Work arrangement:** {role.get('workplace_type') or 'unspecified'}; office days: {role.get('office_days_per_week') or 'not detected'}; relocation: {'yes' if role.get('relocation_assistance') else 'no'}\n")
    out.append(f"- **Sales classification:** `{role.get('sales_classification')}`\n")
    out.append(f"- **Technical core:** `{role.get('technical_core_level')}`\n")
    out.append(f"- **Seniority burden:** `{role.get('seniority_burden')}`; max explicit years detected: {role.get('max_years_mentioned') if role.get('max_years_mentioned') is not None else 'none'}\n")
    out.append(f"- **Requirement evidence:** direct={ev['direct_match_count']}, claimed-skill={ev['claimed_skill_match_count']}, adjacent={ev['adjacent_match_count']}, major gaps={ev['major_gap_count']}, moderate gaps={ev['moderate_gap_count']}\n")
    out.append(f"- **Salary:** {salary_summary(role) or 'not captured'}\n")
    out.append(f"- **Why this band:** {'; '.join(role.get('decision_reasons') or [])}\n\n")

    out.append("**Responsibilities excerpt**\n\n")
    out.append((trunc(role.get("responsibilities_text"), 1200) or "_Not cleanly extracted._") + "\n\n")

    out.append("**Qualification-by-qualification evidence map**\n\n")
    req_rows = []
    for r in role.get("requirements", []):
        req_rows.append({
            "classification": r["classification"],
            "strength": r["strength"],
            "years": ",".join(str(x) for x in r.get("years", [])),
            "domains": ", ".join(x["domain"] for x in r.get("domains", [])),
            "technologies": ", ".join(r.get("technologies", [])),
            "requirement": r["text"],
        })
    out.append(md_table(req_rows, max_cell=360))

    if role.get("preferred_requirements"):
        out.append("\n**Preferred / bonus items**\n\n")
        pref_rows = []
        for r in role["preferred_requirements"]:
            pref_rows.append({
                "classification": r["classification"],
                "domains": ", ".join(x["domain"] for x in r.get("domains", [])),
                "requirement": r["text"],
            })
        out.append(md_table(pref_rows, max_cell=360))

    if ev["major_gap_items"]:
        out.append("\n**Major currently-unproven requirements**\n\n")
        for item in ev["major_gap_items"]:
            out.append(f"- {item}\n")
    if ev["direct_match_items"]:
        out.append("\n**Posted qualifications with direct work-evidence overlap**\n\n")
        for item in ev["direct_match_items"]:
            out.append(f"- {item}\n")

    out.append(f"\n**Apply:** {role.get('apply_url') or ''}\n\n")
    return "".join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Deep requirement-level analysis for ProofLoop Application #001")
    parser.add_argument("--report", type=Path, default=Path("proofloop_role_analysis_report_v0_15.json"))
    parser.add_argument("--db", type=Path, default=Path("proofloop_enriched.db"))
    parser.add_argument("--markdown", type=Path, default=Path("proofloop_role_deep_analysis_report_v0_16.md"))
    parser.add_argument("--json", dest="json_output", type=Path, default=Path("proofloop_role_deep_analysis_report_v0_16.json"))
    parser.add_argument("--decision-pool-limit", type=int, default=30)
    args = parser.parse_args()

    if not args.report.is_file():
        print(f"ERROR: baseline report not found: {args.report}", file=sys.stderr)
        return 2
    if not args.db.is_file():
        print(f"ERROR: database not found: {args.db}", file=sys.stderr)
        return 2

    baseline = json.loads(args.report.read_text(encoding="utf-8"))
    if baseline.get("battery") != EXPECTED_BASELINE:
        print(f"ERROR: expected v0.15 baseline report, got {baseline.get('battery')!r}", file=sys.stderr)
        return 2

    baseline_roles = baseline.get("all_role_dossiers") or []
    baseline_by_id = {r["ashby_id"]: r for r in baseline_roles}
    if len(baseline_by_id) != len(baseline_roles):
        print("ERROR: duplicate ashby_id in v0.15 all_role_dossiers", file=sys.stderr)
        return 1

    db_abs = args.db.resolve()
    conn = sqlite3.connect(db_abs.as_uri() + "?mode=ro", uri=True)
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            print(f"ERROR: SQLite integrity_check returned {integrity!r}", file=sys.stderr)
            return 1
        rows = conn.execute(
            """
            SELECT ashby_id, title, team, description_plain
            FROM roles
            WHERE present_in_api=1
            ORDER BY ashby_id
            """
        ).fetchall()
    finally:
        conn.close()

    db_ids = {r[0] for r in rows}
    baseline_ids = set(baseline_by_id)
    if db_ids != baseline_ids:
        print(
            f"ERROR: baseline/database role IDs differ: db={len(db_ids)} baseline={len(baseline_ids)} "
            f"db_only={len(db_ids-baseline_ids)} baseline_only={len(baseline_ids-db_ids)}",
            file=sys.stderr,
        )
        return 1

    descriptions = {ashby_id: desc or "" for ashby_id, _, _, desc in rows}

    deep_roles: list[dict[str, Any]] = []
    parser_diagnostics = Counter()

    for ashby_id, base in baseline_by_id.items():
        if not candidate_seed(base):
            continue

        description = descriptions[ashby_id]
        sections = extract_sections(description)
        parser_diagnostics[sections["qualification_method"]] += 1

        q_items = split_items(sections["qualifications_text"])
        p_items = split_items(sections["preferred_text"])

        # If no clean qualification section exists, keep the role in the pool but
        # explicitly mark the requirement evidence as incomplete rather than
        # pretending the whole description is qualifications.
        requirements = [classify_requirement_item(x, preferred=False) for x in q_items]
        preferred_requirements = [classify_requirement_item(x, preferred=True) for x in p_items]

        ev = evidence_summary(requirements)
        seniority, max_years = seniority_burden(requirements)
        lane = career_lane(base)
        loc_path = location_path(base)

        major_domains = sorted({
            d["domain"]
            for r in requirements if r["classification"] == "MAJOR_GAP"
            for d in r.get("domains", [])
        })
        all_tech = sorted({
            tech for r in requirements + preferred_requirements for tech in r.get("technologies", [])
        })

        role = dict(base)
        role.update({
            "career_lane": lane,
            "title_alignment": title_alignment(base),
            "location_path": loc_path,
            "responsibilities_text": sections["responsibilities_text"],
            "qualifications_text": sections["qualifications_text"],
            "preferred_text": sections["preferred_text"],
            "deep_responsibility_extraction_method": sections["responsibility_method"],
            "deep_qualification_extraction_method": sections["qualification_method"],
            "deep_preferred_extraction_method": sections["preferred_method"],
            "requirements": requirements,
            "preferred_requirements": preferred_requirements,
            "qualification_parse_complete": bool(q_items),
            "requirement_evidence_summary": ev,
            "seniority_burden": seniority,
            "max_years_mentioned": max_years,
            "major_gap_domains": major_domains,
            "qualification_technologies": all_tech,
        })
        band, reasons = decision_band(role)
        role["decision_band"] = band
        role["decision_reasons"] = reasons
        deep_roles.append(role)

    deep_roles.sort(key=review_sort_key)
    decision_pool = [
        r for r in deep_roles
        if r["decision_band"] in {"A_TOP5_REVIEW", "B_SERIOUS_REVIEW", "C_STRETCH_REVIEW"}
        and r["career_lane"] in {"PRIMARY_SUPPORT_IT", "ADJACENT_TECHNICAL"}
    ]
    decision_pool = decision_pool[: max(1, args.decision_pool_limit)]

    # Always preserve known benchmark roles from the previous analysis so they
    # can be compared even when a stricter rule places them outside the top pool.
    benchmark_titles = {
        "Dedicated Support Engineer - San Francisco",
        "IT Support Specialist",
        "AI Support Engineer - San Francisco",
        "Early Access Deployment Engineer",
        "Technical Systems Program Manager, User Operations",
        "Vendor Security Technical Program Manager",
        "Technical Threat Investigator, Threat Intel Engineering",
        "Applied AI Engineer, Enterprise",
    }
    benchmarks = [r for r in deep_roles if r["title"] in benchmark_titles]

    band_counts = Counter(r["decision_band"] for r in deep_roles)
    lane_counts = Counter(r["career_lane"] for r in deep_roles)
    loc_counts = Counter(r["location_path"] for r in deep_roles)
    seniority_counts = Counter(r["seniority_burden"] for r in deep_roles)
    major_gap_domain_counts = Counter(d for r in deep_roles for d in r["major_gap_domains"])

    payload = {
        "analysis": VERSION,
        "generated_at_utc": utc_now(),
        "baseline_report": str(args.report.resolve()),
        "database": str(db_abs),
        "database_mode": "read-only",
        "validation": {
            "baseline_battery": baseline.get("battery"),
            "baseline_roles": len(baseline_roles),
            "database_current_roles": len(rows),
            "role_ids_exact_match": True,
            "sqlite_integrity": "ok",
        },
        "methodology_notes": [
            "This layer consumes the v0.15 report instead of replacing it.",
            "The final top five are NOT selected by this script.",
            "Strong sales classifications are excluded from the candidate seed.",
            "Non-US/jurisdiction-mismatch roles are not promoted into the decision pool.",
            "Qualifications are extracted only from exact line-level headings; ordinary prose containing words like requirements no longer starts a qualifications section.",
            "Resume programming-language entries are treated as skill claims, not proof of years of production software engineering.",
            "Major gap means current evidence does not establish a posted expectation; it is not a claim that the skill cannot be learned.",
            "Location paths preserve remote-now, remote-needs-confirmation, relocation-supported, and onsite/location-dependency as separate states.",
            "Decision bands are rule-based and transparent; they are not an opaque numeric fit score.",
        ],
        "evidence_profile": {
            "domain_evidence_tiers": DOMAIN_EVIDENCE_TIERS,
            "tier_meanings": {
                "DIRECT_WORK_EVIDENCE": "Resume describes real work in this area.",
                "RESUME_SKILL_CLAIM": "Resume lists the skill, but does not by itself establish professional production depth.",
                "ADJACENT_EVIDENCE": "Related experience exists, but not enough to treat the requirement as directly proven.",
                "NOT_EVIDENCED": "Current resume/project evidence does not establish this specialized domain.",
                "UNKNOWN": "Parser could not map the requirement to a defined evidence domain.",
            },
        },
        "candidate_funnel": {
            "baseline_current_roles": len(baseline_roles),
            "deep_candidate_seed": len(deep_roles),
            "decision_band_counts": dict(band_counts),
            "career_lane_counts": dict(lane_counts),
            "location_path_counts": dict(loc_counts),
            "seniority_burden_counts": dict(seniority_counts),
            "decision_review_pool_emitted": len(decision_pool),
        },
        "major_gap_domain_counts": dict(major_gap_domain_counts.most_common()),
        "parser_diagnostics": dict(parser_diagnostics),
        "decision_review_pool": decision_pool,
        "comparison_benchmarks": benchmarks,
        "all_deep_candidates": deep_roles,
    }

    args.json_output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md: list[str] = []
    md.append("# ProofLoop Role Deep Analysis Report v0.16\n\n")
    md.append(f"Generated: `{payload['generated_at_utc']}`  \n")
    md.append(f"Baseline: `{args.report.resolve()}`  \n")
    md.append(f"Database: `{db_abs}`  \n")
    md.append("Database access: **read-only**\n\n")

    md.append("## Purpose\n\n")
    md.append(
        "This is the second-stage role analysis. v0.15 established the 815-role landscape, "
        "location/sales/technical classifications, and the first deep-review pool. v0.16 "
        "moves from role-level signals to **qualification-by-qualification evidence mapping**. "
        "It is designed to be used *with* v0.15 when choosing the final top five; it does not "
        "choose those five automatically.\n\n"
    )

    md.append("## Baseline validation\n\n")
    md.append(md_table([payload["validation"]]))

    md.append("## Methodology guardrails\n\n")
    for note in payload["methodology_notes"]:
        md.append(f"- {note}\n")

    md.append("\n## Candidate funnel\n\n")
    funnel = payload["candidate_funnel"]
    md.append(f"- Baseline current roles: **{funnel['baseline_current_roles']}**\n")
    md.append(f"- Roles entering deep requirement analysis: **{funnel['deep_candidate_seed']}**\n")
    md.append(f"- Decision-review pool emitted: **{funnel['decision_review_pool_emitted']}**\n\n")
    md.append("### Decision bands\n\n")
    md.append(md_table([{"band": k, "roles": v} for k, v in band_counts.items()]))
    md.append("\n### Career lanes\n\n")
    md.append(md_table([{"lane": k, "roles": v} for k, v in lane_counts.items()]))
    md.append("\n### Location paths\n\n")
    md.append(md_table([{"location_path": k, "roles": v} for k, v in loc_counts.items()]))
    md.append("\n### Seniority burden\n\n")
    md.append(md_table([{"seniority": k, "roles": v} for k, v in seniority_counts.items()]))

    md.append("\n## Decision-review pool\n\n")
    md.append(
        "This is an ordered **manual review pool**, not a final ranking. Ordering is lexicographic "
        "and transparent: decision band → career lane → location path → fewer major/moderate gaps "
        "→ lower seniority burden → more direct qualification matches.\n\n"
    )
    md.append(md_table([report_row(r) for r in decision_pool], max_cell=260))

    md.append("\n## Benchmark roles carried forward from v0.15\n\n")
    md.append(md_table([report_row(r) for r in benchmarks], max_cell=280))

    md.append("\n## Major gap domains across the deep candidate set\n\n")
    md.append(md_table([{"domain": k, "roles_or_mentions": v} for k, v in major_gap_domain_counts.most_common()]))

    md.append("\n## Parser diagnostics\n\n")
    md.append(
        "The qualification parser now requires an exact line-level heading. This specifically fixes "
        "the v0.15 failure mode where the word `requirements` inside ordinary prose could be mistaken "
        "for a Qualifications heading.\n\n"
    )
    md.append(md_table([{"method": k, "roles": v} for k, v in parser_diagnostics.items()], max_cell=320))

    md.append("\n## Detailed candidate dossiers\n\n")
    for role in decision_pool:
        md.append(dossier_markdown(role))

    md.append("\n## Comparison benchmark dossiers\n\n")
    pool_ids = {r["ashby_id"] for r in decision_pool}
    for role in benchmarks:
        if role["ashby_id"] not in pool_ids:
            md.append(dossier_markdown(role))

    args.markdown.write_text("".join(md), encoding="utf-8")

    print(VERSION)
    print(f"Baseline report:             {args.report.resolve()}")
    print(f"Database:                    {db_abs}")
    print("Database mode:               READ ONLY")
    print(f"Baseline current roles:      {len(baseline_roles)}")
    print(f"Deep candidate seed:         {len(deep_roles)}")
    print(f"A_TOP5_REVIEW:               {band_counts.get('A_TOP5_REVIEW', 0)}")
    print(f"B_SERIOUS_REVIEW:            {band_counts.get('B_SERIOUS_REVIEW', 0)}")
    print(f"C_STRETCH_REVIEW:            {band_counts.get('C_STRETCH_REVIEW', 0)}")
    print(f"Decision pool emitted:       {len(decision_pool)}")
    print(f"Markdown report:             {args.markdown}")
    print(f"JSON report:                 {args.json_output}")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
