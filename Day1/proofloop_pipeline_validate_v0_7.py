#!/usr/bin/env python3
"""
ProofLoop Full Pipeline Validator v0.7

Validates the current ProofLoop artifacts end-to-end before formal testing.

It validates:
1. Source ZIP
2. v0.1 HTML parser behavior
3. v0.2 HTML -> JSONL behavior
4. Canonical JSONL structure and expected count
5. v0.3.1 validator success and expected-count failure behavior
6. CSV structure and row-for-row equality with JSONL
7. v0.4.1 converter reproduction and expected-count failure behavior
8. SQLite structure, integrity, constraints, and row-for-row equality
9. v0.5 importer reproduction in a temporary database
10. v0.6 database validator on the reproduced database
11. Existing validation report consistency
12. Python syntax compilation for the pipeline scripts

All regeneration happens in a temporary directory. Existing project artifacts are read-only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import py_compile
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

FIELDS = (
    "role_id",
    "title",
    "team",
    "display_location",
    "career_url",
    "apply_url",
)

SCRIPT_FILES = (
    "proofloop_openai_ingest_v0_1.py",
    "proofloop_openai_ingest_v0_2.py",
    "proofloop_openai_validate_v0_3_1.py",
    "proofloop_jsonl_to_csv_v0_4_1.py",
    "proofloop_jsonl_to_sqlite_v0_5.py",
    "proofloop_sqlite_validate_v0_6.py",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def add(checks, name, passed, detail):
    checks.append({
        "name": name,
        "passed": bool(passed),
        "detail": detail,
    })


def run(cmd):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def load_jsonl(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                raise ValueError(f"Blank JSONL line {line_number}")
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError(f"JSONL line {line_number} is not an object")
            records.append(obj)
    return records


def load_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = tuple(reader.fieldnames or ())

    normalized = []
    for i, row in enumerate(rows, start=1):
        item = dict(row)
        try:
            item["role_id"] = int(item["role_id"])
        except Exception as exc:
            raise ValueError(
                f"CSV row {i} has invalid role_id: {item.get('role_id')!r}"
            ) from exc
        normalized.append(item)

    return fieldnames, normalized


def db_snapshot(path: Path):
    with sqlite3.connect(path) as conn:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        schema = conn.execute("PRAGMA table_info(roles)").fetchall()
        rows = conn.execute(
            """
            SELECT role_id, title, team, display_location, career_url, apply_url
            FROM roles
            ORDER BY role_id
            """
        ).fetchall()
        indexes = conn.execute("PRAGMA index_list(roles)").fetchall()

    records = [
        dict(zip(FIELDS, row))
        for row in rows
    ]

    return {
        "integrity": integrity,
        "schema": schema,
        "records": records,
        "indexes": indexes,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Validate the current ProofLoop pipeline end-to-end."
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project directory containing the pipeline files.",
    )
    ap.add_argument(
        "--expected",
        type=int,
        default=817,
        help="Expected role count.",
    )
    ap.add_argument(
        "--report",
        type=Path,
        default=Path("proofloop_pipeline_validation_report.json"),
        help="Output JSON validation report.",
    )
    args = ap.parse_args()

    root = args.root.resolve()
    expected = args.expected
    checks = []
    metrics = {}
    hashes = {}

    paths = {
        "zip": root / "OpenAI Careers.zip",
        "jsonl": root / "openai_roles.jsonl",
        "csv": root / "openai_roles.csv",
        "db": root / "proofloop.db",
        "db_report": root / "proofloop_db_validation_report.json",
    }

    # Required artifacts.
    for label, path in paths.items():
        add(
            checks,
            f"{label}_exists",
            path.is_file(),
            str(path),
        )

    missing = [str(p) for p in paths.values() if not p.is_file()]
    if missing:
        print("Missing required artifact(s):")
        for item in missing:
            print(f"- {item}")
        return 2

    # Required scripts.
    script_paths = [root / name for name in SCRIPT_FILES]
    for path in script_paths:
        add(
            checks,
            f"script_exists:{path.name}",
            path.is_file(),
            str(path),
        )

    if any(not p.is_file() for p in script_paths):
        print("One or more required scripts are missing.")
        return 2

    # Syntax compilation.
    for path in script_paths:
        try:
            py_compile.compile(str(path), doraise=True)
            add(
                checks,
                f"syntax:{path.name}",
                True,
                "Python syntax compiled successfully.",
            )
        except Exception as exc:
            add(
                checks,
                f"syntax:{path.name}",
                False,
                str(exc),
            )

    # File hashes for evidence/provenance.
    for label, path in paths.items():
        hashes[label] = sha256(path)

    # Inspect ZIP.
    try:
        with zipfile.ZipFile(paths["zip"]) as zf:
            html_names = [
                name for name in zf.namelist()
                if name.lower().endswith((".html", ".htm"))
            ]
        add(
            checks,
            "source_zip_readable",
            True,
            f"Found {len(html_names)} HTML file(s): {html_names}",
        )
        add(
            checks,
            "source_zip_has_html",
            len(html_names) >= 1,
            f"HTML entries: {html_names}",
        )
    except Exception as exc:
        add(checks, "source_zip_readable", False, str(exc))
        html_names = []

    # Canonical JSONL.
    try:
        jsonl_records = load_jsonl(paths["jsonl"])
        metrics["jsonl_rows"] = len(jsonl_records)
        add(
            checks,
            "jsonl_loads",
            True,
            f"Loaded {len(jsonl_records)} JSON objects.",
        )
        add(
            checks,
            "jsonl_expected_count",
            len(jsonl_records) == expected,
            f"Found {len(jsonl_records)}; expected {expected}.",
        )
        add(
            checks,
            "jsonl_fields_exact",
            all(tuple(record.keys()) == FIELDS for record in jsonl_records),
            "Every JSONL record uses the expected ordered field set.",
        )
    except Exception as exc:
        jsonl_records = []
        add(checks, "jsonl_loads", False, str(exc))

    # Canonical CSV.
    try:
        csv_fields, csv_records = load_csv(paths["csv"])
        metrics["csv_rows"] = len(csv_records)
        add(
            checks,
            "csv_loads",
            True,
            f"Loaded {len(csv_records)} CSV rows.",
        )
        add(
            checks,
            "csv_header_matches",
            csv_fields == FIELDS,
            f"CSV header: {csv_fields}",
        )
        add(
            checks,
            "csv_expected_count",
            len(csv_records) == expected,
            f"Found {len(csv_records)}; expected {expected}.",
        )
        add(
            checks,
            "csv_matches_jsonl_row_for_row",
            csv_records == jsonl_records,
            (
                "CSV and JSONL match row-for-row."
                if csv_records == jsonl_records
                else "CSV and JSONL differ."
            ),
        )
    except Exception as exc:
        csv_records = []
        add(checks, "csv_loads", False, str(exc))

    # Canonical SQLite.
    try:
        live_db = db_snapshot(paths["db"])
        metrics["sqlite_rows"] = len(live_db["records"])
        add(
            checks,
            "sqlite_integrity",
            live_db["integrity"] == "ok",
            f"PRAGMA integrity_check returned {live_db['integrity']!r}.",
        )
        add(
            checks,
            "sqlite_expected_count",
            len(live_db["records"]) == expected,
            f"Found {len(live_db['records'])}; expected {expected}.",
        )
        add(
            checks,
            "sqlite_matches_jsonl_row_for_row",
            live_db["records"] == jsonl_records,
            (
                "SQLite and JSONL match row-for-row."
                if live_db["records"] == jsonl_records
                else "SQLite and JSONL differ."
            ),
        )
    except Exception as exc:
        live_db = None
        add(checks, "sqlite_integrity", False, str(exc))

    # Existing DB validation report.
    try:
        db_report = json.loads(
            paths["db_report"].read_text(encoding="utf-8")
        )
        summary = db_report.get("summary", {})
        add(
            checks,
            "existing_db_report_passes",
            (
                summary.get("result") == "PASS"
                and summary.get("failed") == 0
                and summary.get("passed") == summary.get("checks")
            ),
            f"Summary: {summary}",
        )
        add(
            checks,
            "existing_db_report_count_matches",
            db_report.get("metrics", {}).get("row_count") == expected,
            f"Report row_count={db_report.get('metrics', {}).get('row_count')}",
        )
    except Exception as exc:
        add(checks, "existing_db_report_readable", False, str(exc))

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)

        # v0.1 should parse/validate the source successfully.
        p = run([
            sys.executable,
            str(root / "proofloop_openai_ingest_v0_1.py"),
            str(paths["zip"]),
            "--expected",
            str(expected),
            "--show",
            "0",
        ])
        add(
            checks,
            "v0_1_source_ingest_passes",
            p.returncode == 0,
            f"exit={p.returncode}; stdout={p.stdout.strip()[-500:]}",
        )

        # v0.2 should reproduce canonical JSONL exactly.
        regen_jsonl = temp / "openai_roles_regenerated.jsonl"
        p = run([
            sys.executable,
            str(root / "proofloop_openai_ingest_v0_2.py"),
            str(paths["zip"]),
            "--expected",
            str(expected),
            "--show",
            "0",
            "--output",
            str(regen_jsonl),
        ])
        add(
            checks,
            "v0_2_source_ingest_passes",
            p.returncode == 0 and regen_jsonl.is_file(),
            f"exit={p.returncode}; output exists={regen_jsonl.is_file()}",
        )

        if regen_jsonl.is_file():
            regenerated = load_jsonl(regen_jsonl)
            add(
                checks,
                "v0_2_regenerates_jsonl_semantically",
                regenerated == jsonl_records,
                (
                    "Regenerated JSONL matches canonical JSONL row-for-row."
                    if regenerated == jsonl_records
                    else "Regenerated JSONL differs from canonical JSONL."
                ),
            )
            add(
                checks,
                "v0_2_regenerates_jsonl_byte_for_byte",
                regen_jsonl.read_bytes() == paths["jsonl"].read_bytes(),
                (
                    "Regenerated JSONL is byte-for-byte identical."
                    if regen_jsonl.read_bytes() == paths["jsonl"].read_bytes()
                    else "Regenerated JSONL is semantically comparable but bytes differ."
                ),
            )

        # v0.3.1 normal success.
        p = run([
            sys.executable,
            str(root / "proofloop_openai_validate_v0_3_1.py"),
            str(paths["jsonl"]),
            "--expected",
            str(expected),
        ])
        add(
            checks,
            "v0_3_1_validator_accepts_good_jsonl",
            p.returncode == 0,
            f"exit={p.returncode}",
        )

        # v0.3.1 must reject a deliberately wrong expected count.
        p = run([
            sys.executable,
            str(root / "proofloop_openai_validate_v0_3_1.py"),
            str(paths["jsonl"]),
            "--expected",
            str(expected + 1),
        ])
        add(
            checks,
            "v0_3_1_validator_rejects_wrong_expected_count",
            p.returncode != 0,
            f"exit={p.returncode}",
        )

        # v0.4.1 should reproduce CSV.
        regen_csv = temp / "openai_roles_regenerated.csv"
        p = run([
            sys.executable,
            str(root / "proofloop_jsonl_to_csv_v0_4_1.py"),
            str(paths["jsonl"]),
            "--output",
            str(regen_csv),
            "--expected",
            str(expected),
        ])
        add(
            checks,
            "v0_4_1_csv_export_passes",
            p.returncode == 0 and regen_csv.is_file(),
            f"exit={p.returncode}; output exists={regen_csv.is_file()}",
        )

        if regen_csv.is_file():
            _, regen_csv_records = load_csv(regen_csv)
            add(
                checks,
                "v0_4_1_regenerates_csv_semantically",
                regen_csv_records == csv_records,
                (
                    "Regenerated CSV matches canonical CSV row-for-row."
                    if regen_csv_records == csv_records
                    else "Regenerated CSV differs from canonical CSV."
                ),
            )

        # v0.4.1 must reject wrong expected count.
        wrong_csv = temp / "wrong_count.csv"
        p = run([
            sys.executable,
            str(root / "proofloop_jsonl_to_csv_v0_4_1.py"),
            str(paths["jsonl"]),
            "--output",
            str(wrong_csv),
            "--expected",
            str(expected + 1),
        ])
        add(
            checks,
            "v0_4_1_converter_rejects_wrong_expected_count",
            p.returncode != 0,
            f"exit={p.returncode}",
        )

        # v0.5 should reproduce SQLite.
        regen_db = temp / "proofloop_regenerated.db"
        p = run([
            sys.executable,
            str(root / "proofloop_jsonl_to_sqlite_v0_5.py"),
            str(paths["jsonl"]),
            "--output",
            str(regen_db),
            "--expected",
            str(expected),
        ])
        add(
            checks,
            "v0_5_sqlite_import_passes",
            p.returncode == 0 and regen_db.is_file(),
            f"exit={p.returncode}; output exists={regen_db.is_file()}",
        )

        if regen_db.is_file():
            regen_db_snapshot = db_snapshot(regen_db)
            add(
                checks,
                "v0_5_regenerates_sqlite_data",
                regen_db_snapshot["records"] == jsonl_records,
                (
                    "Regenerated SQLite matches JSONL row-for-row."
                    if regen_db_snapshot["records"] == jsonl_records
                    else "Regenerated SQLite differs from JSONL."
                ),
            )
            if live_db is not None:
                add(
                    checks,
                    "v0_5_regenerates_sqlite_schema",
                    regen_db_snapshot["schema"] == live_db["schema"],
                    (
                        "Regenerated SQLite schema matches canonical database."
                        if regen_db_snapshot["schema"] == live_db["schema"]
                        else "Regenerated SQLite schema differs."
                    ),
                )

            # v0.6 against regenerated DB.
            fresh_report = temp / "fresh_db_report.json"
            p = run([
                sys.executable,
                str(root / "proofloop_sqlite_validate_v0_6.py"),
                str(regen_db),
                "--jsonl",
                str(paths["jsonl"]),
                "--expected",
                str(expected),
                "--report",
                str(fresh_report),
            ])
            add(
                checks,
                "v0_6_validator_passes_regenerated_database",
                p.returncode == 0 and fresh_report.is_file(),
                f"exit={p.returncode}; report exists={fresh_report.is_file()}",
            )

            if fresh_report.is_file():
                fresh = json.loads(
                    fresh_report.read_text(encoding="utf-8")
                )
                summary = fresh.get("summary", {})
                add(
                    checks,
                    "v0_6_report_all_checks_pass",
                    (
                        summary.get("result") == "PASS"
                        and summary.get("failed") == 0
                        and summary.get("passed") == summary.get("checks")
                    ),
                    f"Fresh summary: {summary}",
                )

    passed = sum(1 for item in checks if item["passed"])
    failed = len(checks) - passed
    result = "PASS" if failed == 0 else "FAIL"

    report = {
        "validator": "ProofLoop Full Pipeline Validator v0.7",
        "root": str(root),
        "expected_rows": expected,
        "metrics": metrics,
        "hashes_sha256": hashes,
        "summary": {
            "checks": len(checks),
            "passed": passed,
            "failed": failed,
            "result": result,
        },
        "checks": checks,
    }

    report_path = (
        args.report
        if args.report.is_absolute()
        else root / args.report
    )
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("ProofLoop Full Pipeline Validator v0.7")
    print(f"Project root:      {root}")
    print(f"Expected roles:    {expected}")
    print(f"Checks run:        {len(checks)}")
    print(f"Checks passed:     {passed}")
    print(f"Checks failed:     {failed}")
    print(f"Validation report: {report_path}")

    print("\nCheck results:")
    for item in checks:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"[{status}] {item['name']}: {item['detail']}")

    print(f"\nRESULT: {result}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
