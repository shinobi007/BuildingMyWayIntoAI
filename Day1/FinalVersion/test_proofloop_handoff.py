#!/usr/bin/env python3
"""Offline Stage 8 regression suite. Tiny synthetic corpus; no network, no real resume data."""
from __future__ import annotations
import argparse, contextlib, copy, hashlib, json, os, sqlite3, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path
import proofloop_handoff as P

HERE=Path(__file__).parent

def put(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def fixture(folder:Path):
    folder.mkdir(parents=True,exist_ok=True)
    paths={k:folder/(k+'.json' if k in P.JSON_KEYS else k+'.md' if k.endswith('_md') else k+'.sqlite3') for k in P.INPUT_KEYS}
    jobs=[{'id':'job-a','title':' Support Engineer ','descriptionPlain':'Technical support for Python APIs, working on real systems.\nYou might thrive if you have:\n- Skills in troubleshooting systems.',
           'descriptionHtml':'<p>Technical support</p>','jobUrl':'https://jobs.ashbyhq.com/openai/job-a','applyUrl':'https://jobs.ashbyhq.com/openai/job-a/application'},
          {'id':'job-b','title':'Software Engineer','descriptionPlain':'Full-stack systems.','descriptionHtml':'<p>Full-stack systems.</p>',
           'jobUrl':'https://jobs.ashbyhq.com/openai/job-b','applyUrl':'https://jobs.ashbyhq.com/openai/job-b/application'}]
    put(paths['snapshot'],{'jobs':jobs,'apiVersion':'1'})
    with contextlib.closing(sqlite3.connect(paths['db'])) as db:
        db.execute('CREATE TABLE roles(id TEXT PRIMARY KEY,board TEXT,source_index INTEGER,source_sha256 TEXT,title TEXT,job_url TEXT,apply_url TEXT,description_plain TEXT,description_html TEXT,raw_json TEXT,canonical_json TEXT,provenance_json TEXT)')
        for i,job in enumerate(jobs,1):
            db.execute('INSERT INTO roles VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(
                job['id'],'openai',i,P.digest(paths['snapshot']),job['title'].strip(),job['jobUrl'],job['applyUrl'],job['descriptionPlain'],job['descriptionHtml'],
                json.dumps(job),json.dumps({'title':job['title'].strip()}),json.dumps({'source_index':i})))
        db.commit()
    put(paths['store'],{'stage':'store','status':'PASS','board':'openai','input':{'source_sha256':P.digest(paths['snapshot']),'records':2},'database':{'sha256':P.digest(paths['db'])}})
    put(paths['validation'],{'stage':'independent_validation','status':'PASS','failed':0,
                             'files':{'sqlite_sha256':P.digest(paths['db']),'snapshot_sha256':P.digest(paths['snapshot'])},
                             'checks':{f'check_{i}':True for i in range(24)}})
    br=[{'id':job['id'],'title':job['title'].strip(),'source_index':i,'job_url':job['jobUrl'],'band':'DEEP_REVIEW_PRIORITY' if i==1 else 'HOLD_WITH_REASONS'} for i,job in enumerate(jobs,1)]
    put(paths['broad'],{'stage':'broad_analysis','status':'PASS','board':'openai','inputs':{'db_sha256':P.digest(paths['db']),'source_snapshot_sha256':P.digest(paths['snapshot'])},
                        'counts':{'total':2},'roles':br,'deep_review_pool':[{'id':'job-a','title':'Support Engineer'}]})
    put(paths['candidates'],{'database_sha256':P.digest(paths['db']),'candidate_ids':['job-a'],'candidates':[{'id':'job-a','title':'Support Engineer'}]})
    put(paths['evidence'],{'status':'UNVERIFIED_RESUME_CLAIMS','source_description':'From resume: work experience and skills; contact test.person@example.com',
         'evidence':[{'id':'PRIVATE_DEMO','kind':'DATED_WORK_HISTORY','dates':'2020-01 to 2024-01',
                      'summary':'Customer support test.person@example.com, (801) 555-1234',
                      'topics':['technical_support','python'], 'secret':'DO_NOT_COPY'}]})
    deep_in={'db_sha256':P.digest(paths['db']),'store_report_sha256':P.digest(paths['store']),
             'validation_report_sha256':P.digest(paths['validation']),'broad_report_sha256':P.digest(paths['broad']),
             'candidate_pool_sha256':P.digest(paths['candidates']),'private_evidence_sha256':P.digest(paths['evidence']),
             'source_snapshot_sha256':P.digest(paths['snapshot'])}
    d={'id':'job-a','title':'Support Engineer','source_index':1,'requirements':[{'source_text':'Experience with Python'}]}
    put(paths['deep'],{'stage':'deep_analysis','status':'PASS','board':'openai','inputs':deep_in,
                       'profile':{'status':'UNVERIFIED_RESUME_CLAIMS'},'counts':{'reviewed':1,'extracted_requirements':1},'dossiers':[d]})
    put(paths['deep_summary'],{'stage':'deep_review_summary','status':'PASS','board':'openai',
                               'inputs':deep_in,'counts':{'reviewed':1,'extracted_requirements':1},
                               'review_queue':[{'id':'job-a'}]})
    adv_in={'db_sha256':P.digest(paths['db']),'store_sha256':P.digest(paths['store']),
            'validation_sha256':P.digest(paths['validation']),'broad_sha256':P.digest(paths['broad']),
            'candidates_sha256':P.digest(paths['candidates']),'deep_sha256':P.digest(paths['deep']),
            'deep_summary_sha256':P.digest(paths['deep_summary']),'evidence_sha256':P.digest(paths['evidence']),
            'source_snapshot_sha256':P.digest(paths['snapshot'])}
    aa={'id':'job-a','title':'Support Engineer','source_index':1,'stage6_requirement_count':1,
        'stage7_review_requirement_count':1,'comparison_group':'EVIDENCE_REVIEW_WITH_UNRESOLVED_GAPS',
        'geography':{'policy':'REVIEW_ELIGIBILITY'},'expectations':[{'source_text':'Experience with Python'}]}
    put(paths['advanced'],{'stage':'advanced_comparative_analysis','status':'PASS','board':'openai','inputs':adv_in,
                            'counts':{'corpus_roles':2,'stage6_dossiers':1,'rescue_review_candidates':1,
                                      'stage7_review_lines':1,'supplement_recovered_roles':0,
                                      'embedded_heading_issues':0,'still_missing_sections':0,'comparison_cautions':{}},
                            'dossiers':[aa]})
    cover=[{'id':'job-a','title':'Support Engineer','source_index':1,'stage5_band':'DEEP_REVIEW_PRIORITY',
            'in_stage6_pool':True,'blind_spot_revisit':False},
           {'id':'job-b','title':'Software Engineer','source_index':2,'stage5_band':'HOLD_WITH_REASONS',
            'in_stage6_pool':False,'blind_spot_revisit':True}]
    put(paths['coverage'],{'stage':'coverage_audit','status':'PASS','inputs':adv_in,'counts':{'all_roles':2,'outside_deep_pool':1,'actionable_revisit':1},
                           'all_roles':cover,'revisit_outside_pool':[{'id':'job-b','title':'Software Engineer'}]})
    put(paths['comparison'],{'stage':'comparative_matrix','status':'PASS','population':1,'inputs':adv_in,
                             'entries':[{'id':'job-a','title':'Support Engineer','requirements':1,
                                         'group':'EVIDENCE_REVIEW_WITH_UNRESOLVED_GAPS','geography':'REVIEW_ELIGIBILITY'}]})
    for k in ['broad_md','deep_md','advanced_md']:
        paths[k].write_text('# Tiny synthetic report '+k+'\n',encoding='utf-8')
    stage7_sha={'advanced_analysis_report.json':P.digest(paths['advanced']),
                'coverage_audit.json':P.digest(paths['coverage']),
                'comparison_matrix.json':P.digest(paths['comparison']),
                'advanced_analysis_report.md':P.digest(paths['advanced_md'])}
    put(paths['stage7_manifest'],{'stage':'stage7_pre_ai_manifest','status':'PASS','board':'openai',
                                  'private_evidence_status':'UNVERIFIED_RESUME_CLAIMS',
                                  'no_ai_selection_yet':True,'ai_may_disagree_with_all_heuristic_groups':True,
                                  'stage7_outputs_sha256':stage7_sha})
    return paths

