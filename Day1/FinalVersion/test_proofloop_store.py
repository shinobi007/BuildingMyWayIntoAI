#!/usr/bin/env python3
"""Stage 3 synthetic regression suite. No network or access to project originals."""
from __future__ import annotations
import argparse
import contextlib
import copy
import hashlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime,timezone
from pathlib import Path
from unittest import mock

import proofloop_store as store


def fixture(ident="11111111-1111-4111-8111-111111111111", index=1):
    raw={"id": ident, "title":"Engineer", "someUnfamiliarSourceField": {"nested":True}}
    c={"id":ident,"title":"Engineer","department":"Technical","team":"Infra",
       "employment_type":"FullTime","location":"Remote US","published_at":"2026-10-01T00:00:00+00:00",
       "is_listed":True,"is_remote":None,"workplace_type":None,
       "should_display_compensation":False,
       "job_url":f"https://jobs.ashbyhq.com/example/{ident}",
       "apply_url":f"https://jobs.ashbyhq.com/example/{ident}/application",
       "description_plain":"Hello engineer", "description_html":"<p>Hello engineer</p>",
       "address":{"postalAddress":{"addressCountry":"US"}},
       "secondary_locations":[{"location":"NYC","address":{"postalAddress":{"addressLocality":"New York"}}}],
       "compensation":{"compensationTiers":[{"id":"tier-1","tierSummary":"range", "title":"NYC", "additionalInformation":None,
                     "components":[{"id":"c1","compensationType":"Salary","interval":"1 YEAR",
                                    "currencyCode":"USD","minValue":100000,"maxValue":150000,"summary":"$100-$150K"}]}],
                      "summaryComponents":[{"compensationType":"Salary","interval":"1 YEAR","currencyCode":"USD",
                                             "minValue":100000,"maxValue":150000}]}}
    p={"provider":"ashby","board":"example","source_index":index,"snapshot_sha256":"a"*64}
    return {"raw":raw,"canonical":c,"provenance":p}


