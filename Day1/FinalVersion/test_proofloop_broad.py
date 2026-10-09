#!/usr/bin/env python3
"""Stage 5 synthetic regressions. Windows-safe: every SQLite connection is explicitly closed."""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
import proofloop_broad as a

PROFILE = {
 'schema_version':1,
 'preferred_domains':['technical_support','api_integration','programming','automation','systems_network','testing_data','security_investigation','documentation'],
 'exclude_sales':True,'require_technical_core':True,'allow_us_remote':True,'allow_us_relocation':True,
 'require_relocation_assistance':True,'allow_non_us':False,'max_deep_candidates':10,
}

def role(*,title='IT Support Specialist',team='IT',location='Seattle',country='United States',workplace='Hybrid',remote=True,
         description='About the Role\nIn this role, you will:\n- Troubleshoot systems and APIs.\nYou might thrive in this role if you:\n- Have 3+ years of experience in support.\nAbout OpenAI\nSales can partner with product.'):
    return {'board':'openai','id':'0000-0001','title':title,'team':team,'department':'IT','job_url':'https://jobs.ashbyhq.com/openai/0000-0001',
            'apply_url':'https://jobs.ashbyhq.com/openai/0000-0001/application', 'source_index':1, 'source_sha256':'a'*64,
            'published_at':'2026-10-08T01:00:00Z','location':location,'workplace_type':workplace,'is_remote':None if remote is None else int(remote),
            'address_json':json.dumps({'postalAddress':{'addressCountry':country}}),'compensation_json':json.dumps({'compensationTierSummary':None}),
            'should_display_compensation':None, 'description_plain':description}