class Stage8Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='proofloop-stage8-tests-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.paths=fixture(self.root/'inputs')

    def data(self,key):return P.load_json(self.paths[key])
    def edit(self,key,fn):
        obj=self.data(key);fn(obj);put(self.paths[key],obj)
    def refuse(self,needle=None):
        with self.assertRaises((ValueError,OSError,KeyError,TypeError,sqlite3.Error)) as cm:P.check_inputs(self.paths)
        if needle:self.assertIn(needle,str(cm.exception))
    def compiled(self):
        meta=P.check_inputs(self.paths);src=P.read_source(self.paths,meta);return meta,src

    def test_baseline_cross_stage_consistent(self):
        m=P.check_inputs(self.paths);self.assertEqual(len(m['roles']),2)
    def test_original_source_description_and_raw_preserved(self):
        m,s=self.compiled();self.assertEqual(s[0]['original_raw_job']['descriptionPlain'],self.data('snapshot')['jobs'][0]['descriptionPlain'])
    def test_original_title_whitespace_not_lost(self):
        m,s=self.compiled();self.assertEqual(s[0]['original_raw_job']['title'],' Support Engineer ')
    def test_data_traces_not_certificate(self):
        m,s=self.compiled();a=P.audit(m,s);self.assertFalse(a['constraints']['qualifications_certified'])
    def test_missing_private_evidence_keeps_output_absent(self):
        self.paths['evidence'].unlink()
        with self.assertRaises(ValueError):P.run(self.paths,self.root/'absent')
        self.assertFalse((self.root/'absent').exists())
    def test_broken_json_refused(self):
        self.paths['coverage'].write_text('{bad',encoding='utf-8')
        with self.assertRaises(json.JSONDecodeError):P.check_inputs(self.paths)
    def test_json_array_refused(self):
        self.paths['deep'].write_text('[]',encoding='utf-8');self.refuse('Expected JSON object')
    def test_store_failed_status_refused(self):self.edit('store',lambda x:x.update(status='FAIL'));self.refuse('not PASS')
    def test_validation_incomplete_checks_refused(self):self.edit('validation',lambda x:x['checks'].pop('check_1'));self.refuse('incomplete')
    def test_validation_failed_check_refused(self):self.edit('validation',lambda x:x['checks'].update(check_0=False));self.refuse('incomplete')
    def test_forged_store_hash_refused(self):self.edit('store',lambda x:x['database'].update(sha256='0'*64));self.refuse('Fingerprint mismatch')
    def test_wrong_snapshot_hash_refused(self):self.edit('store',lambda x:x['input'].update(source_sha256='x'));self.refuse('Fingerprint mismatch')
    def test_tampered_broad_report_refused(self):self.edit('broad',lambda x:x['roles'][0].update(title='Fake'));self.refuse('Fingerprint mismatch')
    def test_tampered_deep_report_refused(self):self.edit('deep',lambda x:x.update(version='tampered'));self.refuse('Fingerprint mismatch')
    def test_tampered_advanced_report_refused(self):self.edit('advanced',lambda x:x['counts'].update(corpus_roles=5));self.refuse('Fingerprint mismatch')
    def test_tampered_coverage_refused(self):self.edit('coverage',lambda x:x.update(note='changed'));self.refuse('Fingerprint mismatch')
    def test_tampered_matrix_refused(self):self.edit('comparison',lambda x:x.update(note='changed'));self.refuse('Fingerprint mismatch')
    def test_tampered_advanced_md_refused(self):
        self.paths['advanced_md'].write_text('bad',encoding='utf-8');self.refuse('Fingerprint mismatch')
    def test_missing_stage7_manifest_hash_refused(self):self.edit('stage7_manifest',lambda x:x['stage7_outputs_sha256'].pop('comparison_matrix.json'));self.refuse('Fingerprint mismatch')
    def test_unverified_status_cannot_change(self):self.edit('stage7_manifest',lambda x:x.update(private_evidence_status='VERIFIED'));self.refuse('unverified')
    def test_stage7_cannot_assert_top_five(self):self.edit('stage7_manifest',lambda x:x.update(no_ai_selection_yet=False));self.refuse('restrictions')
    def test_duplicate_stage5_role_detected(self):
        m=P.check_inputs(self.paths);m['data']['broad']['roles'].append(copy.deepcopy(m['data']['broad']['roles'][0]))
        with self.assertRaises(ValueError):P.indexed(m['data']['broad']['roles'],'role')
    def test_duplicate_coverage_detected(self):
        m=P.check_inputs(self.paths);m['data']['coverage']['all_roles'].append(copy.deepcopy(m['data']['coverage']['all_roles'][0]))
        with self.assertRaises(ValueError):P.indexed(m['data']['coverage']['all_roles'],'coverage')
    def test_source_snapshot_duplicate_job_rejected(self):
        m=P.check_inputs(self.paths);m['data']['snapshot']['jobs'][1]['id']='job-a'
        with self.assertRaises(ValueError):P.read_source(self.paths,m)
    def test_raw_db_record_tamper_detected(self):
        m=P.check_inputs(self.paths)
        with contextlib.closing(sqlite3.connect(self.paths['db'])) as db:
            db.execute("UPDATE roles SET raw_json='{}' WHERE id='job-a'");db.commit()
        with self.assertRaisesRegex(ValueError,'raw fields diverge'):P.read_source(self.paths,m)
    def test_database_description_tamper_detected(self):
        m=P.check_inputs(self.paths)
        with contextlib.closing(sqlite3.connect(self.paths['db'])) as db:
            db.execute("UPDATE roles SET description_plain='oops' WHERE id='job-a'");db.commit()
        with self.assertRaisesRegex(ValueError,'description differs'):P.read_source(self.paths,m)
    def test_database_connection_closed_on_success(self):
        self.compiled(); new=self.paths['db'].with_suffix('.bak');os.rename(self.paths['db'],new);os.rename(new,self.paths['db'])
    def test_database_connection_closed_on_query_error(self):
        m=P.check_inputs(self.paths)
        with contextlib.closing(sqlite3.connect(self.paths['db'])) as db:
            db.execute('DROP TABLE roles');db.commit()
        with self.assertRaises(sqlite3.Error):P.read_source(self.paths,m)
        new=self.paths['db'].with_suffix('.bak');os.rename(self.paths['db'],new);os.rename(new,self.paths['db'])
    def test_run_publishes_full_archive_and_stage_reports(self):
        out=self.root/'stage8_live';a=P.run(self.paths,out)
        self.assertEqual(a['counts']['source_postings'],2)
        self.assertTrue((out/'ai_handoff_bundle.zip').is_file())
        self.assertTrue((out/'stage8_audit_report.md').is_file())
    def test_zip_integrity_and_file_hashes(self):
        out=self.root/'stage8_zip';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            self.assertIsNone(z.testzip());man=json.loads(z.read('handoff_manifest.json'))
            for name,info in man['files'].items():
                self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(),info['sha256'])
    def test_handoff_includes_every_report_stage_5_to_8(self):
        out=self.root/'stage8_reports';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            for name in list(P.REPORTS.values())+['stage8/stage8_audit_report.json']:
                self.assertIn('reports/'+name,z.namelist())
    def test_full_original_description_in_source_jsonl(self):
        out=self.root/'stage8_source';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            lines=z.read('source/all_816_source_roles.jsonl').decode().splitlines()
        self.assertEqual(len(lines),2);self.assertEqual(json.loads(lines[0])['original_raw_job']['title'],' Support Engineer ')
    def test_candidate_profile_present_with_all_structured_evidence(self):
        out=self.root/'stage8_profile';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            profile=json.loads(z.read('candidate/candidate_evidence_public.json'))
            self.assertEqual(profile['status'],'UNVERIFIED_RESUME_CLAIMS')
            self.assertEqual(len(profile['evidence']),1)
            self.assertEqual(profile['evidence'][0]['dates'],'2020-01 to 2024-01')
            self.assertEqual(profile['evidence'][0]['topics'],['technical_support','python'])
            self.assertEqual(profile['provenance']['source_file_sha256'],P.digest(self.paths['evidence']))
            man=json.loads(z.read('handoff_manifest.json'))
            self.assertTrue(man['candidate_evidence_included'])
            self.assertTrue(man['contact_sanitized'])
    def test_no_contact_info_or_extra_secret_in_handoff(self):
        out=self.root/'stage8_contacts';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            data=z.read('candidate/candidate_evidence_public.json').decode()
            self.assertNotIn('test.person@example.com',data)
            self.assertNotIn('(801) 555-1234',data)
            self.assertNotIn('DO_NOT_COPY',data)
            self.assertIn('[CONTACT_REMOVED]',data)
            profile=json.loads(data)
            self.assertEqual(profile['provenance']['unknown_fields_excluded'],1)
            self.assertGreaterEqual(profile['provenance']['contact_matches_redacted'],2)
    def test_additive_proofloop_update_does_not_claim_proficiency(self):
        out=self.root/'stage8_project';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            update=json.loads(z.read('candidate/PROJECT_PROOFLOOP_UPDATE.json'))
        self.assertEqual(update['updated_project_evidence_id'],'PROJECT_PROOFLOOP_STAGES1TO8')
        self.assertEqual(update['kind'],'CURRENT_PROJECT_ARTIFACT')
        self.assertIn('no claim of sole authorship',update['limitations'][0])
        self.assertEqual(update['source_jobs'],2)
    def test_direct_contact_and_social_links_redacted(self):
        profile={'status':'UNVERIFIED_RESUME_CLAIMS', 'source_description':'User linkedin.com/in/sample-123',
                 'evidence':[{'id':'WORK1','kind':'DATED_WORK_HISTORY',
                              'summary':'Email a@example.com; call 435-555-1212; https://github.com/example',
                              'topics':['python']}]}
        public,meta=P.public_candidate_evidence(profile,'hash')
        data=json.dumps(public)
        for snippet in ['a@example.com','435-555-1212','github.com/example','linkedin.com/in/sample-123']:
            self.assertNotIn(snippet,data)
        self.assertEqual(meta['source_record_count'],1)
    def test_duplicate_evidence_id_rejected(self):
        profile={'status':'UNVERIFIED_RESUME_CLAIMS','evidence':[{'id':'dup'},{'id':'dup'}]}
        with self.assertRaisesRegex(ValueError,'Duplicate'):P.public_candidate_evidence(profile,'hash')
    def test_candidate_evidence_not_reinterpreted_as_verified(self):
        profile={'status':'VERIFIED','evidence':[{'id':'a'}]}
        with self.assertRaisesRegex(ValueError,'unverified'):P.public_candidate_evidence(profile,'hash')
    def test_optional_resume_source_included_with_provenance(self):
        resume=self.root/'resume.md'
        resume.write_text('Work: supported SaaS systems\nEmail demo@example.com\n',encoding='utf-8')
        out=self.root/'stage8_resume';P.run(self.paths,out,resume)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            text=z.read('candidate/resume_professional_claims.md').decode()
            self.assertIn('supported SaaS systems',text)
            self.assertNotIn('demo@example.com',text)
            man=json.loads(z.read('handoff_manifest.json'))
            self.assertTrue(man['redacted_resume_claims_included'])
            self.assertEqual(man['resume_source_sha256'],P.digest(resume))
            self.assertIn('candidate/resume_professional_claims.md',man['files'])
    def test_resume_without_argument_not_included(self):
        out=self.root/'stage8_no_resume';P.run(self.paths,out)
        with zipfile.ZipFile(out/'ai_handoff_bundle.zip') as z:
            self.assertNotIn('candidate/resume_professional_claims.md',z.namelist())
            man=json.loads(z.read('handoff_manifest.json'))
            self.assertFalse(man['redacted_resume_claims_included'])
    def test_output_no_overwrite(self):
        out=self.root/'used';P.run(self.paths,out)
        with self.assertRaisesRegex(ValueError,'already exists'):P.run(self.paths,out)
    def test_audit_raises_nonblocking_review_flags(self):
        m,s=self.compiled();a=P.audit(m,s);self.assertGreater(len(a['review_flags']),0);self.assertTrue(a['integrity_checks']['cross_stage_population'])
    def test_no_final_five_in_manifest(self):
        out=self.root/'manifest';P.run(self.paths,out);self.assertTrue(json.loads((out/'stage8_handoff_manifest.json').read_text())['no_final_five'])
    def test_cli_success(self):
        out=self.root/'cli';args=[sys.executable,str(HERE/'proofloop_handoff.py')]
        for k,v in self.paths.items():args.extend(['--'+k.replace('_','-'),str(v)])
        result=subprocess.run(args+['--output-dir',str(out)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('PASS: Stage 8',result.stdout)
    def test_cli_missing_input_failure(self):
        out=self.root/'fail';args=[sys.executable,str(HERE/'proofloop_handoff.py')]
        for k,v in self.paths.items():args.extend(['--'+k.replace('_','-'),str(v if k!='snapshot' else self.root/'absent.json')])
        result=subprocess.run(args+['--output-dir',str(out)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertIn('FAIL:',result.stderr);self.assertFalse(out.exists())
    def test_original_inputs_not_modified(self):
        before={k:P.digest(v) for k,v in self.paths.items()};P.run(self.paths,self.root/'no_modify')
        self.assertEqual(before,{k:P.digest(v) for k,v in self.paths.items()})
    def test_partial_failure_no_output_published(self):
        self.paths['snapshot'].write_text('{}',encoding='utf-8')
        with self.assertRaises(ValueError):P.run(self.paths,self.root/'never_publish')
        self.assertFalse((self.root/'never_publish').exists())


def main():
    p=argparse.ArgumentParser();p.add_argument('--report-dir',type=Path,required=True);args=p.parse_args()
    if args.report_dir.exists():raise SystemExit('FAIL: report directory exists (no overwrite)')
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Stage8Tests)
    class Recording(unittest.TextTestResult):
        def __init__(self,*a,**kw):super().__init__(*a,**kw);self.cases=[]
        def addSuccess(self,test):super().addSuccess(test);self.cases.append({'test':test._testMethodName,'status':'PASS'})
        def addError(self,test,err):super().addError(test,err);self.cases.append({'test':test._testMethodName,'status':'ERROR'})
        def addFailure(self,test,err):super().addFailure(test,err);self.cases.append({'test':test._testMethodName,'status':'FAIL'})
    runner=unittest.TextTestRunner(verbosity=2,resultclass=Recording)
    result=runner.run(suite)
    args.report_dir.mkdir(parents=True)
    report={'stage':'stage8_handoff_tests','program_version':P.VERSION,'status':'PASS' if result.wasSuccessful() else 'FAIL',
            'tests_run':result.testsRun,'passed':sum(x['status']=='PASS' for x in result.cases),
            'errors':len(result.errors),'failures':len(result.failures),'skipped':len(result.skipped),'cases':result.cases}
    P.put_json(args.report_dir/'test_report.json',report)
    (args.report_dir/'test_report.md').write_text('# Stage 8 — Regression Tests\n\n**'+report['status']+'** — '+str(report['passed'])+'/'+str(report['tests_run'])+' passed; '+str(report['errors'])+' errors.\n\n'+'\n'.join('- '+x['status']+': `'+x['test']+'`' for x in result.cases)+'\n',encoding='utf-8')
    print('Test reports: '+str(args.report_dir))
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
