#!/usr/bin/env python3
"""Stage 6 synthetic regression tests. Uses disposable, always-closed SQLite connections."""
from __future__ import annotations
import argparse
from contextlib import closing
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
import proofloop_deep as s

BASE_DESC='''ABOUT THE ROLE
In this role, you will:
 - Debug support issues.
You might thrive in this role if you have:
 - Have 8+ years of experience in support engineering, ideally at a startup.
 - Are comfortable troubleshooting REST APIs, SQL and distributed systems.
 - Have strong written communication skills.
About OpenAI
This is boilerplate.
'''


def evidence():
    return {'schema_version':1,'status':'UNVERIFIED_RESUME_CLAIMS','evidence':[
        {'id':'A','kind':'DATED_WORK_HISTORY','dates':'2022-06 to 2024-06','summary':'User support and REST APIs','topics':['technical_support','api_integration']},
        {'id':'B','kind':'RESUME_SKILL_LISTING','summary':'Listed SQL','topics':['sql']} ]}


def broad_dossier(id='test-role'):
    return {'id':id,'title':'AI Support Engineer','source_index':1,'band':'DEEP_REVIEW_PRIORITY',
      'seniority_title_signal':'UNSPECIFIED_OR_OTHER','review_flags':[],
      'location':{'policy':'RELOCATION_NOT_CONFIRMED','category':'US_OFFICE_RELOCATION_NOT_STATED',
                  'remote_metadata_conflict':False},
      'sales':{'classification':'NO_STRONG_SALES_EVIDENCE'},
      'technical':{'classification':'HANDS_ON_EVIDENCE'}}


def write_json(path,x):path.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')


def synthetic_bundle(root):
    db=root/'db.sqlite3'
    with closing(sqlite3.connect(db)) as conn:
        conn.execute('''CREATE TABLE roles (id TEXT PRIMARY KEY,title TEXT,source_index INTEGER,job_url TEXT,apply_url TEXT,
                        published_at TEXT,description_plain TEXT,source_sha256 TEXT)''')
        conn.execute('''INSERT INTO roles VALUES (?,?,?,?,?,?,?,?)''',('test-role','AI Support Engineer',1,
               'https://jobs.ashbyhq.com/openai/test-role','https://jobs.ashbyhq.com/openai/test-role/application',
               '2026-10-09T00:00:00Z',BASE_DESC,'a'*64))
        conn.commit()
    dbhash=s.digest(db)
    store=root/'store.json'; validation=root/'validation.json'; broad=root/'broad.json'; pool=root/'pool.json'; ev=root/'private.json'
    d=broad_dossier()
    pr={'id':'test-role','title':'AI Support Engineer','source_index':1,'band':'DEEP_REVIEW_PRIORITY'}
    write_json(store,{'stage':'store','status':'PASS','board':'openai',
        'database':{'sha256':dbhash},'input':{'records':1,'source_sha256':'a'*64}})
    write_json(validation,{'stage':'independent_validation','status':'PASS','failed':0,
        'files':{'sqlite_sha256':dbhash}})
    write_json(broad,{'stage':'broad_analysis','status':'PASS','board':'openai',
        'inputs':{'db_sha256':dbhash},'deep_review_pool':[pr],'roles':[d]})
    write_json(pool,{'board':'openai','database_sha256':dbhash,'candidate_ids':['test-role'],'candidates':[pr]})
    write_json(ev,evidence())
    return [db,store,validation,broad,pool,ev]


