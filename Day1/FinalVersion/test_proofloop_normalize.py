"""Synthetic positive/negative tests for ProofLoop Stage 1 (stdlib only)."""
import json
import argparse
import sys
from datetime import datetime, timezone
import tempfile
import unittest
from pathlib import Path

from proofloop_normalize import execute, inspect_snapshot, source_hash


def sample_job(id_="x-123"):
    return {
        "id": id_, "title": "  IT Engineer  ", "department": "IT", "team": "Infra",
        "employmentType": "FullTime", "location": "Seattle", "isRemote": None,
        "isListed": True, "workplaceType": None, "publishedAt": "2026-10-07T10:00:00Z",
        "shouldDisplayCompensationOnJobPostings": False,
        "secondaryLocations": [{"location": "US", "address": {"postalAddress": {"addressCountry": "US"}}}],
        "address": {"postalAddress": {"addressLocality": "Seattle"}},
        "jobUrl": "https://jobs.ashbyhq.com/acme/x-123",
        "applyUrl": "https://jobs.ashbyhq.com/acme/x-123/application",
        "descriptionHtml": "<p>Technician</p>", "descriptionPlain": "Technician",
        "compensation": {"compensationTiers": [], "summaryComponents": []},
    }


def snapshot(jobs):
    return json.dumps({"apiVersion": "1", "jobs": jobs}).encode()


