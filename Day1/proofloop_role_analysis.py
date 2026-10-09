#!/usr/bin/env python3
"""
ProofLoop Role Selection Transparency Battery v0.14

Purpose
-------
Run one read-only analysis battery against proofloop_enriched.db and generate
a transparent, reproducible report for role selection.

The report is intentionally exploratory. It does NOT decide which role to apply
to and it does NOT treat keyword overlap as a fit score.

Outputs
-------
- proofloop_role_analysis_report.md     Human-readable GitHub-friendly report
- proofloop_role_analysis_report.json   Full machine-readable results

Key questions covered
---------------------
1. What is the current role population?
2. What do Ashby's remote/workplace fields actually say?
3. Where are roles located, including secondary locations?
4. Which roles have US-Remote anywhere in their allowed locations?
5. Which structured location/workplace fields conflict?
6. What does the description actually say around "remote" and "relocation"?
7. Which teams/job families dominate the current population?
8. Which roles overlap with the user's documented technical evidence vocabulary?
9. Which roles contain sales / revenue / quota / prospecting signals?
10. What explicit experience-year signals appear?
11. What education/degree signals appear?
12. What compensation is present, with interval preserved?
13. What data-quality gaps or null fields should affect interpretation?

Safety / integrity
------------------
- Opens SQLite in read-only mode.
- Executes SELECT / PRAGMA queries only.
- Does not modify proofloop_enriched.db.
- Does not modify source JSON/JSONL artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VERSION = "ProofLoop Role Selection Transparency Battery v0.14"

RELEVANT_TEAMS = (
    "Support Delivery",
    "Support Operations",
    "Support Automation",
    "IT",
    "Security",
    "Trust & Safety",
    "Intelligence & Investigations",
    "Technical Success",
    "User Operations",
    "Technical Program Management",
)

# These are evidence-vocabulary signals based on the user's resume and the
# project discussion. They are discovery aids, NOT proof of qualification.
EVIDENCE_SIGNALS = {
    "support": (
        "%support%",
    ),
    "troubleshooting": (
        "%troubleshoot%",
        "%diagnos%",
        "%root cause%",
    ),
    "api_integrations": (
        "%api%",
        "%integration%",
        "%webhook%",
    ),
    "automation": (
        "%automat%",
        "%workflow%",
    ),
    "scripting_programming": (
        "%python%",
        "%javascript%",
        "%powershell%",
        "%bash%",
        "%script%",
    ),
    "sql_data": (
        "%sql%",
        "%database%",
        "%data analysis%",
    ),
    "ticketing_itsm": (
        "%jira%",
        "%ticket%",
        "%itsm%",
        "%service desk%",
        "%servicenow%",
        "%zendesk%",
    ),
    "network_dns": (
        "%dns%",
        "%network%",
        "%router%",
    ),
    "uat_testing": (
        "%uat%",
        "%user acceptance%",
        "%test%",
        "%bug%",
    ),
    "documentation": (
        "%documentation%",
        "%knowledge base%",
        "%sop%",
        "%runbook%",
        "%troubleshooting guide%",
    ),
    "crm_saas": (
        "%crm%",
        "%salesforce%",
        "%saas%",
        "%microsoft 365%",
        "%exchange%",
    ),
}

SALES_PATTERNS = {
    "sales_cycle": "%sales cycle%",
    "quota": "%quota%",
    "pipeline": "%pipeline generation%",
    "prospecting": "%prospect%",
    "revenue_target": "%revenue target%",
    "closing": "%close deals%",
    "closing_alt": "%closing deals%",
    "book_of_business": "%book of business%",
    "territory": "%territory%",
    "commission": "%commission%",
    "pre_sales": "%pre-sales%",
    "presales": "%presales%",
    "account_expansion": "%account expansion%",
}

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def markdown_escape(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.replace("|", r"\|")
    text = text.replace("\r", " ").replace("\n", " ")
    return text


def truncate(value: Any, limit: int = 220) -> str:
    if value is None:
        return ""
    text = re.sub(r"\s+", " ", str(value)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def dict_rows(cursor: sqlite3.Cursor) -> list[dict[str, Any]]:
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def query(
    conn: sqlite3.Connection,
    sql: str,
    params: tuple[Any, ...] = (),
) -> list[dict[str, Any]]:
    return dict_rows(conn.execute(sql, params))


def context_snippet(
    text: str | None,
    needle: str,
    before: int = 160,
    after: int = 300,
) -> str | None:
    if not text:
        return None
    lower = text.lower()
    pos = lower.find(needle.lower())
    if pos < 0:
        return None
    start = max(0, pos - before)
    end = min(len(text), pos + len(needle) + after)
    snippet = text[start:end]
    return re.sub(r"\s+", " ", snippet).strip()


def detect_year_mentions(text: str | None) -> list[dict[str, Any]]:
    """
    Extract likely experience-year mentions more broadly than the original
    SQL CASE statement. These are still mentions, not automatically hard
    requirements.
    """
    if not text:
        return []

    clean = re.sub(r"\s+", " ", text)
    patterns = [
        re.compile(
            r"(?i)\b(?:at least|minimum(?: of)?|min\.?)\s+"
            r"(\d{1,2})\s*\+?\s*(?:years?|yrs?)\b"
        ),
        re.compile(
            r"(?i)\b(\d{1,2})\s*\+\s*(?:years?|yrs?)\b"
        ),
        re.compile(
            r"(?i)\b(\d{1,2})\s*(?:-|–|—|to)\s*(\d{1,2})\s+"
            r"(?:years?|yrs?)\b"
        ),
        re.compile(
            r"(?i)\b(\d{1,2})\s+(?:years?|yrs?)\s+of\b"
        ),
        re.compile(
            r"(?i)\b("
            + "|".join(NUMBER_WORDS)
            + r")\s+(?:years?|yrs?)\s+of\b"
        ),
    ]

    results: list[dict[str, Any]] = []
    seen_spans: set[tuple[int, int]] = set()

    for pattern in patterns:
        for m in pattern.finditer(clean):
            if m.span() in seen_spans:
                continue
            seen_spans.add(m.span())

            raw = m.group(0)
            nums: list[int] = []
            for g in m.groups():
                if not g:
                    continue
                gl = g.lower()
                if gl.isdigit():
                    nums.append(int(gl))
                elif gl in NUMBER_WORDS:
                    nums.append(NUMBER_WORDS[gl])

            results.append(
                {
                    "raw": raw,
                    "numbers": nums,
                    "max_years_mentioned": max(nums) if nums else None,
                    "context": truncate(
                        clean[max(0, m.start() - 120): m.end() + 220],
                        380,
                    ),
                }
            )

    return results


def education_signals(text: str | None) -> list[str]:
    if not text:
        return []

    low = text.lower()
    signals: list[str] = []

    checks = [
        ("PHD", ("ph.d", "phd", "doctorate")),
        ("MASTERS", ("master's degree", "masters degree", "m.s.", " ms ")),
        ("BACHELORS", ("bachelor's degree", "bachelors degree", "b.s.", " bs ")),
        (
            "DEGREE_OR_EQUIVALENT",
            (
                "degree or equivalent",
                "equivalent experience",
                "or equivalent practical experience",
            ),
        ),
    ]

    for label, needles in checks:
        if any(n in low for n in needles):
            signals.append(label)

    if "degree" in low and not signals:
        signals.append("DEGREE_MENTION_UNCLASSIFIED")

    return signals


def sql_like_clause(column: str, patterns: tuple[str, ...]) -> str:
    return "(" + " OR ".join(
        f"LOWER(COALESCE({column},'')) LIKE ?"
        for _ in patterns
    ) + ")"


def make_evidence_query() -> tuple[str, tuple[Any, ...]]:
    select_parts = []
    params: list[Any] = []

    for label, patterns in EVIDENCE_SIGNALS.items():
        clause = sql_like_clause("description_plain", patterns)
        select_parts.append(
            f"CASE WHEN {clause} THEN 1 ELSE 0 END AS {label}"
        )
        params.extend(patterns)

    score_terms = [f"{label}" for label in EVIDENCE_SIGNALS]

    # SQLite cannot reliably reuse SELECT aliases inside another SELECT
    # expression in the same level, so use a CTE.
    inner = ",\n            ".join(select_parts)
    outer_score = " + ".join(score_terms)

    sql = f"""
        WITH signals AS (
            SELECT
                ashby_id,
                title,
                team,
                display_location,
                workplace_type,
                is_remote,
                {inner}
            FROM roles
            WHERE present_in_api = 1
        )
        SELECT
            ashby_id,
            title,
            team,
            display_location,
            workplace_type,
            is_remote,
            {", ".join(EVIDENCE_SIGNALS.keys())},
            ({outer_score}) AS resume_keyword_overlap
        FROM signals
        ORDER BY resume_keyword_overlap DESC, team, title
    """

    return sql, tuple(params)


def make_sales_query() -> tuple[str, tuple[Any, ...]]:
    select_parts = []
    params: list[Any] = []

    for label, pattern in SALES_PATTERNS.items():
        select_parts.append(
            f"CASE WHEN LOWER(COALESCE(description_plain,'')) LIKE ? "
            f"THEN 1 ELSE 0 END AS {label}"
        )
        params.append(pattern)

    inner = ",\n            ".join(select_parts)
    score = " + ".join(SALES_PATTERNS.keys())

    sql = f"""
        WITH sales_signals AS (
            SELECT
                ashby_id,
                title,
                team,
                display_location,
                workplace_type,
                CASE WHEN team = 'Sales' THEN 1 ELSE 0 END AS sales_team,
                CASE
                    WHEN LOWER(title) LIKE '%sales%'
                      OR LOWER(title) LIKE '%account director%'
                      OR LOWER(title) LIKE '%seller%'
                    THEN 1 ELSE 0
                END AS sales_title,
                {inner}
            FROM roles
            WHERE present_in_api = 1
        )
        SELECT *,
               (
                   sales_team + sales_title + {score}
               ) AS sales_signal_count
        FROM sales_signals
        WHERE (
            sales_team + sales_title + {score}
        ) > 0
        ORDER BY sales_signal_count DESC, team, title
    """

    # score expression appears twice and uses the same aliases, not parameters.
    return sql, tuple(params)


def markdown_table(
    rows: list[dict[str, Any]],
    max_cell: int = 180,
) -> str:
    if not rows:
        return "_No rows._\n"

    columns = list(rows[0].keys())
    out = [
        "| " + " | ".join(markdown_escape(c) for c in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]

    for row in rows:
        out.append(
            "| "
            + " | ".join(
                markdown_escape(truncate(row.get(c), max_cell))
                for c in columns
            )
            + " |"
        )

    return "\n".join(out) + "\n"


def details_table(
    title: str,
    rows: list[dict[str, Any]],
    max_cell: int = 180,
) -> str:
    return (
        f"<details>\n<summary>{markdown_escape(title)} "
        f"({len(rows)} rows)</summary>\n\n"
        f"{markdown_table(rows, max_cell=max_cell)}\n"
        "</details>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run a read-only transparency battery against "
            "proofloop_enriched.db."
        )
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("proofloop_enriched.db"),
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=Path("proofloop_role_analysis_report.md"),
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        type=Path,
        default=Path("proofloop_role_analysis_report.json"),
    )
    parser.add_argument(
        "--top-overlap",
        type=int,
        default=100,
        help="Rows shown in the top-overlap summary table. Default: 100",
    )
    args = parser.parse_args()

    if not args.db.is_file():
        print(f"ERROR: Database not found: {args.db}", file=sys.stderr)
        return 2

    db_abs = args.db.resolve()
    uri = db_abs.as_uri() + "?mode=ro"

    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = None

    analyses: dict[str, Any] = {}
    sql_catalog: dict[str, str] = {}

    try:
        integrity = query(conn, "PRAGMA integrity_check")
        analyses["sqlite_integrity"] = integrity

        tables = query(
            conn,
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """,
        )
        analyses["tables"] = tables

        q = """
            SELECT source_status, COUNT(*) AS roles
            FROM roles
            GROUP BY source_status
            ORDER BY source_status
        """
        sql_catalog["source_status_counts"] = q
        analyses["source_status_counts"] = query(conn, q)

        q = """
            SELECT
                COUNT(*) AS current_roles,
                SUM(CASE WHEN present_in_api=1 THEN 1 ELSE 0 END)
                    AS api_current,
                SUM(CASE WHEN present_in_html=1 THEN 1 ELSE 0 END)
                    AS html_present
            FROM roles
        """
        sql_catalog["population_summary"] = q
        analyses["population_summary"] = query(conn, q)

        q = """
            SELECT
                COALESCE(CAST(is_remote AS TEXT), 'NULL') AS is_remote,
                COALESCE(workplace_type, 'NULL') AS workplace_type,
                COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY is_remote, workplace_type
            ORDER BY roles DESC
        """
        sql_catalog["work_arrangement_distribution"] = q
        analyses["work_arrangement_distribution"] = query(conn, q)

        q = """
            SELECT
                COALESCE(display_location, 'NULL') AS location,
                COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY display_location
            ORDER BY roles DESC, display_location
        """
        sql_catalog["primary_location_distribution"] = q
        analyses["primary_location_distribution"] = query(conn, q)

        q = """
            SELECT team, COUNT(*) AS roles
            FROM roles
            WHERE present_in_api = 1
            GROUP BY team
            ORDER BY roles DESC, team
        """
        sql_catalog["team_distribution"] = q
        analyses["team_distribution"] = query(conn, q)

        q = """
            SELECT
                ashby_id,
                title,
                team,
                display_location,
                COALESCE(CAST(is_remote AS TEXT), 'NULL') AS is_remote,
                COALESCE(workplace_type, 'NULL') AS workplace_type
            FROM roles
            WHERE present_in_api = 1
              AND (
                    is_remote = 1
                    OR LOWER(COALESCE(workplace_type,'')) = 'remote'
                  )
            ORDER BY team, title
        """
        sql_catalog["broad_structured_remote_pool"] = q
        analyses["broad_structured_remote_pool"] = query(conn, q)

        q = """
            SELECT
                ashby_id,
                title,
                team,
                display_location,
                workplace_type,
                is_remote
            FROM roles
            WHERE present_in_api = 1
              AND workplace_type = 'Remote'
            ORDER BY team, title
        """
        sql_catalog["true_remote_roles"] = q
        analyses["true_remote_roles"] = query(conn, q)

        q = """
            SELECT
                ashby_id,
                title,
                team,
                display_location,
                workplace_type,
                is_remote
            FROM roles
            WHERE present_in_api = 1
              AND (
                    (
                        display_location = 'US - Remote'
                        AND COALESCE(workplace_type,'') <> 'Remote'
                    )
                    OR
                    (
                        display_location NOT LIKE '%Remote%'
                        AND workplace_type = 'Remote'
                    )
                  )
            ORDER BY display_location, team, title
        """
        sql_catalog["remote_location_conflicts"] = q
        analyses["remote_location_conflicts"] = query(conn, q)

        q = """
            SELECT DISTINCT
                r.ashby_id,
                r.title,
                r.team,
                r.display_location AS primary_location,
                COALESCE(r.workplace_type,'NULL') AS workplace_type,
                COALESCE(CAST(r.is_remote AS TEXT),'NULL') AS is_remote,
                CASE
                    WHEN r.display_location='US - Remote'
                    THEN 'PRIMARY'
                    WHEN EXISTS (
                        SELECT 1
                        FROM api_secondary_locations s
                        WHERE s.ashby_id=r.ashby_id
                          AND s.location='US - Remote'
                    )
                    THEN 'SECONDARY'
                    ELSE 'NONE'
                END AS us_remote_source
            FROM roles r
            WHERE r.present_in_api=1
              AND (
                    r.display_location='US - Remote'
                    OR EXISTS (
                        SELECT 1
                        FROM api_secondary_locations s
                        WHERE s.ashby_id=r.ashby_id
                          AND s.location='US - Remote'
                    )
                  )
            ORDER BY r.team, r.title
        """
        sql_catalog["us_remote_anywhere"] = q
        analyses["us_remote_anywhere"] = query(conn, q)

        q = """
            SELECT
                r.ashby_id,
                r.title,
                r.team,
                r.display_location AS primary_location,
                s.location AS secondary_location,
                COALESCE(r.workplace_type,'NULL') AS workplace_type
            FROM roles r
            JOIN api_secondary_locations s
              ON s.ashby_id=r.ashby_id
            WHERE r.present_in_api=1
            ORDER BY r.team, r.title, s.location_index
        """
        sql_catalog["secondary_locations"] = q
        analyses["secondary_locations"] = query(conn, q)

        q = """
            SELECT
                title,
                team,
                display_location,
                COALESCE(workplace_type,'NULL') AS workplace_type,
                CASE
                    WHEN LOWER(COALESCE(description_plain,'')) LIKE
                         '%relocation assistance%'
                    THEN 'YES' ELSE 'NO'
                END AS relocation_assistance_phrase,
                CASE
                    WHEN LOWER(COALESCE(description_plain,'')) LIKE '%remote%'
                    THEN 'YES' ELSE 'NO'
                END AS mentions_remote,
                CASE
                    WHEN LOWER(COALESCE(description_plain,'')) LIKE '%api%'
                    THEN 'YES' ELSE 'NO'
                END AS api,
                CASE
                    WHEN LOWER(COALESCE(description_plain,'')) LIKE
                         '%troubleshoot%'
                    THEN 'YES' ELSE 'NO'
                END AS troubleshooting,
                CASE
                    WHEN LOWER(COALESCE(description_plain,'')) LIKE '%automat%'
                    THEN 'YES' ELSE 'NO'
                END AS automation,
                CASE
                    WHEN LOWER(COALESCE(description_plain,'')) LIKE '%python%'
                      OR LOWER(COALESCE(description_plain,'')) LIKE
                         '%javascript%'
                      OR LOWER(COALESCE(description_plain,'')) LIKE '%script%'
                    THEN 'YES' ELSE 'NO'
                END AS scripting
            FROM roles
            WHERE present_in_api=1
              AND team IN (
                    'Support Delivery',
                    'Support Operations',
                    'Support Automation',
                    'IT',
                    'Security',
                    'Trust & Safety',
                    'Intelligence & Investigations',
                    'Technical Success',
                    'User Operations',
                    'Technical Program Management'
                  )
            ORDER BY team, title
        """
        sql_catalog["relevant_family_feature_map"] = q
        analyses["relevant_family_feature_map"] = query(conn, q)

        evidence_sql, evidence_params = make_evidence_query()
        sql_catalog["resume_keyword_overlap"] = evidence_sql
        overlap_rows = query(conn, evidence_sql, evidence_params)
        analyses["resume_keyword_overlap"] = overlap_rows

        sales_sql, sales_params = make_sales_query()
        sql_catalog["sales_signal_roles"] = sales_sql
        analyses["sales_signal_roles"] = query(
            conn,
            sales_sql,
            sales_params,
        )

        q = """
            SELECT
                r.ashby_id,
                r.title,
                r.team,
                r.display_location,
                r.workplace_type,
                c.compensation_type,
                c.interval,
                c.currency_code,
                c.min_value,
                c.max_value
            FROM roles r
            JOIN api_compensation_components c
              ON c.ashby_id=r.ashby_id
            WHERE r.present_in_api=1
              AND r.team IN (
                    'Support Delivery',
                    'Support Operations',
                    'Support Automation',
                    'IT',
                    'Security',
                    'Trust & Safety',
                    'Intelligence & Investigations',
                    'Technical Success',
                    'User Operations',
                    'Technical Program Management'
                  )
            ORDER BY r.team, r.title, c.component_index
        """
        sql_catalog["relevant_family_compensation"] = q
        analyses["relevant_family_compensation"] = query(conn, q)

        q = """
            SELECT
                COUNT(*) AS current_roles,
                SUM(CASE WHEN description_plain IS NULL
                              OR TRIM(description_plain)=''
                         THEN 1 ELSE 0 END) AS missing_description,
                SUM(CASE WHEN workplace_type IS NULL
                         THEN 1 ELSE 0 END) AS missing_workplace_type,
                SUM(CASE WHEN is_remote IS NULL
                         THEN 1 ELSE 0 END) AS missing_is_remote,
                SUM(CASE WHEN display_location IS NULL
                              OR TRIM(display_location)=''
                         THEN 1 ELSE 0 END) AS missing_primary_location,
                SUM(CASE WHEN published_at IS NULL
                         THEN 1 ELSE 0 END) AS missing_published_at
            FROM roles
            WHERE present_in_api=1
        """
        sql_catalog["data_quality_summary"] = q
        analyses["data_quality_summary"] = query(conn, q)

        # Pull descriptions once for Python-level contextual analyses.
        description_rows = query(
            conn,
            """
            SELECT
                ashby_id,
                title,
                team,
                display_location,
                workplace_type,
                is_remote,
                description_plain
            FROM roles
            WHERE present_in_api=1
            ORDER BY team, title
            """,
        )

    finally:
        conn.close()

    # Context analysis from actual descriptions.
    remote_contexts = []
    relocation_contexts = []
    year_mentions = []
    education_rows = []

    for row in description_rows:
        text = row.get("description_plain")

        remote_snip = context_snippet(text, "remote")
        if remote_snip:
            remote_contexts.append(
                {
                    "ashby_id": row["ashby_id"],
                    "title": row["title"],
                    "team": row["team"],
                    "display_location": row["display_location"],
                    "workplace_type": row["workplace_type"],
                    "remote_context": remote_snip,
                }
            )

        relocation_snip = context_snippet(text, "relocation")
        if relocation_snip:
            relocation_contexts.append(
                {
                    "ashby_id": row["ashby_id"],
                    "title": row["title"],
                    "team": row["team"],
                    "display_location": row["display_location"],
                    "workplace_type": row["workplace_type"],
                    "relocation_context": relocation_snip,
                }
            )

        mentions = detect_year_mentions(text)
        if mentions:
            year_mentions.append(
                {
                    "ashby_id": row["ashby_id"],
                    "title": row["title"],
                    "team": row["team"],
                    "display_location": row["display_location"],
                    "detected_mentions": mentions,
                    "max_years_mentioned": max(
                        (
                            m["max_years_mentioned"]
                            for m in mentions
                            if m["max_years_mentioned"] is not None
                        ),
                        default=None,
                    ),
                }
            )

        edu = education_signals(text)
        if edu:
            education_rows.append(
                {
                    "ashby_id": row["ashby_id"],
                    "title": row["title"],
                    "team": row["team"],
                    "display_location": row["display_location"],
                    "education_signals": edu,
                }
            )

    analyses["remote_description_contexts"] = remote_contexts
    analyses["relocation_description_contexts"] = relocation_contexts
    analyses["experience_year_mentions"] = year_mentions
    analyses["education_signals"] = education_rows

    # Useful derived summaries.
    work_matrix = {
        (
            r["is_remote"],
            r["workplace_type"],
        ): r["roles"]
        for r in analyses["work_arrangement_distribution"]
    }

    us_remote_rows = analyses["us_remote_anywhere"]
    us_remote_source_counts = Counter(
        r["us_remote_source"] for r in us_remote_rows
    )

    overlap_distribution = Counter(
        r["resume_keyword_overlap"]
        for r in analyses["resume_keyword_overlap"]
    )

    sales_signal_team_counts = Counter(
        r["team"] for r in analyses["sales_signal_roles"]
    )

    derived = {
        "work_arrangement_matrix": {
            f"{k[0]} | {k[1]}": v
            for k, v in work_matrix.items()
        },
        "us_remote_anywhere_count": len(us_remote_rows),
        "us_remote_source_counts": dict(us_remote_source_counts),
        "remote_context_role_count": len(remote_contexts),
        "relocation_context_role_count": len(relocation_contexts),
        "experience_year_signal_role_count": len(year_mentions),
        "education_signal_role_count": len(education_rows),
        "resume_overlap_distribution": dict(
            sorted(overlap_distribution.items(), reverse=True)
        ),
        "sales_signal_role_count": len(
            analyses["sales_signal_roles"]
        ),
        "sales_signal_team_counts": dict(
            sales_signal_team_counts.most_common()
        ),
    }

    # Machine-readable full report.
    payload = {
        "battery": VERSION,
        "generated_at_utc": utc_now(),
        "database": str(db_abs),
        "mode": "read-only",
        "interpretive_guardrails": [
            "present_in_api=1 is treated as the current role population.",
            "is_remote=1 is NOT treated as equivalent to workplace_type=Remote.",
            "Primary and secondary locations are analyzed separately.",
            "US - Remote as a secondary location is evidence of possible geographic flexibility, not proof that Utah is permitted.",
            "Description keyword overlap is a discovery aid, not a qualification or fit score.",
            "Sales signals identify roles needing exclusion/review; absence of a signal does not prove a role is non-sales.",
            "Experience-year detection captures mentions, not necessarily hard requirements.",
            "Education detection captures mentions, not necessarily hard requirements.",
            "Compensation values must be interpreted together with their interval and currency.",
            "No role is selected or rejected solely by this battery.",
        ],
        "relevant_teams": list(RELEVANT_TEAMS),
        "evidence_signal_definitions": EVIDENCE_SIGNALS,
        "sales_signal_definitions": SALES_PATTERNS,
        "derived_summary": derived,
        "sql_catalog": sql_catalog,
        "analyses": analyses,
    }

    args.json_output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Human-readable report.
    md: list[str] = []
    md.append("# ProofLoop Role Selection Transparency Report\n")
    md.append(f"Generated: `{payload['generated_at_utc']}`  \n")
    md.append(f"Database: `{db_abs}`  \n")
    md.append(f"Battery: `{VERSION}`  \n")
    md.append("Database access mode: **read-only**\n")

    md.append("## Purpose\n")
    md.append(
        "This report consolidates the SQL exploration and description-level "
        "analysis used to understand the current OpenAI role population before "
        "choosing Application #001. It is deliberately transparent: the "
        "structured fields, secondary locations, keyword signals, compensation "
        "intervals, and data-quality limitations are all shown separately.\n"
    )

    md.append("## Interpretive guardrails\n")
    for item in payload["interpretive_guardrails"]:
        md.append(f"- {item}\n")

    md.append("\n## Executive data summary\n")
    pop = analyses["population_summary"][0]
    dq = analyses["data_quality_summary"][0]
    md.append(
        f"- Canonical roles in database: **{pop['current_roles']}**\n"
        f"- Current API-present roles: **{pop['api_current']}**\n"
        f"- HTML-present roles: **{pop['html_present']}**\n"
        f"- Roles with `US - Remote` in primary or secondary locations: "
        f"**{derived['us_remote_anywhere_count']}**\n"
        f"- Roles whose descriptions mention remote: "
        f"**{derived['remote_context_role_count']}**\n"
        f"- Roles whose descriptions mention relocation: "
        f"**{derived['relocation_context_role_count']}**\n"
        f"- Roles with detected experience-year language: "
        f"**{derived['experience_year_signal_role_count']}**\n"
        f"- Roles with detected degree/education language: "
        f"**{derived['education_signal_role_count']}**\n"
        f"- Roles with one or more sales-risk signals: "
        f"**{derived['sales_signal_role_count']}**\n"
        f"- Missing descriptions: **{dq['missing_description']}**\n"
        f"- Missing workplace_type: **{dq['missing_workplace_type']}**\n"
        f"- Missing is_remote: **{dq['missing_is_remote']}**\n"
    )

    md.append("\n## 1. Source status\n")
    md.append(markdown_table(analyses["source_status_counts"]))

    md.append("\n## 2. Work-arrangement field behavior\n")
    md.append(
        "This section is intentionally separate from geographic eligibility. "
        "`is_remote`, `workplace_type`, and location strings are independent "
        "pieces of evidence.\n\n"
    )
    md.append(markdown_table(analyses["work_arrangement_distribution"]))

    md.append("\n## 3. Primary location distribution\n")
    md.append(details_table(
        "All primary locations",
        analyses["primary_location_distribution"],
    ))

    md.append("\n## 4. Team distribution\n")
    md.append(details_table(
        "All current teams",
        analyses["team_distribution"],
    ))

    md.append("\n## 5. Broad structured remote pool\n")
    md.append(
        "This deliberately includes the noisy condition `is_remote=1`; it is "
        "kept here so the mismatch with `workplace_type` remains visible.\n\n"
    )
    md.append(details_table(
        "Roles matching is_remote=1 OR workplace_type=Remote",
        analyses["broad_structured_remote_pool"],
    ))

    md.append("\n## 6. Roles explicitly marked workplace_type=Remote\n")
    md.append(markdown_table(analyses["true_remote_roles"]))

    md.append("\n## 7. Structured remote/location conflicts\n")
    md.append(
        "Examples include `US - Remote` paired with `Hybrid`, or a city "
        "primary location paired with `Remote`.\n\n"
    )
    md.append(markdown_table(analyses["remote_location_conflicts"]))

    md.append("\n## 8. US - Remote anywhere in primary or secondary locations\n")
    md.append(
        f"Total unique current roles: **{len(us_remote_rows)}**. "
        f"Source breakdown: `{dict(us_remote_source_counts)}`.\n\n"
    )
    md.append(details_table(
        "US-Remote primary/secondary role inventory",
        us_remote_rows,
    ))

    md.append("\n## 9. Full secondary-location inventory\n")
    md.append(details_table(
        "All secondary-location rows",
        analyses["secondary_locations"],
    ))

    md.append("\n## 10. Relevant-family technical feature map\n")
    md.append(
        "The YES/NO fields below are literal description keyword signals. "
        "They are useful for exploration, not qualification decisions.\n\n"
    )
    md.append(details_table(
        "Relevant technical/support families",
        analyses["relevant_family_feature_map"],
    ))

    md.append("\n## 11. Resume-evidence keyword overlap\n")
    md.append(
        "The overlap count is **not a fit score**. It counts whether a role "
        "description contains vocabulary connected to documented experience "
        "areas such as support, troubleshooting, APIs, automation, scripting, "
        "SQL/data, ticketing/ITSM, network/DNS, UAT/testing, documentation, "
        "and CRM/SaaS.\n\n"
    )
    top_n = analyses["resume_keyword_overlap"][: args.top_overlap]
    md.append(
        f"### Top {len(top_n)} by keyword overlap\n\n"
        + markdown_table(top_n)
    )
    md.append(details_table(
        "Full resume-keyword-overlap inventory",
        analyses["resume_keyword_overlap"],
    ))

    md.append("\n## 12. Sales-risk signal inventory\n")
    md.append(
        "This is intentionally broader than `team='Sales'` so that sales or "
        "revenue responsibilities outside the Sales team remain visible. "
        "Absence from this table does not automatically prove a role is "
        "non-sales.\n\n"
    )
    md.append(details_table(
        "Roles with one or more sales-risk signals",
        analyses["sales_signal_roles"],
    ))

    md.append("\n## 13. Description context around 'remote'\n")
    md.append(details_table(
        "Remote wording contexts",
        remote_contexts,
        max_cell=420,
    ))

    md.append("\n## 14. Description context around 'relocation'\n")
    md.append(details_table(
        "Relocation wording contexts",
        relocation_contexts,
        max_cell=420,
    ))

    md.append("\n## 15. Experience-year language\n")
    md.append(
        "The parser recognizes more patterns than the original SQL CASE "
        "statement, including `5+ years`, `at least 5 years`, ranges, and "
        "spelled-out forms such as `five years of`. These are still mentions, "
        "not automatically hard requirements.\n\n"
    )
    years_for_md = []
    for row in year_mentions:
        mentions = row["detected_mentions"]
        years_for_md.append(
            {
                "title": row["title"],
                "team": row["team"],
                "display_location": row["display_location"],
                "max_years_mentioned": row["max_years_mentioned"],
                "mentions": "; ".join(
                    f"{m['raw']} — {m['context']}"
                    for m in mentions
                ),
            }
        )
    md.append(details_table(
        "Detected experience-year mentions",
        years_for_md,
        max_cell=460,
    ))

    md.append("\n## 16. Education/degree language\n")
    md.append(details_table(
        "Detected education signals",
        education_rows,
    ))

    md.append("\n## 17. Compensation with interval preserved\n")
    md.append(
        "Do not compare raw compensation values without the `interval` "
        "column; hourly and annual values can otherwise look nonsensical "
        "next to each other.\n\n"
    )
    md.append(details_table(
        "Relevant-family compensation components",
        analyses["relevant_family_compensation"],
    ))

    md.append("\n## 18. Data-quality summary\n")
    md.append(markdown_table(analyses["data_quality_summary"]))

    md.append("\n## 19. SQL catalog\n")
    md.append(
        "These are the exact SQL statements executed by this battery. "
        "They are included so every table in the report can be reproduced "
        "manually against the same database.\n\n"
    )
    for name, sql in sql_catalog.items():
        md.append(f"### {name}\n\n```sql\n{sql.strip()}\n```\n\n")

    md.append("## 20. Interpretation notes established so far\n")
    md.append(
        "- `is_remote=1` cannot be treated as equivalent to a fully remote job; "
        "many records pair it with `Hybrid`.\n"
        "- Primary location alone is incomplete because the API contains "
        "secondary locations, including `US - Remote` on some roles whose "
        "primary location is a city.\n"
        "- `US - Remote` plus `Hybrid` is ambiguous and requires description "
        "review rather than automatic Utah eligibility.\n"
        "- Relocation assistance and permission to start remotely are separate "
        "questions.\n"
        "- Sales exclusion cannot be performed by Sales-team membership alone; "
        "sales-adjacent responsibilities can occur in other teams.\n"
        "- Technical relevance cannot be inferred from team/title alone; the "
        "actual work in the description matters.\n"
        "- Keyword overlap with the resume is evidence-discovery only. It does "
        "not establish competence, seniority, or qualification.\n"
        "- Experience and education language must eventually be separated into "
        "required vs preferred vs equivalent-experience statements before being "
        "used as hard gates.\n"
        "- Compensation is useful as a seniority clue only when currency and "
        "interval are preserved.\n"
    )

    args.markdown.write_text(
        "".join(md),
        encoding="utf-8",
    )

    print(VERSION)
    print(f"Database:             {db_abs}")
    print("Database mode:        READ ONLY")
    print(f"Current API roles:    {pop['api_current']}")
    print(f"US-Remote anywhere:   {len(us_remote_rows)}")
    print(f"Remote text matches:  {len(remote_contexts)}")
    print(f"Relocation matches:   {len(relocation_contexts)}")
    print(f"Sales-signal roles:   {len(analyses['sales_signal_roles'])}")
    print(f"Markdown report:      {args.markdown}")
    print(f"JSON report:          {args.json_output}")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