class Stage5Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='proofloop-stage5-tests-')
        self.root=Path(self.temp.name)
        self.db=self.root/'jobs.sqlite3'
        self.store=self.root/'store.json';self.valid=self.root/'valid.json';self.profile_path=self.root/'profile.json'
        self.profile_path.write_text(json.dumps(PROFILE),encoding='utf-8')
        self.make_db()
        self.make_reports()

    def tearDown(self):
        # No open database handles remain when Windows removes the temp directory.
        self.temp.cleanup()

    def make_db(self):
        with closing(sqlite3.connect(self.db)) as conn:
            try:
                conn.executescript('''
                PRAGMA foreign_keys=ON;
                CREATE TABLE roles(id TEXT PRIMARY KEY, board TEXT, source_index INTEGER, source_sha256 TEXT, title TEXT,
                team TEXT,department TEXT,job_url TEXT,apply_url TEXT,published_at TEXT,location TEXT,workplace_type TEXT,
                is_remote INTEGER,address_json TEXT,compensation_json TEXT,should_display_compensation INTEGER,description_plain TEXT);
                CREATE TABLE secondary_locations(role_id TEXT REFERENCES roles(id),ordinal INTEGER,location TEXT,address_json TEXT);
                CREATE TABLE compensation_tiers(id INTEGER);
                CREATE TABLE compensation_components(id INTEGER);
                CREATE TABLE compensation_summary_components(id INTEGER);
                ''')
                r=role()
                conn.execute('INSERT INTO roles ('+','.join(r)+') VALUES('+','.join('?'*len(r))+')',tuple(r.values()))
                conn.commit()
            except BaseException:
                conn.rollback()
                raise

    def make_reports(self):
        digest=a.sha(self.db)
        self.store.write_text(json.dumps({'status':'PASS','board':'openai','database':{'sha256':digest},
          'input':{'jsonl_sha256':'b'*64,'source_sha256':'a'*64,'records':1}}),encoding='utf-8')
        self.valid.write_text(json.dumps({'status':'PASS','failed':0,'passed':24,'files':{
          'sqlite_sha256':digest,'jsonl_sha256':'b'*64},'details':{'source_records':1}}),encoding='utf-8')

    def classified(self,**kwargs):
        return a.classify(role(**kwargs),[],PROFILE)

    def test_profile_contract(self):
        self.assertEqual(a.check_profile(PROFILE)['max_deep_candidates'],10)

    def test_profile_rejects_unknown_domain(self):
        v={**PROFILE,'preferred_domains':['unsupported']}
        with self.assertRaises(ValueError):a.check_profile(v)

    def test_profile_rejects_bad_boolean(self):
        with self.assertRaises(ValueError):a.check_profile({**PROFILE,'exclude_sales':1})

    def test_hybrid_true_not_remote_eligible(self):
        x=self.classified();self.assertEqual(x['location']['category'],'US_OFFICE_RELOCATION_NOT_STATED')
        self.assertTrue(x['location']['remote_metadata_conflict'])
        self.assertEqual(x['band'],'STRETCH_OR_LOGISTICS_REVIEW')

    def test_remote_us_location_advertised(self):
        x=self.classified(location='US - Remote',workplace='Remote',remote=True)
        self.assertEqual(x['location']['category'],'US_REMOTE_ADVERTISED')
        self.assertEqual(x['location']['policy'],'REVIEW_ELIGIBILITY')

    def test_remote_city_requires_confirmation(self):
        x=self.classified(workplace='Remote',remote=True)
        self.assertEqual(x['location']['category'],'US_REMOTE_ELIGIBILITY_UNCONFIRMED')

    def test_relocation_detection(self):
        x=self.classified(description='About the role\nIn this role, you will: Troubleshoot APIs. We offer relocation assistance to new employees.\nQualifications: 2+ years of experience.\nAbout OpenAI')
        self.assertEqual(x['location']['category'],'US_RELOCATION_ASSISTANCE_STATED')
        self.assertEqual(x['band'],'DEEP_REVIEW_PRIORITY')

    def test_negated_relocation_is_not_a_positive_offer(self):
        x=self.classified(description='In this role, you will: Troubleshoot APIs. We do not offer relocation assistance.\nQualifications: 2+ years of experience.\nAbout OpenAI')
        self.assertEqual(x['location']['category'],'US_OFFICE_RELOCATION_NOT_STATED')

    def test_non_us_profile_hold(self):
        x=self.classified(location='Paris',country='France',remote=False,workplace='OnSite')
        self.assertEqual(x['location']['policy'],'OUTSIDE_PROFILE')
        self.assertEqual(x['band'],'HOLD_WITH_REASONS')

    def test_null_remote_remains_unknown(self):
        x=self.classified(remote=None,workplace=None)
        self.assertIsNone(x['location']['is_remote'])

    def test_commissioning_not_sales(self):
        x=self.classified(description='About the role\nIn this role, you will: Commissioning systems and troubleshooting APIs.\nQualifications: Experience with networks.\nAbout OpenAI')
        self.assertEqual(x['sales']['classification'],'NO_STRONG_SALES_EVIDENCE')

    def test_sales_quota_exclusion(self):
        x=self.classified(description='About the role\nIn this role, you will: Own revenue quotas and troubleshoot APIs.\nQualifications: 2+ years of experience.\nAbout OpenAI')
        self.assertEqual(x['sales']['classification'],'SALES_PRIMARY_EVIDENCE')
        self.assertEqual(x['band'],'HOLD_WITH_REASONS')

    def test_sales_team_exclusion(self):
        self.assertEqual(self.classified(team='Sales')['sales']['classification'],'SALES_PRIMARY_EVIDENCE')

    def test_employer_boilerplate_ignored(self):
        x=self.classified(description='About the Role\nIn this role, you will: Troubleshoot APIs.\nQualifications: 3+ years of experience.\nAbout OpenAI\nGrow your sales quota.')
        self.assertEqual(x['sales']['classification'],'NO_STRONG_SALES_EVIDENCE')

    def test_missing_qualifications_not_zero_requirements(self):
        x=self.classified(description='In this role, you will: Troubleshoot APIs.\nAbout OpenAI')
        self.assertEqual(x['qualification_screen']['section_method'],'heading_not_found')
        self.assertIn('qualification_heading_missing',x['review_flags'])

    def test_year_evidence_does_not_claim_match(self):
        x=self.classified(description='In this role, you will: Troubleshoot APIs.\nYou might thrive in this role if: Have 8+ years of experience in engineering, ideally in startups.\nAbout OpenAI')
        self.assertTrue(x['qualification_screen']['years_evidence'])
        self.assertEqual(x['qualification_screen']['required_vs_preferred'],'NOT_CLASSIFIED_AT_BROAD_STAGE')

    def test_markdown_escapes_untrusted_titles(self):
        x=self.classified(title='<script>alert(1)</script> Software Engineer')
        rep={'status':'PASS','board':'openai','counts':{'total':1,'bands':{},'locations':{},'sales':{},'technical':{}},
             'max_deep_candidates':1,'inputs':{'db_sha256':'a','profile_sha256':'b'},
             'deep_review_pool':[{'title':x['title'],'band':x['band'],'job_url':x['job_url']}]}
        output=a.md_report(rep)
        self.assertNotIn('<script>',output)
        self.assertIn('&lt;script&gt;',output)

    def test_full_run(self):
        out=self.root/'done'
        r=a.run(self.db,self.store,self.valid,self.profile_path,out)
        self.assertEqual(r['counts']['total'],1)
        self.assertEqual(len(r['deep_review_pool']),1)
        self.assertTrue((out/'broad_analysis_report.md').exists())
        self.assertTrue((out/'deep_review_candidates.json').exists())

    def test_run_no_overwrite(self):
        out=self.root/'done'
        a.run(self.db,self.store,self.valid,self.profile_path,out)
        old=(out/'broad_analysis_report.json').read_bytes()
        with self.assertRaises(FileExistsError):a.run(self.db,self.store,self.valid,self.profile_path,out)
        self.assertEqual((out/'broad_analysis_report.json').read_bytes(),old)

    def test_corrupted_database_hash_blocks_run(self):
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute("UPDATE roles SET title='tampered'")
            conn.commit()
        with self.assertRaisesRegex(ValueError,'SHA'):
            a.run(self.db,self.store,self.valid,self.profile_path,self.root/'none')
        self.assertFalse((self.root/'none').exists())

    def test_invalid_validation_report_blocks_run(self):
        obj=json.loads(self.valid.read_text());obj['status']='FAIL';self.valid.write_text(json.dumps(obj))
        with self.assertRaises(ValueError):a.run(self.db,self.store,self.valid,self.profile_path,self.root/'none')

    def test_input_failure_no_output(self):
        with self.assertRaises(ValueError):a.run(self.root/'missing.db',self.store,self.valid,self.profile_path,self.root/'none')
        self.assertFalse((self.root/'none').exists())

    def test_choose_review_unique_and_bounded(self):
        ds=[]
        for i in range(60):
            d=self.classified();d['id']=str(i)
            d['band']='DEEP_REVIEW_PRIORITY' if i<30 else 'STRETCH_OR_LOGISTICS_REVIEW'
            ds.append(d)
        p=a.choose_review(ds,10)
        self.assertEqual(len(p),10);self.assertEqual(len(set(x['id'] for x in p)),10)
        self.assertTrue(any(x['band']=='STRETCH_OR_LOGISTICS_REVIEW' for x in p))

    def test_sqlite_handle_closes_even_on_error(self):
        with self.assertRaises(ValueError):
            self._forced_failure()

    def _forced_failure(self):
        # A read-only connection must close explicitly (critical on Windows).
        conn=sqlite3.connect(self.db.resolve().as_uri()+'?mode=ro',uri=True)
        try:
            with closing(conn):
                raise ValueError('deliberate')
        finally:
            with self.assertRaises(sqlite3.ProgrammingError):conn.execute('SELECT 1')

