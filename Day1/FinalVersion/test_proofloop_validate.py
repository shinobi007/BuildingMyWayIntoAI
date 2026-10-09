#!/usr/bin/env python3
"""Stage 4 synthetic regression tests (no network). Stage 3 creates test fixtures only.

Stage 4 validation is independently implemented and never imports Stage 3.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import io
import json
import shutil
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from datetime import datetime,timezone

import proofloop_validate as validator
import proofloop_store as fixture_builder  # fixture generator ONLY, not used by validator


def serialized(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()

def data_example(index: int):
    return {
        "id":f"00000000-0000-4000-8000-{index:012d}",
        "title":"Support Engineer " if index==1 else "IT Specialist",
        "department":"Engineering", "team":"IT", "employmentType":"FullTime", "location":"Seattle",
        "shouldDisplayCompensationOnJobPostings": True,
        "secondaryLocations":[{"location":"Remote, US","address":{"postalAddress":{"addressCountry":"United States"}}}] if index==1 else [],
        "publishedAt":"2026-10-01T00:00:00+00:00", "isListed": True,"isRemote":None,
        "workplaceType":None,"address":{"postalAddress":{"addressCountry":"United States"}},
        "jobUrl":f"https://jobs.ashbyhq.com/openai/00000000-0000-4000-8000-{index:012d}",
        "applyUrl":f"https://jobs.ashbyhq.com/openai/00000000-0000-4000-8000-{index:012d}/application",
        "descriptionHtml":"<p>Support</p>","descriptionPlain":"Support",
        "compensation": {"compensationTierSummary":"Example", "scrapeableCompensationSalarySummary":"$50-$75",
                         "compensationTiers":[{"id":"tier1","tierSummary":"range","title":None,"additionalInformation":None,
                                               "components":[{"id":"component1","summary":"salary","compensationType":"Salary",
                                                              "interval":"1 YEAR","currencyCode":"USD","minValue":50000,"maxValue":75000}]}] if index==1 else [],
                         "summaryComponents":[{"compensationType":"Salary","interval":"1 YEAR","currencyCode":"USD","minValue":50000,"maxValue":75000}] if index==1 else []}
    }


def fixture(root:Path):
    raw=[data_example(1),data_example(2)]
    source=root/"ashby_snapshot.json"
    source.write_text(serialized({"apiVersion":"1","jobs":raw}),encoding="utf-8")
    snapshot_hash=sha(source)
    mapping=validator.SOURCE_TO_CANONICAL
    rows=[]
    for i,item in enumerate(raw,1):
        canonical={ck:item[sk].strip() if sk in ("title","team","department","location") and isinstance(item[sk],str) else item[sk]
                   for sk,ck in mapping.items()}
        rows.append({"canonical":canonical,"raw":item,
                     "provenance":{"board":"openai","provider":"ashby","source_index":i,"snapshot_sha256":snapshot_hash}})
    lines=root/"jobs.jsonl"
    lines.write_text(''.join(serialized(r)+'\n' for r in rows),encoding='utf-8')
    norm=root/"normalization_report.json"
    norm.write_text(json.dumps({"stage":"normalize","status":"PASS","board":"openai","normalized_sha256":sha(lines),
                     "audit":{"source_sha256":snapshot_hash,"record_count":len(rows)}}),encoding='utf-8')
    store_bundle=root/"store_bundle"
    fixture_builder.build(lines,store_bundle,norm,None,False)
    store=store_bundle/"reports"/"store_report.json"
    db=store_bundle/"db"/"jobs.sqlite3"
    return source,lines,db,norm,store


class Stage4Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='proofloop-stage4-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.paths=list(fixture(self.root))

    def result(self):
        return validator.validate(*self.paths)

    def mutate_json(self,index,mutator):
        path=self.paths[index];data=json.loads(path.read_text(encoding='utf-8'))
        mutator(data);path.write_text(json.dumps(data),encoding='utf-8')

    def mutate_db(self, sql, args=(), *, disable_foreign_keys=False):
        # sqlite3.Connection.__exit__ commits/rolls back but does NOT close.
        # contextlib.closing is essential for Windows, where an unclosed
        # connection prevents TemporaryDirectory cleanup of jobs.sqlite3.
        with contextlib.closing(sqlite3.connect(self.paths[2])) as conn:
            if disable_foreign_keys:
                conn.execute('PRAGMA foreign_keys=OFF')
            with conn:
                conn.execute(sql, args)

    def test_baseline_passes(self):
        r=self.result();self.assertEqual(r['status'],'PASS');self.assertEqual(r['failed'],0)

    def test_all_expected_checks_present(self):
        self.assertEqual(len(self.result()['checks']),24)

    def test_fully_read_only_inputs(self):
        before=[sha(p) for p in self.paths]
        self.result()
        self.assertEqual(before,[sha(p) for p in self.paths])

    def test_corrupted_source_object_fails(self):
        self.mutate_json(0,lambda d:d['jobs'][0].update(title='Tampered'))
        self.assertEqual(self.result()['status'],'FAIL')

    def test_source_additional_record_detected(self):
        self.mutate_json(0,lambda d:d['jobs'].append(data_example(3)))
        self.assertFalse(self.result()['checks']['source_normalized_count'])

    def test_corrupt_normalization_report_hash(self):
        self.mutate_json(3,lambda d:d.update(normalized_sha256='x'*64))
        self.assertFalse(self.result()['checks']['normalization_report_hashes'])

    def test_corrupt_store_report_hash(self):
        self.mutate_json(4,lambda d:d['database'].update(sha256='z'*64))
        self.assertFalse(self.result()['checks']['store_report_hashes'])

    def test_corrupt_store_report_count(self):
        self.mutate_json(4,lambda d:d['database']['counts'].update(roles=20))
        self.assertFalse(self.result()['checks']['store_report_database_counts'])

    def test_wrong_board_in_report(self):
        self.mutate_json(3,lambda d:d.update(board='unknown'))
        self.assertFalse(self.result()['checks']['report_run_identity'])

    def test_bad_jsonl_canonical_field_detected(self):
        p=self.paths[1];data=[json.loads(x) for x in p.read_text().splitlines()];data[0]['canonical']['title']='BAD'
        p.write_text(''.join(serialized(x)+'\n' for x in data),encoding='utf-8')
        self.assertFalse(self.result()['checks']['canonical_projection_exact'])

    def test_database_scalar_tampering_detected(self):
        self.mutate_db('UPDATE roles SET team=? WHERE source_index=1',('BAD',))
        self.assertFalse(self.result()['checks']['db_scalar_projection'])

    def test_database_raw_json_tampering_detected(self):
        self.mutate_db('UPDATE roles SET raw_json=? WHERE source_index=1',('{"not":"source"}',))
        self.assertFalse(self.result()['checks']['db_source_raw_objects'])

    def test_database_canonical_json_tampering_detected(self):
        self.mutate_db('UPDATE roles SET canonical_json=? WHERE source_index=1',('{"not":"canonical"}',))
        self.assertFalse(self.result()['checks']['db_canonical_objects'])

    def test_database_provenance_tampering_detected(self):
        self.mutate_db('UPDATE roles SET source_index=? WHERE source_index=1',(5,))
        self.assertFalse(self.result()['checks']['db_provenance'])

    def test_database_secondary_location_corruption(self):
        self.mutate_db('UPDATE secondary_locations SET location=? WHERE ordinal=0',('Mars',))
        self.assertFalse(self.result()['checks']['db_all_child_rows'])

    def test_database_compensation_scalar_corruption(self):
        self.mutate_db('UPDATE compensation_components SET min_value=? WHERE ordinal=0',(123.0,))
        self.assertFalse(self.result()['checks']['db_all_child_rows'])

    def test_database_summary_component_corruption(self):
        self.mutate_db('UPDATE compensation_summary_components SET currency_code=? WHERE ordinal=0',('BTC',))
        self.assertFalse(self.result()['checks']['db_all_child_rows'])

    def test_database_deleted_child_detected(self):
        self.mutate_db('DELETE FROM compensation_tiers WHERE ordinal=0')
        self.assertFalse(self.result()['checks']['relational_row_counts'])

    def test_database_orphan_detected(self):
        self.mutate_db("UPDATE secondary_locations SET role_id='not-real'",
                       disable_foreign_keys=True)
        self.assertFalse(self.result()['checks']['foreign_keys'])

    def test_database_connection_closed_after_mutation(self):
        # Explicitly prove the connection is closed; tests on POSIX otherwise
        # may pass even when Windows would fail to remove the temp database.
        real_connect = sqlite3.connect
        opened = []
        def capture(*args, **kwargs):
            conn = real_connect(*args, **kwargs)
            opened.append(conn)
            return conn
        with mock.patch.object(sqlite3, 'connect', side_effect=capture):
            self.mutate_db('UPDATE roles SET team=? WHERE source_index=1', ('CLOSED',))
        self.assertEqual(len(opened), 1)
        with self.assertRaises(sqlite3.ProgrammingError):
            opened[0].execute('SELECT 1')

    def test_database_connection_closed_after_failed_mutation(self):
        real_connect = sqlite3.connect
        opened = []
        def capture(*args, **kwargs):
            conn = real_connect(*args, **kwargs)
            opened.append(conn)
            return conn
        with mock.patch.object(sqlite3, 'connect', side_effect=capture):
            with self.assertRaises(sqlite3.OperationalError):
                self.mutate_db('UPDATE nonexistent_table SET x=1')
        self.assertEqual(len(opened), 1)
        with self.assertRaises(sqlite3.ProgrammingError):
            opened[0].execute('SELECT 1')

    def test_missing_db_fails_safely(self):
        self.paths[2].unlink()
        with self.assertRaises(ValueError):
            self.result()

    def test_write_report_no_overwrite(self):
        out=self.root/'result';validator.write_report(self.result(),out)
        before=sha(out/'validation_report.json')
        with self.assertRaises(FileExistsError):
            validator.write_report(self.result(),out)
        self.assertEqual(before,sha(out/'validation_report.json'))

    def test_cli_success_reports(self):
        out=self.root/'cli_success'
        args=sum(([option,str(path)] for option,path in zip(("--snapshot","--jsonl","--db","--normalization-report","--store-report"),self.paths)),[])
        with contextlib.redirect_stdout(io.StringIO()):
            result=validator.main(args+["--output-dir",str(out)])
        self.assertEqual(result,0)
        self.assertEqual(json.loads((out/'validation_report.json').read_text())['status'],'PASS')
        self.assertTrue((out/'validation_report.md').exists())

    def test_cli_detected_mismatch_reports_failure(self):
        self.mutate_db('UPDATE roles SET location=? WHERE source_index=1',('BAD',))
        out=self.root/'cli_failed'
        args=sum(([option,str(path)] for option,path in zip(("--snapshot","--jsonl","--db","--normalization-report","--store-report"),self.paths)),[])
        with contextlib.redirect_stdout(io.StringIO()):
            result=validator.main(args+["--output-dir",str(out)])
        self.assertEqual(result,1)
        self.assertEqual(json.loads((out/'validation_report.json').read_text())['status'],'FAIL')

    def test_cli_missing_input_generates_failure_report(self):
        self.paths[0].unlink()
        out=self.root/'cli_missing'
        args=sum(([option,str(path)] for option,path in zip(("--snapshot","--jsonl","--db","--normalization-report","--store-report"),self.paths)),[])
        with contextlib.redirect_stderr(io.StringIO()):
            result=validator.main(args+["--output-dir",str(out)])
        self.assertEqual(result,2)
        self.assertEqual(json.loads((out/'validation_report.json').read_text())['status'],'FAIL')


class RecordedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.entries=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.entries.append({"name":test._testMethodName,"status":"PASS"})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.entries.append({"name":test._testMethodName,"status":"FAIL"})
    def addError(self,test,err):
        super().addError(test,err);self.entries.append({"name":test._testMethodName,"status":"ERROR"})


def main(argv=None):
    parser=argparse.ArgumentParser(description='Run Stage 4 negative and positive tests')
    parser.add_argument('--report-dir',type=Path,required=True)
    a=parser.parse_args(argv)
    if a.report_dir.exists():
        print('FAIL: report directory already exists',file=sys.stderr);return 2
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Stage4Tests)
    runner=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult)
    result=runner.run(suite)
    report={"stage":"independent_validation_tests","status":"PASS" if result.wasSuccessful() else "FAIL",
            "generated_at_utc":datetime.now(timezone.utc).isoformat(timespec='seconds'),
            "tests_run":result.testsRun,"passed":len([x for x in result.entries if x['status']=='PASS']),
            "failures":len(result.failures),"errors":len(result.errors),"cases":result.entries}
    if not a.report_dir.exists():
        a.report_dir.mkdir(parents=True)
    (a.report_dir/'test_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (a.report_dir/'test_report.md').write_text('# ProofLoop Stage 4 — Test Report\n\n'+f"**{report['status']}**: {report['passed']}/{report['tests_run']} passed\n\n"+'\n'.join(f"- {v['status']}: `{v['name']}`" for v in result.entries)+'\n',encoding='utf-8')
    print('Test reports:',a.report_dir)
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':
    raise SystemExit(main())
