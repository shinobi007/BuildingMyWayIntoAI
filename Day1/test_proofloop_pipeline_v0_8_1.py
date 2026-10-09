#!/usr/bin/env python3
"""
ProofLoop Pipeline Test Suite v0.8.1

Formal automated tests for the current ProofLoop pipeline.

Changes in v0.8.1:
- imports the resource-safe SQLite importer v0.5.1
- writes a machine-readable JSON test report every run
- records per-test PASS/FAIL/ERROR/SKIP status and duration
- preserves regression tests for bugs found during validation
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

from proofloop_openai_ingest_v0_2 import (
    CareersParser,
    Role,
    unwrap_google_url,
    write_jsonl,
)
from proofloop_jsonl_to_sqlite_v0_5_1 import create_database
from proofloop_sqlite_validate_v0_6 import validate_database


ROOT = Path(__file__).resolve().parent
VALIDATOR_V031 = ROOT / "proofloop_openai_validate_v0_3_1.py"
CSV_V041 = ROOT / "proofloop_jsonl_to_csv_v0_4_1.py"


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def sample_record(role_id: int = 1) -> dict:
    suffix = str(role_id)
    return {
        "role_id": role_id,
        "title": f"Example Engineer {suffix}",
        "team": "Example Team",
        "display_location": "US Remote",
        "career_url": f"https://openai.com/careers/example-role-{suffix}/",
        "apply_url": (
            f"https://jobs.ashbyhq.com/openai/example-{suffix}/application"
        ),
    }


def write_records_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


class TestProofLoopPipeline(unittest.TestCase):

    def test_01_google_redirect_is_unwrapped(self):
        wrapped = (
            "https://www.google.com/url?"
            "q=https%3A%2F%2Fopenai.com%2Fcareers%2Fexample-role%2F"
        )
        self.assertEqual(
            unwrap_google_url(wrapped),
            "https://openai.com/careers/example-role/",
        )

    def test_02_html_parser_extracts_one_role(self):
        html = """
        <html>
          <body>
            <h2>
              <a href="https://openai.com/careers/example-role/">
                Example Engineer
              </a>
            </h2>
            <p>Example Team</p>
            <p>US Remote</p>
            <p>
              <a href="https://jobs.ashbyhq.com/openai/example/application">
                Apply now
              </a>
            </p>
          </body>
        </html>
        """

        parser = CareersParser()
        parser.feed(html)
        parser.close()

        self.assertEqual(len(parser.roles), 1)

        role = parser.roles[0]
        self.assertEqual(role.role_id, 1)
        self.assertEqual(role.title, "Example Engineer")
        self.assertEqual(role.team, "Example Team")
        self.assertEqual(role.display_location, "US Remote")
        self.assertEqual(
            role.career_url,
            "https://openai.com/careers/example-role/",
        )
        self.assertEqual(
            role.apply_url,
            "https://jobs.ashbyhq.com/openai/example/application",
        )

    def test_03_jsonl_writer_round_trip(self):
        roles = [
            Role(
                role_id=1,
                title="Example Engineer",
                team="Example Team",
                display_location="US Remote",
                career_url="https://openai.com/careers/example-role/",
                apply_url=(
                    "https://jobs.ashbyhq.com/openai/example/application"
                ),
            )
        ]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roles.jsonl"
            write_jsonl(roles, path)

            lines = path.read_text(encoding="utf-8").splitlines()

            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record["role_id"], 1)
            self.assertEqual(record["title"], "Example Engineer")

    def test_04_sqlite_import_creates_expected_rows(self):
        records = [sample_record(1), sample_record(2)]

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "proofloop.db"
            count = create_database(records, db_path)

            self.assertEqual(count, 2)

            conn = sqlite3.connect(db_path)
            try:
                db_count = conn.execute(
                    "SELECT COUNT(*) FROM roles"
                ).fetchone()[0]
            finally:
                conn.close()

            self.assertEqual(db_count, 2)

    def test_05_sqlite_rejects_duplicate_career_url(self):
        first = sample_record(1)
        second = sample_record(2)
        second["career_url"] = first["career_url"]

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "proofloop.db"

            with self.assertRaises(sqlite3.IntegrityError):
                create_database([first, second], db_path)

    def test_06_sqlite_validator_passes_clean_synthetic_pipeline(self):
        records = [sample_record(1), sample_record(2)]

        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            jsonl_path = temp / "roles.jsonl"
            db_path = temp / "proofloop.db"

            write_records_jsonl(jsonl_path, records)
            create_database(records, db_path)

            checks, metrics = validate_database(
                db_path,
                expected_count=2,
                jsonl_path=jsonl_path,
            )

            self.assertEqual(metrics["row_count"], 2)
            self.assertTrue(checks)
            self.assertTrue(all(check["passed"] for check in checks))

    def test_07_v031_validator_accepts_correct_expected_count(self):
        self.assertTrue(VALIDATOR_V031.is_file())

        with tempfile.TemporaryDirectory() as tmp:
            jsonl_path = Path(tmp) / "roles.jsonl"
            write_records_jsonl(
                jsonl_path,
                [sample_record(1), sample_record(2)],
            )

            result = run_script(
                str(VALIDATOR_V031),
                str(jsonl_path),
                "--expected",
                "2",
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=result.stdout + result.stderr,
            )
            self.assertIn("RESULT: PASS", result.stdout)

    def test_08_v031_validator_rejects_wrong_expected_count_regression(self):
        """
        Regression test for the v0.3 bug discovered during validation:
        [FAIL] could be printed while the program still returned PASS/0.
        """
        with tempfile.TemporaryDirectory() as tmp:
            jsonl_path = Path(tmp) / "roles.jsonl"
            write_records_jsonl(
                jsonl_path,
                [sample_record(1), sample_record(2)],
            )

            result = run_script(
                str(VALIDATOR_V031),
                str(jsonl_path),
                "--expected",
                "3",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RESULT: FAIL", result.stdout)

    def test_09_v041_csv_converter_accepts_correct_count(self):
        self.assertTrue(CSV_V041.is_file())

        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            jsonl_path = temp / "roles.jsonl"
            csv_path = temp / "roles.csv"

            write_records_jsonl(
                jsonl_path,
                [sample_record(1), sample_record(2)],
            )

            result = run_script(
                str(CSV_V041),
                str(jsonl_path),
                "--output",
                str(csv_path),
                "--expected",
                "2",
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=result.stdout + result.stderr,
            )
            self.assertTrue(csv_path.is_file())
            self.assertIn("RESULT: PASS", result.stdout)

    def test_10_v041_converter_rejects_wrong_expected_count_regression(self):
        """
        Regression test for the v0.4 bug discovered during validation:
        [FAIL] could be printed while the program still returned PASS/0.
        """
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            jsonl_path = temp / "roles.jsonl"
            csv_path = temp / "roles.csv"

            write_records_jsonl(
                jsonl_path,
                [sample_record(1), sample_record(2)],
            )

            result = run_script(
                str(CSV_V041),
                str(jsonl_path),
                "--output",
                str(csv_path),
                "--expected",
                "3",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RESULT: FAIL", result.stdout)
            self.assertFalse(
                csv_path.exists(),
                "CSV should not be written when expected-count validation fails.",
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
        description="Run ProofLoop's formal automated test suite."
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("proofloop_test_report.json"),
        help="JSON test report output path.",
    )
    args = parser.parse_args()

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestProofLoopPipeline
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
        "test_suite": "ProofLoop Pipeline Test Suite v0.8.1",
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

    print("\nProofLoop test report")
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