class NormalizationTests(unittest.TestCase):
    def test_valid_and_null_preservation(self):
        raw = snapshot([sample_job()])
        rows, stats = inspect_snapshot(raw, board="acme", expected_count=1)
        self.assertEqual(rows[0]["canonical"]["title"], "IT Engineer")
        self.assertEqual(rows[0]["raw"]["title"], "  IT Engineer  ")
        self.assertIsNone(rows[0]["canonical"]["is_remote"])
        self.assertIsNone(rows[0]["canonical"]["workplace_type"])
        self.assertEqual(stats["secondary_location_count"], 1)
        self.assertEqual(rows[0]["provenance"]["snapshot_sha256"], source_hash(raw))

    def test_unknown_fields_are_retained_and_reported(self):
        job = sample_job()
        job["newField"] = {"deep": [1, None]}
        rows, stats = inspect_snapshot(snapshot([job]), board="acme")
        self.assertEqual(rows[0]["raw"]["newField"], job["newField"])
        self.assertEqual(stats["unrecognized_source_fields"], {"newField": 1})

    def test_duplicate_ids_fail(self):
        with self.assertRaisesRegex(ValueError, "duplicate posting ID"):
            inspect_snapshot(snapshot([sample_job(), sample_job()]), board="acme")

    def test_required_blank_title_fails(self):
        job = sample_job(); job["title"] = " "
        with self.assertRaisesRegex(ValueError, "blank required field title"):
            inspect_snapshot(snapshot([job]), board="acme")

    def test_bad_remote_type_fails_not_coerced(self):
        job = sample_job(); job["isRemote"] = "false"
        with self.assertRaisesRegex(ValueError, "isRemote expected bool"):
            inspect_snapshot(snapshot([job]), board="acme")

    def test_bad_secondary_location_item_fails(self):
        job = sample_job(); job["secondaryLocations"] = [12]
        with self.assertRaisesRegex(ValueError, "secondaryLocations"):
            inspect_snapshot(snapshot([job]), board="acme")

    def test_bad_compensation_components_fail(self):
        job = sample_job(); job["compensation"] = {"compensationTiers": [{"components": "salary"}]}
        with self.assertRaisesRegex(ValueError, "components must be"):
            inspect_snapshot(snapshot([job]), board="acme")

    def test_non_https_url_fails(self):
        job = sample_job(); job["applyUrl"] = "http://example.com"
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            inspect_snapshot(snapshot([job]), board="acme")

    def test_wrong_expected_count_fails(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            inspect_snapshot(snapshot([sample_job()]), board="acme", expected_count=815)

    def test_missing_jobs_fails(self):
        with self.assertRaisesRegex(ValueError, "jobs array"):
            inspect_snapshot(b'{"apiVersion":"1"}', board="acme")

    def test_invalid_json_fails(self):
        with self.assertRaisesRegex(ValueError, "valid UTF-8 JSON"):
            inspect_snapshot(b'{broken', board="acme")

    def test_empty_requires_explicit_acknowledgement(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            inspect_snapshot(snapshot([]), board="acme")
        rows, info = inspect_snapshot(snapshot([]), board="acme", allow_empty=True)
        self.assertEqual(info["record_count"], 0)

    def test_successful_publish_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); src = p / "snapshot.json"; src.write_bytes(snapshot([sample_job()]))
            out = p / "runs" / "test"
            rpt = execute(src, out, board="acme", expected_count=1)
            self.assertEqual(rpt["status"], "PASS")
            self.assertEqual(len((out / "normalized/jobs.jsonl").read_text().splitlines()), 1)
            self.assertEqual(json.loads((out / "reports/normalization_report.json").read_text())["audit"]["record_count"], 1)
            previous = (out / "normalized/jobs.jsonl").read_bytes()
            with self.assertRaisesRegex(ValueError, "refusing overwrite"):
                execute(src, out, board="acme")
            self.assertEqual(previous, (out / "normalized/jobs.jsonl").read_bytes())
            self.assertEqual(src.read_bytes(), snapshot([sample_job()]))

    def test_bad_input_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); src = p / "bad.json"; src.write_bytes(snapshot([sample_job(), sample_job()]))
            out = p / "run"
            with self.assertRaisesRegex(ValueError, "duplicate"):
                execute(src, out, board="acme")
            self.assertFalse(out.exists())

    def test_reject_non_json_nan(self):
        with self.assertRaisesRegex(ValueError, "Non-JSON numeric constant"):
            inspect_snapshot(b'{"jobs":[{"id":"x","title":"Test","someNumeric":NaN}]}', board="acme")

    def test_unknown_nested_compensation_preserved(self):
        job = sample_job()
        job["compensation"]["futureCompField"] = {"subfield": "unchanged"}
        rows, info = inspect_snapshot(snapshot([job]), board="acme")
        self.assertEqual(rows[0]["canonical"]["compensation"]["futureCompField"], {"subfield": "unchanged"})
        self.assertEqual(info["nested_field_occurrences"]["compensation"]["futureCompField"], 1)

    def test_deterministic_canonical_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); src = p / "snapshot.json"; src.write_bytes(snapshot([sample_job()]))
            a=execute(src,p/"a",board="acme")
            b=execute(src,p/"b",board="acme")
            self.assertEqual(a["normalized_sha256"],b["normalized_sha256"])
            self.assertEqual((p/"a/normalized/jobs.jsonl").read_bytes(),(p/"b/normalized/jobs.jsonl").read_bytes())


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.case_results.append({"test": test.id(), "status": "PASS"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.case_results.append({"test": test.id(), "status": "FAIL", "reason": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.case_results.append({"test": test.id(), "status": "ERROR", "reason": self._exc_info_to_string(err, test)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.case_results.append({"test": test.id(), "status": "SKIP", "reason": reason})


def main():
    parser = argparse.ArgumentParser(description="Run Stage 1 synthetic regression tests and optionally save reports")
    parser.add_argument("--report-dir", type=Path, help="New report directory (refuses to overwrite)")
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    status = "PASS" if result.wasSuccessful() else "FAIL"
    report = {
        "stage": "normalize_tests", "status": status,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tests_run": result.testsRun, "passed": sum(x["status"] == "PASS" for x in result.case_results),
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "cases": result.case_results,
    }
    if args.report_dir:
        args.report_dir.mkdir(parents=True, exist_ok=False)
        (args.report_dir / "test_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        lines = ["# Stage 1 — Synthetic Test Report", "", f"**Result:** {status}", "", f"- Tests: {result.testsRun}", f"- Passed: {report['passed']}", f"- Failed: {len(result.failures)}", f"- Errors: {len(result.errors)}", f"- Skipped: {len(result.skipped)}", "", "## Individual cases", ""]
        lines.extend(f"- {case['status']}: `{case['test']}`" for case in result.case_results)
        lines.append("")
        (args.report_dir / "test_report.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"Test reports: {args.report_dir}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