class Recorder(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.cases=[]
    def addSuccess(self,test):super().addSuccess(test);self.cases.append({'test':test._testMethodName,'status':'PASS'})
    def addFailure(self,test,err):super().addFailure(test,err);self.cases.append({'test':test._testMethodName,'status':'FAIL'})
    def addError(self,test,err):super().addError(test,err);self.cases.append({'test':test._testMethodName,'status':'ERROR'})
    def addSkip(self,test,reason):super().addSkip(test,reason);self.cases.append({'test':test._testMethodName,'status':'SKIP'})

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--report-dir',type=Path,required=True)
    opts=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Stage5Tests)
    runner=unittest.TextTestRunner(verbosity=2,resultclass=Recorder)
    result=runner.run(suite)
    reports=opts.report_dir
    if reports.exists():
        print('FAIL: report dir already exists:',reports,file=__import__('sys').stderr)
        raise SystemExit(2)
    reports.mkdir(parents=True,exist_ok=False)
    data={'stage':'broad_analysis_tests','status':'PASS' if result.wasSuccessful() else 'FAIL',
          'generated_at_utc':datetime.now(timezone.utc).isoformat(),'tests_run':result.testsRun,
          'passed':sum(c['status']=='PASS' for c in result.cases),'failures':len(result.failures),
          'errors':len(result.errors),'skipped':len(result.skipped),'cases':result.cases}
    (reports/'test_report.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    lines=['# ProofLoop Stage 5 — Test Report','',f"**{data['status']}**: {data['passed']}/{result.testsRun} passed",'']
    lines.extend('- '+c['status']+': `'+c['test']+'`' for c in result.cases)
    (reports/'test_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Test reports:',reports)
    raise SystemExit(0 if result.wasSuccessful() else 1)
