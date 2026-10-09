#!/usr/bin/env python3
"""
ProofLoop Pipeline Tests v0.7

Formal automated tests for the current ProofLoop pipeline.

These tests use tiny synthetic data in temporary directories so they do not
depend on the live 817-role OpenAI dataset and do not modify project data.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from proofloop_openai_ingest_v0_2 import (
    CareersParser,
    Role,
    unwrap_google_url,
    write_jsonl,
)
from proofloop_jsonl_to_sqlite_v0_5 import create_database
from proofloop_sqlite_validate_v0_6 import validate_database


class TestProofLoopPipeline(unittest.TestCase):
    def test_google_redirect_is_unwrapped(self):
        wrapped = (
            "https://www.google.com/url?"
            "q=https%3A%2F%2Fopenai.com%2Fcareers%2Fexample-role%2F"
        )
        self.assertEqual(
            unwrap_google_url(wrapped),
            "https://openai.com/careers/example-role/",
        )

    def test_html_parser_extracts_one_role(self):
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

    def test_jsonl_writer_round_trip(self):
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

    def test_sqlite_import_creates_expected_rows(self):
        records = [
            {
                "role_id": 1,
                "title": "Example Engineer",
                "team": "Example Team",
                "display_location": "US Remote",
                "career_url": "https://openai.com/careers/example-role/",
                "apply_url": (
                    "https://jobs.ashbyhq.com/openai/example/application"
                ),
            },
            {
                "role_id": 2,
                "title": "Second Engineer",
                "team": "Example Team",
                "display_location": "San Francisco, CA",
                "career_url": "https://openai.com/careers/second-role/",
                "apply_url": (
                    "https://jobs.ashbyhq.com/openai/second/application"
                ),
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "proofloop.db"
            count = create_database(records, db_path)

            self.assertEqual(count, 2)

            with sqlite3.connect(db_path) as conn:
                db_count = conn.execute(
                    "SELECT COUNT(*) FROM roles"
                ).fetchone()[0]

            self.assertEqual(db_count, 2)

    def test_sqlite_rejects_duplicate_career_url(self):
        records = [
            {
                "role_id": 1,
                "title": "Example Engineer",
                "team": "Example Team",
                "display_location": "US Remote",
                "career_url": "https://openai.com/careers/example-role/",
                "apply_url": (
                    "https://jobs.ashbyhq.com/openai/example/application"
                ),
            },
            {
                "role_id": 2,
                "title": "Duplicate URL Engineer",
                "team": "Example Team",
                "display_location": "US Remote",
                "career_url": "https://openai.com/careers/example-role/",
                "apply_url": (
                    "https://jobs.ashbyhq.com/openai/different/application"
                ),
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "proofloop.db"

            with self.assertRaises(sqlite3.IntegrityError):
                create_database(records, db_path)

    def test_validator_passes_clean_synthetic_pipeline(self):
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
            ),
            Role(
                role_id=2,
                title="Second Engineer",
                team="Example Team",
                display_location="San Francisco, CA",
                career_url="https://openai.com/careers/second-role/",
                apply_url=(
                    "https://jobs.ashbyhq.com/openai/second/application"
                ),
            ),
        ]

        records = [
            {
                "role_id": role.role_id,
                "title": role.title,
                "team": role.team,
                "display_location": role.display_location,
                "career_url": role.career_url,
                "apply_url": role.apply_url,
            }
            for role in roles
        ]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl_path = tmp_path / "roles.jsonl"
            db_path = tmp_path / "proofloop.db"

            write_jsonl(roles, jsonl_path)
            create_database(records, db_path)

            checks, metrics = validate_database(
                db_path,
                expected_count=2,
                jsonl_path=jsonl_path,
            )

            self.assertEqual(metrics["row_count"], 2)
            self.assertTrue(checks)
            self.assertTrue(all(check["passed"] for check in checks))


if __name__ == "__main__":
    unittest.main(verbosity=2)