class Stage6Tests(unittest.TestCase):
    def test_eight_years_not_satisfied(self):
        r,m=s.extract_requirements(BASE_DESC)
        self.assertEqual(r[0]['years_mentioned'],[8]);self.assertEqual(r[0]['requirement_context'],'EXPECTATION_CONTEXT')
        self.assertTrue(r[0]['contains_preference_qualifier'])
        d=s.review_one({'id':'a','title':'AI Support Engineer','source_index':1,'job_url':'https://a','apply_url':'https://b',
            'description_plain':BASE_DESC,'published_at':None},broad_dossier('a'),evidence())
        self.assertEqual(d['requirements'][0]['duration_requirement_satisfied'],'NOT_ASSESSED')
    def test_stated_requirement_heading(self):
        x,m=s.extract_requirements('Required Qualifications:\n - Have a bachelor degree.\nAbout OpenAI')
        self.assertEqual(x[0]['requirement_context'],'STATED_REQUIREMENT_CONTEXT')
    def test_nice_to_have_does_not_change_prior(self):
        x,m=s.extract_requirements('Requirements:\n - Have 5 years of software work.\nNice to have:\n - Python experience.\nAbout OpenAI')
        self.assertEqual(x[0]['requirement_context'],'EXPECTATION_CONTEXT');self.assertEqual(x[1]['requirement_context'],'PREFERRED_CONTEXT')
    def test_no_heading_is_unknown_not_zero(self):
        x,m=s.extract_requirements('You should know Linux and Python.')
        self.assertEqual(x,[]);self.assertEqual(m['status'],'NOT_EXTRACTED_REQUIRES_MANUAL_REVIEW')
    def test_qual_heading_variants(self):
        for line in ['You will thrive in this role if you have:', 'You might thrive in this role if you have:',
                     'What we look for:', 'Who you are:', 'Qualifications:', 'Preferred Qualifications:']:
            with self.subTest(line=line):self.assertIsNotNone(s.heading(line))
    def test_stop_employer_boilerplate(self):
        x,m=s.extract_requirements('You might thrive in this role if:\n - Python skills.\nAbout OpenAI\n - PhD required')
        self.assertEqual(len(x),1);self.assertNotIn('PhD',x[0]['source_text'])
    def test_bullet_wrap_multiline(self):
        x,m=s.extract_requirements('Requirements:\n - Strong experience with\n   production APIs.\nAbout OpenAI')
        self.assertEqual(x[0]['source_text'],'Strong experience with production APIs.')
    def test_numbered_list(self):
        x,m=s.extract_requirements('Requirements:\n1. Python\n2) SQL\nAbout OpenAI')
        self.assertEqual(len(x),2)
    def test_untrusted_text_escaped(self):
        htmlsafe=s.escape_md('x <img src=x> [click](foo) | hey')
        self.assertNotIn('<img',htmlsafe);self.assertIn('\\[',htmlsafe)
    def test_exact_professional_domains_only(self):
        x,m=s.extract_requirements('Requirements:\n - Work on Kubernetes, GPU and distributed systems.\nAbout OpenAI')
        self.assertIn('distributed_systems',x[0]['topic_signals'])
        self.assertNotIn('technical_support',x[0]['topic_signals'])
    def test_matching_is_only_topic_overlap(self):
        d=s.review_one({'id':'a','title':'AI Support Engineer','source_index':1,'job_url':'https://a','apply_url':'https://b',
            'description_plain':BASE_DESC,'published_at':None},broad_dossier('a'),evidence())
        self.assertEqual(d['requirements'][0]['assessment'],'TOPIC_OVERLAP_NOT_REQUIREMENT_PROOF')
    def test_unknown_evidence_tag_rejected(self):
        e=evidence();e['evidence'][0]['topics'].append('bogus')
        with self.assertRaises(ValueError):s.evidence_profile_check(e)
    def test_non_unique_evidence_rejected(self):
        e=evidence();e['evidence'][1]['id']='A'
        with self.assertRaises(ValueError):s.evidence_profile_check(e)
    def test_missing_work_history_dates_rejected(self):
        e=evidence();del e['evidence'][0]['dates']
        with self.assertRaises(ValueError):s.evidence_profile_check(e)
    def test_unsupported_evidence_status_rejected(self):
        e=evidence();e['status']='VERIFIED'
        with self.assertRaises(ValueError):s.evidence_profile_check(e)
    def test_seniority_explicit_flag(self):
        b=broad_dossier('a');b['seniority_title_signal']='PRINCIPAL_STAFF'
        d=s.review_one({'id':'a','title':'AI Support Engineer','source_index':1,'job_url':'x','apply_url':'y','published_at':None,
                        'description_plain':BASE_DESC},b,evidence())
        self.assertIn('elevated_title_seniority_review',d['review_flags'])
    def test_remote_true_hybrid_flag(self):
        b=broad_dossier('a');b['location']['remote_metadata_conflict']=True
        d=s.review_one({'id':'a','title':'AI Support Engineer','source_index':1,'job_url':'x','apply_url':'y','published_at':None,
                        'description_plain':BASE_DESC},b,evidence())
        self.assertIn('hybrid_not_utah_remote',d['review_flags'])
    def test_db_connection_closure_on_success(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            paths=synthetic_bundle(Path(tmp))
            result=s.checks(*paths)
            self.assertEqual(len(result[5]),1)
            # On Windows the DB can now be unlinked because stage6 closed its handle.
            paths[0].unlink()
            self.assertFalse(paths[0].exists())
    def test_db_connection_closure_on_query_error(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            paths=synthetic_bundle(Path(tmp))
            with closing(sqlite3.connect(paths[0])) as conn:
                conn.execute('DROP TABLE roles');conn.commit()
            newhash=s.digest(paths[0])
            for index in (1,2,3,4):
                document=s.read_json(paths[index])
                if index==1:document['database']['sha256']=newhash
                if index==2:document['files']['sqlite_sha256']=newhash
                if index==3:document['inputs']['db_sha256']=newhash
                if index==4:document['database_sha256']=newhash
                write_json(paths[index],document)
            with self.assertRaises(sqlite3.Error):s.checks(*paths)
            paths[0].unlink()  # Windows should allow deletion if validator closed its connection.
            self.assertFalse(paths[0].exists())
    def test_end_to_end_one_candidate(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p); before=s.digest(a[0]);out=p/'out'
            result=s.run(*a,out)
            self.assertEqual(result['counts']['reviewed'],1)
            self.assertEqual(result['counts']['years_to_review'],1)
            self.assertEqual(result['dossiers'][0]['requirements'][0]['years_mentioned'],[8])
            self.assertTrue((out/'deep_analysis_report.md').exists())
            self.assertEqual(before,s.digest(a[0]))
    def test_refuses_output_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p);out=p/'out';out.mkdir();(out/'sentinel').write_text('keep')
            with self.assertRaises(ValueError):s.run(*a,out)
            self.assertEqual((out/'sentinel').read_text(),'keep')
    def test_incorrect_database_digest_rejected(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p)
            with closing(sqlite3.connect(a[0])) as c:
                c.execute("UPDATE roles SET title='tampered'");c.commit()
            with self.assertRaisesRegex(ValueError,'database integrity mismatch'):s.checks(*a)
    def test_failed_validation_report_rejected(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p);r=s.read_json(a[2]);r['status']='FAIL';write_json(a[2],r)
            with self.assertRaises(ValueError):s.checks(*a)
    def test_broad_pool_disagreement_rejected(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p);r=s.read_json(a[4]);r['candidate_ids']=['different'];write_json(a[4],r)
            with self.assertRaisesRegex(ValueError,'order/identities'):s.checks(*a)
    def test_broad_role_title_disagreement_rejected(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p);r=s.read_json(a[3]);r['roles'][0]['title']='Oops';write_json(a[3],r)
            with self.assertRaises(ValueError):s.checks(*a)
    def test_missing_candidate_rejected(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p)
            with closing(sqlite3.connect(a[0])) as c:
                c.execute('DELETE FROM roles');c.commit()
            # Refresh declared DB fingerprints to isolate existence check.
            newhash=s.digest(a[0])
            for pos in (1,2,3,4):
                obj=s.read_json(a[pos])
                if pos==1:obj['database']['sha256']=newhash
                elif pos==2:obj['files']['sqlite_sha256']=newhash
                elif pos==3:obj['inputs']['db_sha256']=newhash
                else:obj['database_sha256']=newhash
                write_json(a[pos],obj)
            with self.assertRaisesRegex(ValueError,'Missing database candidate'):s.checks(*a)
    def test_read_only_database_query(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p)
            before=s.digest(a[0]);s.checks(*a)
            self.assertEqual(before,s.digest(a[0]))
    def test_truncated_requirement_cap(self):
        x,m=s.extract_requirements('Requirements:\n'+'\n'.join('- Item '+str(i)+' Python' for i in range(60))+'\nAbout OpenAI')
        self.assertTrue(m['truncated']);self.assertEqual(len(x),45)
    def test_main_success(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p)
            argv=[]
            for name,path in zip(('db','store-report','validation-report','broad-report','candidates','evidence'),a):
                argv.extend(('--'+name,str(path)))
            argv+=['--output-dir',str(p/'done')]
            self.assertEqual(s.main(argv),0)
    def test_main_input_failure(self):
        with tempfile.TemporaryDirectory(prefix='stage6-test-') as tmp:
            p=Path(tmp);a=synthetic_bundle(p);a[5].unlink()
            argv=[]
            for name,path in zip(('db','store-report','validation-report','broad-report','candidates','evidence'),a):
                argv.extend(('--'+name,str(path)))
            argv+=['--output-dir',str(p/'done')]
            self.assertEqual(s.main(argv),1)
            self.assertFalse((p/'done').exists())


def run_tests(output:Path):
    if output.exists():raise ValueError('Test report directory already exists; choose a new name')
    stream=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Stage6Tests)
    runner=unittest.TextTestRunner(stream=stream,verbosity=2)
    result=runner.run(suite)
    transcript=stream.getvalue()
    print(transcript,end='')
    total=result.testsRun; passed=total-len(result.failures)-len(result.errors)-len(result.skipped)
    items=[{'name':test.id().split('.')[-1],'status':'FAIL'} for test,msg in result.failures]
    items += [{'name':test.id().split('.')[-1],'status':'ERROR'} for test,msg in result.errors]
    items += [{'name':test.id().split('.')[-1],'status':'SKIP'} for test,msg in result.skipped]
    statuses={x['name']:x['status'] for x in items}
    cases=[{'name':name[5:],'status':statuses.get(name[5:],'PASS')} for name in sorted(x for x in dir(Stage6Tests) if x.startswith('test_'))]
    report={'stage':'deep_analysis_tests','status':'PASS' if result.wasSuccessful() else 'FAIL','program_version':s.VERSION,
            'generated_utc':datetime.now(timezone.utc).isoformat(),'tests_run':total,'passed':passed,
            'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'cases':cases}
    txt=json.dumps(report,indent=2)+'\n'
    md=f"# ProofLoop Stage 6 — Test Report\n\n**{report['status']}**: {passed}/{total} passed ({len(result.failures)} failures, {len(result.errors)} errors)\n\n"+''.join(f"- {r['status']}: `{r['name']}`\n" for r in cases)
    output.mkdir(parents=True,exist_ok=False)
    (output/'test_report.json').write_text(txt,encoding='utf-8')
    (output/'test_report.md').write_text(md,encoding='utf-8')
    print('Test reports: '+str(output))
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report-dir',type=Path,required=True)
    args=ap.parse_args()
    try:sys.exit(run_tests(args.report_dir))
    except (ValueError,OSError) as exc:print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
