#!/usr/bin/env python3
"""ProofLoop Stage 7: full-corpus audit and evidence-bounded advanced comparison.

No network, no source mutation, no qualification certification, no final top-five.
This script is a *separate analytical lens* over Stage 5/6 immutable reports,
not a replacement for them. Source job text is untrusted external input.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import closing
from datetime import datetime, timezone
from hashlib import sha256
import html
import json
from pathlib import Path
import re
import sqlite3
import sys

VERSION = '0.7.0'
MAX_JSON_BYTES = 90 * 1024 * 1024
MAX_DB_BYTES = 600 * 1024 * 1024
MAX_ROLE_DESCRIPTION = 700_000
MAX_ROLES = 5000

SUPPLEMENT_HEADINGS = (
    (re.compile(r"^you may be a strong fit if you\s*:?$",re.I),'EXPECTATION_CONTEXT'),
    (re.compile(r"^your background might look something like\s*:?$",re.I),'EXPECTATION_CONTEXT'),
    (re.compile(r"^you might thrive here if you\s*:?$",re.I),'EXPECTATION_CONTEXT'),
    # Preserve evidence of the source's actual spelling rather than silently editing the posting.
    (re.compile(r"^you might thrive int his role if you\s*:?$",re.I),'EXPECTATION_CONTEXT'),
    (re.compile(r"^(?:you['’]?ll|you will|you might) thrive in this role if you\s*:?$", re.I), 'EXPECTATION_CONTEXT'),
    (re.compile(r"^(?:who (?:we['’]?re|we are) looking for|what (?:you['’]?ll|you will) bring to the (?:role|team)|what you need to succeed)\s*:?$", re.I), 'EXPECTATION_CONTEXT'),
    (re.compile(r'^(?:what (?:you should|we expect) (?:have|bring)|key qualifications|what makes you successful)\s*:?$', re.I), 'EXPECTATION_CONTEXT'),
    (re.compile(r'^(?:preferred skills|preferred experience|nice[- ]to[- ]have(?: skills)?|bonus qualifications)\s*:?$',re.I), 'PREFERRED_CONTEXT'),
    (re.compile(r'^(?:required skills|minimum requirements|must[- ]have qualifications)\s*:?$',re.I), 'STATED_REQUIREMENT_CONTEXT'),
)
SEPARATE_HEADING = re.compile(r'\b(?:Preferred Skills|Preferred Qualifications|Minimum Qualifications|Required Qualifications|Nice to Have)\b\s*:?',re.I)
END_SECTION = re.compile(r'^(?:about (?:openai|the team|the role|the company)|in this role[,:]? you will|what you(?: will|.ll) do|benefits(?: and perks)?|compensation|equal opportunity|how to apply|applicant privacy|our commitment to|job description)$',re.I)
LIST_BULLET = re.compile(r'^\s*(?:[-*•]|\d+[.)])\s+(.*)$')
EXPERIENCE_YEARS = re.compile(r'\b(?:at least\s+|minimum(?: of)?\s+|over\s+|more than\s+)?(\d{1,2})\s*(?:\+|or more)?\s*(?:years?|yrs?)\b',re.I)
EXPLICIT_CREDENTIAL = re.compile(r'\b(?:bachelor(?:\x27s|s)?|master(?:\x27s|s)?|ph\.?d\.?|doctorate|(?:university |college )?degree|certification|clearance)\b',re.I)
TRAVEL = re.compile(r'\b(?:travel (?:up to|at least|approximately|about)\s*\d{1,3}\s*%|\d{1,3}\s*%\s*travel|frequent travel|regular travel)\b',re.I)
CLEARANCE = re.compile(r'\b(?:active security clearance|ability to obtain (?:a|an) (?:security )?clearance|US (?:citizen|citizenship) required|U\.S\. citizen(?:ship)? required|must be (?:a )?(?:US|U\.S\.) citizen)\b',re.I)
PREFERENCE = re.compile(r'\b(?:a plus|nice to have|preferred|ideally|bonus|advantageous)\b',re.I)
BOILERPLATE_MARKER = re.compile(r'^\s*about openai\s*$',re.I|re.M)


def file_hash(path:Path)->str:
    h=sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def read_json(path:Path)->dict:
    if not path.is_file() or path.stat().st_size>MAX_JSON_BYTES: raise ValueError('Missing/oversized input: '+path.name)
    with path.open(encoding='utf-8-sig') as f:
        result=json.load(f,parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Invalid JSON constant')))
    if not isinstance(result,dict): raise ValueError('Expected JSON object: '+path.name)
    return result


def ids_unique(rows:list, name:str)->dict:
    if not isinstance(rows,list): raise ValueError(name+' must be a list')
    out={}
    for obj in rows:
        if not isinstance(obj,dict) or not isinstance(obj.get('id'),str) or not obj['id'] or obj['id'] in out:
            raise ValueError('Missing or duplicate IDs in '+name)
        out[obj['id']]=obj
    return out


def title_family(title:str)->str:
    t=title.casefold()
    if re.search(r'\b(?:support|help desk|service desk|it specialist|it admin)\b',t): return 'SUPPORT_IT'
    if re.search(r'\b(?:security|threat|incident response|grc|trust and safety)\b',t):return 'SECURITY'
    if re.search(r'\b(?:technical program|program manager|project manager|operations lead)\b',t):return 'PROGRAM_OPERATIONS'
    if re.search(r'\b(?:data engineer|data scientist|analytics|data analyst)\b',t):return 'DATA_ANALYTICS'
    if re.search(r'\b(?:developer relations|developer experience|devrel|api platform|integrations?|solutions engineer|applied ai engineer)\b',t):return 'API_APPLIED'
    if re.search(r'\b(?:network|systems?|infra|sre|reliability|compute|cloud|firmware)\b',t):return 'INFRA_SYSTEMS'
    if re.search(r'\b(?:software engineer|full.stack engineer|frontend|backend|engineering)\b',t):return 'SOFTWARE_ENGINEERING'
    return 'OTHER'


def trim_boilerplate(body:str)->str:
    m=BOILERPLATE_MARKER.search(body)
    return body[:m.start()] if m else body


def heading_variant(line:str):
    s=line.strip().strip('*_# ').strip()
    if len(s)>110:return None
    for rx,kind in SUPPLEMENT_HEADINGS:
        if rx.fullmatch(s):return (s,kind)
    return None


def supplementary_extract(description:str)->tuple[list[dict],dict]:
    """Only recognized extra headings; no guessing requirements from narrative.

    Does not overwrite Stage 6 extraction. Every recovered line traces its section.
    """
    if not isinstance(description,str):return [],{'status':'NO_SOURCE_TEXT','headings':[]}
    body=trim_boilerplate(description[:MAX_ROLE_DESCRIPTION]);lines=body.splitlines()
    found=[]; current=None; buf=[]; collected=[]
    def flush():
        nonlocal buf
        if current and buf:
            text=' '.join(x.strip() for x in buf if x.strip())
            text=re.sub(r'\s+',' ',text).strip()
            if text:
                collected.append({'source_text':text,'section_heading':current[0], 'context':current[1]})
        buf=[]
    for line in lines:
        s=line.strip()
        head=heading_variant(s)
        if head:
            flush();current=head;found.append(head[0]);continue
        if current and (END_SECTION.fullmatch(s.strip(': ')) or (s.lower().startswith('about openai'))):
            flush();current=None;continue
        if current and s:
            bm=LIST_BULLET.match(s)
            if bm:
                flush();buf=[bm.group(1)]
            elif buf:buf.append(s)
            else:buf=[s]
    flush()
    # No silent truncation: expose it.
    exceeded=len(collected)>60
    return collected[:60],{'status':'SUPPLEMENT_FOUND' if collected else 'NOT_FOUND','headings':found,'truncated':exceeded}


def split_embedded_heading(s:str)->tuple[str,str|None]:
    # Stage 6 sometimes folded a new preferred heading into previous bullet.
    m=SEPARATE_HEADING.search(s)
    if m and m.start()>8 and (m.start() >= len(s)-100):
        return s[:m.start()].strip(),s[m.start():].strip()
    return s,None


def decompose(s:str)->list[str]:
    """Conservative decomposition at semicolon boundaries only; never silently loses text."""
    parts=[x.strip() for x in s.split(';') if x.strip()]
    return parts[:10] if parts else [s]


def requirement_review(req:dict,profile_map:dict)->dict:
    text=req['source_text']
    clean,heading_issue=split_embedded_heading(text)
    context=req.get('requirement_context',req.get('context','EXPECTATION_CONTEXT'))
    if not isinstance(context,str):context='EXPECTATION_CONTEXT'
    qualifier=bool(PREFERENCE.search(clean))
    strength=('PREFERRED_OR_BONUS' if context=='PREFERRED_CONTEXT' or qualifier else
              'EXPLICIT_MINIMUM' if context=='STATED_REQUIREMENT_CONTEXT' else 'EXPECTATION_NOT_FORMALLY_CLASSIFIED')
    topic_refs=req.get('topic_overlap_evidence') or []
    ids=sorted({x['id'] for x in topic_refs if isinstance(x,dict) and x.get('id') in profile_map})
    kinds=sorted({profile_map[x]['kind'] for x in ids})
    yr_nums=[int(x) for x in EXPERIENCE_YEARS.findall(clean)]
    themes=sorted(set(req.get('topic_signals') or []))
    # Distinguish topical correspondence from proved end-to-end capability.
    claim_kind=('CURRENT_PROJECT_ONLY' if ids and all(profile_map[x]['kind']=='CURRENT_PROJECT_ARTIFACT' for x in ids) else
                'WORK_OR_CREDENTIAL_TOPIC_OVERLAP' if ids and any(profile_map[x]['kind'] in ('DATED_WORK_HISTORY','EDUCATION_CREDENTIAL') for x in ids) else
                'OTHER_UNVERIFIED_TOPIC_OVERLAP' if ids else 'NO_TOPIC_SUPPORT_IDENTIFIED')
    obligations=[]
    if yr_nums:obligations.append('EXPERIENCE_DURATION_NOT_VERIFIED')
    if EXPLICIT_CREDENTIAL.search(clean):obligations.append('CREDENTIAL_OR_DEGREE_NOT_VERIFIED')
    if CLEARANCE.search(clean):obligations.append('CITIZENSHIP_OR_CLEARANCE_REVIEW')
    if re.search(r'\b(?:production|at scale|large.scale|distributed systems|staff|lead(?:ing)? teams?)\b',clean,re.I):
        obligations.append('PRODUCTION_SCALE_OR_LEADERSHIP_NOT_VERIFIED')
    if not ids:obligations.append('MISSING_RELEVANT_PROFILE_TOPIC_EVIDENCE')
    if heading_issue:obligations.append('EMBEDDED_HEADING_REQUIRES_MANUAL_REVIEW')
    return {'id':req.get('id'), 'original_source_text':text,'cleaned_for_review':clean,
            'section_heading':req.get('section_heading'), 'requirement_strength':strength,
            'segments':decompose(clean),'topics':themes,'source_stage':req.get('source_stage','STAGE6'),
            'evidence_ids':ids,'evidence_kinds':kinds,'evidence_relation':claim_kind,
            'experience_year_numbers':yr_nums,'credentials_mentioned':bool(EXPLICIT_CREDENTIAL.search(clean)),
            'unresolved_obligations':obligations,'extraction_issue':heading_issue,
            'assessment':'NOT_CERTIFIED_ONLY_TOPIC_ALIGNMENT'}


def make_requirements(stage6:dict,body:str,profile_map:dict)->tuple[list[dict],dict]:
    original=stage6.get('requirements',[])
    if not isinstance(original,list):raise ValueError('Bad Stage 6 requirement list')
    supp,smethod=supplementary_extract(body)
    # Stage6 is source of truth; supplementary heads are added only if Stage6 lacked a section.
    use_supp=not original and bool(supp)
    requirements=[]
    if use_supp:
        for i,r in enumerate(supp,1):
            req={'id':f'S7R{i:03}','source_text':r['source_text'],'section_heading':r['section_heading'],
                 'requirement_context':r['context'],'source_stage':'STAGE7_SUPPLEMENT',
                 'topic_signals':[], 'topic_overlap_evidence':[]}
            requirements.append(requirement_review(req,profile_map))
    else:
        requirements=[requirement_review(r,profile_map) for r in original]
    assessment=('SUPPLEMENT_RECOVERED_REQUIRES_MANUAL_CONFIRMATION' if use_supp else
                'NO_SECTION_FOUND_MANUAL_REVIEW' if not requirements else 'STAGE6_REVIEW_REFINED')
    return requirements,{'assessment':assessment,'stage6_count':len(original),
        'stage7_supplement_count':len(supp),'supplement_used':use_supp,
        'stage7_supplement_method':smethod,'embedded_heading_issue_count':sum(bool(r['extraction_issue']) for r in requirements)}


def candidate_group(d:dict,review:list[dict])->tuple[str,list[str]]:
    flags=[]
    loc=d['location']['policy']
    if loc=='RELOCATION_NOT_CONFIRMED':flags.append('FUNDING_UNCONFIRMED')
    if loc=='RELOCATION_DEPENDENT':flags.append('RELOCATION_TERMS_UNVERIFIED')
    if d['location'].get('remote_metadata_conflict'):flags.append('REMOTE_METADATA_CONFLICT')
    if d['seniority_title_signal']=='PRINCIPAL_STAFF':flags.append('ELEVATED_SENIORITY')
    if any(r['experience_year_numbers'] and max(r['experience_year_numbers'])>=7 and r['requirement_strength']!='PREFERRED_OR_BONUS' for r in review): flags.append('HIGH_EXPERIENCE_EXPECTATION')
    if any('CITIZENSHIP_OR_CLEARANCE_REVIEW' in r['unresolved_obligations'] for r in review):flags.append('SCREENING_ELIGIBILITY_UNKNOWN')
    if not review:flags.append('QUALIFICATIONS_NOT_PARSED')
    if not review: return 'MANUAL_REQUIREMENTS_REVIEW',flags
    if 'ELEVATED_SENIORITY' in flags or 'HIGH_EXPERIENCE_EXPECTATION' in flags:
        return 'HIGH_EXPECTATION_STRETCH_REVIEW',flags
    if d['sales']['classification']=='SALES_PRIMARY_EVIDENCE':return 'PRIMARY_SALES_ACTIVITY_REVIEW',flags
    if d['technical']['classification']!='HANDS_ON_EVIDENCE':return 'TECHNICAL_CORE_REVIEW',flags
    if loc=='RELOCATION_NOT_CONFIRMED':return 'TECHNICAL_REVIEW_LOGISTICS_UNKNOWN',flags
    return 'EVIDENCE_REVIEW_WITH_UNRESOLVED_GAPS',flags


def find_rescue(role:dict, in_deep:bool, text:str)->tuple[list[str],bool]:
    if in_deep:return [],False
    reasons=[];title=role['title'].casefold()
    if role['technical']['classification']=='HANDS_ON_EVIDENCE' and role['sales']['classification']!='SALES_PRIMARY_EVIDENCE':
        reasons.append('HANDS_ON_TECHNICAL_OUTSIDE_100_POOL')
    if re.search(r'\b(?:technical (?:program|support|operations)|support (?:engineer|operations|delivery)|it support|developer (?:experience|relations)|incident response|api integration)\b',title):
        reasons.append('PREFERRED_ROLE_FAMILY_OUTSIDE_POOL')
    if role['band']=='DEEP_REVIEW_PRIORITY':reasons.append('STAGE5_PRIORITY_EXCLUDED_BY_CAP')
    if role['sales']['classification']=='SALES_CONTEXT_REVIEW' and role['technical']['classification']=='HANDS_ON_EVIDENCE':
        reasons.append('SALES_CONTEXT_COULD_BE_FALSE_POSITIVE')
    if role['location']['policy']=='OUTSIDE_PROFILE':
        reasons.append('LOCATION_OUTSIDE_USER_PROFILE')
    if role['sales']['classification']=='SALES_PRIMARY_EVIDENCE':reasons.append('PRIMARY_SALES_POTENTIAL_BLOCKER')
    if role['technical']['classification']=='TECHNICAL_CORE_UNCONFIRMED':reasons.append('TECHNICAL_CORE_UNCONFIRMED')
    if role['seniority_title_signal']=='PRINCIPAL_STAFF':reasons.append('PRINCIPAL_LEVEL')
    actionable=bool(set(reasons)&{'HANDS_ON_TECHNICAL_OUTSIDE_100_POOL','PREFERRED_ROLE_FAMILY_OUTSIDE_POOL','STAGE5_PRIORITY_EXCLUDED_BY_CAP','SALES_CONTEXT_COULD_BE_FALSE_POSITIVE'})
    if role['location']['policy']=='OUTSIDE_PROFILE' or role['sales']['classification']=='SALES_PRIMARY_EVIDENCE':actionable=False
    return reasons,actionable


def load_and_check(paths:dict)->tuple[dict,dict,dict,dict,dict,dict,dict,str,list[dict]]:
    for key,p in paths.items():
        if not p.is_file():raise ValueError('Missing input '+key+': '+p.name)
    if paths['db'].stat().st_size>MAX_DB_BYTES:raise ValueError('Database too large')
    store=read_json(paths['store']);validation=read_json(paths['validation'])
    broad=read_json(paths['broad']);pool=read_json(paths['candidates'])
    deep=read_json(paths['deep']);summary=read_json(paths['deep_summary'])
    evidence=read_json(paths['evidence'])
    if store.get('stage')!='store' or store.get('status')!='PASS':raise ValueError('Invalid store report')
    dbsha=file_hash(paths['db']); srcsha=store.get('input',{}).get('source_sha256')
    if store.get('database',{}).get('sha256')!=dbsha:raise ValueError('Store database SHA mismatch')
    if validation.get('stage')!='independent_validation' or validation.get('status')!='PASS' or validation.get('failed')!=0 or validation.get('files',{}).get('sqlite_sha256')!=dbsha:
        raise ValueError('Independent validator status/SHA mismatch')
    if broad.get('status')!='PASS' or broad.get('stage')!='broad_analysis' or broad.get('inputs',{}).get('db_sha256')!=dbsha:raise ValueError('Stage 5 report/database mismatch')
    if pool.get('database_sha256')!=dbsha or pool.get('candidate_ids')!=[r['id'] for r in broad['deep_review_pool']]:
        raise ValueError('Stage 5 candidate handoff IDs mismatch')
    if pool.get('candidates')!=broad.get('deep_review_pool'):raise ValueError('Stage 5 review pool mismatch')
    if deep.get('stage')!='deep_analysis' or deep.get('status')!='PASS' or deep.get('inputs',{}).get('db_sha256')!=dbsha:
        raise ValueError('Stage 6 deep report mismatch')
    if summary.get('stage')!='deep_review_summary' or summary.get('status')!='PASS':raise ValueError('Bad Stage 6 summary')
    for k,key in [('store','store_report_sha256'),('validation','validation_report_sha256'),('broad','broad_report_sha256'),('candidates','candidate_pool_sha256'),('evidence','private_evidence_sha256')]:
        if deep['inputs'].get(key)!=file_hash(paths[k]):raise ValueError('Stage 6 upstream fingerprint mismatch: '+key)
    if summary.get('inputs')!=deep.get('inputs') or summary.get('counts')!=deep.get('counts'):
        raise ValueError('Stage 6 summary mismatch')
    if evidence.get('status')!='UNVERIFIED_RESUME_CLAIMS' or not isinstance(evidence.get('evidence'),list):
        raise ValueError('Stage 6 candidate evidence must remain labeled unverified')
    evmap=ids_unique(evidence['evidence'],'candidate evidence')
    by_broad=ids_unique(broad['roles'],'Stage 5 roles')
    by_deep=ids_unique(deep['dossiers'],'Stage 6 dossiers')
    if not 1<=len(by_broad)<=MAX_ROLES or len(by_broad)!=store['input']['records']:raise ValueError('Stage 5 role count mismatch')
    if set(by_deep)!=set(pool['candidate_ids']) or [d['id'] for d in deep['dossiers']]!=pool['candidate_ids']:
        raise ValueError('Stage 6 population/order mismatch')
    if len(summary.get('review_queue',[]))!=len(by_deep) or [d['id'] for d in summary['review_queue']]!=pool['candidate_ids']:
        raise ValueError('Stage 6 review queue mismatch')
    if any(by_broad[i]['title']!=d['title'] or by_broad[i]['source_index']!=d['source_index'] for i,d in by_deep.items()):
        raise ValueError('Stage 5/6 role identity mismatch')
    if sum(len(d['requirements']) for d in by_deep.values())!=deep['counts']['extracted_requirements']:
        raise ValueError('Stage 6 requirement count mismatch')
    boards={x.get('board') for x in (store,broad,deep,summary,pool)}
    if len(boards)!=1:raise ValueError('Board identity mismatch')
    if broad.get('inputs',{}).get('source_snapshot_sha256')!=srcsha or deep['inputs'].get('source_snapshot_sha256')!=srcsha:
        raise ValueError('Source snapshot fingerprint mismatch')
    with closing(sqlite3.connect(paths['db'].resolve().as_uri()+'?mode=ro',uri=True)) as conn:
        conn.row_factory=sqlite3.Row
        conn.execute('PRAGMA query_only=ON')
        if conn.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity check failed')
        if conn.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('SQLite orphan rows')
        rows=[dict(row) for row in conn.execute('SELECT id,board,title,source_index,source_sha256,description_plain,job_url,apply_url,published_at FROM roles ORDER BY source_index')]
    if len(rows)!=len(by_broad) or {x['id'] for x in rows}!=set(by_broad):raise ValueError('Database and Stage 5 population mismatch')
    for row in rows:
        b=by_broad[row['id']]
        if (row['title']!=b['title'] or row['source_index']!=b['source_index'] or row['source_sha256']!=srcsha
                or row['board']!=store['board'] or row['job_url']!=b['job_url'] or row['apply_url']!=b['apply_url']):
            raise ValueError('Stage 5 role/database mismatch: '+row['id'])
        if row['id'] in by_deep:
            d=by_deep[row['id']]
            if row['job_url']!=d['job_url'] or row['published_at']!=d['published_at']:
                raise ValueError('Stage 6 role/database mismatch: '+row['id'])
    return store,validation,broad,pool,deep,summary,evmap,dbsha,rows


def safe_md(text)->str:
    return html.escape(str(text).replace('\n',' '),quote=False).replace('|','\\|').replace('`','\\`').replace('[','\\[').replace(']','\\]')


def build(paths:dict)->tuple[dict,dict,dict,dict,dict]:
    store,validation,broad,pool,deep,summary,profile,dbsha,rows=load_and_check(paths)
    b_by={r['id']:r for r in broad['roles']};d_by={r['id']:r for r in deep['dossiers']}
    dossiers=[];covered=[];rescue=[];audit=[];extraction_findings=[];flags_counter=Counter();req_counts=Counter();family_counts=Counter()
    for row in rows:
        b=b_by[row['id']];is_deep=row['id'] in d_by
        body=row.get('description_plain') or ''
        if len(body)>MAX_ROLE_DESCRIPTION:body=body[:MAX_ROLE_DESCRIPTION]
        family=title_family(row['title']); family_counts[family]+=1
        outside_reasons,actionable=find_rescue(b,is_deep,body)
        # Extract supplemental requirements for ALL 816 even when excluded; no candidate is invisible.
        supp,parse=supplementary_extract(body)
        if is_deep:
            d=d_by[row['id']]
            requirements,details=make_requirements(d,body,profile)
            family_flags,flags=candidate_group(d,requirements)
            for f in flags:flags_counter[f]+=1
            for requirement in requirements:
                for f in requirement['unresolved_obligations']: req_counts[f]+=1
            if details['supplement_used'] or details['embedded_heading_issue_count'] or not requirements:
                extraction_findings.append({'id':row['id'],'title':row['title'],'stage6_count':details['stage6_count'],
                   'supplement_count':details['stage7_supplement_count'],'used_supplement':details['supplement_used'],
                   'assessment':details['assessment'],'embedded_heading_issues':details['embedded_heading_issue_count']})
            # Do NOT expose private evidence text, only stable evidence IDs and unverified status.
            dossiers.append({'id':row['id'],'title':row['title'],'job_url':row['job_url'], 'source_index':row['source_index'],
                'family':family,'stage5_band':b['band'],'stage6_requirement_count':len(d['requirements']),
                'stage7_review_requirement_count':len(requirements),'qualification_extraction':details,
                'expectations':requirements,'comparison_group':family_flags,'comparison_cautions':flags,
                'geography':{'classification':d['location']['category'],'policy':d['location']['policy'],
                    'primary':d['location']['primary_location'],'remote_eligible_from_utah':'UNCONFIRMED',
                    'relocation_assistance_amount':'UNCONFIRMED',
                    'relocation_evidence':d['location'].get('relocation_evidence',[])[:2],
                    'hybrid_conflict':d['location'].get('remote_metadata_conflict',False)},
                'sales_classification':d['sales']['classification'],'seniority_title_signal':d['seniority_title_signal'],
                'evidence_status':'UNVERIFIED_RESUME_CLAIMS',
                'required_human_review':['VALIDATE_PROFILE_AND_PROFICIENCY','VERIFY_WORK_LOCATION_AND_FUNDING','INTERPRET_COMPOUND_REQUIREMENTS','CHECK_CURRENT_POSTING_AVAILABILITY']+(['MANUALLY_REVIEW_REQUIREMENTS'] if not requirements else [])})
        if not is_deep and actionable:
            rescue.append({'id':row['id'],'title':row['title'],'job_url':row['job_url'],
              'source_index':row['source_index'],'family':family,'stage5_band':b['band'],
              'review_reasons':outside_reasons,'stage7_supplemental_requirements':len(supp),
              'geography_policy':b['location']['policy'],'sales_classification':b['sales']['classification'],
              'status':'REVISIT_FOR_AI_REVIEW_NOT_PROMOTED_OR_QUALIFIED'})
        audit.append({'id':row['id'],'title':row['title'],'job_url':row['job_url'],'source_index':row['source_index'],
            'family':family,'stage5_band':b['band'],'in_stage6_pool':is_deep,
            'stage5_blockers':b['blockers'],'location_policy':b['location']['policy'],
            'sales_classification':b['sales']['classification'],
            'stage7_supplement_headings':parse['headings'][:6],
            'stage7_supplement_requirements':len(supp),'blind_spot_reasons':outside_reasons,
            'blind_spot_revisit':actionable,'notes':'Not a current-availability confirmation'})
    # Deterministic order: primary index from source, not fabricated qualification score.
    rescue.sort(key=lambda x:(x['family'] not in ('SUPPORT_IT','API_APPLIED','PROGRAM_OPERATIONS'),
                              x['stage5_band']!='DEEP_REVIEW_PRIORITY',x['title'].casefold(),x['id']))
    group_count=dict(sorted(Counter(x['comparison_group'] for x in dossiers).items()))
    counts={'corpus_roles':len(rows),'stage6_dossiers':len(dossiers),'stage5_excluded_roles':len(rows)-len(dossiers),
        'rescue_review_candidates':len(rescue),'stage7_review_lines':sum(len(x['expectations']) for x in dossiers),
        'stage6_lines':sum(x['stage6_requirement_count'] for x in dossiers),
        'supplement_recovered_roles':sum(x['qualification_extraction']['supplement_used'] for x in dossiers),
        'still_missing_sections':sum(not x['expectations'] for x in dossiers),
        'embedded_heading_issues':sum(x['qualification_extraction']['embedded_heading_issue_count'] for x in dossiers),
        'comparison_groups':group_count,'roles_by_family':dict(sorted(family_counts.items())),
        'unresolved_requirement_flags':dict(sorted(req_counts.items())),'comparison_cautions':dict(sorted(flags_counter.items()))}
    inputs={key+'_sha256':file_hash(paths[key]) for key in ('db','store','validation','broad','candidates','deep','deep_summary','evidence')}
    inputs['source_snapshot_sha256']=store['input']['source_sha256']
    report={'stage':'advanced_comparative_analysis','version':VERSION,'status':'PASS',
            'generated_utc':datetime.now(timezone.utc).isoformat(),'board':store['board'],'inputs':inputs,
            'counts':counts,'methodology':{'role_universe':'ENTIRE_VERIFIED_DATABASE',
                'stage6_dossiers_are_not_a_final_ranking':True,'rescue_audit_all_excluded_roles':True,
                'stage7_extraction_is_supplemental_not_mutation':True,'no_certified_skill_matches':True,
                'experience_requirements_not_automatically_satisfied':True,
                'work_history_is_unverified_resume_claims':True,'separate_logistics_and_professional_review':True,
                'no_final_five':True,'stage8_ai_handoff_must_include_stages5_6_7_8':True},
            'dossiers':dossiers,'extraction_findings':extraction_findings,
            'limitations':['No employer verification of job availability, location policy, relocation amounts, visa or clearance eligibility',
               'Stage 7 extraction is conservative; other requirements may exist in freeform prose',
               'Topic overlap, résumé assertions and an AI-assisted codebase do not prove independent competency',
               'Dates or listed credentials are not independently verified; years/seniority never auto-satisfied',
               'Full original descriptions and Stage 5/6 reports must be supplied alongside this report for AI review',
               'Not a quantified job-fit score and not a final top-five recommendation']}
    coverage={'stage':'coverage_audit','status':'PASS','inputs':inputs,'counts':{'all_roles':len(audit),
             'outside_deep_pool':len(rows)-len(dossiers),'actionable_revisit':len(rescue)},
             'all_roles':audit,'revisit_outside_pool':rescue,
             'rule':'Revisit candidates without pretending that they qualify or that all other roles were exhaustively semantically assessed'}
    matrix={'stage':'comparative_matrix','status':'PASS','inputs':inputs,'population':len(dossiers),
            'note':'Unranked; grouping is heuristic; complete details in advanced report',
            'entries':[{'id':d['id'],'title':d['title'],'family':d['family'],'job_url':d['job_url'],
                        'group':d['comparison_group'],'cautions':d['comparison_cautions'],
                        'geography':d['geography']['policy'],'requirements':len(d['expectations']),
                        'unresolved':sorted(set(f for r in d['expectations'] for f in r['unresolved_obligations'])),
                        'stage6_requirement_count':d['stage6_requirement_count']} for d in dossiers]}
    manifest={'stage':'stage7_pre_ai_manifest','status':'PASS','source_snapshot_sha256':store['input']['source_sha256'],
              'db_sha256':dbsha,'board':store['board'],'private_evidence_status':'UNVERIFIED_RESUME_CLAIMS',
              'prior_report_fingerprints':inputs,
              'stage8_expected_materials':['Stage 5 broad_analysis_report.json','Stage 5 deep_review_candidates.json',
                 'Stage 6 deep_analysis_report.json','Stage 6 deep_review_summary.json',
                 'Stage 7 advanced_analysis_report.json','Stage 7 coverage_audit.json',
                 'Stage 7 comparison_matrix.json','Stage 7 stage7_pre_ai_manifest.json',
                 'Stage 8 independent audit report','ALL 816 ORIGINAL DATABASE JOB DESCRIPTIONS WITH IDS',
                 'Optional user-approved private candidate evidence, expressly labeled unverified'],
              'no_ai_selection_yet':True,'ai_may_disagree_with_all_heuristic_groups':True,
              'checklist':['Audit all 816 roles','Confirm qualifications and private profile','Review 13 original Stage 6 extraction gaps and Stage 7 outcomes',
                           'Recheck current job posting status','Do not conflate remote metadata with Utah remote eligibility',
                           'Separate role fit from relocation','Human reviews five targets before applying']}
    return report,coverage,matrix,manifest,inputs


def markdown(report:dict,coverage:dict,matrix:dict)->str:
    n=report['counts']; out=['# ProofLoop Stage 7 — Advanced Comparative Analysis','',
      '**Status: PASS (analytical process only). No qualification certification and no final top five.**','',
      '## Scope','',f"- Entire role universe audited: **{n['corpus_roles']}**",
      f"- Detailed Stage 6 dossiers: **{n['stage6_dossiers']}**",
      f"- Outside-pool roles considered: **{n['stage5_excluded_roles']}**",
      f"- Outside-pool roles marked for re-review: **{n['rescue_review_candidates']}**",
      f"- Requirement review lines: **{n['stage7_review_lines']}** (Stage 6 had {n['stage6_lines']})",
      f"- Stage 6 missing sections recovered by supplemental headings: **{n['supplement_recovered_roles']}**",
      f"- Still without extracted qualification section: **{n['still_missing_sections']}**",
      f"- Embedded heading issues detected: **{n['embedded_heading_issues']}**",'',
      '## Comparison groups are NOT verified job fit or a ranking','', '| Group | Roles |','|---|---:|']
    out += [f'| {k} | {v} |' for k,v in n['comparison_groups'].items()]
    out += ['', '## Outstanding requirement flags','', '| Flag | Lines |','|---|---:|']
    out += [f'| {k} | {v} |' for k,v in n['unresolved_requirement_flags'].items()]
    out += ['','## Outside-pool candidates worth a second look','',
         'These were not deep reviewed in Stage 6. They require an independent requirements read before any comparison.','',
         '| Title | Stage 5 band | Reason |','|---|---|---|']
    for r in coverage['revisit_outside_pool'][:75]:
        out.append(f"| {safe_md(r['title'])} | {r['stage5_band']} | {safe_md(', '.join(r['review_reasons']))} |")
    out += ['','## First 100 Stage 6 candidate comparison records (unranked, original source order)','',
           '| Role | Group | Unverified requirements | Geography |','|---|---|---|---|']
    for d in matrix['entries']:
        out.append(f"| {safe_md(d['title'])} | {d['group']} | {safe_md(', '.join(d['unresolved']) or 'Human review needed')} | {d['geography']} |")
    out += ['', '## Stage 8 requirements','',
         'Do not hand AI only the Stage 7 comparison summary. Preserve all reports from Stages **5, 6, 7, and 8**, the full source text of every candidate, and the ability to inspect all 816 records.',
         'The AI must be allowed to challenge Stage 5 role exclusion, Stage 6 extraction and Stage 7 groupings.',
         'Private résumé-derived evidence must never be represented as independently verified.',
         '','## Boundaries','']
    out += ['- '+safe_md(x) for x in report['limitations']]
    return '\n'.join(out)+'\n'


def run(paths:dict,out:Path)->dict:
    if out.exists():raise ValueError('Output directory already exists; choose a new one')
    report,coverage,matrix,manifest,_=build(paths)
    # Stage 7 report fingerprints calculated over exact published text; manifest includes them.
    generated={
        'advanced_analysis_report.json':json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        'coverage_audit.json':json.dumps(coverage,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        'comparison_matrix.json':json.dumps(matrix,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        'advanced_analysis_report.md':markdown(report,coverage,matrix)}
    manifest['stage7_outputs_sha256']={name:sha256(txt.encode('utf-8')).hexdigest() for name,txt in generated.items()}
    generated['stage7_pre_ai_manifest.json']=json.dumps(manifest,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    out.mkdir(parents=True,exist_ok=False)
    try:
        for name,txt in generated.items():
            (out/name).write_text(txt,encoding='utf-8',newline='\n')
    except BaseException:
        for path in out.iterdir():
            if path.is_file():path.unlink()
        out.rmdir()
        raise
    return report


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('db','store','validation','broad','candidates','deep','deep-summary','evidence','output-dir'):
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args(argv)
    d={key.replace('-','_'):getattr(a,key.replace('-','_')) for key in ('db','store','validation','broad','candidates','deep','deep-summary','evidence')}
    # Canonical key 'deep_summary' consumed downstream only as dict key.
    try:
        result=run(d,a.output_dir)
    except (OSError,ValueError,KeyError,TypeError,sqlite3.Error) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);return 1
    c=result['counts'];print(f"PASS: Stage 7 audited {c['corpus_roles']} roles; compared {c['stage6_dossiers']} dossiers")
    print(f"Recovered {c['supplement_recovered_roles']} previously unparsed sections; {c['still_missing_sections']} still need review")
    print(f"Outside-pool roles flagged for revisit: {c['rescue_review_candidates']}")
    print('Output: '+str(a.output_dir))
    print('Reports: advanced_analysis_report.json/.md, coverage_audit.json, comparison_matrix.json, stage7_pre_ai_manifest.json')
    return 0

if __name__=='__main__':sys.exit(main())
