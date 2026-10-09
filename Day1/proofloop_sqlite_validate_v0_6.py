#!/usr/bin/env python3
"""
ProofLoop SQLite Validator v0.6

Automatically validates the SQLite database created from the OpenAI role inventory.

Checks:
- database file exists and opens
- SQLite integrity_check passes
- roles table exists
- expected columns, types, NOT NULL flags, and primary key are present
- UNIQUE indexes exist for career_url and apply_url
- expected row count matches
- role_id values are unique and sequential
- required text fields are neither NULL nor blank
- career_url and apply_url values are unique
- URL shapes look correct
- optional JSONL source matches the database row-for-row
- database constraints actually reject bad inserts, using an in-memory copy

Writes a JSON validation report for documentation/evidence.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


EXPECTED_SCHEMA = [
    ("role_id", "INTEGER", 0, 1),          # SQLite reports NOT NULL=0 for INTEGER PRIMARY KEY
    ("title", "TEXT", 1, 0),
    ("team", "TEXT", 1, 0),
    ("display_location", "TEXT", 1, 0),
    ("career_url", "TEXT", 1, 0),
    ("apply_url", "TEXT", 1, 0),
]

REQUIRED_TEXT_FIELDS = (
    "title",
    "team",
    "display_location",
    "career_url",
    "apply_url",
)


def add_check(checks, name: str, passed: bool, detail: str) -> None:
    checks.append({
        "name": name,
        "passed": bool(passed),
        "detail": detail,
    })


def load_jsonl(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                raise ValueError(f"Blank line at JSONL line {line_number}")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: "
                    f"{exc.msg} at column {exc.colno}"
                ) from exc
            if not isinstance(record, dict):
                raise ValueError(f"JSONL line {line_number} is not an object")
            records.append(record)
    return records


def get_unique_index_columns(conn: sqlite3.Connection, table: str):
    """Return a mapping of unique index name -> indexed column names."""
    mapping = {}
    for row in conn.execute(f"PRAGMA index_list({table})"):
        # seq, name, unique, origin, partial
        _, index_name, is_unique, origin, _ = row
        if is_unique:
            cols = [
                info_row[2]
                for info_row in conn.execute(
                    f"PRAGMA index_info('{index_name}')"
                )
            ]
            mapping[index_name] = {
                "columns": cols,
                "origin": origin,
            }
    return mapping


def constraint_rejection_checks(source_conn: sqlite3.Connection):
    """
    Copy the real database into memory and deliberately try invalid INSERTs.
    The real database is never modified.
    """
    checks = []

    mem = sqlite3.connect(":memory:")
    try:
        source_conn.backup(mem)

        base = mem.execute(
            """
            SELECT title, team, display_location, career_url, apply_url
            FROM roles
            WHERE role_id = 1
            """
        ).fetchone()

        if base is None:
            add_check(
                checks,
                "constraint_test_setup",
                False,
                "Could not find role_id=1 for constraint tests.",
            )
            return checks

        title, team, location, career_url, apply_url = base

        tests = [
            (
                "reject_duplicate_primary_key",
                """
                INSERT INTO roles
                (role_id, title, team, display_location, career_url, apply_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (1, title, team, location,
                 "https://example.invalid/unique-career-pk",
                 "https://example.invalid/unique-apply-pk"),
            ),
            (
                "reject_duplicate_career_url",
                """
                INSERT INTO roles
                (role_id, title, team, display_location, career_url, apply_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (999001, title, team, location,
                 career_url,
                 "https://example.invalid/unique-apply-career"),
            ),
            (
                "reject_duplicate_apply_url",
                """
                INSERT INTO roles
                (role_id, title, team, display_location, career_url, apply_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (999002, title, team, location,
                 "https://example.invalid/unique-career-apply",
                 apply_url),
            ),
            (
                "reject_null_required_field",
                """
                INSERT INTO roles
                (role_id, title, team, display_location, career_url, apply_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (999003, None, team, location,
                 "https://example.invalid/unique-career-null",
                 "https://example.invalid/unique-apply-null"),
            ),
        ]

        for name, sql, params in tests:
            before = mem.execute("SELECT COUNT(*) FROM roles").fetchone()[0]
            rejected = False
            error_text = ""

            try:
                mem.execute(sql, params)
                mem.rollback()
            except sqlite3.IntegrityError as exc:
                rejected = True
                error_text = str(exc)
                mem.rollback()

            after = mem.execute("SELECT COUNT(*) FROM roles").fetchone()[0]

            add_check(
                checks,
                name,
                rejected and before == after,
                (
                    f"Rejected as expected ({error_text}); "
                    f"row count remained {after}."
                    if rejected
                    else f"BAD INSERT WAS ACCEPTED; row count is {after}."
                ),
            )

    finally:
        mem.close()

    return checks


def validate_database(
    db_path: Path,
    expected_count: int | None,
    jsonl_path: Path | None,
):
    checks = []
    metrics = {}

    conn = sqlite3.connect(db_path)

    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        add_check(
            checks,
            "sqlite_integrity_check",
            integrity == "ok",
            f"PRAGMA integrity_check returned {integrity!r}.",
        )

        table_exists = conn.execute(
            """
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type = 'table' AND name = 'roles'
            """
        ).fetchone()[0] == 1

        add_check(
            checks,
            "roles_table_exists",
            table_exists,
            "roles table exists." if table_exists else "roles table is missing.",
        )

        if not table_exists:
            return checks, metrics

        table_info = conn.execute("PRAGMA table_info(roles)").fetchall()
        actual_schema = [
            (row[1], row[2].upper(), row[3], row[5])
            for row in table_info
        ]
        add_check(
            checks,
            "schema_matches",
            actual_schema == EXPECTED_SCHEMA,
            f"Actual schema: {actual_schema}",
        )

        unique_indexes = get_unique_index_columns(conn, "roles")
        unique_column_sets = {
            tuple(info["columns"]) for info in unique_indexes.values()
        }

        add_check(
            checks,
            "career_url_unique_constraint",
            ("career_url",) in unique_column_sets,
            f"Unique indexes: {unique_indexes}",
        )
        add_check(
            checks,
            "apply_url_unique_constraint",
            ("apply_url",) in unique_column_sets,
            f"Unique indexes: {unique_indexes}",
        )

        row_count = conn.execute(
            "SELECT COUNT(*) FROM roles"
        ).fetchone()[0]
        metrics["row_count"] = row_count

        if expected_count is not None:
            add_check(
                checks,
                "expected_row_count",
                row_count == expected_count,
                f"Database has {row_count} rows; expected {expected_count}.",
            )
        else:
            add_check(
                checks,
                "row_count_nonzero",
                row_count > 0,
                f"Database has {row_count} rows.",
            )

        role_ids = [
            row[0]
            for row in conn.execute(
                "SELECT role_id FROM roles ORDER BY role_id"
            )
        ]

        expected_ids = list(range(1, row_count + 1))
        add_check(
            checks,
            "role_ids_sequential",
            role_ids == expected_ids,
            (
                f"role_id values are sequential 1..{row_count}."
                if role_ids == expected_ids
                else "role_id values contain gaps, duplicates, or unexpected values."
            ),
        )

        for field in REQUIRED_TEXT_FIELDS:
            bad_count = conn.execute(
                f"""
                SELECT COUNT(*)
                FROM roles
                WHERE {field} IS NULL OR TRIM({field}) = ''
                """
            ).fetchone()[0]

            add_check(
                checks,
                f"{field}_not_blank",
                bad_count == 0,
                f"{bad_count} NULL/blank value(s) found in {field}.",
            )

        duplicate_career = conn.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT career_url
                FROM roles
                GROUP BY career_url
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]

        duplicate_apply = conn.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT apply_url
                FROM roles
                GROUP BY apply_url
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]

        add_check(
            checks,
            "career_url_values_unique",
            duplicate_career == 0,
            f"{duplicate_career} duplicate career_url group(s).",
        )
        add_check(
            checks,
            "apply_url_values_unique",
            duplicate_apply == 0,
            f"{duplicate_apply} duplicate apply_url group(s).",
        )

        bad_career_shape = conn.execute(
            """
            SELECT COUNT(*)
            FROM roles
            WHERE career_url NOT LIKE 'https://openai.com/careers/%'
            """
        ).fetchone()[0]

        bad_apply_shape = conn.execute(
            """
            SELECT COUNT(*)
            FROM roles
            WHERE apply_url NOT LIKE 'https://jobs.ashbyhq.com/openai/%'
            """
        ).fetchone()[0]

        add_check(
            checks,
            "career_url_shape",
            bad_career_shape == 0,
            f"{bad_career_shape} unexpected career_url value(s).",
        )
        add_check(
            checks,
            "apply_url_shape",
            bad_apply_shape == 0,
            f"{bad_apply_shape} unexpected apply_url value(s).",
        )

        # Cross-check the source JSONL against SQLite if supplied.
        if jsonl_path is not None:
            records = load_jsonl(jsonl_path)
            add_check(
                checks,
                "jsonl_row_count_matches_database",
                len(records) == row_count,
                f"JSONL={len(records)} records; SQLite={row_count} rows.",
            )

            db_rows = conn.execute(
                """
                SELECT
                    role_id,
                    title,
                    team,
                    display_location,
                    career_url,
                    apply_url
                FROM roles
                ORDER BY role_id
                """
            ).fetchall()

            jsonl_rows = [
                (
                    record.get("role_id"),
                    record.get("title"),
                    record.get("team"),
                    record.get("display_location"),
                    record.get("career_url"),
                    record.get("apply_url"),
                )
                for record in records
            ]

            add_check(
                checks,
                "jsonl_matches_database_row_for_row",
                jsonl_rows == db_rows,
                (
                    "Every JSONL record matches its SQLite row."
                    if jsonl_rows == db_rows
                    else "JSONL and SQLite differ."
                ),
            )

        checks.extend(constraint_rejection_checks(conn))

    finally:
        conn.close()

    return checks, metrics


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Automatically validate the ProofLoop SQLite database."
    )
    parser.add_argument(
        "database",
        type=Path,
        help="Path to proofloop.db",
    )
    parser.add_argument(
        "--expected",
        type=int,
        default=None,
        help="Expected number of role rows.",
    )
    parser.add_argument(
        "--jsonl",
        type=Path,
        default=None,
        help="Optional canonical JSONL file to cross-check row-for-row.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("proofloop_db_validation_report.json"),
        help="Path for the machine-readable JSON validation report.",
    )

    args = parser.parse_args()

    if not args.database.is_file():
        print(f"ERROR: Database not found: {args.database}", file=sys.stderr)
        return 2

    if args.jsonl is not None and not args.jsonl.is_file():
        print(f"ERROR: JSONL file not found: {args.jsonl}", file=sys.stderr)
        return 2

    try:
        checks, metrics = validate_database(
            args.database,
            args.expected,
            args.jsonl,
        )
    except Exception as exc:
        print(f"ERROR: Validation could not complete: {exc}", file=sys.stderr)
        return 2

    passed = sum(1 for check in checks if check["passed"])
    failed = len(checks) - passed
    overall_pass = failed == 0

    report = {
        "validator": "ProofLoop SQLite Validator v0.6",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": str(args.database),
        "jsonl_source": str(args.jsonl) if args.jsonl else None,
        "expected_rows": args.expected,
        "metrics": metrics,
        "summary": {
            "checks": len(checks),
            "passed": passed,
            "failed": failed,
            "result": "PASS" if overall_pass else "FAIL",
        },
        "checks": checks,
    }

    args.report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("ProofLoop SQLite Validator v0.6")
    print(f"Database:          {args.database}")
    if args.jsonl:
        print(f"JSONL source:      {args.jsonl}")
    if args.expected is not None:
        print(f"Expected rows:     {args.expected}")
    if "row_count" in metrics:
        print(f"Database rows:     {metrics['row_count']}")
    print(f"Checks run:        {len(checks)}")
    print(f"Checks passed:     {passed}")
    print(f"Checks failed:     {failed}")
    print(f"Validation report: {args.report}")

    print("\nCheck results:")
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] {check['name']}: {check['detail']}")

    print(f"\nRESULT: {'PASS' if overall_pass else 'FAIL'}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
