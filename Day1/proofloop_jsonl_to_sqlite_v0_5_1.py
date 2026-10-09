#!/usr/bin/env python3
"""
ProofLoop JSONL -> SQLite Importer v0.5.1

Reads the canonical OpenAI role inventory from JSONL and stores it in
a SQLite database.

Fix in v0.5.1:
- explicitly closes SQLite connections on every path
- avoids Windows temporary-file locking after database work
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

FIELDS = (
    "role_id",
    "title",
    "team",
    "display_location",
    "career_url",
    "apply_url",
)


def load_jsonl(path: Path):
    """Load and minimally validate the canonical JSONL records."""
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Line {line_number} is invalid JSON: "
                    f"{exc.msg} at column {exc.colno}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"Line {line_number} is not a JSON object."
                )

            missing = [
                field for field in FIELDS
                if field not in record
            ]
            if missing:
                raise ValueError(
                    f"Line {line_number} is missing fields: "
                    + ", ".join(missing)
                )

            records.append(record)

    return records


def create_database(records, db_path: Path):
    """Create the SQLite database, insert records, commit, and close it."""
    conn = sqlite3.connect(db_path)

    try:
        conn.execute(
            """
            CREATE TABLE roles (
                role_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                team TEXT NOT NULL,
                display_location TEXT NOT NULL,
                career_url TEXT NOT NULL UNIQUE,
                apply_url TEXT NOT NULL UNIQUE
            )
            """
        )

        conn.executemany(
            """
            INSERT INTO roles (
                role_id,
                title,
                team,
                display_location,
                career_url,
                apply_url
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    record["role_id"],
                    record["title"],
                    record["team"],
                    record["display_location"],
                    record["career_url"],
                    record["apply_url"],
                )
                for record in records
            ],
        )

        count = conn.execute(
            "SELECT COUNT(*) FROM roles"
        ).fetchone()[0]

        conn.commit()
        return count

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Import ProofLoop OpenAI role JSONL into SQLite."
    )
    parser.add_argument(
        "jsonl_file",
        type=Path,
        help="Path to the canonical JSONL role inventory."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("proofloop.db"),
        help="SQLite database output path."
    )
    parser.add_argument(
        "--expected",
        type=int,
        default=None,
        help="Optional expected record count."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacement of an existing output database."
    )

    args = parser.parse_args()

    if not args.jsonl_file.is_file():
        print(
            f"ERROR: Input file not found: {args.jsonl_file}",
            file=sys.stderr,
        )
        return 2

    if args.output.exists():
        if not args.overwrite:
            print(
                f"ERROR: Database already exists: {args.output}\n"
                "Use --overwrite only if you intentionally want to replace it.",
                file=sys.stderr,
            )
            return 1
        args.output.unlink()

    try:
        records = load_jsonl(args.jsonl_file)
        inserted_count = create_database(records, args.output)
    except Exception as exc:
        if args.output.exists():
            try:
                args.output.unlink()
            except OSError:
                pass
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("ProofLoop JSONL -> SQLite Importer v0.5.1")
    print(f"Input JSONL:      {args.jsonl_file}")
    print(f"SQLite database:  {args.output}")
    print(f"Records loaded:   {len(records)}")
    print(f"Rows in database: {inserted_count}")

    failed = False

    if args.expected is not None:
        status = (
            "PASS"
            if len(records) == args.expected
            and inserted_count == args.expected
            else "FAIL"
        )
        print(f"Expected records: {args.expected}  [{status}]")
        if status == "FAIL":
            failed = True

    if inserted_count != len(records):
        print("RESULT: FAIL - database row count differs from input")
        return 1

    if failed:
        print("RESULT: FAIL")
        return 1

    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
