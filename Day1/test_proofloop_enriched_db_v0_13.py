#!/usr/bin/env python3
"""
ProofLoop Enriched Database Test Suite v0.13

Formal synthetic tests for the enriched Source A + Source B database layer.

These are TESTS, not validation of the real 818-role database.
They use temporary synthetic data and do not modify:
- proofloop.db
- proofloop_enriched.db
- openai_roles.jsonl
- openai_ashby_roles.jsonl

Produces:
    proofloop_enriched_test_report.json
"""

from __future__ import annotations

import argparse
import json
import platform
import sqlite3
import subprocess
import sys
import tempfile
import time
import traceback
import unittest
from datetime import datetime, timezone
from pathlib import Path

from proofloop_build_enriched_db_v0_11 import (
    ashby_id_from_url,
    build_database,
    normalize_text,
)


ROOT = Path(__file__).resolve().parent
BUILDER = ROOT / "proofloop_build_enriched_db_v0_11.py"


def html_role(
    role_id: int,
    ashby_id: str,
    title: str = "Example Engineer",
    team: str = "Example Team",
    location: str = "San Francisco",
) -> dict:
    return {
        "role_id": role_id,
        "title": title,
        "team": team,
        "display_location": location,
        "career_url": f"https://openai.com/careers/example-{role_id}/",
        "apply_url": (
            f"https://jobs.ashbyhq.com/openai/{ashby_id}/application"
        ),
    }