class Stage3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="proofloop-stage3-test-")
        self.addCleanup(self.tmp.cleanup)
        self.dir=Path(self.tmp.name)
        self.source=self.dir/"jobs.jsonl"
        self.dest=self.dir/"bundle"
        self.rows=[fixture()]
        self.write()

    def write(self):
        data="".join(store.compact(x)+"\n" for x in self.rows)
        self.source.write_text(data,encoding="utf-8")

    def run_build(self, expected=None, report=None, allow_empty=False):
        return store.build(self.source,self.dest,report,expected,allow_empty)

    def assert_rejected(self, contains=None):
        with self.assertRaises((ValueError,sqlite3.Error,TypeError,KeyError,UnicodeError)) as c:
            self.run_build()
        if contains:
            self.assertIn(contains,str(c.exception))
        self.assertFalse(self.dest.exists())

    def test_success_persists_raw_canonical_provenance(self):
        out=self.run_build(expected=1)
        self.assertEqual(out["database"]["counts"]["roles"],1)
        db=self.dest/"db/jobs.sqlite3"
        con=sqlite3.connect(db)
        try:
            stored=con.execute("SELECT raw_json,canonical_json,provenance_json FROM roles").fetchone()
            for got,k in zip(stored,("raw","canonical","provenance")):
                self.assertEqual(json.loads(got),self.rows[0][k])
        finally:con.close()

    def test_all_child_tables_and_details(self):
        out=self.run_build()
        expected={"roles":1,"secondary_locations":1,"compensation_tiers":1,
                  "compensation_components":1,"compensation_summary_components":1}
        self.assertEqual(out["database"]["counts"],expected)
        self.assertTrue(all(out["database"]["checks"].values()))

    def test_null_bool_is_preserved(self):
        self.run_build()
        con=sqlite3.connect(self.dest/"db/jobs.sqlite3")
        try:
            values=con.execute("SELECT is_remote,workplace_type,should_display_compensation FROM roles").fetchone()
            self.assertEqual(values,(None,None,0))
        finally:con.close()

    def test_sql_metacharacters_are_data(self):
        self.rows[0]["canonical"]["title"]="Engineer'; DROP TABLE roles;--"
        self.write()
        self.run_build()
        con=sqlite3.connect(self.dest/"db/jobs.sqlite3")
        try:self.assertEqual(con.execute("SELECT COUNT(*) FROM roles").fetchone()[0],1)
        finally:con.close()

    def test_source_not_modified(self):
        before=self.source.read_bytes()
        self.run_build()
        self.assertEqual(self.source.read_bytes(),before)

    def test_existing_bundle_not_overwritten(self):
        self.dest.mkdir()
        sentinel=self.dest/"keep.txt";sentinel.write_text("existing",encoding="utf-8")
        with self.assertRaises(FileExistsError):self.run_build()
        self.assertEqual(sentinel.read_text(encoding="utf-8"),"existing")

    def test_report_sha_validates(self):
        report=self.dir/"normalize.json"
        report.write_text(json.dumps({"stage":"normalize","status":"PASS",
          "normalized_sha256":store.digest(self.source),
          "audit":{"record_count":1,"source_sha256":"a"*64}}),encoding="utf-8")
        out=self.run_build(report=report)
        self.assertTrue(out["input"]["normalization_report_verified"])
        self.assertEqual(out["input"]["jsonl_sha256"],store.digest(self.source))

    def test_wrong_sha_report_fails(self):
        report=self.dir/"normalize.json"
        report.write_text(json.dumps({"stage":"normalize","status":"PASS",
          "normalized_sha256":"0"*64,"audit":{"record_count":1,"source_sha256":"a"*64}}))
        with self.assertRaisesRegex(ValueError,"SHA-256"):
            self.run_build(report=report)
        self.assertFalse(self.dest.exists())

    def test_wrong_report_count_rejected(self):
        report=self.dir/"normalize.json"
        report.write_text(json.dumps({"stage":"normalize","status":"PASS",
          "normalized_sha256":store.digest(self.source),
          "audit":{"record_count":2,"source_sha256":"a"*64}}))
        with self.assertRaisesRegex(ValueError,"record count"):
            self.run_build(report=report)

    def test_duplicate_job_id_rejected(self):
        dup=copy.deepcopy(self.rows[0]);dup["provenance"]["source_index"]=2
        self.rows.append(dup);self.write();self.assert_rejected("Duplicate job ID")

    def test_duplicate_source_index_rejected(self):
        self.rows.append(fixture("22222222-2222-4222-8222-222222222222",1))
        self.write();self.assert_rejected("duplicate source index")

    def test_multiple_boards_rejected(self):
        nextrow=fixture("22222222-2222-4222-8222-222222222222",2)
        nextrow["provenance"]["board"]="other"
        self.rows.append(nextrow);self.write();self.assert_rejected("one board")

    def test_duplicate_source_hashes_rejected(self):
        nextrow=fixture("22222222-2222-4222-8222-222222222222",2)
        nextrow["provenance"]["snapshot_sha256"]="b"*64
        self.rows.append(nextrow);self.write();self.assert_rejected("one board")

    def test_mismatched_raw_id_rejected(self):
        self.rows[0]["raw"]["id"]="different";self.write();self.assert_rejected("IDs differ")

    def test_unsafe_http_url_rejected(self):
        self.rows[0]["canonical"]["apply_url"]="http://example.com/apply"
        self.write();self.assert_rejected("HTTPS")

    def test_wrong_bool_type_not_coerced(self):
        self.rows[0]["canonical"]["is_remote"]="false"
        self.write();self.assert_rejected("boolean")

    def test_malformed_json_rejected(self):
        self.source.write_text("{broken\n",encoding="utf-8")
        self.assert_rejected()

    def test_blank_line_rejected(self):
        self.source.write_text(self.source.read_text(encoding="utf-8")+"\n",encoding="utf-8")
        self.assert_rejected("Blank JSONL")

    def test_malformed_child_rejected(self):
        self.rows[0]["canonical"]["compensation"]["compensationTiers"][0]["components"]="not a list"
        self.write();self.assert_rejected("array")

    def test_wrong_expected_count_rejected(self):
        with self.assertRaisesRegex(ValueError,"Expected 2"):
            self.run_build(expected=2)
        self.assertFalse(self.dest.exists())

    def test_empty_requires_opt_in(self):
        self.rows=[];self.write();self.assert_rejected("--allow-empty")
        out=self.run_build(allow_empty=True)
        self.assertEqual(out["database"]["counts"]["roles"],0)

    def test_staging_rollback_after_injected_insert_failure(self):
        with mock.patch.object(store,"insert_records",side_effect=ValueError("synthetic insertion failure")):
            with self.assertRaisesRegex(ValueError,"synthetic insertion failure"):
                self.run_build()
        self.assertFalse(self.dest.exists())
        self.assertFalse(list(self.dir.glob(".proofloop-stage3-*")))

    def test_foreign_keys_enforced_and_integrity(self):
        self.run_build()
        con=sqlite3.connect(self.dest/"db/jobs.sqlite3")
        try:
            con.execute("PRAGMA foreign_keys=ON")
            with self.assertRaises(sqlite3.IntegrityError):
                con.execute("INSERT INTO secondary_locations VALUES ('not-a-role',0,'city','{}','{}')")
            self.assertEqual(con.execute("PRAGMA integrity_check").fetchone()[0],"ok")
        finally:con.close()

    def test_report_documents_verification(self):
        out=self.run_build()
        report=json.loads((self.dest/"reports/store_report.json").read_text(encoding="utf-8"))
        self.assertEqual(out,report)
        self.assertIn("SQLite Build Report",(self.dest/"reports/store_report.md").read_text())
        self.assertEqual(report["database"]["sha256"],store.digest(self.dest/"db/jobs.sqlite3"))


class RecordingResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.cases=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.cases.append({"test":test.id(),"status":"PASS"})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.cases.append({"test":test.id(),"status":"FAIL"})
    def addError(self,test,err):
        super().addError(test,err);self.cases.append({"test":test.id(),"status":"ERROR"})
    def addSkip(self,test,reason):
        super().addSkip(test,reason);self.cases.append({"test":test.id(),"status":"SKIP"})


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--report-dir",type=Path)
    args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Stage3Tests)
    runner=unittest.TextTestRunner(stream=sys.stderr,verbosity=2,resultclass=RecordingResult)
    result=runner.run(suite)
    info={"stage":"store_tests","status":"PASS" if result.wasSuccessful() else "FAIL",
          "tests_run":result.testsRun,"passed":sum(c["status"]=="PASS" for c in result.cases),
          "failures":len(result.failures),"errors":len(result.errors),"skipped":len(result.skipped),
          "cases":result.cases,"program_version":store.VERSION,"generated_at_utc":store.timestamp()}
    if args.report_dir:
        args.report_dir.mkdir(parents=True,exist_ok=True)
        (args.report_dir/"test_report.json").write_text(json.dumps(info,indent=2)+"\n",encoding="utf-8")
        md=["# ProofLoop Stage 3 — Synthetic Test Report","",
            f"**Result:** {info['status']}","",f"- Tests: {info['tests_run']}",
            f"- Passed: {info['passed']}",f"- Failed: {info['failures']}",
            f"- Errors: {info['errors']}",f"- Skipped: {info['skipped']}","", "## Cases",""]
        md += [f"- {c['status']}: `{c['test']}`" for c in info["cases"]]
        (args.report_dir/"test_report.md").write_text("\n".join(md)+"\n",encoding="utf-8")
        print("Test reports:", args.report_dir)
    return 0 if result.wasSuccessful() else 1

if __name__=="__main__":
    raise SystemExit(main())
