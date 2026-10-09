#!/usr/bin/env python3
"""
ProofLoop Enriched SQLite Builder v0.11

Builds a NEW enriched SQLite database from the two preserved source branches:

Source A:
    openai_roles.jsonl
    817 HTML-derived historical roles

Source B:
    openai_ashby_roles.jsonl
    815 normalized API snapshot roles

Reconciliation:
    openai_ashby_reconciliation_report_v0_9_1.json

Important:
- Does NOT modify proofloop.db.
- Does NOT modify either JSONL source.
- Refuses to overwrite the enriched database unless --overwrite is supplied.
- Uses Ashby UUID as the stable cross-source identity.
- Preserves exact source rows in dedicated source tables.
- Creates a canonical union of all unique postings.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def normalize_text(value):
    if value is None:
        return None
    return re.sub(r"\s+", " ", str(value)).strip()


def ashby_id_from_url(url: str | None) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2 and parts[0].lower() == "openai":
        return parts[1]
    return ""


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, 1):
            line = raw.strip()
            if not line:
                raise ValueError(f"Blank JSONL line at line {line_number}")
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: "
                    f"{exc.msg} column {exc.colno}"
                ) from exc
            if not isinstance(obj, dict):
                raise ValueError(
                    f"JSONL line {line_number} is not a JSON object"
                )
            rows.append(obj)
    return rows


def bool_to_int(value):
    if value is None:
        return None
    return 1 if bool(value) else 0


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE build_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE roles (
            ashby_id TEXT PRIMARY KEY,
            html_role_id INTEGER UNIQUE,
            title TEXT NOT NULL,
            team TEXT NOT NULL,
            department TEXT,
            employment_type TEXT,
            display_location TEXT,
            published_at TEXT,
            is_listed INTEGER CHECK (is_listed IN (0, 1) OR is_listed IS NULL),
            is_remote INTEGER CHECK (is_remote IN (0, 1) OR is_remote IS NULL),
            workplace_type TEXT,
            career_url TEXT,
            job_url TEXT,
            apply_url TEXT NOT NULL UNIQUE,
            description_plain TEXT,
            description_html TEXT,
            present_in_html INTEGER NOT NULL CHECK (present_in_html IN (0, 1)),
            present_in_api INTEGER NOT NULL CHECK (present_in_api IN (0, 1)),
            source_status TEXT NOT NULL CHECK (
                source_status IN ('matched', 'html_only', 'api_only')
            )
        );

        CREATE TABLE html_roles (
            html_role_id INTEGER PRIMARY KEY,
            ashby_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            team TEXT NOT NULL,
            display_location TEXT NOT NULL,
            career_url TEXT NOT NULL UNIQUE,
            apply_url TEXT NOT NULL UNIQUE,
            FOREIGN KEY (ashby_id) REFERENCES roles(ashby_id)
        );

        CREATE TABLE api_roles (
            ashby_id TEXT PRIMARY KEY,
            source_index INTEGER NOT NULL UNIQUE,
            source_snapshot TEXT NOT NULL,
            title_raw TEXT,
            title_normalized TEXT,
            department TEXT,
            team_raw TEXT,
            team_normalized TEXT,
            employment_type TEXT,
            primary_location TEXT,
            published_at TEXT,
            is_listed INTEGER CHECK (is_listed IN (0, 1) OR is_listed IS NULL),
            is_remote INTEGER CHECK (is_remote IN (0, 1) OR is_remote IS NULL),
            workplace_type TEXT,
            address_json TEXT,
            job_url TEXT NOT NULL UNIQUE,
            apply_url TEXT NOT NULL UNIQUE,
            description_plain TEXT,
            description_html TEXT,
            compensation_json TEXT,
            FOREIGN KEY (ashby_id) REFERENCES roles(ashby_id)
        );

        CREATE TABLE api_secondary_locations (
            ashby_id TEXT NOT NULL,
            location_index INTEGER NOT NULL,
            location TEXT,
            address_json TEXT,
            PRIMARY KEY (ashby_id, location_index),
            FOREIGN KEY (ashby_id) REFERENCES api_roles(ashby_id)
        );

        CREATE TABLE api_compensation_components (
            ashby_id TEXT NOT NULL,
            component_index INTEGER NOT NULL,
            compensation_type TEXT,
            interval TEXT,
            currency_code TEXT,
            min_value REAL,
            max_value REAL,
            PRIMARY KEY (ashby_id, component_index),
            FOREIGN KEY (ashby_id) REFERENCES api_roles(ashby_id)
        );

        CREATE INDEX idx_roles_title ON roles(title);
        CREATE INDEX idx_roles_team ON roles(team);
        CREATE INDEX idx_roles_department ON roles(department);
        CREATE INDEX idx_roles_location ON roles(display_location);
        CREATE INDEX idx_roles_source_status ON roles(source_status);
        CREATE INDEX idx_api_published_at ON api_roles(published_at);
        CREATE INDEX idx_comp_type ON api_compensation_components(compensation_type);
        """
    )


