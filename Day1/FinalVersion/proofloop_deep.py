#!/usr/bin/env python3
"""ProofLoop Stage 6 v0.6.0: evidence-labeled deep review of Stage 5's candidate pool.

Read-only input database; no network; no unverified qualification assertions.
Source passages are untrusted data. Deliberately does NOT produce a top-five ranking.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import html
import json
import re
import sqlite3
import sys
from pathlib import Path

VERSION = '0.6.0'
MAX_DATABASE = 600 * 1024 * 1024
MAX_REPORT = 75 * 1024 * 1024
MAX_CANDIDATES = 300

TOPIC_PATTERNS = {
  'technical_support':r'\b(?:technical|IT|customer|user|production)\s+support\b|\bsupport engineer(?:ing)?\b|\btroubleshoot\w*\b|\bservice desk\b|\bhelp desk\b',
  'jira_itsm':r'\b(?:Jira|ITSM|ticketing|ticket queues?|ServiceNow|Zendesk)\b',
  'crm':r'\bCRM\b|\bSalesforce\b|\bHighLevel\b',
  'api_integration':r'\b(?:REST(?:ful)?|APIs?|webhooks?|integration(?:s)?)\b',
  'python':r'\bPython\b', 'javascript':r'\bJavaScript\b', 'sql':r'\bSQL\b|\bPostgreSQL\b|\bMySQL\b',
  'powershell':r'\bPowerShell\b', 'automation':r'\bautomat\w*\b|\bworkflows?\b',
  'dns_network':r'\bDNS\b|\bnetwork(?:ing|s)?\b|\brouters?\b|\bTCP/IP\b',
  'documentation':r'\b(?:SOPs?|runbooks?|documentation|knowledge base|training guides?)\b',
  'testing':r'\b(?:test(?:ing|ed)?|UAT|QA|validation|quality assurance)\b',
  'security':r'\b(?:security|incident response|SOC|threats?)\b',
  'cloud':r'\b(?:cloud|AWS|Azure|GCP|Kubernetes|Terraform)\b',
  'distributed_systems':r'\bdistributed systems?\b|\bscal\w*\s+systems?\b',
  'machine_learning':r'\b(?:machine learning|deep learning|ML|AI training|RLHF)\b',
  'macos':r'\bmacOS\b|\bMac\s+OS\b', 'jamf':r'\bJamf\b', 'intune':r'\bIntune\b',
  'linux':r'\bLinux\b', 'customer_communication':r'\b(?:customer|stakeholder|end.user|communication)\b',
}
COMPILED = {k:re.compile(p,re.I) for k,p in TOPIC_PATTERNS.items()}
START_HEADERS = [
 (r'you might thrive in this role if(?: you)?(?: have)?\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'you will thrive in this role if(?: you)?(?: have)?\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'we expect you to\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'(?:minimum|required|basic|essential) qualifications\s*:?$', 'STATED_REQUIREMENT_CONTEXT'),
 (r'(?:must[- ]?haves?|requirements?|qualifications?|what (?:we are|we.re) looking for)\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'(?:preferred|desired) qualifications\s*:?$', 'PREFERRED_CONTEXT'),
 (r'(?:nice[- ]to[- ]have(?:s)?|bonus points|it would be great if you)\s*:?$', 'PREFERRED_CONTEXT'),
 (r'you(?:.re| are) a good fit if\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'what (?:you bring|we seek|you.ll bring)\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'you will be successful if\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'what we look for\s*:?$', 'EXPECTATION_CONTEXT'),
 (r'who you are\s*:?$', 'EXPECTATION_CONTEXT'),
]
STOP_HEADERS = [r'about (?:openai|the company|the team)\s*:?$',r'benefits(?: and perks)?\s*:?$',r'compensation\s*:?$',
 r'(?:equal opportunity|applicant privacy|background checks)\b',r'in this role[, ]*you will\s*:?$',
 r'what you(?:.ll| will) do\s*:?$',r'our tech stack\s*:?$', r'how to apply\s*:?$']
YEAR_RX = re.compile(r'\b(?:(?:at least|minimum(?: of)?|over|more than)\s+)?(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:professional\s+)?(?:experience|working|in\s+\w+)',re.I)
DEGREE_RX = re.compile(r'\b(?:Ph\.?D\.?|doctorate|bachelor\.?s?|master\.?s?|degree|equivalent (?:experience|training))\b',re.I)


def digest(path:Path)->str:
    hasher=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b''):hasher.update(chunk)
    return hasher.hexdigest()


def read_json(path:Path)->dict:
    if not path.is_file() or path.stat().st_size>MAX_REPORT:raise ValueError('Missing or overlarge JSON input: '+path.name)
    with path.open(encoding='utf-8-sig') as fh:
        obj=json.load(fh,parse_constant=lambda val:(_ for _ in ()).throw(ValueError('Invalid JSON constant '+val)))
    if not isinstance(obj,dict):raise ValueError('Expected JSON object: '+path.name)
    return obj


def evidence_profile_check(obj:dict)->dict:
    if obj.get('schema_version')!=1:raise ValueError('Candidate evidence schema_version must be 1')
    if obj.get('status')!='UNVERIFIED_RESUME_CLAIMS':raise ValueError('Profile must label evidence as unverified résumé claims')
    evidence=obj.get('evidence')
    if not isinstance(evidence,list) or not evidence:raise ValueError('Nonempty evidence list required')
    ids=set()
    for row in evidence:
        if not isinstance(row,dict):raise ValueError('Evidence entries must be objects')
        ident=row.get('id')
        if not isinstance(ident,str) or not ident or ident in ids:raise ValueError('Duplicate or blank evidence id')
        ids.add(ident)
        if row.get('kind') not in ('DATED_WORK_HISTORY','RESUME_PROJECT_CLAIM','RESUME_SKILL_LISTING','EDUCATION_CREDENTIAL','CURRENT_PROJECT_ARTIFACT'):
            raise ValueError('Unknown evidence kind: '+str(ident))
        if not isinstance(row.get('summary'),str) or not row['summary'].strip():raise ValueError('Evidence summary missing')
        tags=row.get('topics')
        if not isinstance(tags,list) or len(tags)!=len(set(tags)) or any(tag not in TOPIC_PATTERNS for tag in tags):
            raise ValueError('Unknown or duplicate topic for evidence '+ident)
        if row['kind']=='DATED_WORK_HISTORY' and (not isinstance(row.get('dates'),str) or not row['dates']):
            raise ValueError('Missing dates for work-history evidence')
    return obj


def heading(line:str)->tuple[str,str]|None:
    s=line.strip().strip('*_# ')
    if len(s)>100:return None
    for rx,label in START_HEADERS:
        if re.fullmatch(rx,s,re.I):return s,label
    return None


def is_stop(line:str)->bool:
    s=line.strip().strip('*_# ')
    return len(s)<125 and any(re.match(rx,s,re.I) for rx in STOP_HEADERS)


def extract_requirements(description:str)->tuple[list[dict],dict]:
    """Conservative plain-text extraction. No recognized heading != no qualifications."""
    lines=description.splitlines(); current=None; all_items=[]; current_buf=[]; found_heads=[]
    def flush():
        nonlocal current_buf
        if current and current_buf:
            raw=' '.join(s.strip() for s in current_buf if s.strip())
            raw=re.sub(r'\s+',' ',raw).strip()
            if raw:
                tags=sorted(k for k,p in COMPILED.items() if p.search(raw))
                nums=[int(x) for x in YEAR_RX.findall(raw)]
                all_items.append({'id':f'R{len(all_items)+1:03}', 'source_text':raw,
                                  'section_heading':current[0], 'requirement_context':current[1],
                                  'topic_signals':tags,'years_mentioned':nums,
                                  'degree_mentioned':bool(DEGREE_RX.search(raw)),
                                  'contains_preference_qualifier':bool(re.search(r'\b(?:ideally|preferably|a plus|nice to have)\b',raw,re.I))})
        current_buf=[]
    for line in lines:
        t=line.strip()
        h=heading(t)
        if h:
            flush();current=h;found_heads.append(h[0]);continue
        if current and is_stop(t):flush();current=None;continue
        if current:
            if not t:continue
            bullet=re.match(r'^\s*(?:[-*•]|\d+[.)])\s+(.*)$',t)
            if bullet:
                flush();current_buf=[bullet.group(1)]
            elif current_buf:
                # preserve wrapped multi-line bullet content
                current_buf.append(t)
            else:
                # Some feeds use paragraphs instead of bullets.
                current_buf=[t]
    flush()
    # Limit unexpectedly huge/free-form untrusted input with explicit truncation signal.
    truncated=len(all_items)>45
    return all_items[:45],{'status':('EXTRACTED' if all_items else 'NOT_EXTRACTED_REQUIRES_MANUAL_REVIEW'),
                          'headings':found_heads,'items_extracted':len(all_items[:45]),'truncated':truncated,
                          'scope':'Recognized qualification sections only; roles may have other requirements outside these sections'}


def review_one(row:dict,broad:dict,profile:dict)->dict:
    requirements,method=extract_requirements(row.get('description_plain') or '')
    evidence=profile['evidence']
    for req in requirements:
        topics=req['topic_signals']
        refs=[{'id':e['id'],'kind':e['kind'],'shared_topics':sorted(set(topics)&set(e['topics']))}
              for e in evidence if set(topics)&set(e['topics'])]
        req['topic_overlap_evidence']=refs
        req['assessment']=('TOPIC_OVERLAP_NOT_REQUIREMENT_PROOF' if refs else 'NO_PROFILE_TOPIC_EVIDENCE')
        req['duration_requirement_satisfied']='NOT_ASSESSED' if req['years_mentioned'] else 'NOT_APPLICABLE'
        req['education_requirement_satisfied']='NOT_ASSESSED' if req['degree_mentioned'] else 'NOT_APPLICABLE'
    explicit_years=sum(bool(r['years_mentioned']) for r in requirements)
    no_profile=sum(not r['topic_overlap_evidence'] for r in requirements)
    overlap=sum(bool(r['topic_overlap_evidence']) for r in requirements)
    years=[{'requirement_id':r['id'],'years':r['years_mentioned'],'source_text':r['source_text']}
           for r in requirements if r['years_mentioned']]
    qual_flags=[]
    if method['status']!='EXTRACTED':qual_flags.append('requirements_not_parsed_not_zero')
    if method['truncated']:qual_flags.append('requirements_truncated')
    if explicit_years:qual_flags.append('numeric_experience_not_verified')
    if any(r['degree_mentioned'] for r in requirements):qual_flags.append('degree_or_equivalent_not_verified')
    if broad['seniority_title_signal'] in ('PRINCIPAL_STAFF','SENIOR_LEAD'):qual_flags.append('elevated_title_seniority_review')
    if broad['location']['policy']=='RELOCATION_NOT_CONFIRMED':qual_flags.append('relocation_funding_not_established')
    if broad['location']['policy']=='RELOCATION_DEPENDENT':qual_flags.append('relocation_terms_and_amount_not_confirmed')
    if broad['location']['remote_metadata_conflict']:qual_flags.append('hybrid_not_utah_remote')
    return {'id':row['id'],'title':row['title'],'source_index':row['source_index'],'job_url':row['job_url'],
            'apply_url':row['apply_url'],'published_at':row['published_at'],
            'broad_band':broad['band'],'seniority_title_signal':broad['seniority_title_signal'],
            'technical':broad['technical'],'sales':broad['sales'],
            'location':broad['location'],'broad_review_flags':broad['review_flags'],
            'qualification_extraction':method,'requirements':requirements,'explicit_years':years,
            'coverage':{'extracted_requirements':len(requirements),'requirements_with_topic_overlap':overlap,
                        'requirements_without_profile_topic_evidence':no_profile,
                        'interpretation':'Topic matches are leads for review, not proof of full qualifications'},
            'review_flags':qual_flags,'candidate_evidence_status':profile['status']}


def checks(db:Path,store_path:Path,validation_path:Path,broad_path:Path,pool_path:Path,evidence_path:Path):
    for p in (db,store_path,validation_path,broad_path,pool_path,evidence_path):
        if not p.is_file():raise ValueError('Missing input: '+p.name)
    if db.stat().st_size>MAX_DATABASE:raise ValueError('Database larger than safety limit')
    store,validation,broad,pool=(read_json(p) for p in (store_path,validation_path,broad_path,pool_path))
    profile=evidence_profile_check(read_json(evidence_path))
    dh=digest(db)
    if (store.get('stage')!='store' or store.get('status')!='PASS' or
        store.get('database',{}).get('sha256')!=dh):raise ValueError('Store report/database integrity mismatch')
    if (validation.get('stage')!='independent_validation' or validation.get('status')!='PASS' or
        validation.get('failed')!=0 or validation.get('files',{}).get('sqlite_sha256')!=dh):
        raise ValueError('Independent validation report/database mismatch')
    if broad.get('stage')!='broad_analysis' or broad.get('status')!='PASS':raise ValueError('Invalid Stage 5 report')
    if broad.get('inputs',{}).get('db_sha256')!=dh or pool.get('database_sha256')!=dh:
        raise ValueError('Broad report or review pool DB fingerprint mismatch')
    if broad.get('board')!=pool.get('board') or broad.get('board')!=store.get('board'):
        raise ValueError('Board mismatch')
    ids=pool.get('candidate_ids');entries=pool.get('candidates')
    if not isinstance(ids,list) or not 1<=len(ids)<=MAX_CANDIDATES or not isinstance(entries,list) or len(entries)!=len(ids):
        raise ValueError('Candidate handoff malformed or oversized')
    if len(ids)!=len(set(ids)) or ids!=[x.get('id') for x in entries if isinstance(x,dict)]:
        raise ValueError('Candidate handoff order/identities inconsistent')
    broad_pool=broad.get('deep_review_pool')
    if ids!=[x.get('id') for x in broad_pool] or entries!=broad_pool:
        raise ValueError('Candidate pool differs from actual Stage 5 report')
    allroles=broad.get('roles')
    if not isinstance(allroles,list) or len(allroles)!=store.get('input',{}).get('records'):
        raise ValueError('Broad role record population disagrees with database')
    byid={x.get('id'):x for x in allroles}
    if len(byid)!=len(allroles) or not all(i in byid for i in ids):
        raise ValueError('Candidate IDs not in broad role population')
    with closing(sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True)) as conn:
        conn.row_factory=sqlite3.Row
        if conn.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite corruption')
        if conn.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Foreign key violations')
        # Parameterized IDs; do not build dynamic SQL from user-provided values.
        rows=[]
        for ident in ids:
            item=conn.execute('SELECT id,title,source_index,job_url,apply_url,published_at,description_plain,source_sha256 FROM roles WHERE id=?',(ident,)).fetchone()
            if item is None:raise ValueError('Missing database candidate '+ident)
            row=dict(item)
            if row['source_sha256']!=store['input']['source_sha256']:raise ValueError('Candidate source fingerprint mismatch')
            if row['title']!=byid[ident]['title'] or row['source_index']!=byid[ident]['source_index']:
                raise ValueError('Broad/database candidate values differ')
            rows.append(row)
    return store,validation,broad,pool,profile,rows,byid,dh


def run(db:Path,store_path:Path,validation_path:Path,broad_path:Path,pool_path:Path,evidence_path:Path,output_dir:Path)->dict:
    if output_dir.exists():raise ValueError('Output directory exists; choose a new output name')
    store,validation,broad,pool,profile,rows,byid,dh=checks(db,store_path,validation_path,broad_path,pool_path,evidence_path)
    dossiers=[review_one(row,byid[row['id']],profile) for row in rows]
    counts={'reviewed':len(dossiers),
            'extracted_requirements':sum(len(x['requirements']) for x in dossiers),
            'parsing_uncertain':sum(x['qualification_extraction']['status']!='EXTRACTED' for x in dossiers),
            'years_to_review':sum(len(x['explicit_years']) for x in dossiers),
            'title_seniority_review':sum('elevated_title_seniority_review' in x['review_flags'] for x in dossiers),
            'location_policies':dict(Counter(x['location']['policy'] for x in dossiers)),
            'flags':dict(Counter(f for x in dossiers for f in x['review_flags']))}
    report={'stage':'deep_analysis','version':VERSION,'status':'PASS','generated_utc':datetime.now(timezone.utc).isoformat(),
            'board':store['board'],'inputs':{'db_sha256':dh,'store_report_sha256':digest(store_path),
                'validation_report_sha256':digest(validation_path),'broad_report_sha256':digest(broad_path),
                'candidate_pool_sha256':digest(pool_path),'private_evidence_sha256':digest(evidence_path),
                'source_snapshot_sha256':store['input']['source_sha256']},
            'profile':{'status':profile['status'],'count':len(profile['evidence']),
                       'source_description':profile.get('source_description','private résumé-derived profile')},
            'methodology':{'no_automatic_qualification_claims':True,'final_top_five_not_selected':True,
                'all_source_requirements_untrusted_text':True,'qualification_sections_conservative':True,
                'financial_and_geographic_feasibility_not_certified':True},
            'counts':counts,'dossiers':dossiers,
            'limitations':['Only selected 100 reviewed, not all 816','Plain-text section extraction can miss nonstandard headings or qualifications outside detected sections',
              'Keyword topic overlap does not establish a full requirement match','Resume claims are not independently verified',
              'Duration, credentials and production scope require manual assessment','Relocation offers do not establish financial sufficiency',
              'Snapshot membership is not live job availability','No top-five ranking at this stage']}
    # Validate and render all files in memory before publication; no accidental overwrite.
    jtxt=json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    summary={'stage':'deep_review_summary','status':'PASS','board':report['board'],'inputs':report['inputs'],
             'counts':counts,'review_queue':[{'id':x['id'],'title':x['title'],'job_url':x['job_url'],
                     'extracted_requirements':x['coverage']['extracted_requirements'],
                     'topic_overlap':x['coverage']['requirements_with_topic_overlap'],
                     'review_flags':x['review_flags'],'location_policy':x['location']['policy']} for x in dossiers],
             'warning':'This is not a top-five ranking or verified qualification recommendation'}
    stxt=json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    mtxt=markdown(report)
    output_dir.mkdir(parents=True,exist_ok=False)
    try:
        for name,value in [('deep_analysis_report.json',jtxt),('deep_analysis_report.md',mtxt),('deep_review_summary.json',stxt)]:
            with (output_dir/name).open('x',encoding='utf-8',newline='\n') as fh:fh.write(value)
    except BaseException:
        for p in output_dir.iterdir():
            if p.is_file():p.unlink()
        output_dir.rmdir()
        raise
    return report


def escape_md(s:str)->str:
    s=re.sub(r'\s+',' ',str(s)).strip()
    return html.escape(s,quote=False).replace('|','\\|').replace('`','\\`').replace('[','\\[').replace(']','\\]')


def markdown(report:dict)->str:
    counts=report['counts']
    out=['# ProofLoop Stage 6 — Deep Qualification Evidence Review','',
         '**Status:** PASS (data processing only; no qualification certification)','',
         f"**Board:** `{report['board']}` · **Review pool:** {counts['reviewed']} · **Extracted lines:** {counts['extracted_requirements']} · **Needs section review:** {counts['parsing_uncertain']}",'',
         '## Interpretation','',
         'Topic overlap is **not** evidence that every part of a requirement is satisfied. Résumé claims are not independently verified.',
         'Experience duration, seniority, education, work geography and relocation funding require human confirmation.',
         'Source job text is external/untrusted data. This report makes **no** top-five selection.','',
         '## Candidate dossiers','']
    for idx,d in enumerate(report['dossiers'],1):
        out.extend([f"### {idx}. {escape_md(d['title'])}",'',
                    f"- **Posting:** {d['job_url']}",
                    f"- **ID:** `{d['id']}` · **Source index:** {d['source_index']} · **Broad band:** `{d['broad_band']}`",
                    f"- **Geography:** `{d['location']['policy']}` / `{d['location']['category']}` (employer confirmation required)",
                    f"- **Qualification extraction:** `{d['qualification_extraction']['status']}`; {d['qualification_extraction']['items_extracted']} lines",
                    f"- **Review flags:** {', '.join('`'+f+'`' for f in d['review_flags']) or 'none assigned'}",''])
        if not d['requirements']:
            out.extend(['**No reliable structured qualification lines extracted; inspect the original posting manually.**',''])
        for r in d['requirements']:
            txt=escape_md(r['source_text'])
            out.extend([f"**{r['id']} — {escape_md(r['section_heading'])}** (`{r['requirement_context']}`)",'',
                        f"> {txt}",'',
                        'Topic signals: '+(', '.join('`'+x+'`' for x in r['topic_signals']) or 'none')+
                        ' · Evidence references: '+(', '.join('`'+x['id']+'`' for x in r['topic_overlap_evidence']) or 'none')+
                        ' · Assessment: **'+r['assessment']+'**' +
                        (' · **YEARS NOT VERIFIED**' if r['years_mentioned'] else '') +
                        (' · **EDUCATION NOT VERIFIED**' if r['degree_mentioned'] else ''),''])
    out.extend(['## Limitations','']+[f'- {escape_md(x)}' for x in report['limitations']])
    return '\n'.join(out)+'\n'


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ('db','store-report','validation-report','broad-report','candidates','evidence','output-dir'):
        p.add_argument('--'+flag,type=Path,required=True)
    args=p.parse_args(argv)
    try:
        result=run(args.db,args.store_report,args.validation_report,args.broad_report,args.candidates,args.evidence,args.output_dir)
    except (ValueError,OSError,sqlite3.Error) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);return 1
    print(f"PASS: deep reviewed {result['counts']['reviewed']} postings; extracted {result['counts']['extracted_requirements']} qualification lines")
    print('Missing/uncertain sections: '+str(result['counts']['parsing_uncertain']))
    print('Output: '+str(args.output_dir))
    print('Reports: deep_analysis_report.json/.md and deep_review_summary.json')
    return 0

if __name__=='__main__':sys.exit(main())
