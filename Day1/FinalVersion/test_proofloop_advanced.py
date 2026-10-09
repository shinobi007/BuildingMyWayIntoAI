#!/usr/bin/env python3
"""Stage 7 offline regression suite: synthetic fixtures, mutation tests and Windows safety."""
from __future__ import annotations
import argparse
import copy
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import proofloop_advanced as adv

BASE = 'https://jobs.ashbyhq.com/openai/'

def put(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def fixture(root:Path):
    paths={name:root/(name+'.json') for name in ('store','validation','broad','candidates','deep','deep_summary','evidence')}
    paths['db']=root/'jobs.sqlite3'
    c=sqlite3.connect(paths['db'])
    try:
        c.execute('CREATE TABLE roles (id TEXT PRIMARY KEY,board TEXT,title TEXT,source_index INTEGER,source_sha256 TEXT,description_plain TEXT,job_url TEXT,apply_url TEXT,published_at TEXT)')
        roles=[('a1','Software Engineer, Integrations',1,
                "You will thrive in this role if you have:\n- 8+ years of production Python experience; building distributed systems.\n- Bachelor's degree or equivalent.\nAbout OpenAI\nNo headings here."),
               ('b2','Technical Program Manager, Support Delivery',2,
                'You May Be A Strong Fit If You:\n- Troubleshoot service desk workflows.\n- Experience with Jira.\nAbout OpenAI'),
               ('c3','Account Executive',3,"Your background might look something like:\n- Lead quota-driven sales.\nAbout OpenAI")]
        for ident,title,ordinal,body in roles:
            c.execute('INSERT INTO roles VALUES (?,?,?,?,?,?,?,?,?)',(ident,'openai',title,ordinal,'snapshotsha',body,BASE+ident,BASE+ident+'/application','2026-10-09'))
        c.commit()
    finally:c.close()
    dbsha=adv.file_hash(paths['db'])
    store={'stage':'store','status':'PASS','board':'openai','input':{'source_sha256':'snapshotsha','records':3},'database':{'sha256':dbsha}}
    validation={'stage':'independent_validation','status':'PASS','failed':0,'files':{'sqlite_sha256':dbsha}}
    loc={'category':'US_REMOTE_ADVERTISED','policy':'REVIEW_ELIGIBILITY','primary_location':'US - Remote','remote_metadata_conflict':False,'relocation_evidence':[]}
    tech={'classification':'HANDS_ON_EVIDENCE'}; sales={'classification':'NO_STRONG_SALES_EVIDENCE'}
    def broad_role(ident,title,ordinal,band,te,sal):
        return {'id':ident,'title':title,'source_index':ordinal,'job_url':BASE+ident,'apply_url':BASE+ident+'/application',
                'band':band,'blockers':[],'location':loc,'sales':{'classification':sal},
                'technical':{'classification':te},'seniority_title_signal':'UNSPECIFIED_OR_OTHER'}
    r1=broad_role('a1',roles[0][1],1,'DEEP_REVIEW_PRIORITY','HANDS_ON_EVIDENCE','NO_STRONG_SALES_EVIDENCE')
    r2=broad_role('b2',roles[1][1],2,'HOLD_WITH_REASONS','TECHNICAL_CORE_UNCONFIRMED','NO_STRONG_SALES_EVIDENCE')
    r3=broad_role('c3',roles[2][1],3,'HOLD_WITH_REASONS','TECHNICAL_CORE_UNCONFIRMED','SALES_PRIMARY_EVIDENCE')
    pool_entry={'id':'a1','title':roles[0][1],'source_index':1,'job_url':BASE+'a1', 'band':'DEEP_REVIEW_PRIORITY'}
    broad={'stage':'broad_analysis','status':'PASS','board':'openai','inputs':{'db_sha256':dbsha,'source_snapshot_sha256':'snapshotsha'},
           'roles':[r1,r2,r3],'deep_review_pool':[pool_entry]}
    candidates={'board':'openai','database_sha256':dbsha,'candidate_ids':['a1'],'candidates':[pool_entry]}
    evidence={'schema_version':1,'status':'UNVERIFIED_RESUME_CLAIMS','evidence':[
        {'id':'WORK1','kind':'DATED_WORK_HISTORY','dates':'2020 to 2022','topics':['python'],'summary':'unverified'},
        {'id':'PROOF','kind':'CURRENT_PROJECT_ARTIFACT','topics':['python'],'summary':'AI-assisted project'}]}
    for k,obj in [('store',store),('validation',validation),('broad',broad),('candidates',candidates),('evidence',evidence)]: put(paths[k],obj)
    reqs=[{'id':'R001','source_text':'8+ years of production Python experience; building distributed systems.',
           'section_heading':'You will thrive in this role if you have:',
           'requirement_context':'EXPECTATION_CONTEXT','topic_signals':['python'],
           'topic_overlap_evidence':[{'id':'WORK1','kind':'DATED_WORK_HISTORY','shared_topics':['python']}]},
          {'id':'R002','source_text':"Bachelor's degree or equivalent.",
           'section_heading':'You will thrive in this role if you have:',
           'requirement_context':'EXPECTATION_CONTEXT','topic_signals':[],
           'topic_overlap_evidence':[]}]
    dossier={'id':'a1','title':roles[0][1],'source_index':1,'job_url':BASE+'a1',
            'published_at':'2026-10-09','requirements':reqs,'seniority_title_signal':'UNSPECIFIED_OR_OTHER',
            'location':loc,'sales':sales,'technical':tech}
    inputs={'db_sha256':dbsha,'source_snapshot_sha256':'snapshotsha',
        'store_report_sha256':adv.file_hash(paths['store']),
        'validation_report_sha256':adv.file_hash(paths['validation']),
        'broad_report_sha256':adv.file_hash(paths['broad']),
        'candidate_pool_sha256':adv.file_hash(paths['candidates']),
        'private_evidence_sha256':adv.file_hash(paths['evidence'])}
    deep={'stage':'deep_analysis','status':'PASS','board':'openai','inputs':inputs,
          'counts':{'extracted_requirements':2,'reviewed':1},'dossiers':[dossier]}
    summary={'stage':'deep_review_summary','status':'PASS','board':'openai','inputs':inputs,
           'counts':deep['counts'],'review_queue':[{'id':'a1','title':roles[0][1]}]}
    put(paths['deep'],deep);put(paths['deep_summary'],summary)
    return paths


class Stage7Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='proofloop-stage7-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.paths=fixture(self.root)

    def edit(self,key,edit):
        obj=adv.read_json(self.paths[key]);edit(obj);put(self.paths[key],obj)

    def run_report(self):return adv.build(self.paths)

    def test_baseline(self):
        report,coverage,matrix,manifest,_=self.run_report()
        self.assertEqual(report['counts']['corpus_roles'],3)
        self.assertEqual(report['counts']['stage6_dossiers'],1)
        self.assertEqual(coverage['counts']['outside_deep_pool'],2)
        self.assertEqual(len(matrix['entries']),1)
        self.assertTrue(manifest['no_ai_selection_yet'])

    def test_all_816_analogue_audited(self):
        _,coverage,_,_,_=self.run_report();self.assertEqual(len(coverage['all_roles']),3)
        self.assertEqual({x['id'] for x in coverage['all_roles']},{'a1','b2','c3'})

    def test_missed_support_role_recovered_to_revisit(self):
        _,coverage,_,_,_=self.run_report()
        self.assertIn('b2',[r['id'] for r in coverage['revisit_outside_pool']])

    def test_sales_primary_not_rescued(self):
        _,coverage,_,_,_=self.run_report()
        self.assertNotIn('c3',[r['id'] for r in coverage['revisit_outside_pool']])

    def test_previously_missed_headings(self):
        samples=['You May Be A Strong Fit If You','Your background might look something like:',
                 'You Might Thrive Here If You','You might thrive int his role if you:',
                 'You’ll thrive in this role if you:','Preferred Skills']
        for x in samples:
            with self.subTest(x=x):
                rows,method=adv.supplementary_extract(x+'\n- A valid example.\nAbout OpenAI\n- excluded')
                self.assertEqual(len(rows),1)
                self.assertEqual(method['status'],'SUPPLEMENT_FOUND')

    def test_boilerplate_not_extracted(self):
        req,method=adv.supplementary_extract('About OpenAI\nYou Might Thrive Here If You\n- invalid')
        self.assertFalse(req)

    def test_preference_preserved(self):
        req={'source_text':'Experience with Kubernetes is a plus','requirement_context':'PREFERRED_CONTEXT',
             'topic_signals':[],'topic_overlap_evidence':[]}
        self.assertEqual(adv.requirement_review(req,{})['requirement_strength'],'PREFERRED_OR_BONUS')

    def test_years_never_satisfied(self):
        report,*_=self.run_report()
        a=report['dossiers'][0]['expectations'][0]
        self.assertEqual(a['experience_year_numbers'],[8]);self.assertIn('EXPERIENCE_DURATION_NOT_VERIFIED',a['unresolved_obligations'])
        self.assertEqual(a['assessment'],'NOT_CERTIFIED_ONLY_TOPIC_ALIGNMENT')

    def test_degree_unverified(self):
        report,*_=self.run_report()
        self.assertIn('CREDENTIAL_OR_DEGREE_NOT_VERIFIED',report['dossiers'][0]['expectations'][1]['unresolved_obligations'])

    def test_security_clearance_flag(self):
        r=adv.requirement_review({'source_text':'Active security clearance required','topic_overlap_evidence':[]},{})
        self.assertIn('CITIZENSHIP_OR_CLEARANCE_REVIEW',r['unresolved_obligations'])

    def test_semicolon_compound_split_without_claims(self):
        rr=adv.requirement_review({'source_text':'Python; operating large-scale distributed systems', 'topic_overlap_evidence':[]},{})
        self.assertEqual(rr['segments'],['Python','operating large-scale distributed systems'])
        self.assertEqual(rr['assessment'],'NOT_CERTIFIED_ONLY_TOPIC_ALIGNMENT')

    def test_embedded_heading_detected_without_silent_change(self):
        original='Experience building API systems. Preferred Skills'
        x=adv.requirement_review({'source_text':original,'topic_overlap_evidence':[]},{})
        self.assertEqual(x['original_source_text'],original)
        self.assertIn('EMBEDDED_HEADING_REQUIRES_MANUAL_REVIEW',x['unresolved_obligations'])

    def test_current_project_not_work_history(self):
        r={'source_text':'Python', 'topic_overlap_evidence':[{'id':'PROOF'}]}
        profile={'PROOF':{'kind':'CURRENT_PROJECT_ARTIFACT'}}
        self.assertEqual(adv.requirement_review(r,profile)['evidence_relation'],'CURRENT_PROJECT_ONLY')

    def test_work_claim_does_not_prove_skill(self):
        r={'source_text':'Python', 'topic_overlap_evidence':[{'id':'WORK1'}]}
        profile={'WORK1':{'kind':'DATED_WORK_HISTORY'}}
        self.assertEqual(adv.requirement_review(r,profile)['assessment'],'NOT_CERTIFIED_ONLY_TOPIC_ALIGNMENT')

    def test_lack_of_extraction_is_not_zero_requirements(self):
        req,method=adv.make_requirements({'requirements':[]},'narrative paragraph',{})
        self.assertEqual(method['assessment'],'NO_SECTION_FOUND_MANUAL_REVIEW');self.assertFalse(req)

    def test_supplement_fills_missing_stage6(self):
        req,method=adv.make_requirements({'requirements':[]},'Your background might look something like:\n- 7+ years of API engineering.\nAbout OpenAI',{})
        self.assertTrue(method['supplement_used']);self.assertIn('EXPERIENCE_DURATION_NOT_VERIFIED',req[0]['unresolved_obligations'])

    def test_stage6_not_overwritten_by_supplement(self):
        req,method=adv.make_requirements({'requirements':[{'source_text':'Python','id':'R001','topic_overlap_evidence':[]}]},
                                          'You Might Thrive Here If You\n- Different req',{})
        self.assertFalse(method['supplement_used']);self.assertEqual(len(req),1)

    def test_no_unsupported_qualification_scoring(self):
        report,*_=self.run_report()
        self.assertNotIn('qualification_score',report['dossiers'][0])
        self.assertNotIn('final_top_five',report)

    def test_stage5_pool_tamper_rejected(self):
        self.edit('candidates',lambda x:x['candidate_ids'].append('b2'))
        with self.assertRaises(ValueError):self.run_report()

    def test_stage6_role_title_tamper_rejected(self):
        self.edit('deep',lambda x:x['dossiers'][0].update(title='Changed'))
        with self.assertRaises(ValueError):self.run_report()

    def test_stage6_count_tamper_rejected(self):
        self.edit('deep',lambda x:x['counts'].update(extracted_requirements=99))
        with self.assertRaises(ValueError):self.run_report()

    def test_stage6_summary_tamper_rejected(self):
        self.edit('deep_summary',lambda x:x['counts'].update(reviewed=222))
        with self.assertRaises(ValueError):self.run_report()

    def test_broad_report_modified_rejected(self):
        self.edit('broad',lambda x:x['roles'][0].update(title='Fake'))
        with self.assertRaises(ValueError):self.run_report()

    def test_bad_store_hash_rejected(self):
        self.edit('store',lambda x:x['database'].update(sha256='bad'))
        with self.assertRaises(ValueError):self.run_report()

    def test_bad_validation_report_rejected(self):
        self.edit('validation',lambda x:x.update(status='FAIL'))
        with self.assertRaises(ValueError):self.run_report()

    def test_evidence_changes_invalidate_report(self):
        self.edit('evidence',lambda x:x['evidence'][0]['topics'].append('rust'))
        with self.assertRaises(ValueError):self.run_report()

    def test_no_output_on_failed_validation(self):
        self.edit('validation',lambda x:x.update(status='FAIL'))
        p=self.root/'failed'
        with self.assertRaises(ValueError):adv.run(self.paths,p)
        self.assertFalse(p.exists())

    def test_missing_input_rejected(self):
        self.paths['deep_summary'].unlink()
        with self.assertRaises(ValueError):self.run_report()

    def test_corrupted_sqlite_hash_rejected(self):
        with self.paths['db'].open('ab') as f:f.write(b'dirty')
        with self.assertRaises(ValueError):self.run_report()

    def test_duplicate_broad_id_rejected(self):
        self.edit('broad',lambda x:x['roles'].append(copy.deepcopy(x['roles'][0])))
        with self.assertRaises(ValueError):self.run_report()

    def test_sqlite_connection_closed_on_success(self):
        self.run_report()
        # Real Windows also validates the cleanup via TemporaryDirectory. Specifically ensure
        # no handle remains by moving and unlinking the test database now.
        alternate=self.root/'renamed.sqlite3';self.paths['db'].rename(alternate);alternate.rename(self.paths['db'])

    def test_sqlite_connection_closed_on_error(self):
        self.edit('broad',lambda x:x['roles'][0].update(title='changed'))
        with self.assertRaises(ValueError):self.run_report()
        alternate=self.root/'renamed.sqlite3';self.paths['db'].rename(alternate);alternate.rename(self.paths['db'])

    def test_output_report_and_hash_manifest(self):
        path=self.root/'saved';result=adv.run(self.paths,path)
        manifest=adv.read_json(path/'stage7_pre_ai_manifest.json')
        for name,h in manifest['stage7_outputs_sha256'].items():
            self.assertEqual(adv.file_hash(path/name),h)
        self.assertEqual(adv.read_json(path/'advanced_analysis_report.json')['counts'],result['counts'])
        self.assertTrue((path/'advanced_analysis_report.md').is_file())

    def test_no_overwrite(self):
        path=self.root/'saved';adv.run(self.paths,path)
        with self.assertRaises(ValueError):adv.run(self.paths,path)

    def test_private_evidence_not_copied_to_report(self):
        adv.run(self.paths,self.root/'saved')
        text=(self.root/'saved'/'advanced_analysis_report.json').read_text(encoding='utf-8')
        self.assertNotIn('AI-assisted project',text)
        self.assertNotIn('private email',text)

    def test_markdown_untrusted_titles_escaped(self):
        self.assertIn('&lt;',adv.safe_md('<script>alert(1)</script>'))
        self.assertIn('\\|',adv.safe_md('x|y'))

    def test_us_remote_not_certified(self):
        report,*_=self.run_report()
        self.assertEqual(report['dossiers'][0]['geography']['remote_eligible_from_utah'],'UNCONFIRMED')

    def test_read_only_db(self):
        old=adv.file_hash(self.paths['db'])
        adv.run(self.paths,self.root/'saved')
        self.assertEqual(old,adv.file_hash(self.paths['db']))

    def test_cli_success(self):
        script=Path(adv.__file__)
        args=[sys.executable,str(script)]
        for k in ('db','store','validation','broad','candidates','deep','deep_summary','evidence'):
            args.extend(['--'+k.replace('_','-'),str(self.paths[k])])
        args.extend(['--output-dir',str(self.root/'cli')])
        p=subprocess.run(args,capture_output=True,text=True,timeout=12)
        self.assertEqual(p.returncode,0,msg=p.stderr)
        self.assertIn('PASS: Stage 7 audited 3 roles',p.stdout)

    def test_cli_failure_no_publication(self):
        script=Path(adv.__file__);p=subprocess.run([sys.executable,str(script),'--db',str(self.paths['db']),
             '--store',str(self.paths['store']),'--validation','does-not-exist.json',
             '--broad',str(self.paths['broad']),'--candidates',str(self.paths['candidates']),
             '--deep',str(self.paths['deep']),'--deep-summary',str(self.paths['deep_summary']),
             '--evidence',str(self.paths['evidence']),'--output-dir',str(self.root/'nope')],
             capture_output=True,text=True,timeout=12)
        self.assertNotEqual(p.returncode,0)
        self.assertFalse((self.root/'nope').exists())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report-dir',type=Path)
    args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Stage7Tests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    entries=[]
    for name in dir(Stage7Tests):
        if name.startswith('test_'):
            bad=any(x._testMethodName==name for x,_ in result.errors+result.failures)
            entries.append({'test':name,'status':'FAIL' if bad else 'PASS'})
    entries.sort(key=lambda x:x['test'])
    report={'stage':'advanced_analysis_tests','program_version':adv.VERSION,
        'generated_utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS' if result.wasSuccessful() else 'FAIL',
        'tests_run':result.testsRun,'passed':result.testsRun-len(result.errors)-len(result.failures)-len(result.skipped),
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'cases':entries}
    if args.report_dir:
        try:
            args.report_dir.mkdir(parents=True,exist_ok=False)
            put(args.report_dir/'test_report.json',report)
            lines=['# ProofLoop Stage 7 — Regression Tests','',
                f"**{report['status']}** — {report['passed']}/{report['tests_run']} passed; {report['errors']} errors; {report['failures']} failures.",'']
            lines.extend('- '+x['status']+': `'+x['test']+'`' for x in entries)
            (args.report_dir/'test_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
            print('Test reports: '+str(args.report_dir))
        except (ValueError,OSError) as e:
            print('Could not save test reports: '+str(e),file=sys.stderr)
            return 1
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':sys.exit(main())