def api_role(
    source_index: int,
    ashby_id: str,
    title: str = "Example Engineer",
    team: str = "Example Team",
    location: str = "San Francisco",
    secondary_locations=None,
    compensation=None,
) -> dict:
    return {
        "source_index": source_index,
        "source_snapshot": "synthetic_api_snapshot.json",
        "ashby_id": ashby_id,
        "title": title,
        "department": team,
        "team": team,
        "employment_type": "FullTime",
        "primary_location": location,
        "secondary_locations": secondary_locations or [],
        "published_at": "2026-10-07T12:00:00-06:00",
        "is_listed": True,
        "is_remote": False,
        "workplace_type": "Hybrid",
        "address": {
            "postalAddress": {
                "addressLocality": location,
                "addressCountry": "United States",
            }
        },
        "job_url": f"https://jobs.ashbyhq.com/openai/{ashby_id}",
        "apply_url": (
            f"https://jobs.ashbyhq.com/openai/{ashby_id}/application"
        ),
        "description_plain": "Synthetic role description.",
        "description_html": "<p>Synthetic role description.</p>",
        "compensation": compensation or {
            "summaryComponents": []
        },
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_json(path: Path, obj: dict) -> None:
    path.write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def synthetic_reconciliation(
    matched: int,
    html_only: int,
    api_only: int,
) -> dict:
    return {
        "summary": {
            "html_roles": matched + html_only,
            "api_roles": matched + api_only,
            "matched": matched,
            "html_only": html_only,
            "api_only": api_only,
            "matched_cosmetic_only_changes": 0,
            "matched_substantive_title_or_team_changes": 0,
            "html_records_without_ashby_id": 0,
            "api_records_without_ashby_id": 0,
        }
    }


class TestProofLoopEnrichedDatabase(unittest.TestCase):

    def test_01_normalize_text_collapses_whitespace(self):
        self.assertEqual(
            normalize_text("  Applied   AI  Engineer "),
            "Applied AI Engineer",
        )

    def test_02_ashby_id_extraction_from_apply_url(self):
        aid = "11111111-1111-1111-1111-111111111111"
        url = f"https://jobs.ashbyhq.com/openai/{aid}/application"
        self.assertEqual(ashby_id_from_url(url), aid)

    def test_03_builder_creates_union_and_source_statuses(self):
        matched_id = "11111111-1111-1111-1111-111111111111"
        html_only_id = "22222222-2222-2222-2222-222222222222"
        api_only_id = "33333333-3333-3333-3333-333333333333"

        html_rows = [
            html_role(1, matched_id),
            html_role(2, html_only_id, title="Historical Role"),
        ]
        api_rows = [
            api_role(1, matched_id),
            api_role(2, api_only_id, title="New API Role"),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            result = build_database(
                html_rows,
                api_rows,
                synthetic_reconciliation(1, 1, 1),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            self.assertEqual(result["table_counts"]["roles"], 3)
            self.assertEqual(
                result["status_counts"],
                {"api_only": 1, "html_only": 1, "matched": 1},
            )

    def test_04_matched_role_prefers_api_values_but_normalizes_whitespace(self):
        aid = "11111111-1111-1111-1111-111111111111"

        html_rows = [
            html_role(
                1,
                aid,
                title="Applied AI Engineer",
                team="Applied AI",
            )
        ]
        api_rows = [
            api_role(
                1,
                aid,
                title=" Applied   AI Engineer ",
                team="Applied  AI ",
            )
        ]

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            build_database(
                html_rows,
                api_rows,
                synthetic_reconciliation(1, 0, 0),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            conn = sqlite3.connect(db)
            try:
                row = conn.execute(
                    "SELECT title, team FROM roles WHERE ashby_id=?",
                    (aid,),
                ).fetchone()
            finally:
                conn.close()

            self.assertEqual(row, ("Applied AI Engineer", "Applied AI"))

    def test_05_html_source_row_is_preserved_exactly(self):
        aid = "11111111-1111-1111-1111-111111111111"
        original = html_role(
            1,
            aid,
            title="  Historical  Title  ",
            team=" Team  Name ",
        )

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            build_database(
                [original],
                [],
                synthetic_reconciliation(0, 1, 0),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            conn = sqlite3.connect(db)
            try:
                row = conn.execute(
                    """
                    SELECT title, team
                    FROM html_roles
                    WHERE html_role_id=1
                    """
                ).fetchone()
            finally:
                conn.close()

            self.assertEqual(
                row,
                ("  Historical  Title  ", " Team  Name "),
            )

    def test_06_api_source_preserves_raw_and_normalized_text(self):
        aid = "11111111-1111-1111-1111-111111111111"
        api = api_role(
            1,
            aid,
            title=" Engineer   Name ",
            team=" Team   Name ",
        )

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            build_database(
                [],
                [api],
                synthetic_reconciliation(0, 0, 1),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            conn = sqlite3.connect(db)
            try:
                row = conn.execute(
                    """
                    SELECT
                        title_raw, title_normalized,
                        team_raw, team_normalized
                    FROM api_roles
                    WHERE ashby_id=?
                    """,
                    (aid,),
                ).fetchone()
            finally:
                conn.close()

            self.assertEqual(
                row,
                (
                    " Engineer   Name ",
                    "Engineer Name",
                    " Team   Name ",
                    "Team Name",
                ),
            )

    def test_07_secondary_locations_become_relational_rows(self):
        aid = "11111111-1111-1111-1111-111111111111"
        secondary = [
            {
                "location": "New York City",
                "address": {
                    "postalAddress": {
                        "addressLocality": "New York City"
                    }
                },
            },
            {
                "location": "Washington, DC",
                "address": {
                    "postalAddress": {
                        "addressLocality": "Washington"
                    }
                },
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            build_database(
                [],
                [api_role(1, aid, secondary_locations=secondary)],
                synthetic_reconciliation(0, 0, 1),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            conn = sqlite3.connect(db)
            try:
                rows = conn.execute(
                    """
                    SELECT location_index, location
                    FROM api_secondary_locations
                    WHERE ashby_id=?
                    ORDER BY location_index
                    """,
                    (aid,),
                ).fetchall()
            finally:
                conn.close()

            self.assertEqual(
                rows,
                [(1, "New York City"), (2, "Washington, DC")],
            )

    def test_08_compensation_components_become_relational_rows(self):
        aid = "11111111-1111-1111-1111-111111111111"
        compensation = {
            "summaryComponents": [
                {
                    "compensationType": "Salary",
                    "interval": "1 YEAR",
                    "currencyCode": "USD",
                    "minValue": 100000,
                    "maxValue": 150000,
                },
                {
                    "compensationType": "EquityCashValue",
                    "interval": "1 YEAR",
                    "currencyCode": "USD",
                    "minValue": None,
                    "maxValue": None,
                },
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            build_database(
                [],
                [api_role(1, aid, compensation=compensation)],
                synthetic_reconciliation(0, 0, 1),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            conn = sqlite3.connect(db)
            try:
                rows = conn.execute(
                    """
                    SELECT
                        component_index, compensation_type,
                        currency_code, min_value, max_value
                    FROM api_compensation_components
                    WHERE ashby_id=?
                    ORDER BY component_index
                    """,
                    (aid,),
                ).fetchall()
            finally:
                conn.close()

            self.assertEqual(
                rows,
                [
                    (1, "Salary", "USD", 100000.0, 150000.0),
                    (2, "EquityCashValue", "USD", None, None),
                ],
            )

    def test_09_schema_rejects_invalid_source_status(self):
        aid = "11111111-1111-1111-1111-111111111111"

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "enriched.db"
            build_database(
                [],
                [api_role(1, aid)],
                synthetic_reconciliation(0, 0, 1),
                db,
                "html.jsonl",
                "api.jsonl",
                "reconciliation.json",
            )

            conn = sqlite3.connect(db)
            try:
                with self.assertRaises(sqlite3.IntegrityError):
                    conn.execute(
                        """
                        INSERT INTO roles (
                            ashby_id, title, team, apply_url,
                            present_in_html, present_in_api, source_status
                        )
                        VALUES (?, 'x', 'x', ?, 0, 1, 'bad_status')
                        """,
                        (
                            "99999999-9999-9999-9999-999999999999",
                            "https://example.invalid/application",
                        ),
                    )
            finally:
                conn.close()

    def test_10_builder_refuses_to_overwrite_existing_database(self):
        self.assertTrue(BUILDER.is_file())

        matched_id = "11111111-1111-1111-1111-111111111111"

        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            html_path = temp / "html.jsonl"
            api_path = temp / "api.jsonl"
            reconciliation_path = temp / "reconciliation.json"
            db_path = temp / "enriched.db"
            report_path = temp / "report.json"

            write_jsonl(
                html_path,
                [html_role(1, matched_id)],
            )
            write_jsonl(
                api_path,
                [api_role(1, matched_id)],
            )
            write_json(
                reconciliation_path,
                synthetic_reconciliation(1, 0, 0),
            )

            db_path.write_bytes(b"DO NOT OVERWRITE")

            proc = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--html-jsonl",
                    str(html_path),
                    "--api-jsonl",
                    str(api_path),
                    "--reconciliation-report",
                    str(reconciliation_path),
                    "--output",
                    str(db_path),
                    "--report",
                    str(report_path),
                    "--expected-html",
                    "1",
                    "--expected-api",
                    "1",
                    "--expected-union",
                    "1",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(db_path.read_bytes(), b"DO NOT OVERWRITE")

    def test_11_builder_rejects_wrong_expected_counts(self):
        self.assertTrue(BUILDER.is_file())

        matched_id = "11111111-1111-1111-1111-111111111111"

        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            html_path = temp / "html.jsonl"
            api_path = temp / "api.jsonl"
            reconciliation_path = temp / "reconciliation.json"
            db_path = temp / "enriched.db"
            report_path = temp / "report.json"

            write_jsonl(
                html_path,
                [html_role(1, matched_id)],
            )
            write_jsonl(
                api_path,
                [api_role(1, matched_id)],
            )
            write_json(
                reconciliation_path,
                synthetic_reconciliation(1, 0, 0),
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--html-jsonl",
                    str(html_path),
                    "--api-jsonl",
                    str(api_path),
                    "--reconciliation-report",
                    str(reconciliation_path),
                    "--output",
                    str(db_path),
                    "--report",
                    str(report_path),
                    "--expected-html",
                    "2",
                    "--expected-api",
                    "1",
                    "--expected-union",
                    "1",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(db_path.exists())

    def test_12_builder_cli_creates_report_with_correct_counts(self):
        self.assertTrue(BUILDER.is_file())

        matched_id = "11111111-1111-1111-1111-111111111111"
        html_only_id = "22222222-2222-2222-2222-222222222222"
        api_only_id = "33333333-3333-3333-3333-333333333333"

        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            html_path = temp / "html.jsonl"
            api_path = temp / "api.jsonl"
            reconciliation_path = temp / "reconciliation.json"
            db_path = temp / "enriched.db"
            report_path = temp / "report.json"

            write_jsonl(
                html_path,
                [
                    html_role(1, matched_id),
                    html_role(2, html_only_id),
                ],
            )
            write_jsonl(
                api_path,
                [
                    api_role(1, matched_id),
                    api_role(2, api_only_id),
                ],
            )
            write_json(
                reconciliation_path,
                synthetic_reconciliation(1, 1, 1),
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--html-jsonl",
                    str(html_path),
                    "--api-jsonl",
                    str(api_path),
                    "--reconciliation-report",
                    str(reconciliation_path),
                    "--output",
                    str(db_path),
                    "--report",
                    str(report_path),
                    "--expected-html",
                    "2",
                    "--expected-api",
                    "2",
                    "--expected-union",
                    "3",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            self.assertEqual(
                proc.returncode,
                0,
                msg=proc.stdout + proc.stderr,
            )
            self.assertTrue(db_path.is_file())
            self.assertTrue(report_path.is_file())

            report = json.loads(
                report_path.read_text(encoding="utf-8")
            )

            self.assertEqual(report["result"], "PASS")
            self.assertEqual(
                report["observed"],
                {
                    "html_roles": 2,
                    "api_roles": 2,
                    "canonical_union": 3,
                },
            )
            self.assertEqual(
                report["status_counts"],
                {
                    "api_only": 1,
                    "html_only": 1,
                    "matched": 1,
                },
            )


class ReportingTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_results = []
        self._started_at = {}

    def startTest(self, test):
        self._started_at[test.id()] = time.perf_counter()
        super().startTest(test)

    def _duration(self, test):
        start = self._started_at.pop(test.id(), None)
        if start is None:
            return None
        return round(time.perf_counter() - start, 6)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.case_results.append({
            "test": test.id(),
            "status": "PASS",
            "duration_seconds": self._duration(test),
            "detail": None,
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.case_results.append({
            "test": test.id(),
            "status": "FAIL",
            "duration_seconds": self._duration(test),
            "detail": "".join(traceback.format_exception(*err)),
        })

    def addError(self, test, err):
        super().addError(test, err)
        self.case_results.append({
            "test": test.id(),
            "status": "ERROR",
            "duration_seconds": self._duration(test),
            "detail": "".join(traceback.format_exception(*err)),
        })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.case_results.append({
            "test": test.id(),
            "status": "SKIP",
            "duration_seconds": self._duration(test),
            "detail": reason,
        })


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run ProofLoop enriched-database synthetic tests."
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("proofloop_enriched_test_report.json"),
    )
    args = parser.parse_args()

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestProofLoopEnrichedDatabase
    )

    started = time.perf_counter()

    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=ReportingTestResult,
    )
    result = runner.run(suite)

    duration = round(time.perf_counter() - started, 6)

    summary = {
        "tests_run": result.testsRun,
        "passed": sum(
            1 for item in result.case_results
            if item["status"] == "PASS"
        ),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "result": "PASS" if result.wasSuccessful() else "FAIL",
    }

    report = {
        "test_suite": "ProofLoop Enriched Database Test Suite v0.13",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "duration_seconds": duration,
        "summary": summary,
        "tests": result.case_results,
    }

    args.report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("\nProofLoop enriched test report")
    print(f"Report:       {args.report}")
    print(f"Tests run:    {summary['tests_run']}")
    print(f"Passed:       {summary['passed']}")
    print(f"Failed:       {summary['failed']}")
    print(f"Errors:       {summary['errors']}")
    print(f"Skipped:      {summary['skipped']}")
    print(f"RESULT:       {summary['result']}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
