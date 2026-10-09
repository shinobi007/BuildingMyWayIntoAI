#!/usr/bin/env python3
"""ProofLoop Stage 8: independent pre-AI audit, immutable source-linked handoff.

Stdlib only. Reads inputs without mutating them. Exports public job/source text and
Stage 5-8 reports AND full contact-sanitized candidate qualification evidence.
The immutable source profile remains a separately fingerprinted input.
No AI decision, no eligibility certification, no publication to external systems.
"""
from __future__ import annotations
import argparse, contextlib, hashlib, html, json, os, re, shutil, sqlite3, sys, tempfile, zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VERSION='0.8.1'
MAX_JSON=100*1024*1024
MAX_DB=650*1024*1024
INPUT_KEYS=['snapshot','db','store','validation','broad','candidates','deep','deep_summary','advanced','coverage','comparison','stage7_manifest','evidence','broad_md','deep_md','advanced_md']
JSON_KEYS=set(INPUT_KEYS)-{'db','broad_md','deep_md','advanced_md'}
REPORTS={'broad':'stage5/broad_analysis_report.json','candidates':'stage5/deep_review_candidates.json',
         'broad_md':'stage5/broad_analysis_report.md','deep':'stage6/deep_analysis_report.json',
         'deep_summary':'stage6/deep_review_summary.json','deep_md':'stage6/deep_analysis_report.md',
         'advanced':'stage7/advanced_analysis_report.json','coverage':'stage7/coverage_audit.json',
         'comparison':'stage7/comparison_matrix.json','stage7_manifest':'stage7/stage7_pre_ai_manifest.json',
         'advanced_md':'stage7/advanced_analysis_report.md'}

def digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def load_json(path:Path)->dict:
    if not path.is_file() or path.stat().st_size>MAX_JSON:raise ValueError('Missing or oversized input: '+path.name)
    with path.open(encoding='utf-8-sig') as f:
        obj=json.load(f,parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Invalid JSON numeric constant')))
    if not isinstance(obj,dict):raise ValueError('Expected JSON object: '+path.name)
    return obj

def indexed(arr,key:str)->dict:
    if not isinstance(arr,list): raise ValueError(key+' is not a list')
    out={}
    for v in arr:
        if not isinstance(v,dict) or not isinstance(v.get('id'),str) or not v['id'] or v['id'] in out:
            raise ValueError('Duplicate or invalid IDs: '+key)
        out[v['id']]=v
    return out

def sha_equal(actual, expected, purpose):
    if actual!=expected: raise ValueError('Fingerprint mismatch: '+purpose)

def check_inputs(paths:dict)->dict:
    data={k:load_json(paths[k]) for k in JSON_KEYS}
    hashes={k:digest(p) for k,p in paths.items()}
    s,v,b,p,d,ds,a,c,m,man=(data[k] for k in ['store','validation','broad','candidates','deep','deep_summary','advanced','coverage','comparison','stage7_manifest'])
    dbsha=hashes['db'];srcsha=hashes['snapshot']
    if any(x.get('status')!='PASS' for x in [s,v,b,d,ds,a,c,m,man]):raise ValueError('An upstream report is not PASS')
    if any(x.get('board')!='openai' for x in [s,b,d,ds,a,man]):raise ValueError('Board inconsistency')
    sha_equal(dbsha,s['database']['sha256'],'store database')
    sha_equal(srcsha,s['input']['source_sha256'],'store original source')
    sha_equal(dbsha,v['files']['sqlite_sha256'],'independent validation database')
    sha_equal(srcsha,v['files']['snapshot_sha256'],'independent validation source')
    if v.get('failed') or len(v.get('checks',{}))!=24 or not all(v['checks'].values()):raise ValueError('Independent validation incomplete')
    upstream={'db':'db_sha256','store':'store_sha256','validation':'validation_sha256','broad':'broad_sha256',
              'candidates':'candidates_sha256','deep':'deep_sha256','deep_summary':'deep_summary_sha256',
              'evidence':'evidence_sha256','snapshot':'source_snapshot_sha256'}
    for key,field in upstream.items():sha_equal(hashes[key],a['inputs'].get(field),'Stage 7 '+key)
    for key,field in [('advanced','advanced_analysis_report.json'),('coverage','coverage_audit.json'),
                      ('comparison','comparison_matrix.json'),('advanced_md','advanced_analysis_report.md')]:
        sha_equal(hashes[key],man['stage7_outputs_sha256'].get(field),'Stage 7 manifest '+key)
    if man.get('no_ai_selection_yet') is not True or man.get('ai_may_disagree_with_all_heuristic_groups') is not True:
        raise ValueError('Stage 7 AI review restrictions absent')
    for key,field in [('store','store_report_sha256'),('validation','validation_report_sha256'),
                      ('broad','broad_report_sha256'),('candidates','candidate_pool_sha256'),('evidence','private_evidence_sha256')]:
        sha_equal(hashes[key],d['inputs'].get(field),'Stage 6 '+key)
    if d.get('profile',{}).get('status')!='UNVERIFIED_RESUME_CLAIMS' or man.get('private_evidence_status')!='UNVERIFIED_RESUME_CLAIMS':
        raise ValueError('Evidence must remain unverified')
    if ds.get('counts')!=d.get('counts') or ds.get('inputs')!=d.get('inputs'):raise ValueError('Stage 6 summary mismatch')
    if b['inputs']['db_sha256']!=dbsha or p['database_sha256']!=dbsha:raise ValueError('Stage 5 database mismatch')
    if b['inputs']['source_snapshot_sha256']!=srcsha or a['inputs']['source_snapshot_sha256']!=srcsha:
        raise ValueError('Snapshot report mismatch')
    if b.get('counts',{}).get('total')!=s['input']['records']: raise ValueError('Stage 5 record count mismatch')
    if len(p['candidate_ids'])!=len(p['candidates']):raise ValueError('Handoff size mismatch')
    if p['candidates']!=b['deep_review_pool'] or p['candidate_ids']!=[x['id'] for x in p['candidates']]:
        raise ValueError('Stage 5 review pool differs')
    roles=indexed(b['roles'],'stage5 roles');deep=indexed(d['dossiers'],'stage6 dossiers');adv=indexed(a['dossiers'],'stage7 dossiers')
    allcov=indexed(c['all_roles'],'coverage all roles'); revisit=indexed(c['revisit_outside_pool'],'revisit roles')
    matrix=indexed(m['entries'],'comparison matrix');queue=indexed(ds['review_queue'],'stage6 queue')
    if len(roles)!=s['input']['records'] or len(roles)>5000 or len(roles)<1:
        raise ValueError('Unexpected role count')
    if set(deep)!=set(adv) or set(deep)!=set(matrix) or set(deep)!=set(queue) or set(deep)!=set(p['candidate_ids']):
        raise ValueError('Stage 5-7 deep candidate identity disagreement')
    if set(roles)!=set(allcov) or (set(deep)&set(revisit)) or not set(revisit)<=set(roles):
        raise ValueError('Coverage or revisit population disagreement')
    if [x['id'] for x in d['dossiers']]!=p['candidate_ids']:raise ValueError('Stage 6 order mismatch')
    if [x['id'] for x in c['all_roles']]!=[x['id'] for x in b['roles']]:raise ValueError('All role order mismatch')
    if len(revisit)!=c['counts']['actionable_revisit'] or len(revisit)!=a['counts']['rescue_review_candidates']:
        raise ValueError('Revisit count mismatch')
    if len(deep)!=a['counts']['stage6_dossiers'] or len(deep)!=d['counts']['reviewed'] or len(matrix)!=m['population']:
        raise ValueError('Dossier count mismatch')
    if sum(len(x['requirements']) for x in d['dossiers'])!=d['counts']['extracted_requirements']:
        raise ValueError('Stage 6 requirement count mismatch')
    if sum(len(x['expectations']) for x in a['dossiers'])!=a['counts']['stage7_review_lines']:
        raise ValueError('Stage 7 requirement count mismatch')
    for ident,br in roles.items():
        co=allcov[ident]
        if (co['title'],co['source_index'],co['stage5_band'])!=(br['title'],br['source_index'],br['band']):
            raise ValueError('Coverage role identity/classification disagreement: '+ident)
        if co['in_stage6_pool']!=(ident in deep):raise ValueError('Coverage deep-membership mismatch: '+ident)
        if co['blind_spot_revisit']!=(ident in revisit):raise ValueError('Coverage revisit mismatch: '+ident)
    for ident,dd in deep.items():
        aa=adv[ident];mm=matrix[ident];bb=roles[ident]
        if (dd['title'],aa['title'],mm['title'],bb['title']) != (dd['title'],)*4:
            raise ValueError('Dossier title disagreement: '+ident)
        if dd['source_index']!=aa['source_index'] or dd['source_index']!=bb['source_index']:
            raise ValueError('Dossier source index disagreement: '+ident)
        if mm['requirements']!=aa['stage7_review_requirement_count'] or aa['stage6_requirement_count']!=len(dd['requirements']):
            raise ValueError('Requirement count disagreement: '+ident)
        if mm['group']!=aa['comparison_group'] or mm['geography']!=aa['geography']['policy']:
            raise ValueError('Comparison matrix mismatch: '+ident)
    if len(c['all_roles'])!=c['counts']['all_roles'] or len(roles)!=a['counts']['corpus_roles']:
        raise ValueError('Corpus counts disagreement')
    if len(roles)-len(deep)!=c['counts']['outside_deep_pool']:raise ValueError('Outside pool count mismatch')
    return {'data':data,'hashes':hashes,'roles':roles,'deep':deep,'advanced':adv,'coverage':allcov,'revisit':revisit}

def read_source(paths:dict, meta:dict)->list[dict]:
    snapshot=meta['data']['snapshot']
    raw=snapshot.get('jobs')
    if not isinstance(raw,list) or len(raw)!=len(meta['roles']):raise ValueError('Original snapshot count mismatch')
    ids=set();out=[]
    if paths['db'].stat().st_size>MAX_DB:raise ValueError('Oversized DB')
    with contextlib.closing(sqlite3.connect(paths['db'].resolve().as_uri()+'?mode=ro',uri=True)) as conn:
        conn.row_factory=sqlite3.Row; conn.execute('PRAGMA query_only=ON')
        if conn.execute('PRAGMA integrity_check').fetchone()[0]!='ok' or conn.execute('PRAGMA foreign_key_check').fetchall():
            raise ValueError('Database integrity/foreign keys failed')
        rows=conn.execute('SELECT id,board,source_index,source_sha256,title,job_url,apply_url,description_plain,description_html,raw_json,canonical_json,provenance_json FROM roles ORDER BY source_index').fetchall()
        if len(rows)!=len(raw):raise ValueError('DB role count mismatch')
        for ix,(original,r) in enumerate(zip(raw,rows),1):
            if r['id'] in ids:raise ValueError('Duplicate DB IDs')
            ids.add(r['id']); ident=r['id']
            role=meta['roles'].get(ident);coverage=meta['coverage'].get(ident)
            if not role or not coverage or r['source_index']!=ix or original.get('id')!=ident or r['title']!=(original.get('title') or '').strip():
                raise ValueError('DB-to-original positional identity disagreement at '+str(ix))
            if r['source_sha256']!=meta['hashes']['snapshot'] or r['board']!='openai':
                raise ValueError('DB source provenance disagreement')
            if json.loads(r['raw_json'])!=original:raise ValueError('DB raw fields diverge from original source: '+ident)
            if r['description_plain']!=original.get('descriptionPlain') or r['description_html']!=original.get('descriptionHtml'):
                raise ValueError('DB description differs from source: '+ident)
            if r['job_url']!=original.get('jobUrl') or r['apply_url']!=original.get('applyUrl'):
                raise ValueError('DB application link diverges: '+ident)
            if (role['id'],role['title'],role['source_index'],role['job_url'])!=(ident,r['title'],ix,r['job_url']):
                raise ValueError('Stage 5 role differs from source: '+ident)
            prov=json.loads(r['provenance_json']);canonical=json.loads(r['canonical_json'])
            # Preserve the full source and the normalized/provenance projections, not just a search excerpt.
            out.append({'id':ident,'source_index':ix,'board':'openai','original_raw_job':original,
                        'canonical':canonical,'provenance':prov,'stage5_band':role['band'],
                        'stage6_deep_review':ident in meta['deep'],
                        'stage7_revisit_flag':ident in meta['revisit'],
                        'source_job_url':r['job_url'], 'captured_snapshot_sha256':meta['hashes']['snapshot']})
    return out

# Contact details are not required to evaluate professional evidence. Export only the
# established Stage 6 schema fields; report excluded fields rather than copying any
# unknown metadata or secrets from the original local profile.
CONTACT_PATTERNS = [
    re.compile(r"(?i)\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b"),
    re.compile(r"(?i)\b(?:https?://)?(?:www\.)?(?:linkedin\.com/in|github\.com|facebook\.com|instagram\.com)/[^\s,;]+"),
    re.compile(r"(?<![\w.])(?:\+?1[ .\-]?)?\(?\d{3}\)?[ .\-]\d{3}[ .\-]\d{4}(?!\d)"),
    re.compile(r"(?i)\b\d{1,6}\s+(?:[A-Za-z0-9]+\s+){1,5}(?:Street|St\.|Road|Rd\.|Avenue|Ave\.|Boulevard|Blvd\.|Lane|Ln\.|Drive|Dr\.)\b"),
]

def contact_clean(s:str)->tuple[str,int]:
    removed=0
    for regex in CONTACT_PATTERNS:
        s,n=regex.subn('[CONTACT_REMOVED]',s)
        removed+=n
    return s,removed

def public_candidate_evidence(original:dict, original_sha:str)->tuple[dict,dict]:
    if original.get('status')!='UNVERIFIED_RESUME_CLAIMS':
        raise ValueError('Candidate evidence must remain unverified')
    records=original.get('evidence')
    if not isinstance(records,list) or not records or len(records)>500:
        raise ValueError('Missing or oversized candidate evidence list')
    safe_records=[]; ids=set(); fields_excluded=0; contact_removed=0
    permitted={'id','kind','dates','summary','topics'}
    for entry in records:
        if not isinstance(entry,dict) or not isinstance(entry.get('id'),str) or not entry['id'] or entry['id'] in ids:
            raise ValueError('Duplicate or malformed candidate evidence IDs')
        ids.add(entry['id'])
        fields_excluded+=len(set(entry)-permitted)
        safe={}
        for key in ('id','kind','dates','summary'):
            if key in entry:
                if not isinstance(entry[key],str):raise ValueError('Invalid candidate evidence string: '+key)
                safe[key],n=contact_clean(entry[key]);contact_removed+=n
        if 'topics' in entry:
            if not isinstance(entry['topics'],list) or any(not isinstance(v,str) for v in entry['topics']):
                raise ValueError('Candidate topics must be a list of strings')
            safe['topics']=[]
            for topic in entry['topics']:
                clean,n=contact_clean(topic);safe['topics'].append(clean);contact_removed+=n
        safe_records.append(safe)
    fields_excluded+=len(set(original)-{'schema_version','status','source_description','evidence'})
    summary=original.get('source_description','')
    if not isinstance(summary,str):raise ValueError('Invalid source description')
    summary,n=contact_clean(summary);contact_removed+=n
    public={'schema_version':original.get('schema_version'), 'status':'UNVERIFIED_RESUME_CLAIMS',
            'source_description':summary, 'evidence':safe_records,
            'provenance':{'source_file_sha256':original_sha,'source_stage':'Stage 6 / candidate_evidence.private.json',
                          'all_evidence_records_included':True, 'source_record_count':len(records),
                          'original_evidence_records_unchanged_in_stages_6_and_7':True,
                          'only_contact_safe_schema_fields_exported':True,
                          'unknown_fields_excluded':fields_excluded,'contact_matches_redacted':contact_removed},
            'caution':'Unverified resume claims. Topic overlap does not prove competency, tenure or independent development.'}
    return public,public['provenance']

def project_evidence_addendum(meta:dict)->dict:
    # Derived from the presence and identity of verified stage reports in this run;
    # do not rewrite the original candidate profile or retroactively change Stage 6.
    return {'stage':'candidate_project_evidence_addendum','version':VERSION,
      'original_project_evidence_id':'PROJECT_PROOFLOOP_STAGES1TO5',
      'updated_project_evidence_id':'PROJECT_PROOFLOOP_STAGES1TO8',
      'kind':'CURRENT_PROJECT_ARTIFACT',
      'project':'Building My Way Into AI / ProofLoop — Attempt 001, OpenAI',
      'summary':'Collaborative, human-executed Python job-analysis pipeline: API snapshot acquisition, normalized JSONL, SQLite, independent validation, broad review, deep qualification dossiers, full-corpus comparative audit, and independent pre-AI evidence handoff.',
      'stages':[{'stage':5,'evidence_file':'reports/stage5/broad_analysis_report.json'},
                {'stage':6,'evidence_file':'reports/stage6/deep_analysis_report.json'},
                {'stage':7,'evidence_file':'reports/stage7/advanced_analysis_report.json'},
                {'stage':8,'evidence_file':'reports/stage8/stage8_audit_report.json'}],
      'source_jobs':len(meta['roles']), 'detailed_dossiers':len(meta['deep']),
      'topics':['python','sql','api_integration','automation','testing','documentation','research','data_provenance'],
      'verification_scope':'Reports and source IDs checked for internal integrity; prior Windows test results separately observed in conversation but not independently re-read by this script.',
      'limitations':['AI-assisted development; no claim of sole authorship or independently established coding proficiency',
                     'Current project work is distinct from professional work history',
                     'No evidence of years of production engineering implied',
                     'Earlier Stage 6/7 profile and SHA-256 preserved without mutation'] }

def audit(meta:dict,source:list[dict], resume_claims_present:bool=False)->dict:
    a=meta['data']['advanced']; d=meta['data']['deep'];b=meta['data']['broad']
    _,profile_meta=public_candidate_evidence(meta['data']['evidence'],meta['hashes']['evidence'])
    flags=[]
    def warn(code,count,detail,priority='REVIEW'):
        if count:flags.append({'code':code,'count':count,'priority':priority,'reason':detail})
    n=len(source)
    warn('OUTSIDE_100_REVISIT',len(meta['revisit']),'Heuristic recall leads—not qualified recommendations','HIGH')
    warn('EMBEDDED_HEADING_ARTIFACTS',a['counts'].get('embedded_heading_issues',0),'Requirement extraction may include a subsequent heading','HIGH')
    warn('EXTRACTION_COMPLETENESS_UNVERIFIED',n,'Recognized headings are not assurance that all requirements were extracted')
    warn('UNVERIFIED_CANDIDATE_EVIDENCE',len(meta['deep']),'Candidate résumé evidence is included without contact details, but claims remain provisional and require user confirmation','HIGH')
    warn('EXPERIENCE_DURATION_UNKNOWN',a['counts'].get('unresolved_requirement_flags',{}).get('EXPERIENCE_DURATION_NOT_VERIFIED',0),'Number of years in job descriptions is not years established for candidate')
    warn('RELOCATION_FUNDING_UNKNOWN',a['counts'].get('comparison_cautions',{}).get('FUNDING_UNCONFIRMED',0),'No demonstrated relocation funding for these roles')
    warn('REMOTE_METADATA_AMBIGUITY',a['counts'].get('comparison_cautions',{}).get('REMOTE_METADATA_CONFLICT',0),'isRemote=true can coexist with hybrid attendance')
    warn('STAGE7_DOC_STALE_EXAMPLE',1,'Stage 7 README example states 826 lines; actual run reports 879. Use the reports as authoritative, update docs.')
    warn('POSTING_AVAILABILITY_NOT_REFRESHED',n,'Source is a time-stamped snapshot, not real-time confirmation','HIGH')
    if a['counts'].get('still_missing_sections')==0 and a['counts'].get('embedded_heading_issues'):
        warn('ZERO_MISSING_DOES_NOT_MEAN_ZERO_EXTRACTION_RISK',a['counts']['embedded_heading_issues'],
             'Zero missing headings coexists with embedded heading issues')
    summary={'source_postings':n,'stage5_evaluated':len(meta['roles']),'stage6_dossiers':len(meta['deep']),
             'outside_dossiers':n-len(meta['deep']),'stage7_revisit_flags':len(meta['revisit']),
             'stage6_extracted_requirements':d['counts']['extracted_requirements'],
             'stage7_review_lines':a['counts']['stage7_review_lines'],
             'stage7_original_missing_sections_recovered':a['counts']['supplement_recovered_roles'],
             'embedded_heading_artifacts':a['counts']['embedded_heading_issues']}
    return {'stage':'independent_pre_ai_audit','version':VERSION,'status':'PASS_WITH_REVIEW_FLAGS' if flags else 'PASS',
            'generated_at_utc':datetime.now(timezone.utc).isoformat(),'board':'openai',
            'integrity_checks':{'snapshot_raw_jobs_equal_database':True,'database_integrity':True,
              'cross_stage_fingerprints':True,'cross_stage_population':True,'all_source_descriptions_preserved':True,
              'stage5_through_stage7_dossier_identity':True,'stage7_revisit_identity':True,'stage6_unverified_evidence_status':True},
            'counts':summary,'review_flags':flags,
            'constraints':{'final_five_selected':False,'qualifications_certified':False,'location_eligibility_certified':False,
                           'current_posting_availability_confirmed':False,'candidate_evidence_included':True,'contact_sanitized':True,'raw_private_profile_included':False,'redacted_resume_claims_included':resume_claims_present,
                           'AI_may_challenge_all_classifications':True},
            'candidate_evidence_export':{'record_count':profile_meta['source_record_count'],'original_profile_sha256':profile_meta['source_file_sha256'], 'excluded_extra_fields':profile_meta['unknown_fields_excluded'], 'redacted_contact_matches':profile_meta['contact_matches_redacted']},'input_sha256':meta['hashes'],'known_limits':['Structural independence does not establish semantic correctness of every extracted requirement',
                'Snapshot reflects one historical fetch; recheck job status when applying',
                'Contact-sanitized candidate evidence is present but remains unverified; cross-check with the user before relying on claims']}

def put_json(path:Path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def markdown(a:dict)->str:
    c=a['counts']
    lines=['# ProofLoop Stage 8 — Independent Pre-AI Audit','','**Integrity: PASS** · **Review flags: '+str(len(a['review_flags']))+'** · **No top-five decision**','','## Verified coverage',
          f"- Original source postings: **{c['source_postings']}**",f"- Stage 5 roles: **{c['stage5_evaluated']}**", f"- Stage 6/7 detailed dossiers: **{c['stage6_dossiers']}**",
          f"- Outside-pool roles flagged for review: **{c['stage7_revisit_flags']}**", f"- Requirements reviewed: Stage 6 **{c['stage6_extracted_requirements']}**, Stage 7 **{c['stage7_review_lines']}**",'',
          '## Independent review flags','', '| Flag | Count | Why it matters |','|---|---:|---|']
    for item in a['review_flags']:
        reason=html.escape(item['reason']).replace('|','\\|')
        lines.append(f"| `{item['code']}` | {item['count']} | {reason} |")
    lines+=['','## Boundaries','', '- **All 816 original postings and all Stage 5–8 reports are in the handoff archive.**',
            '- The 175 revisit leads must not be treated as qualified matches.','- The full structured candidate-evidence profile is included with contact details removed; claims remain unverified.',
            '- Verify relocation funding, remote eligibility, and current openings directly with the employer.',
            '- The AI should audit the entire corpus, challenge previous labels, and present recommendations only after evidence review.','']
    return '\n'.join(lines)

GUIDE='''# Building My Way Into AI — ProofLoop Stage 8 AI Review Protocol

## Files and provenance
- `source/all_816_source_roles.jsonl`: all 816 records with ORIGINAL employer-provided fields (including full descriptions and application URLs), canonical projections, source indices and provenance. This is snapshot data, NOT live vacancy confirmation.
- `reports/stage5/*`: complete Stage 5 broad review and its 100-role selection.
- `reports/stage6/*`: full 100-role deep dossier and summary, with provisional candidate evidence IDs.
- `reports/stage7/*`: comparative analysis, full-corpus audit, matrix, input manifest.
- `reports/stage8/*`: independent audit findings and review flags.
- `candidate/candidate_evidence_public.json`: contact-sanitized, full structured candidate evidence from the ORIGINAL Stage 6 profile.
- `candidate/PROJECT_PROOFLOOP_UPDATE.json`: additive project update to Stage 8, not professional work history.
- `candidate/resume_professional_claims.md`: fuller candidate résumé content without direct contact details, when `--resume-claims` is provided.
- `handoff_manifest.json`: SHA-256 and bytes of every file in this archive other than itself.

## AI instructions (not automatic authorization to submit applications)
1. Check the manifest hashes and reconcile contradictions between source text and any heuristic report. Never blindly assume classification correctness.
2. Read descriptions from all 816 roles as needed; focus deeply on the 100 dossiers **and** 175 out-of-pool recall leads. Check other roles if evidence warrants it; avoid assuming unflagged equals unqualified.
3. Audit requirement extraction, particularly supplementary headings, minimum versus preferred requirements, complex OR/AND alternatives, and embedded-heading artifacts.
4. Read the included candidate JSON evidence, the ProofLoop project addendum, AND the résumé claims Markdown (when present). Treat résumé claims as **unverified**, and do not infer proficiency, professional tenure or independent authorship from skill keywords or the collaborative ProofLoop project. Clarify uncertainties with the user before firm qualification judgments.
5. Compare practical opportunity and verified qualifications separately. The user resides in southern Utah; remote metadata alone is not proof of Utah eligibility. Relocation assistance, when stated, has unconfirmed dollar value and eligibility.
6. Avoid sales-primary opportunities unless the user changes this constraint; interpret technical roles adjacent to sales based on actual duties.
7. Check current availability, listed qualifications and work arrangements at the employer's official posting before submitting any application. Time-stamped URLs are historical evidence, not confirmation.
8. Challenge the Stage 5–7 screens; preserve rejected alternatives and dissenting reasoning. No arbitrary numerical scores or asserted probability of hiring.
9. Recommend five defensible applications with alternatives and explicit gaps, not necessarily the five best technical matches; the **one** shared Building My Way Into AI / ProofLoop technical project remains the founding targeted project for Attempt #001.
10. Do not send applications without user review and approval. Record decisions, reasons, dates and observed employer requirements as a traceable audit trail.

## Candidate evidence present; personal contact details absent
This archive INCLUDES the complete structured résumé-derived qualification evidence from Stage 6 (sanitized at the field/contact level), plus a separately sourced Stage 1–8 project update and, when provided, a fuller contact-redacted résumé transcription. It excludes the raw private input bytes, original résumé PDF and direct contact details such as email, phone, postal address and profile links. The full original evidence SHA-256 is preserved for provenance. Review the actual exported candidate file before publishing, because employer names, dated work history and credential claims can still be personally identifying. The user has requested this professional content in the shareable archive; no job application is authorized by the archive.

## Open quality notes
Stage 7's README sample contained an outdated requirement-line count. The current machine-generated reports are authoritative for the current run; inspect the Stage 8 audit flags for other limitations.
'''

def export(paths, root:Path, meta:dict, source:list[dict], a:dict, resume_claims:Path|None=None):
    handoff=root/'handoff'
    (handoff/'source').mkdir(parents=True)
    with (handoff/'source/all_816_source_roles.jsonl').open('w',encoding='utf-8',newline='\n') as f:
        for obj in source:f.write(json.dumps(obj,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
    for k,dest in REPORTS.items():
        to=handoff/'reports'/dest;to.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(paths[k],to)
    profile,profile_meta=public_candidate_evidence(meta['data']['evidence'],meta['hashes']['evidence'])
    put_json(handoff/'candidate/candidate_evidence_public.json',profile)
    put_json(handoff/'candidate/PROJECT_PROOFLOOP_UPDATE.json',project_evidence_addendum(meta))
    if resume_claims is not None:
        safe_resume,_=contact_clean(resume_claims.read_text(encoding='utf-8-sig'))
        (handoff/'candidate/resume_professional_claims.md').write_text(safe_resume,encoding='utf-8')
    put_json(handoff/'reports/stage8/stage8_audit_report.json',a)
    (handoff/'reports/stage8/stage8_audit_report.md').write_text(markdown(a),encoding='utf-8')
    (handoff/'AI_REVIEW_GUIDE.md').write_text(GUIDE,encoding='utf-8')
    manifest={'stage':'stage8_complete_handoff','version':VERSION,'board':'openai',
              'counts':a['counts'],'source_sha256':meta['hashes']['snapshot'],
              'db_sha256':meta['hashes']['db'],'candidate_evidence_included':True,'contact_sanitized':True,'raw_private_profile_included':False,
              'candidate_record_count':profile_meta['source_record_count'],
              'redacted_resume_claims_included':resume_claims is not None,
              'resume_source_sha256':digest(resume_claims) if resume_claims is not None else None,
              'candidate_source_evidence_sha256':meta['hashes']['evidence'],
              'all_stage_5_6_7_8_reports_included':True,'no_final_five':True,
              'files':{p.relative_to(handoff).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
                       for p in sorted(handoff.rglob('*')) if p.is_file()}}
    put_json(handoff/'handoff_manifest.json',manifest)
    with zipfile.ZipFile(root/'ai_handoff_bundle.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for p in sorted(handoff.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(handoff).as_posix())
    if zipfile.ZipFile(root/'ai_handoff_bundle.zip').testzip() is not None:raise ValueError('ZIP integrity failed')
    put_json(root/'stage8_audit_report.json',a)
    (root/'stage8_audit_report.md').write_text(markdown(a),encoding='utf-8')
    put_json(root/'stage8_handoff_manifest.json',manifest)
    return manifest

def run(paths:dict, output:Path, resume_claims:Path|None=None)->dict:
    if output.exists():raise ValueError('Output path already exists (no overwrites): '+output.name)
    if resume_claims is not None and (not resume_claims.is_file() or resume_claims.stat().st_size>1024*1024):
        raise ValueError('Missing or oversized redacted resume claims input')
    if output.parent.exists() and not output.parent.is_dir():raise ValueError('Output parent not a directory')
    for key in INPUT_KEYS:
        if not paths[key].is_file():raise ValueError('Missing input: '+paths[key].name)
        if key=='db' and paths[key].stat().st_size>MAX_DB:raise ValueError('Database too large')
    for key in ['evidence','snapshot','db']:
        if paths[key].resolve().is_relative_to(output.resolve()):raise ValueError('Input must not be nested in output')
    meta=check_inputs(paths);source=read_source(paths,meta);a=audit(meta,source,resume_claims is not None)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stage8-build-',dir=output.parent) as tmp:
        tmpdir=Path(tmp)/'bundle';tmpdir.mkdir()
        export(paths,tmpdir,meta,source,a,resume_claims)
        tmpdir.rename(output)
    return a

def main(argv=None)->int:
    ap=argparse.ArgumentParser(description=__doc__)
    for k in INPUT_KEYS: ap.add_argument('--'+k.replace('_','-'),required=True,type=Path)
    ap.add_argument('--output-dir',required=True,type=Path)
    ap.add_argument('--resume-claims',required=False,type=Path,help='Optional contact-redacted source résumé transcription; recommended for complete AI handoff')
    args=ap.parse_args(argv)
    paths={k:getattr(args,k) for k in INPUT_KEYS}
    try:a=run(paths,args.output_dir,args.resume_claims)
    except (OSError,ValueError,KeyError,TypeError,sqlite3.DatabaseError,json.JSONDecodeError) as e:
        print('FAIL: '+str(e),file=sys.stderr);return 1
    print(f"PASS: Stage 8 audited {a['counts']['source_postings']} source roles; verified Stage 5-7 identities")
    print(f"Review flags: {len(a['review_flags'])}; recall leads: {a['counts']['stage7_revisit_flags']}")
    print('Output: '+str(args.output_dir))
    print('Candidate evidence: INCLUDED, contact-sanitized; project update through Stage 8')
    print('Full résumé claims transcription: '+('INCLUDED' if args.resume_claims else 'NOT SUPPLIED'))
    print('Reports: stage8_audit_report.json/.md; stage8_handoff_manifest.json; ai_handoff_bundle.zip')
    return 0
if __name__=='__main__':sys.exit(main())
