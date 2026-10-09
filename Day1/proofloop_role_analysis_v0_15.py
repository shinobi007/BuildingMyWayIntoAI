#!/usr/bin/env python3
"""
ProofLoop Role Selection Transparency Battery v0.15

A read-only, evidence-preserving analysis pass over proofloop_enriched.db.

This revision improves v0.14 in the places the first run exposed:
- Sales detection uses regex / phrase logic instead of raw substring matching,
  avoiding obvious false positives such as "commissioning" -> "commission".
- Strong sales exclusion evidence is separated from weak/contextual sales signals.
- Location feasibility combines primary location, secondary locations,
  workplace_type, is_remote, actual remote wording, office-day wording,
  and relocation-assistance wording.
- Experience and education signals are extracted preferentially from the
  qualifications section rather than the entire posting.
- Compensation is summarized with interval and currency preserved.
- Resume/evidence overlap remains transparent and is explicitly NOT a fit score.
- A bounded deep-review pool is produced using explainable rules, not a hidden
  numeric ranking.
- Candidate dossiers preserve the actual evidence used to classify each role.

Outputs:
    proofloop_role_analysis_report_v0_15.md
    proofloop_role_analysis_report_v0_15.json

The script does not modify the database or source artifacts.
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


VERSION = "ProofLoop Role Selection Transparency Battery v0.15"

# ---------------------------------------------------------------------------
# Project-specific evidence vocabulary
# ---------------------------------------------------------------------------
# These categories describe documented evidence areas used for discovery.
# They are NOT certifications, qualifications, or automatic role-fit claims.
EVIDENCE_PATTERNS: dict[str, tuple[str, ...]] = {
    "support": (
        r"\bsupport\b",
        r"\bservice desk\b",
        r"\bhelp desk\b",
    ),
    "troubleshooting": (
        r"\btroubleshoot(?:ing|ed|s)?\b",
        r"\bdebug(?:ging|ged)?\b",
        r"\bdiagnos(?:e|is|ing|tic)\b",
        r"\broot cause\b",
        r"\bincident(?:s)?\b",
    ),
    "api_integrations": (
        r"\bapi(?:s)?\b",
        r"\bintegration(?:s)?\b",
        r"\bwebhook(?:s)?\b",
        r"\bauthentication\b",
    ),
    "automation": (
        r"\bautomat(?:e|ed|es|ing|ion)\b",
        r"\bworkflow(?:s)?\b",
        r"\borchestrat(?:e|ed|es|ing|ion)\b",
    ),
    "scripting_programming": (
        r"\bpython\b",
        r"\bjavascript\b",
        r"\bpowershell\b",
        r"\bbash\b",
        r"\bscript(?:s|ing|ed)?\b",
        r"\bcod(?:e|ing)\b",
    ),
    "sql_data": (
        r"\bsql\b",
        r"\bdatabase(?:s)?\b",
        r"\bdata analysis\b",
        r"\bquery(?:ing|ies)?\b",
    ),
    "ticketing_itsm": (
        r"\bjira\b",
        r"\bticket(?:s|ing)?\b",
        r"\bitsm\b",
        r"\bservice desk\b",
        r"\bservicenow\b",
        r"\bzendesk\b",
    ),
    "network_identity_device": (
        r"\bdns\b",
        r"\bnetwork(?:ing)?\b",
        r"\brouter(?:s)?\b",
        r"\bidentity\b",
        r"\bdevice management\b",
        r"\bintune\b",
        r"\bjamf\b",
        r"\bazure ad\b",
    ),
    "uat_testing": (
        r"\buat\b",
        r"\buser acceptance\b",
        r"\btest(?:ing|ed|s)?\b",
        r"\bbug(?:s)?\b",
        r"\breproduc(?:e|ing|tion)\b",
        r"\bevaluation(?:s)?\b",
    ),
    "documentation": (
        r"\bdocumentation\b",
        r"\bknowledge base\b",
        r"\bsop(?:s)?\b",
        r"\brunbook(?:s)?\b",
        r"\bplaybook(?:s)?\b",
        r"\btroubleshooting guide(?:s)?\b",
    ),
    "crm_saas": (
        r"\bcrm\b",
        r"\bsalesforce\b",
        r"\bsaas\b",
        r"\bmicrosoft 365\b",
        r"\boffice 365\b",
        r"\bgoogle workspace\b",
        r"\batlassian\b",
    ),
}

# Technical-core signals answer a different question from evidence overlap:
# "Does the work itself appear genuinely hands-on technical?"
TECHNICAL_CORE_PATTERNS: dict[str, tuple[str, ...]] = {
    "hands_on_troubleshooting": (
        r"\btroubleshoot(?:ing|ed|s)?\b",
        r"\bdebug(?:ging|ged)?\b",
        r"\breproduc(?:e|ing|tion)\b",
        r"\blogs?\b",
        r"\btelemetry\b",
        r"\broot cause\b",
    ),
    "systems_infrastructure": (
        r"\binfrastructure\b",
        r"\bsystems?\b",
        r"\bnetwork(?:ing)?\b",
        r"\bidentity\b",
        r"\bcloud\b",
        r"\bdevice management\b",
    ),
    "api_integration": (
        r"\bapi(?:s)?\b",
        r"\bintegration(?:s)?\b",
        r"\bauthentication\b",
        r"\bwebhook(?:s)?\b",
    ),
    "coding_scripting": (
        r"\bpython\b",
        r"\bjavascript\b",
        r"\bpowershell\b",
        r"\bbash\b",
        r"\bscript(?:s|ing|ed)?\b",
        r"\bsoftware engineering\b",
        r"\bcod(?:e|ing)\b",
    ),
    "automation_workflows": (
        r"\bautomat(?:e|ed|es|ing|ion)\b",
        r"\bworkflow(?:s)?\b",
        r"\bagent(?:ic)? workflow(?:s)?\b",
    ),
    "testing_evaluation": (
        r"\btest(?:ing|ed|s)?\b",
        r"\bevaluation(?:s)?\b",
        r"\bquality assurance\b",
        r"\buat\b",
    ),
    "technical_support": (
        r"\btechnical support\b",
        r"\bsupport engineering\b",
        r"\bit support\b",
        r"\bservice desk\b",
    ),
    "security_investigation": (
        r"\bsecurity\b",
        r"\bthreat intelligence\b",
        r"\bincident response\b",
        r"\binvestigat(?:e|ion|ing|or)\b",
        r"\bosint\b",
    ),
}

# Strong sales evidence is intended to support the user's hard NO SALES rule.
# It is intentionally conservative and uses word boundaries/context.
STRONG_SALES_PATTERNS: dict[str, tuple[str, ...]] = {
    "quota": (r"\bquota(?:s)?\b",),
    "sales_cycle": (r"\bsales cycle(?:s)?\b",),
    "pipeline_generation": (
        r"\bpipeline generation\b",
        r"\bgenerate(?:s|d|ing)? (?:a |the )?pipeline\b",
    ),
    "prospecting": (
        r"\bprospecting\b",
        r"\bprospect(?:s|ing)\b",
    ),
    "closing_deals": (
        r"\bclos(?:e|es|ed|ing) (?:the )?(?:deal|deals|business)\b",
        r"\bdeal closure\b",
    ),
    "book_of_business": (r"\bbook of business\b",),
    "revenue_target": (
        r"\brevenue target(?:s)?\b",
        r"\brevenue quota(?:s)?\b",
    ),
    "account_expansion": (
        r"\baccount expansion\b",
        r"\bexpand(?:ing)? accounts?\b",
    ),
    "commission_compensation": (
        # Deliberately excludes "commissioning" by requiring a word boundary.
        r"\bcommission\b.{0,80}\b(compensation|pay|earnings|plan)\b",
        r"\b(compensation|pay|earnings|plan)\b.{0,80}\bcommission\b",
    ),
}

# Context signals are NOT automatic exclusion evidence. They flag roles for
# manual review because these terms can appear in non-sales technical work.
CONTEXT_SALES_PATTERNS: dict[str, tuple[str, ...]] = {
    "pre_sales": (r"\bpre[- ]sales\b", r"\bpresales\b"),
    "business_development": (r"\bbusiness development\b",),
    "commercial": (r"\bcommercial\b",),
    "go_to_market": (r"\bgo[- ]to[- ]market\b", r"\bgtm\b"),
    "customer_expansion": (r"\bcustomer expansion\b",),
    "revenue": (r"\brevenue\b",),
    "territory": (r"\bterritor(?:y|ies)\b",),
    "sales_collaboration": (r"\bwork(?:ing)? (?:closely )?with sales\b",),
}

HARD_SALES_TITLE_PATTERNS = (
    r"\baccount director\b",
    r"\bsales development\b",
    r"\bseller\b",
    r"\bsales representative\b",
    r"\bclient partner\b",
)

QUALIFICATION_HEADINGS = (
    "you might thrive in this role if you",
    "you might thrive in this role if",
    "you’ll thrive in this role if you",
    "you'll thrive in this role if you",
    "you’ll thrive in this role if",
    "you'll thrive in this role if",
    "you may be a fit if",
    "you are a good fit if",
    "requirements",
    "qualifications",
    "what we're looking for",
    "what we’re looking for",
)

SECTION_END_HEADINGS = (
    "about openai",
    "compensation",
    "benefits",
    "equal opportunity",
    "background checks",
    "application and accommodations",
)

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15,
}

US_LOCATION_HINTS = (
    "united states", "us - remote", "u.s. - remote", "usa - remote",
    "san francisco", "seattle", "bellevue", "new york", "washington, dc",
    "washington dc", "mountain view", "california", "new york city",
    "dc", "ohio", "texas", "virginia", "maryland", "atlanta", "chicago",
)


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_ws(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def trunc(value: Any, limit: int = 240) -> str:
    text = normalize_ws("" if value is None else str(value))
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def md_escape(value: Any) -> str:
    return trunc(value, 10000).replace("|", r"\|")


def md_table(rows: list[dict[str, Any]], max_cell: int = 220) -> str:
    if not rows:
        return "_No rows._\n"
    cols = list(rows[0].keys())
    out = [
        "| " + " | ".join(md_escape(c) for c in cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for row in rows:
        out.append(
            "| "
            + " | ".join(md_escape(trunc(row.get(c), max_cell)) for c in cols)
            + " |"
        )
    return "\n".join(out) + "\n"


def details(title: str, rows: list[dict[str, Any]], max_cell: int = 220) -> str:
    return (
        f"<details>\n<summary>{md_escape(title)} ({len(rows)} rows)</summary>\n\n"
        f"{md_table(rows, max_cell=max_cell)}\n"
        "</details>\n"
    )


def compile_many(patterns: Iterable[str]) -> list[re.Pattern[str]]:
    return [re.compile(p, re.IGNORECASE | re.DOTALL) for p in patterns]


def matched_labels(text: str, groups: dict[str, tuple[str, ...]]) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for label, patterns in groups.items():
        matches = []
        for pattern in compile_many(patterns):
            m = pattern.search(text)
            if m:
                matches.append(m.group(0))
        if matches:
            found[label] = matches
    return found


def context_around(text: str, match: re.Match[str], before: int = 140, after: int = 260) -> str:
    return normalize_ws(text[max(0, match.start() - before): min(len(text), match.end() + after)])


def first_context(text: str, patterns: Iterable[str], before: int = 140, after: int = 260) -> str | None:
    for pattern in compile_many(patterns):
        m = pattern.search(text)
        if m:
            return context_around(text, m, before, after)
    return None


def is_us_location(location: str | None) -> bool:
    low = (location or "").lower()
    return any(h in low for h in US_LOCATION_HINTS)


def read_rows(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    cur = conn.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


# ---------------------------------------------------------------------------
# Description-section parsing
# ---------------------------------------------------------------------------

def extract_qualification_section(description: str) -> tuple[str, str]:
    """Return (section_text, extraction_method)."""
    low = description.lower()
    starts: list[tuple[int, str]] = []
    for heading in QUALIFICATION_HEADINGS:
        idx = low.find(heading)
        if idx >= 0:
            starts.append((idx, heading))
    if not starts:
        return description, "whole_description_fallback"

    start, heading = min(starts, key=lambda x: x[0])
    end = len(description)
    for end_heading in SECTION_END_HEADINGS:
        idx = low.find(end_heading, start + len(heading))
        if idx >= 0:
            end = min(end, idx)
    return description[start:end].strip(), f"heading:{heading}"


def extract_responsibility_section(description: str) -> tuple[str, str]:
    low = description.lower()
    starts = []
    for heading in (
        "in this role, you will",
        "in this role you will",
        "you’ll be responsible for",
        "you'll be responsible for",
        "responsibilities",
    ):
        idx = low.find(heading)
        if idx >= 0:
            starts.append((idx, heading))
    if not starts:
        return description, "whole_description_fallback"

    start, heading = min(starts, key=lambda x: x[0])
    end = len(description)
    for qheading in QUALIFICATION_HEADINGS + SECTION_END_HEADINGS:
        idx = low.find(qheading, start + len(heading))
        if idx >= 0:
            end = min(end, idx)
    return description[start:end].strip(), f"heading:{heading}"


# ---------------------------------------------------------------------------
# Requirement extraction
# ---------------------------------------------------------------------------
YEAR_PATTERNS = [
    re.compile(r"\b(?:at least|minimum(?: of)?|min\.?)[ ]+(\d{1,2})\s*\+?\s*(?:years?|yrs?)\b", re.I),
    re.compile(r"\b(\d{1,2})\s*\+\s*(?:years?|yrs?)\b", re.I),
    re.compile(r"\b(\d{1,2})\s*(?:-|–|—|to)\s*(\d{1,2})\s+(?:years?|yrs?)\b", re.I),
    re.compile(r"\b(\d{1,2})\s+(?:years?|yrs?)\s+of\b", re.I),
    re.compile(r"\b(" + "|".join(NUMBER_WORDS) + r")\s+(?:years?|yrs?)\s+of\b", re.I),
]


def detect_year_mentions(section: str) -> list[dict[str, Any]]:
    clean = normalize_ws(section)
    seen = set()
    found = []
    for pattern in YEAR_PATTERNS:
        for m in pattern.finditer(clean):
            span = m.span()
            if span in seen:
                continue
            seen.add(span)
            nums: list[int] = []
            for group in m.groups():
                if not group:
                    continue
                gl = group.lower()
                if gl.isdigit():
                    nums.append(int(gl))
                elif gl in NUMBER_WORDS:
                    nums.append(NUMBER_WORDS[gl])
            found.append({
                "raw": m.group(0),
                "numbers": nums,
                "minimum_years_implied": min(nums) if nums else None,
                "maximum_years_mentioned": max(nums) if nums else None,
                "context": context_around(clean, m, 120, 220),
            })
    return found


def education_signals(section: str) -> list[dict[str, str]]:
    clean = normalize_ws(section)
    groups = {
        "PHD": (r"\bph\.?d\.?\b", r"\bdoctorate\b"),
        "MASTERS": (r"\bmaster'?s degree\b", r"\bmasters degree\b", r"\bm\.?s\.?\b"),
        "BACHELORS": (r"\bbachelor'?s degree\b", r"\bbachelors degree\b", r"\bb\.?s\.?\b"),
        "EQUIVALENT_EXPERIENCE": (
            r"\bdegree or equivalent\b",
            r"\bequivalent experience\b",
            r"\bequivalent practical experience\b",
        ),
    }
    out = []
    for label, patterns in groups.items():
        for pat in compile_many(patterns):
            m = pat.search(clean)
            if m:
                out.append({"signal": label, "context": context_around(clean, m, 100, 180)})
                break
    return out


# ---------------------------------------------------------------------------
# Location / sales / technical classifications
# ---------------------------------------------------------------------------
REMOTE_EXPLICIT_PATTERNS = (
    r"\bremote(?:ly)? within (?:the )?(?:united states|u\.?s\.?)\b",
    r"\b(?:united states|u\.?s\.?) remote\b",
    r"\bremote role\b",
    r"\bfully remote\b",
    r"\bwork remotely\b",
)

OFFICE_DAY_PATTERNS = (
    r"\brequires?\s+(\d|one|two|three|four|five)\s+days?\s+(?:in (?:the )?office|onsite|on[- ]site)(?:\s+per week)?\b",
    r"\bhybrid work model of\s+(\d|one|two|three|four|five)\s+days?\s+in (?:the )?office(?:\s+per week)?\b",
    r"\b(\d|one|two|three|four|five)\s+days?\s+in (?:the )?office\s+per week\b",
)

RELOCATION_PATTERNS = (
    r"\boffer(?:s|ed|ing)? relocation assistance\b",
    r"\brelocation assistance (?:is )?(?:available|provided|offered)\b",
    r"\brelocation package\b",
)


def office_days(description: str) -> tuple[int | None, str | None]:
    clean = normalize_ws(description)
    for pat in compile_many(OFFICE_DAY_PATTERNS):
        m = pat.search(clean)
        if not m:
            continue
        raw = m.group(1).lower()
        days = int(raw) if raw.isdigit() else NUMBER_WORDS.get(raw)
        return days, context_around(clean, m, 100, 180)
    return None, None


def classify_location(role: dict[str, Any]) -> dict[str, Any]:
    primary = role.get("display_location") or ""
    secondaries = role.get("secondary_locations") or []
    all_locations = [primary] + secondaries
    description = role.get("description_plain") or ""
    workplace = role.get("workplace_type")
    is_remote = role.get("is_remote")

    us_remote_primary = primary.strip().lower() in {"us - remote", "u.s. - remote", "usa - remote"}
    us_remote_secondary = any((x or "").strip().lower() in {"us - remote", "u.s. - remote", "usa - remote"} for x in secondaries)
    any_us_remote = us_remote_primary or us_remote_secondary

    explicit_remote_context = first_context(description, REMOTE_EXPLICIT_PATTERNS)
    relocation_context = first_context(description, RELOCATION_PATTERNS)
    days, office_context = office_days(description)

    has_us_office = any(is_us_location(x) and "remote" not in (x or "").lower() for x in all_locations)

    if workplace == "Remote" and any_us_remote:
        category = "A_US_REMOTE_STRONG"
        confidence = "HIGH"
        reason = "workplace_type=Remote and US - Remote appears in primary or secondary locations"
    elif any_us_remote and explicit_remote_context:
        category = "A_US_REMOTE_STRONG"
        confidence = "HIGH"
        reason = "US - Remote appears in locations and description explicitly describes US remote work"
    elif any_us_remote:
        category = "B_US_REMOTE_AMBIGUOUS"
        confidence = "MEDIUM"
        reason = "US - Remote appears in primary/secondary locations, but structured/descriptive remote evidence is ambiguous"
    elif workplace == "Remote" and has_us_office:
        category = "B_REMOTE_US_LOCATION_AMBIGUOUS"
        confidence = "MEDIUM"
        reason = "workplace_type=Remote with a US city location but no explicit US - Remote location"
    elif relocation_context and has_us_office:
        category = "C_US_RELOCATION_SUPPORTED"
        confidence = "HIGH"
        reason = "US office location with explicit relocation-assistance wording"
    elif has_us_office and days:
        category = "D_US_ONSITE_OR_HYBRID"
        confidence = "HIGH"
        reason = f"US office location with explicit {days}-day office requirement and no proven Utah-remote path"
    elif has_us_office:
        category = "D_US_LOCATION_UNCLEAR"
        confidence = "MEDIUM"
        reason = "US office location, but remote/relocation terms are not conclusive"
    else:
        category = "E_NON_US_OR_JURISDICTION_MISMATCH"
        confidence = "HIGH"
        reason = "No US-remote or US-office path identified from current posting data"

    return {
        "location_category": category,
        "location_confidence": confidence,
        "location_reason": reason,
        "us_remote_primary": us_remote_primary,
        "us_remote_secondary": us_remote_secondary,
        "remote_description_context": explicit_remote_context,
        "relocation_assistance": bool(relocation_context),
        "relocation_context": relocation_context,
        "office_days_per_week": days,
        "office_requirement_context": office_context,
    }


def classify_sales(role: dict[str, Any], responsibility_text: str, qualification_text: str) -> dict[str, Any]:
    title = role["title"] or ""
    team = role["team"] or ""
    combined = normalize_ws((responsibility_text or "") + " " + (qualification_text or ""))

    strong = matched_labels(combined, STRONG_SALES_PATTERNS)
    context = matched_labels(combined, CONTEXT_SALES_PATTERNS)
    title_hits = [p.pattern for p in compile_many(HARD_SALES_TITLE_PATTERNS) if p.search(title)]

    hard_team = team.strip().lower() == "sales"
    if hard_team or title_hits:
        classification = "EXCLUDE_STRONG_SALES"
        reason = "Sales team or strongly sales-specific title"
    elif strong:
        classification = "EXCLUDE_STRONG_SALES"
        reason = "Description contains strong sales-function evidence such as quota/pipeline/prospecting/closing"
    elif context:
        classification = "REVIEW_SALES_CONTEXT"
        reason = "Sales-adjacent context exists, but no strong sales-function evidence was detected"
    else:
        classification = "NO_SALES_SIGNAL_FOUND"
        reason = "No strong or contextual sales signal detected by current rules"

    return {
        "sales_classification": classification,
        "sales_reason": reason,
        "sales_team": hard_team,
        "sales_title_patterns": title_hits,
        "strong_sales_signals": strong,
        "context_sales_signals": context,
    }


def classify_technical(role: dict[str, Any], responsibility_text: str) -> dict[str, Any]:
    text = normalize_ws(responsibility_text)
    technical = matched_labels(text, TECHNICAL_CORE_PATTERNS)
    evidence = matched_labels(normalize_ws(role.get("description_plain") or ""), EVIDENCE_PATTERNS)

    technical_count = len(technical)
    evidence_count = len(evidence)

    # Transparent bands, not a role-fit score.
    if technical_count >= 4:
        core = "HIGH"
    elif technical_count >= 2:
        core = "MEDIUM"
    elif technical_count == 1:
        core = "LOW"
    else:
        core = "NONE_DETECTED"

    return {
        "technical_core_level": core,
        "technical_core_signal_count": technical_count,
        "technical_core_signals": technical,
        "resume_evidence_overlap_count": evidence_count,
        "resume_evidence_overlap_categories": evidence,
    }


def review_priority(dossier: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if dossier["sales_classification"] == "EXCLUDE_STRONG_SALES":
        return "EXCLUDED_SALES", [dossier["sales_reason"]]

    if dossier["technical_core_level"] in {"NONE_DETECTED", "LOW"}:
        return "LOW_TECHNICAL_PRIORITY", ["Insufficient hands-on technical signals for the user's stated target"]

    loc = dossier["location_category"]
    overlap = dossier["resume_evidence_overlap_count"]
    tech = dossier["technical_core_signal_count"]

    if loc == "A_US_REMOTE_STRONG" and overlap >= 4 and tech >= 2:
        reasons.extend(["Strong current US-remote evidence", f"{overlap} documented-evidence vocabulary categories overlap"])
        return "P1_DEEP_REVIEW", reasons

    if loc == "B_US_REMOTE_AMBIGUOUS" and overlap >= 5 and tech >= 2:
        reasons.extend(["US-Remote appears in posting locations but remote status needs manual confirmation", f"{overlap} evidence-overlap categories"])
        return "P1_DEEP_REVIEW", reasons

    if loc == "C_US_RELOCATION_SUPPORTED" and overlap >= 5 and tech >= 2:
        reasons.extend(["Strong technical/evidence overlap", "Explicit relocation assistance may make non-Utah role financially possible"])
        return "P1_DEEP_REVIEW", reasons

    if loc in {"A_US_REMOTE_STRONG", "B_US_REMOTE_AMBIGUOUS", "B_REMOTE_US_LOCATION_AMBIGUOUS", "C_US_RELOCATION_SUPPORTED"} and overlap >= 3:
        reasons.extend(["Potentially workable geography or relocation path", f"{overlap} evidence-overlap categories"])
        return "P2_REVIEW", reasons

    if loc.startswith("D_US_") and overlap >= 6:
        reasons.extend(["Strong evidence overlap but no proven Utah-remote path", "Keep as relocation/location benchmark"])
        return "P2_REVIEW", reasons

    return "P3_BACKGROUND", ["Technical role worth preserving, but current geography/evidence intersection is weaker"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Run ProofLoop role-selection transparency analysis v0.15")
    parser.add_argument("--db", type=Path, default=Path("proofloop_enriched.db"))
    parser.add_argument("--markdown", type=Path, default=Path("proofloop_role_analysis_report_v0_15.md"))
    parser.add_argument("--json", dest="json_output", type=Path, default=Path("proofloop_role_analysis_report_v0_15.json"))
    parser.add_argument("--deep-review-limit", type=int, default=75)
    args = parser.parse_args()

    if not args.db.is_file():
        print(f"ERROR: database not found: {args.db}", file=sys.stderr)
        return 2

    db_abs = args.db.resolve()
    conn = sqlite3.connect(db_abs.as_uri() + "?mode=ro", uri=True)

    sql_catalog: dict[str, str] = {}
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            print(f"ERROR: SQLite integrity_check returned {integrity!r}", file=sys.stderr)
            return 1

        role_sql = """
            SELECT
                ashby_id, title, team, department, employment_type,
                display_location, published_at, is_listed, is_remote,
                workplace_type, career_url, job_url, apply_url,
                description_plain, present_in_html, present_in_api, source_status
            FROM roles
            WHERE present_in_api = 1
            ORDER BY team, title, ashby_id
        """
        sql_catalog["current_roles"] = role_sql
        roles = read_rows(conn, role_sql)

        sec_sql = """
            SELECT ashby_id, location_index, location
            FROM api_secondary_locations
            ORDER BY ashby_id, location_index
        """
        sql_catalog["secondary_locations"] = sec_sql
        secondary_rows = read_rows(conn, sec_sql)

        comp_sql = """
            SELECT ashby_id, component_index, compensation_type, interval,
                   currency_code, min_value, max_value
            FROM api_compensation_components
            ORDER BY ashby_id, component_index
        """
        sql_catalog["compensation_components"] = comp_sql
        comp_rows = read_rows(conn, comp_sql)

        source_sql = """
            SELECT source_status, COUNT(*) AS roles
            FROM roles
            GROUP BY source_status
            ORDER BY source_status
        """
        sql_catalog["source_status_counts"] = source_sql
        source_counts = read_rows(conn, source_sql)

        team_sql = """
            SELECT team, COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY team
            ORDER BY roles DESC, team
        """
        sql_catalog["team_counts"] = team_sql
        team_counts = read_rows(conn, team_sql)

        primary_sql = """
            SELECT COALESCE(display_location,'NULL') AS location, COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY display_location
            ORDER BY roles DESC, location
        """
        sql_catalog["primary_location_counts"] = primary_sql
        primary_counts = read_rows(conn, primary_sql)

        arrangement_sql = """
            SELECT COALESCE(CAST(is_remote AS TEXT),'NULL') AS is_remote,
                   COALESCE(workplace_type,'NULL') AS workplace_type,
                   COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY is_remote, workplace_type
            ORDER BY roles DESC
        """
        sql_catalog["work_arrangement_counts"] = arrangement_sql
        arrangement_counts = read_rows(conn, arrangement_sql)

        quality_sql = """
            SELECT
                COUNT(*) AS current_roles,
                SUM(CASE WHEN description_plain IS NULL OR TRIM(description_plain)='' THEN 1 ELSE 0 END) AS missing_description,
                SUM(CASE WHEN workplace_type IS NULL THEN 1 ELSE 0 END) AS missing_workplace_type,
                SUM(CASE WHEN is_remote IS NULL THEN 1 ELSE 0 END) AS missing_is_remote,
                SUM(CASE WHEN display_location IS NULL OR TRIM(display_location)='' THEN 1 ELSE 0 END) AS missing_primary_location,
                SUM(CASE WHEN published_at IS NULL THEN 1 ELSE 0 END) AS missing_published_at
            FROM roles
            WHERE present_in_api = 1
        """
        sql_catalog["data_quality"] = quality_sql
        data_quality = read_rows(conn, quality_sql)[0]
    finally:
        conn.close()

    secondary_by_id: dict[str, list[str]] = defaultdict(list)
    for row in secondary_rows:
        if row["location"]:
            secondary_by_id[row["ashby_id"]].append(row["location"])

    comp_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in comp_rows:
        comp_by_id[row["ashby_id"]].append({
            "compensation_type": row["compensation_type"],
            "interval": row["interval"],
            "currency_code": row["currency_code"],
            "min_value": row["min_value"],
            "max_value": row["max_value"],
        })

    dossiers: list[dict[str, Any]] = []

    for role in roles:
        role = dict(role)
        role["secondary_locations"] = secondary_by_id.get(role["ashby_id"], [])
        role["compensation_components"] = comp_by_id.get(role["ashby_id"], [])
        desc = role.get("description_plain") or ""

        qualifications, q_method = extract_qualification_section(desc)
        responsibilities, r_method = extract_responsibility_section(desc)

        loc = classify_location(role)
        sales = classify_sales(role, responsibilities, qualifications)
        tech = classify_technical(role, responsibilities)
        years = detect_year_mentions(qualifications)
        education = education_signals(qualifications)

        salary_components = [
            c for c in role["compensation_components"]
            if (c.get("compensation_type") or "").lower() == "salary"
        ]

        dossier = {
            "ashby_id": role["ashby_id"],
            "title": role["title"],
            "team": role["team"],
            "department": role["department"],
            "employment_type": role["employment_type"],
            "published_at": role["published_at"],
            "primary_location": role["display_location"],
            "secondary_locations": role["secondary_locations"],
            "workplace_type": role["workplace_type"],
            "is_remote": role["is_remote"],
            **loc,
            **sales,
            **tech,
            "qualification_extraction_method": q_method,
            "responsibility_extraction_method": r_method,
            "experience_year_mentions": years,
            "education_signals": education,
            "salary_components": salary_components,
            "apply_url": role["apply_url"],
            "job_url": role["job_url"],
        }
        priority, priority_reasons = review_priority(dossier)
        dossier["review_priority"] = priority
        dossier["review_priority_reasons"] = priority_reasons
        dossiers.append(dossier)

    # Derived counts and diagnostic inventories.
    location_counts = Counter(d["location_category"] for d in dossiers)
    sales_counts = Counter(d["sales_classification"] for d in dossiers)
    tech_counts = Counter(d["technical_core_level"] for d in dossiers)
    priority_counts = Counter(d["review_priority"] for d in dossiers)

    us_remote_anywhere = [d for d in dossiers if d["us_remote_primary"] or d["us_remote_secondary"]]
    remote_strong = [d for d in dossiers if d["location_category"] == "A_US_REMOTE_STRONG"]
    relocation_supported = [d for d in dossiers if d["location_category"] == "C_US_RELOCATION_SUPPORTED"]
    sales_excluded = [d for d in dossiers if d["sales_classification"] == "EXCLUDE_STRONG_SALES"]
    sales_context = [d for d in dossiers if d["sales_classification"] == "REVIEW_SALES_CONTEXT"]

    deep_pool = [d for d in dossiers if d["review_priority"] in {"P1_DEEP_REVIEW", "P2_REVIEW"}]
    priority_order = {"P1_DEEP_REVIEW": 0, "P2_REVIEW": 1}
    location_order = {
        "A_US_REMOTE_STRONG": 0,
        "B_US_REMOTE_AMBIGUOUS": 1,
        "B_REMOTE_US_LOCATION_AMBIGUOUS": 2,
        "C_US_RELOCATION_SUPPORTED": 3,
        "D_US_ONSITE_OR_HYBRID": 4,
        "D_US_LOCATION_UNCLEAR": 5,
        "E_NON_US_OR_JURISDICTION_MISMATCH": 6,
    }
    deep_pool.sort(key=lambda d: (
        priority_order.get(d["review_priority"], 9),
        location_order.get(d["location_category"], 9),
        -d["resume_evidence_overlap_count"],
        -d["technical_core_signal_count"],
        d["team"],
        d["title"],
    ))
    deep_pool = deep_pool[: max(1, args.deep_review_limit)]

    # High-value diagnostics for roles likely to matter to this search.
    interesting_titles = re.compile(
        r"(?i)\b(support|technical operations|deployment engineer|early access|"
        r"it support|systems program manager|security program manager|"
        r"threat investigator|support operations|user operations|"
        r"solutions engineer|applied ai engineer)\b"
    )
    named_interest = [d for d in dossiers if interesting_titles.search(d["title"])]

    # Flat report-friendly rows.
    def report_row(d: dict[str, Any]) -> dict[str, Any]:
        years = "; ".join(x["raw"] for x in d["experience_year_mentions"][:4])
        salary = "; ".join(
            f"{c.get('currency_code') or ''} {c.get('min_value')}–{c.get('max_value')} / {c.get('interval') or '?'}"
            for c in d["salary_components"]
        )
        return {
            "title": d["title"],
            "team": d["team"],
            "primary": d["primary_location"],
            "secondary": "; ".join(d["secondary_locations"]),
            "workplace": d["workplace_type"],
            "location_class": d["location_category"],
            "sales": d["sales_classification"],
            "technical": d["technical_core_level"],
            "evidence_overlap": d["resume_evidence_overlap_count"],
            "years_mentions": years,
            "relocation": "YES" if d["relocation_assistance"] else "NO",
            "office_days": d["office_days_per_week"],
            "salary": salary,
            "priority": d["review_priority"],
        }

    derived_summary = {
        "current_api_roles": len(dossiers),
        "us_remote_anywhere": len(us_remote_anywhere),
        "strong_us_remote": len(remote_strong),
        "relocation_supported_us_roles": len(relocation_supported),
        "sales_excluded_roles": len(sales_excluded),
        "sales_context_review_roles": len(sales_context),
        "location_category_counts": dict(location_counts),
        "sales_classification_counts": dict(sales_counts),
        "technical_core_counts": dict(tech_counts),
        "review_priority_counts": dict(priority_counts),
        "deep_review_pool_emitted": len(deep_pool),
    }

    payload = {
        "battery": VERSION,
        "generated_at_utc": utc_now(),
        "database": str(db_abs),
        "database_mode": "read-only",
        "methodology_notes": [
            "No role is selected solely by this battery.",
            "NO SALES is modeled as strong exclusion evidence vs contextual review evidence.",
            "Regex word boundaries are used to prevent obvious substring false positives such as commissioning->commission.",
            "Location feasibility combines primary location, secondary locations, workplace_type, is_remote, actual remote wording, office-day wording, and relocation wording.",
            "US - Remote in a secondary location is not automatically treated as permission to work from Utah.",
            "Relocation assistance is not treated as permission to begin remotely.",
            "Experience and education signals are extracted preferentially from the qualifications section.",
            "Resume/evidence overlap is a discovery aid and not a qualification or fit score.",
            "The deep-review pool uses explainable bands and is not a hidden final ranking.",
            "Compensation is preserved with interval and currency.",
        ],
        "pattern_definitions": {
            "evidence_patterns": EVIDENCE_PATTERNS,
            "technical_core_patterns": TECHNICAL_CORE_PATTERNS,
            "strong_sales_patterns": STRONG_SALES_PATTERNS,
            "context_sales_patterns": CONTEXT_SALES_PATTERNS,
            "hard_sales_title_patterns": HARD_SALES_TITLE_PATTERNS,
        },
        "source_status_counts": source_counts,
        "team_counts": team_counts,
        "primary_location_counts": primary_counts,
        "work_arrangement_counts": arrangement_counts,
        "data_quality": data_quality,
        "derived_summary": derived_summary,
        "sql_catalog": sql_catalog,
        "deep_review_pool": deep_pool,
        "named_interest_roles": named_interest,
        "all_role_dossiers": dossiers,
    }

    args.json_output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md: list[str] = []
    md.append("# ProofLoop Role Selection Transparency Report v0.15\n\n")
    md.append(f"Generated: `{payload['generated_at_utc']}`  \n")
    md.append(f"Database: `{db_abs}`  \n")
    md.append("Database access: **read-only**\n\n")

    md.append("## Purpose\n\n")
    md.append(
        "This revision turns the first exploratory battery into a more defensible role-selection evidence report. "
        "It still does **not** choose Application #001. Its job is to expose the evidence, contradictions, and "
        "candidate-review paths clearly enough that the eventual choice can be defended.\n\n"
    )

    md.append("## Methodology guardrails\n\n")
    for note in payload["methodology_notes"]:
        md.append(f"- {note}\n")

    md.append("\n## Executive summary\n\n")
    for key, value in derived_summary.items():
        if not isinstance(value, dict):
            md.append(f"- **{key.replace('_',' ')}:** {value}\n")

    md.append("\n### Location classification counts\n\n")
    md.append(md_table([{"location_category": k, "roles": v} for k, v in location_counts.most_common()]))

    md.append("\n### Sales classification counts\n\n")
    md.append(md_table([{"sales_classification": k, "roles": v} for k, v in sales_counts.most_common()]))

    md.append("\n### Technical-core counts\n\n")
    md.append(md_table([{"technical_core_level": k, "roles": v} for k, v in tech_counts.most_common()]))

    md.append("\n### Review-priority counts\n\n")
    md.append(md_table([{"review_priority": k, "roles": v} for k, v in priority_counts.most_common()]))

    md.append("\n## 1. Source status\n\n")
    md.append(md_table(source_counts))

    md.append("\n## 2. Work-arrangement field behavior\n\n")
    md.append(md_table(arrangement_counts))

    md.append("\n## 3. Primary location distribution\n\n")
    md.append(details("All primary locations", primary_counts))

    md.append("\n## 4. Team distribution\n\n")
    md.append(details("All teams", team_counts))

    md.append("\n## 5. US-remote evidence inventory\n\n")
    md.append(
        "These are roles where `US - Remote` appears as a primary or secondary location. "
        "The location classification keeps strong remote evidence separate from ambiguous hybrid/secondary evidence.\n\n"
    )
    md.append(details("US-Remote anywhere", [report_row(d) for d in us_remote_anywhere], max_cell=280))

    md.append("\n## 6. Strong US-remote roles\n\n")
    md.append(details("A_US_REMOTE_STRONG", [report_row(d) for d in remote_strong], max_cell=280))

    md.append("\n## 7. Relocation-supported US roles\n\n")
    md.append(
        "These roles explicitly mention relocation assistance. This is preserved as a separate path from remote work; "
        "it does not imply permission to begin from Utah.\n\n"
    )
    md.append(details("C_US_RELOCATION_SUPPORTED", [report_row(d) for d in relocation_supported], max_cell=280))

    md.append("\n## 8. Revised NO SALES analysis\n\n")
    md.append(
        "v0.15 separates strong exclusion evidence from contextual sales-adjacent terms. "
        "It also uses word-boundary regexes so terms such as **commissioning** do not match **commission**.\n\n"
    )
    md.append(details("Strong sales exclusions", [report_row(d) for d in sales_excluded], max_cell=280))
    md.append("\n")
    md.append(details("Sales context requiring manual review", [report_row(d) for d in sales_context], max_cell=280))

    md.append("\n## 9. Deep-review candidate pool\n\n")
    md.append(
        "This is **not a final ranking**. Roles enter this pool only through explicit rules combining technical-core evidence, "
        "documented-evidence overlap, NO-SALES handling, and a plausible US-remote / relocation / US-location path.\n\n"
    )
    md.append(md_table([report_row(d) for d in deep_pool], max_cell=300))

    md.append("\n## 10. Candidate dossiers for deep-review pool\n\n")
    for d in deep_pool:
        md.append(f"### {d['title']} — {d['team']}\n\n")
        md.append(f"- **Priority:** {d['review_priority']} — {'; '.join(d['review_priority_reasons'])}\n")
        md.append(f"- **Location:** {d['location_category']} ({d['location_confidence']}) — {d['location_reason']}\n")
        md.append(f"- **Primary / secondary:** {d['primary_location']} / {', '.join(d['secondary_locations']) or 'none'}\n")
        md.append(f"- **Workplace metadata:** workplace_type={d['workplace_type']!r}, is_remote={d['is_remote']!r}\n")
        md.append(f"- **Relocation assistance:** {'YES' if d['relocation_assistance'] else 'NO'}\n")
        md.append(f"- **Office days detected:** {d['office_days_per_week'] if d['office_days_per_week'] is not None else 'not detected'}\n")
        md.append(f"- **Sales classification:** {d['sales_classification']} — {d['sales_reason']}\n")
        md.append(f"- **Technical core:** {d['technical_core_level']} ({d['technical_core_signal_count']} categories)\n")
        md.append(f"- **Evidence overlap:** {d['resume_evidence_overlap_count']} categories: {', '.join(d['resume_evidence_overlap_categories'].keys()) or 'none'}\n")
        if d["experience_year_mentions"]:
            md.append("- **Experience-year mentions:** " + "; ".join(x["raw"] for x in d["experience_year_mentions"]) + "\n")
        else:
            md.append("- **Experience-year mentions:** none detected in extracted qualification section\n")
        if d["education_signals"]:
            md.append("- **Education signals:** " + "; ".join(x["signal"] for x in d["education_signals"]) + "\n")
        else:
            md.append("- **Education signals:** none detected in extracted qualification section\n")
        if d["remote_description_context"]:
            md.append(f"- **Remote context:** {trunc(d['remote_description_context'], 520)}\n")
        if d["relocation_context"]:
            md.append(f"- **Relocation context:** {trunc(d['relocation_context'], 520)}\n")
        if d["office_requirement_context"]:
            md.append(f"- **Office requirement context:** {trunc(d['office_requirement_context'], 520)}\n")
        if d["salary_components"]:
            salary_text = "; ".join(
                f"{c.get('currency_code') or ''} {c.get('min_value')}–{c.get('max_value')} / {c.get('interval') or '?'}"
                for c in d["salary_components"]
            )
            md.append(f"- **Salary component(s):** {salary_text}\n")
        md.append(f"- **Apply URL:** {d['apply_url']}\n\n")

    md.append("\n## 11. Named-interest inventory\n\n")
    md.append(
        "Broad inventory of titles likely to deserve human attention because they contain support, technical operations, "
        "deployment, IT support, program-management, security-investigation, or applied-AI language.\n\n"
    )
    md.append(details("Named-interest roles", [report_row(d) for d in named_interest], max_cell=280))

    md.append("\n## 12. Experience and education diagnostics\n\n")
    exp_rows = []
    edu_rows = []
    for d in dossiers:
        if d["experience_year_mentions"]:
            exp_rows.append({
                "title": d["title"],
                "team": d["team"],
                "location": d["primary_location"],
                "qualification_method": d["qualification_extraction_method"],
                "mentions": "; ".join(x["raw"] for x in d["experience_year_mentions"]),
                "contexts": " || ".join(x["context"] for x in d["experience_year_mentions"][:3]),
            })
        if d["education_signals"]:
            edu_rows.append({
                "title": d["title"],
                "team": d["team"],
                "location": d["primary_location"],
                "qualification_method": d["qualification_extraction_method"],
                "signals": "; ".join(x["signal"] for x in d["education_signals"]),
                "contexts": " || ".join(x["context"] for x in d["education_signals"][:3]),
            })
    md.append(details("Experience-year mentions from qualification sections", exp_rows, max_cell=460))
    md.append("\n")
    md.append(details("Education signals from qualification sections", edu_rows, max_cell=460))

    md.append("\n## 13. Compensation diagnostics\n\n")
    comp_report = []
    for d in dossiers:
        for c in d["salary_components"]:
            comp_report.append({
                "title": d["title"],
                "team": d["team"],
                "location": d["primary_location"],
                "currency": c.get("currency_code"),
                "interval": c.get("interval"),
                "min": c.get("min_value"),
                "max": c.get("max_value"),
            })
    md.append(details("Salary components with interval preserved", comp_report, max_cell=240))

    md.append("\n## 14. Data-quality summary\n\n")
    md.append(md_table([data_quality]))

    md.append("\n## 15. Exact SQL catalog\n\n")
    for name, sql in sql_catalog.items():
        md.append(f"### {name}\n\n```sql\n{sql.strip()}\n```\n\n")

    md.append("## 16. What this report still does not claim\n\n")
    md.append(
        "- A high evidence-overlap count does not prove qualification.\n"
        "- A remote location field does not prove Utah eligibility unless the posting evidence supports it.\n"
        "- Relocation assistance does not prove the employer will fund every up-front cost or allow delayed relocation.\n"
        "- An experience-year mention is not automatically a hard requirement unless the qualification language says so.\n"
        "- Sales-context terms are not automatic exclusions; strong sales-function evidence is separated from context.\n"
        "- The deep-review pool is a bounded investigation set, not the final application list.\n"
    )

    args.markdown.write_text("".join(md), encoding="utf-8")

    print(VERSION)
    print(f"Database:                    {db_abs}")
    print("Database mode:               READ ONLY")
    print(f"Current API roles:           {len(dossiers)}")
    print(f"US-Remote anywhere:          {len(us_remote_anywhere)}")
    print(f"Strong US-Remote:            {len(remote_strong)}")
    print(f"Relocation-supported US:     {len(relocation_supported)}")
    print(f"Strong sales exclusions:     {len(sales_excluded)}")
    print(f"Sales context review:        {len(sales_context)}")
    print(f"Deep-review pool emitted:    {len(deep_pool)}")
    print(f"Markdown report:             {args.markdown}")
    print(f"JSON report:                 {args.json_output}")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