def build_database(
    html_rows: list[dict],
    api_rows: list[dict],
    reconciliation: dict,
    db_path: Path,
    html_source_name: str,
    api_source_name: str,
    reconciliation_name: str,
) -> dict:
    html_by_id = {}
    api_by_id = {}

    for row in html_rows:
        aid = ashby_id_from_url(row.get("apply_url"))
        if not aid:
            raise ValueError(
                f"HTML role_id={row.get('role_id')} has no Ashby UUID"
            )
        if aid in html_by_id:
            raise ValueError(f"Duplicate HTML Ashby UUID: {aid}")
        html_by_id[aid] = row

    for row in api_rows:
        aid = row.get("ashby_id") or ashby_id_from_url(row.get("apply_url"))
        if not aid:
            raise ValueError(
                f"API source_index={row.get('source_index')} has no Ashby UUID"
            )
        if aid in api_by_id:
            raise ValueError(f"Duplicate API Ashby UUID: {aid}")
        api_by_id[aid] = row

    all_ids = sorted(set(html_by_id) | set(api_by_id))

    conn = sqlite3.connect(db_path)
    try:
        create_schema(conn)

        metadata = {
            "builder": "ProofLoop Enriched SQLite Builder v0.11",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "html_source": html_source_name,
            "api_source": api_source_name,
            "reconciliation_source": reconciliation_name,
            "html_role_count": str(len(html_rows)),
            "api_role_count": str(len(api_rows)),
            "canonical_union_count": str(len(all_ids)),
        }
        conn.executemany(
            "INSERT INTO build_metadata(key, value) VALUES (?, ?)",
            metadata.items(),
        )

        canonical_rows = []

        for aid in all_ids:
            h = html_by_id.get(aid)
            a = api_by_id.get(aid)

            if h and a:
                source_status = "matched"
            elif h:
                source_status = "html_only"
            else:
                source_status = "api_only"

            # API is the richer current source when available, but normalize
            # presentation-only whitespace. HTML remains separately preserved.
            title = (
                normalize_text(a.get("title"))
                if a
                else normalize_text(h.get("title"))
            )
            team = (
                normalize_text(a.get("team"))
                if a
                else normalize_text(h.get("team"))
            )

            apply_url = (
                a.get("apply_url")
                if a and a.get("apply_url")
                else h.get("apply_url")
            )

            canonical_rows.append(
                (
                    aid,
                    h.get("role_id") if h else None,
                    title,
                    team,
                    a.get("department") if a else None,
                    a.get("employment_type") if a else None,
                    (
                        a.get("primary_location")
                        if a and a.get("primary_location")
                        else h.get("display_location") if h else None
                    ),
                    a.get("published_at") if a else None,
                    bool_to_int(a.get("is_listed")) if a else None,
                    bool_to_int(a.get("is_remote")) if a else None,
                    a.get("workplace_type") if a else None,
                    h.get("career_url") if h else None,
                    a.get("job_url") if a else None,
                    apply_url,
                    a.get("description_plain") if a else None,
                    a.get("description_html") if a else None,
                    1 if h else 0,
                    1 if a else 0,
                    source_status,
                )
            )

        conn.executemany(
            """
            INSERT INTO roles (
                ashby_id,
                html_role_id,
                title,
                team,
                department,
                employment_type,
                display_location,
                published_at,
                is_listed,
                is_remote,
                workplace_type,
                career_url,
                job_url,
                apply_url,
                description_plain,
                description_html,
                present_in_html,
                present_in_api,
                source_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            canonical_rows,
        )

        conn.executemany(
            """
            INSERT INTO html_roles (
                html_role_id,
                ashby_id,
                title,
                team,
                display_location,
                career_url,
                apply_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["role_id"],
                    ashby_id_from_url(row["apply_url"]),
                    row["title"],
                    row["team"],
                    row["display_location"],
                    row["career_url"],
                    row["apply_url"],
                )
                for row in html_rows
            ],
        )

        api_insert_rows = []
        secondary_rows = []
        compensation_rows = []

        for row in api_rows:
            aid = row["ashby_id"]

            api_insert_rows.append(
                (
                    aid,
                    row["source_index"],
                    row["source_snapshot"],
                    row.get("title"),
                    normalize_text(row.get("title")),
                    row.get("department"),
                    row.get("team"),
                    normalize_text(row.get("team")),
                    row.get("employment_type"),
                    row.get("primary_location"),
                    row.get("published_at"),
                    bool_to_int(row.get("is_listed")),
                    bool_to_int(row.get("is_remote")),
                    row.get("workplace_type"),
                    json.dumps(
                        row.get("address"),
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    row.get("job_url"),
                    row.get("apply_url"),
                    row.get("description_plain"),
                    row.get("description_html"),
                    json.dumps(
                        row.get("compensation"),
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                )
            )

            for index, location in enumerate(
                row.get("secondary_locations") or [], start=1
            ):
                secondary_rows.append(
                    (
                        aid,
                        index,
                        location.get("location"),
                        json.dumps(
                            location.get("address"),
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ),
                    )
                )

            compensation = row.get("compensation") or {}
            summary_components = compensation.get("summaryComponents") or []

            for index, component in enumerate(summary_components, start=1):
                compensation_rows.append(
                    (
                        aid,
                        index,
                        component.get("compensationType"),
                        component.get("interval"),
                        component.get("currencyCode"),
                        component.get("minValue"),
                        component.get("maxValue"),
                    )
                )

        conn.executemany(
            """
            INSERT INTO api_roles (
                ashby_id,
                source_index,
                source_snapshot,
                title_raw,
                title_normalized,
                department,
                team_raw,
                team_normalized,
                employment_type,
                primary_location,
                published_at,
                is_listed,
                is_remote,
                workplace_type,
                address_json,
                job_url,
                apply_url,
                description_plain,
                description_html,
                compensation_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            api_insert_rows,
        )

        conn.executemany(
            """
            INSERT INTO api_secondary_locations (
                ashby_id,
                location_index,
                location,
                address_json
            )
            VALUES (?, ?, ?, ?)
            """,
            secondary_rows,
        )

        conn.executemany(
            """
            INSERT INTO api_compensation_components (
                ashby_id,
                component_index,
                compensation_type,
                interval,
                currency_code,
                min_value,
                max_value
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            compensation_rows,
        )

        conn.commit()

        counts = {}
        for table in (
            "roles",
            "html_roles",
            "api_roles",
            "api_secondary_locations",
            "api_compensation_components",
        ):
            counts[table] = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

        status_counts = dict(
            conn.execute(
                """
                SELECT source_status, COUNT(*)
                FROM roles
                GROUP BY source_status
                ORDER BY source_status
                """
            ).fetchall()
        )

        return {
            "table_counts": counts,
            "status_counts": status_counts,
            "reconciliation_summary": reconciliation.get("summary", {}),
        }

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build ProofLoop's enriched cross-source SQLite database."
    )
    parser.add_argument(
        "--html-jsonl",
        type=Path,
        default=Path("openai_roles.jsonl"),
    )
    parser.add_argument(
        "--api-jsonl",
        type=Path,
        default=Path("openai_ashby_roles.jsonl"),
    )
    parser.add_argument(
        "--reconciliation-report",
        type=Path,
        default=Path("openai_ashby_reconciliation_report_v0_9_1.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("proofloop_enriched.db"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("proofloop_enriched_db_build_report.json"),
    )
    parser.add_argument(
        "--expected-html",
        type=int,
        default=817,
    )
    parser.add_argument(
        "--expected-api",
        type=int,
        default=815,
    )
    parser.add_argument(
        "--expected-union",
        type=int,
        default=818,
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
    )
    args = parser.parse_args()

    for path in (
        args.html_jsonl,
        args.api_jsonl,
        args.reconciliation_report,
    ):
        if not path.is_file():
            print(f"ERROR: Required input not found: {path}", file=sys.stderr)
            return 2

    if args.output.exists():
        if not args.overwrite:
            print(
                f"ERROR: Output database already exists: {args.output}\n"
                "The original proofloop.db is never modified. "
                "Use --overwrite only to intentionally rebuild "
                "proofloop_enriched.db.",
                file=sys.stderr,
            )
            return 1
        args.output.unlink()

    try:
        html_rows = load_jsonl(args.html_jsonl)
        api_rows = load_jsonl(args.api_jsonl)
        reconciliation = load_json(args.reconciliation_report)

        union_count = len(
            {
                ashby_id_from_url(r.get("apply_url"))
                for r in html_rows
            }
            |
            {
                r.get("ashby_id")
                for r in api_rows
            }
        )

        expected_ok = (
            len(html_rows) == args.expected_html
            and len(api_rows) == args.expected_api
            and union_count == args.expected_union
        )

        if not expected_ok:
            print("ERROR: Expected-count validation failed before build.")
            print(
                f"HTML={len(html_rows)} expected={args.expected_html}; "
                f"API={len(api_rows)} expected={args.expected_api}; "
                f"Union={union_count} expected={args.expected_union}"
            )
            return 1

        build_result = build_database(
            html_rows,
            api_rows,
            reconciliation,
            args.output,
            args.html_jsonl.name,
            args.api_jsonl.name,
            args.reconciliation_report.name,
        )

        report = {
            "builder": "ProofLoop Enriched SQLite Builder v0.11",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "inputs": {
                "html_jsonl": str(args.html_jsonl),
                "api_jsonl": str(args.api_jsonl),
                "reconciliation_report": str(args.reconciliation_report),
            },
            "output_database": str(args.output),
            "expected": {
                "html_roles": args.expected_html,
                "api_roles": args.expected_api,
                "canonical_union": args.expected_union,
            },
            "observed": {
                "html_roles": len(html_rows),
                "api_roles": len(api_rows),
                "canonical_union": union_count,
            },
            **build_result,
            "result": "PASS",
        }

        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    except Exception as exc:
        if args.output.exists():
            try:
                args.output.unlink()
            except OSError:
                pass
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("ProofLoop Enriched SQLite Builder v0.11")
    print(f"HTML roles:          {len(html_rows)}")
    print(f"API roles:           {len(api_rows)}")
    print(f"Canonical union:     {union_count}")
    print(f"Output database:     {args.output}")
    print(f"Build report:        {args.report}")
    print("\nTable counts:")
    for table, count in build_result["table_counts"].items():
        print(f"- {table}: {count}")
    print("\nSource status:")
    for status, count in build_result["status_counts"].items():
        print(f"- {status}: {count}")
    print("\nOriginal proofloop.db: UNCHANGED")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
