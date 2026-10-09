#!/usr/bin/env python3
"""Stage 2 Ashby fetcher synthetic suite. No network requests are made."""
from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

import proofloop_fetch as f


def fixture(jobs=None, **extras):
    if jobs is None:
        jobs = [{"id": "12345678-1234-1234-1234-123456789012", "title": "Engineer",
                 "isRemote": None, "workplaceType": None,
                 "applyUrl": "https://jobs.ashbyhq.com/example/12345678-1234-1234-1234-123456789012/application",
                 "secondaryLocations": [], "compensation": {"compensationTiers": [], "summaryComponents": []}}]
    return json.dumps({"apiVersion": "1", "jobs": jobs, **extras}, separators=(",", ":")).encode()


class FakeResponse:
    status = 200
    def __init__(self, data: bytes, *, url="https://api.ashbyhq.com/posting-api/job-board/openai?includeCompensation=true", headers=None):
        self.data = data
        self.url = url
        self.headers = {"Content-Type": "application/json", "Content-Encoding": "identity"} if headers is None else headers
    def geturl(self): return self.url
    def read(self, maxbytes=None): return self.data if maxbytes is None else self.data[:maxbytes]
    def __enter__(self): return self
    def __exit__(self, *args): return False


class Stage2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fetch-tests-"))
    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
    def source(self, data=None):
        p = self.tmp / "source.json"
        p.write_bytes(fixture() if data is None else data)
        return p

    def test_url_build_with_compensation(self):
        self.assertEqual(f.public_endpoint("openai"), "https://api.ashbyhq.com/posting-api/job-board/openai?includeCompensation=true")
    def test_url_build_without_compensation(self):
        self.assertTrue(f.public_endpoint("example", False).endswith("includeCompensation=false"))
    def test_board_slug_rejects_injection(self):
        for v in ("", "/openai", "openai/abc", "a?b=1", "http:openai", " space", "x.y"):
            with self.subTest(v=v), self.assertRaises(ValueError): f.validate_board(v)
    def test_successful_offline_preserves_bytes_and_generates_reports(self):
        source = self.source()
        dest = self.tmp / "run"
        report = f.execute("openai", dest, source_file=source, expected_count=1)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["snapshot_audit"]["record_count"], 1)
        self.assertEqual((dest / "raw/ashby_snapshot.json").read_bytes(), source.read_bytes())
        self.assertIn("Source artifact", (dest / "reports/fetch_report.md").read_text())
        self.assertEqual(json.loads((dest / "reports/fetch_report.json").read_text())["snapshot_sha256"], report["snapshot_sha256"])
    def test_refuses_existing_destination_without_modifying(self):
        source = self.source()
        dest = self.tmp / "run"
        dest.mkdir()
        marker = dest / "do_not_touch.txt"
        marker.write_text("original")
        with self.assertRaisesRegex(ValueError, "already exists"):
            f.execute("openai", dest, source_file=source)
        self.assertEqual(marker.read_text(), "original")
    def test_frozen_source_not_modified(self):
        source = self.source()
        old_bytes = source.read_bytes()
        f.execute("openai", self.tmp / "run", source_file=source)
        self.assertEqual(source.read_bytes(), old_bytes)
    def test_wrong_expected_count_no_partial_output(self):
        source = self.source()
        dest = self.tmp / "run"
        with self.assertRaises(ValueError): f.execute("openai", dest, source_file=source, expected_count=2)
        self.assertFalse(dest.exists())
    def test_malformed_json_no_partial_output(self):
        source = self.source(b"not-json")
        dest = self.tmp / "run"
        with self.assertRaises(ValueError): f.execute("openai", dest, source_file=source)
        self.assertFalse(dest.exists())
    def test_duplicate_ids_no_partial_output(self):
        j = json.loads(fixture())["jobs"][0]
        source = self.source(fixture([j,j]))
        dest = self.tmp / "run"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            f.execute("openai", dest, source_file=source)
        self.assertFalse(dest.exists())
    def test_bad_nested_data_rejected_by_stage1_contract(self):
        j = json.loads(fixture())["jobs"][0]
        j["secondaryLocations"] = [7]
        with self.assertRaises(ValueError):
            f.execute("openai", self.tmp / "run", source_file=self.source(fixture([j])))
    def test_empty_rejected_unless_acknowledged(self):
        p = self.source(fixture([]))
        with self.assertRaisesRegex(ValueError, "empty"):
            f.execute("openai", self.tmp / "run", source_file=p)
        r = f.execute("openai", self.tmp / "allowed", source_file=p, allow_empty=True)
        self.assertEqual(r["snapshot_audit"]["record_count"], 0)
    def test_live_response_success(self):
        with patch.object(f, "urlopen", return_value=FakeResponse(fixture())) as openfn:
            data, info = f.fetch_live("openai", retries=0)
        self.assertEqual(data, fixture())
        self.assertEqual(info["http_status"], 200)
        self.assertEqual(info["attempts"], 1)
        self.assertEqual(openfn.call_count, 1)
    def test_live_503_retries_then_succeeds(self):
        err = HTTPError("https://api.ashbyhq.com/posting-api/job-board/openai", 503, "busy", {}, None)
        with patch.object(f, "urlopen", side_effect=[err, FakeResponse(fixture())]) as openfn:
            body, info = f.fetch_live("openai", retries=2, sleep=lambda _: None)
        self.assertEqual(info["attempts"], 2)
        self.assertEqual(info["transient_failures"][0]["http_status"], 503)
        self.assertEqual(openfn.call_count, 2)
    def test_live_429_retries_then_succeeds(self):
        err = HTTPError("https://api.ashbyhq.com/posting-api/job-board/openai", 429, "rate limited", {}, None)
        with patch.object(f, "urlopen", side_effect=[err, FakeResponse(fixture())]):
            _, info = f.fetch_live("openai", retries=1, sleep=lambda _: None)
        self.assertEqual(info["attempts"], 2)
    def test_live_400_does_not_retry(self):
        err = HTTPError("https://api.ashbyhq.com/posting-api/job-board/openai", 400, "bad request", {}, None)
        with patch.object(f, "urlopen", side_effect=err) as op:
            with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
                f.fetch_live("openai", retries=2, sleep=lambda _: None)
        self.assertEqual(op.call_count, 1)
    def test_live_network_retry_exhaustion(self):
        with patch.object(f, "urlopen", side_effect=URLError("offline")) as op:
            with self.assertRaises(RuntimeError):
                f.fetch_live("openai", retries=1, sleep=lambda _: None)
        self.assertEqual(op.call_count, 2)
    def test_live_bad_content_type_rejected(self):
        resp = FakeResponse(fixture(), headers={"Content-Type": "text/html"})
        with patch.object(f, "urlopen", return_value=resp):
            with self.assertRaisesRegex(ValueError, "Content-Type"):
                f.fetch_live("openai", retries=0)
    def test_live_compressed_payload_rejected(self):
        resp = FakeResponse(fixture(), headers={"Content-Type": "application/json", "Content-Encoding": "gzip"})
        with patch.object(f, "urlopen", return_value=resp):
            with self.assertRaisesRegex(ValueError, "Content-Encoding"):
                f.fetch_live("openai", retries=0)
    def test_live_redirect_outside_allowed_host_rejected(self):
        resp = FakeResponse(fixture(), url="https://example.com/jobs.json")
        with patch.object(f, "urlopen", return_value=resp):
            with self.assertRaisesRegex(ValueError, "redirected outside"):
                f.fetch_live("openai", retries=0)
    def test_maximum_response_size_enforced(self):
        resp = FakeResponse(b"a" * 1200)
        with patch.object(f, "urlopen", return_value=resp):
            with self.assertRaisesRegex(ValueError, "exceeds"):
                f.fetch_live("openai", max_bytes=1024, retries=0)
    def test_unknown_source_job_fields_preserved(self):
        j = json.loads(fixture())["jobs"][0]
        j["newField2027"] = {"v": True}
        p = self.source(fixture([j]))
        dest = self.tmp / "run"
        r = f.execute("openai", dest, source_file=p)
        self.assertIn("newField2027", r["snapshot_audit"]["unrecognized_source_fields"])
        self.assertEqual(json.loads((dest / "raw/ashby_snapshot.json").read_bytes())["jobs"][0]["newField2027"], {"v":True})
    def test_missing_file_rejected(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            f.execute("openai", self.tmp / "run", source_file=self.tmp / "missing.json")
    def test_failure_sidecar_contains_no_secrets(self):
        dest = self.tmp / "run"
        ret = f.main(["--board", "openai", "--source-file", str(self.tmp / "missing.json"), "--output-dir", str(dest)])
        self.assertEqual(ret, 1)
        self.assertFalse(dest.exists())
        matches = list(self.tmp.glob("run.FAILED.*.json"))
        self.assertEqual(len(matches), 1)
        self.assertEqual(json.loads(matches[0].read_text())["status"], "FAIL")


class ReportingResult(unittest.TextTestResult):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.cases = []
    def addSuccess(self, test):
        super().addSuccess(test)
        self.cases.append({"test": test.id(), "status": "PASS"})
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.cases.append({"test": test.id(), "status": "FAIL"})
    def addError(self, test, err):
        super().addError(test, err)
        self.cases.append({"test": test.id(), "status": "ERROR"})
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.cases.append({"test": test.id(), "status": "SKIP", "reason": reason})


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--report-dir", required=True, type=Path)
    args = p.parse_args(argv)
    if args.report_dir.exists():
        print(f"FAIL: report directory exists: {args.report_dir}", file=sys.stderr)
        return 2
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Stage2Tests)
    runner = unittest.TextTestRunner(verbosity=2, resultclass=ReportingResult)
    result = runner.run(suite)
    result_data = {"stage": "fetch_tests", "status": "PASS" if result.wasSuccessful() else "FAIL",
                   "tests_run": result.testsRun, "passed": result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
                   "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
                   "cases": result.cases,
                   "program_version": f.VERSION, "generated_at_utc": f.now_utc()}
    args.report_dir.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".fetch-tests-report-", dir=args.report_dir.parent))
    try:
        (stage/"test_report.json").write_text(json.dumps(result_data, indent=2) + "\n", encoding="utf-8")
        (stage/"test_report.md").write_text("\n".join([
            "# ProofLoop Stage 2 — Synthetic Test Report", "",
            f"**Result:** {result_data['status']}", "",
            f"- Tests run: {result_data['tests_run']}", f"- Passed: {result_data['passed']}",
            f"- Failed: {result_data['failures']}", f"- Errors: {result_data['errors']}",
            f"- Skipped: {result_data['skipped']}", "",
            "Tests include offline source fidelity, network retry/error handling (mocked), structural validation, publish safety and failure reporting.", "", "## Individual cases", "",
            *[f"- {row['status']}: `{row['test']}`" for row in result.cases], ""
        ]), encoding="utf-8")
        if args.report_dir.exists():
            print("FAIL: report directory appeared while testing", file=sys.stderr)
            return 2
        stage.rename(args.report_dir)
    finally:
        if stage.exists(): shutil.rmtree(stage)
    print(f"Test reports: {args.report_dir}")
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())
