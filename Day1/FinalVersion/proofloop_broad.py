#!/usr/bin/env python3
"""ProofLoop Ashby Stage 5 (v0.5.0): evidence-labeled broad role analysis.

Read-only SQLite input; no network; report outputs are new, exclusive files.
This is discovery and triage, NOT qualification, eligibility, or role ranking.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import html

VERSION = '0.5.0'
MAX_DB = 600 * 1024 * 1024
REGEX_FLAGS = re.IGNORECASE

DOMAIN_PATTERNS = {
    'technical_support': [r'\btechnical support\b', r'\bsupport engineer(?:ing)?\b', r'\bit support\b', r'\bhelp desk\b', r'\bservice desk\b', r'\btroubleshoot(?:ing|s|ed)?\b'],
    'api_integration': [r'\bAPIs?\b', r'\bwebhooks?\b', r'\bREST(?:ful)?\b', r'\bAPI integration\b', r'\bauthentication\b'],
    'programming': [r'\bPython\b', r'\bJavaScript\b', r'\bPowerShell\b', r'\bSQL\b', r'\bsoftware engineer(?:ing)?\b', r'\bscripting\b'],
    'automation': [r'\bautomat(?:e|ed|es|ing|ion)\b', r'\bworkflow(?:s)?\b', r'\borchestrat(?:e|ion|ing)\b'],
    'systems_network': [r'\bnetwork(?:ing|s)?\b', r'\bDNS\b', r'\bidentity management\b', r'\bcloud infrastructure\b', r'\bdevice management\b', r'\boperating systems?\b'],
    'testing_data': [r'\btest(?:ing|s|ed)?\b', r'\bquality assurance\b', r'\bdata analysis\b', r'\bdatabases?\b', r'\bdebug(?:ging|ged)?\b'],
    'security_investigation': [r'\bsecurity engineering\b', r'\bincident response\b', r'\bthreat intelligence\b', r'\bfraud investigation\b', r'\bsecurity operations\b'],
    'documentation': [r'\bknowledge base\b', r'\btechnical documentation\b', r'\brunbooks?\b', r'\bSOPs?\b'],
}
HANDS_ON = [
    r'\btroubleshoot(?:ing|s|ed)?\b', r'\bdebug(?:ging|ged)?\b',
    r'\bbuild(?:ing)?\s+(?:tools?|systems?|software|applications?|integrations?|pipelines?)\b',
    r'\bdevelop(?:ing)?\s+(?:software|systems?|APIs?|tools?|automation)\b',
    r'\bwrite\s+(?:code|scripts?|SQL)\b', r'\bimplement(?:ing)?\s+(?:automation|APIs?|systems?|software)\b',
    r'\bmaintain(?:ing)?\s+(?:production\s+)?(?:systems?|software|infrastructure)\b',
    r'\bincident (?:response|triage|investigation)\b',
]
TECH_TITLE = [
    r'\b(?:IT|technical|customer|developer) support (?:specialist|engineer|technician|analyst)\b',
    r'\b(?:support|software|systems|security|infrastructure|platform|integration|data|QA) engineer\b',
    r'\b(?:IT|security|systems|network|technical support) (?:analyst|administrator|specialist)\b',
]
STRONG_SALES_TITLE = [r'\bsales\s+(?:representative|manager|director|executive|development)\b', r'\baccount executive\b', r'\baccount director\b', r'\bbusiness development (?:representative|manager|director)\b']
SALES_RESPONSIBILITIES = [
    r'\b(?:own|carry|meet|hit|achiev\w*)\s+(?:a\s+)?(?:revenue|sales)\s+(?:quota|target)s?\b',
    r'\bprospect(?:ing)?\s+(?:for\s+)?(?:new\s+)?(?:customers?|clients?|business)\b',
    r'\b(?:close|closing)\s+(?:customer\s+)?deals?\b',
    r'\b(?:own|manage|drive)\s+(?:the\s+)?sales cycle\b',
    r'\bpipeline generation\b', r'\b(?:manage|grow)\s+(?:a\s+)?book of business\b',
]
SALES_CONTEXT = [r'\bpre[- ]sales\b', r'\bgo[- ]to[- ]market\b', r'\bwork(?:ing)? with sales\b', r'\baccount management\b', r'\bcommission\b']
RELOCATION = [r'\b(?:offer|offers|offering|offered|provide|provides|providing|provided)\s+(?:[\w-]+\s+){0,3}relocation assistance\b', r'\brelocation assistance\s+(?:is\s+)?(?:available|provided|offered)\b', r'\brelocation package\b']
OFFICE_DAYS = [r'\b(?:hybrid work model of\s*)?(\d|one|two|three|four|five)\s+days?\s+(?:in the office|in office|on[- ]site)(?:\s+per week)?\b']
REMOTE_US = [r'\b(?:US|U\.S\.|United States)\s*[-–:]?\s*remote\b', r'\bremote (?:within|across|throughout)\s+(?:the\s+)?(?:US|U\.S\.|United States)\b']
QUAL_HEADINGS = [r'you might thrive in this role if', r'you might thrive in this role', r'we\s*(?:are)?\s*seeking someone with experience', r'what (?:we\s*are|we\s*\x27re|we\s*’re) looking for', r'qualifications', r'requirements', r'you will be successful if', r'nice to have', r'we expect you to']
ROLE_HEADINGS = [r'in this role[, ]+you will', r'you will be responsible for', r'what you\s*\x27ll do', r'what you\s*’ll do', r'responsibilities', r'about the role']
END_HEADINGS = [r'about openai', r'about the company', r'benefits', r'equal opportunity', r'background checks', r'applicant privacy', r'compensation']
YEARS = re.compile(r'\b(?:at least\s+|minimum\s+(?:of\s+)?)?(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|working|in\s+\w+)', re.I)
EDUCATION = [r'\bPh\.?D\.?\b', r'\bdoctorate\b', r'\b(?:bachelor|master)\x27?s?\s+degree\b', r'\bdegree or equivalent\b', r'\bequivalent (?:professional |practical )?experience\b']


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def jload(path):
    with path.open(encoding='utf-8-sig') as stream:
        return json.load(stream, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Invalid JSON constant: ' + x)))


def matches(text, patterns, limit=3):
    if not text: return []
    found = []
    for pat in patterns:
        for m in re.finditer(pat, text, REGEX_FLAGS):
            s = re.sub(r'\s+', ' ', text[max(0, m.start()-75):min(len(text), m.end()+100)]).strip()
            if s not in found: found.append(s)
            if len(found) >= limit: return found
    return found


def section(text, starts, ends):
    if not text: return '', 'missing'
    found = [(m.start(), m.end()) for p in starts for m in re.finditer(p, text, REGEX_FLAGS)]
    if not found: return '', 'heading_not_found'
    start, end_head = min(found)
    boundaries = [m.start() for p in ends for m in re.finditer(p, text[end_head:], REGEX_FLAGS)]
    stop = end_head + min(boundaries) if boundaries else len(text)
    return text[end_head:stop].strip(), 'heading_detected'


def role_sections(text):
    # Role duties end at qualification and employer-boilerplate headings.
    responsibilities, rmethod = section(text, ROLE_HEADINGS, QUAL_HEADINGS + END_HEADINGS)
    qualifications, qmethod = section(text, QUAL_HEADINGS, END_HEADINGS)
    return responsibilities, rmethod, qualifications, qmethod


def check_profile(profile):
    if not isinstance(profile, dict) or profile.get('schema_version') != 1: raise ValueError('Profile schema_version must be 1')
    allowed = {'schema_version','preferred_domains','exclude_sales','require_technical_core','allow_us_remote','allow_us_relocation','require_relocation_assistance','allow_non_us','max_deep_candidates'}
    if set(profile) - allowed: raise ValueError('Unknown profile keys: ' + ', '.join(sorted(set(profile)-allowed)))
    for name in ('exclude_sales','require_technical_core','allow_us_remote','allow_us_relocation','require_relocation_assistance','allow_non_us'):
        if type(profile.get(name)) is not bool: raise ValueError(name + ' must be boolean')
    domains = profile.get('preferred_domains')
    if not isinstance(domains, list) or not domains or len(set(domains)) != len(domains) or not all(isinstance(x,str) and x in DOMAIN_PATTERNS for x in domains):
        raise ValueError('preferred_domains must be unique, known domain labels')
    n = profile.get('max_deep_candidates')
    if type(n) is not int or not 1 <= n <= 300: raise ValueError('max_deep_candidates must be 1..300')
    return profile


def get_locations(role, secondary):
    all_names = [role['location'] or ''] + [s.get('location') or '' for s in secondary]
    primary_address = json.loads(role['address_json'])
    addr = [primary_address] + [s.get('address') for s in secondary]
    countries = []
    for value in addr:
        if isinstance(value, dict):
            post = value.get('postalAddress') or {}
            if isinstance(post, dict) and isinstance(post.get('addressCountry'), str): countries.append(post['addressCountry'])
    return all_names, countries


def positive_relocation_evidence(body):
    # Do not count obvious negations such as "do not offer relocation assistance".
    result=[]
    for pattern in RELOCATION:
        for match in re.finditer(pattern, body, REGEX_FLAGS):
            prior=body[max(0,match.start()-45):match.start()].lower()
            if re.search(r"(?:do\s+not|does\s+not|don't|doesn't|will\s+not|cannot|can't|no|without)\s+(?:\w+\s+){0,4}$",prior):
                continue
            evidence=re.sub(r'\s+', ' ', body[max(0,match.start()-75):match.end()+100]).strip()
            if evidence not in result: result.append(evidence)
            if len(result)>=2: return result
    return result


def location_evidence(role, secondary, body, profile):
    locs, countries = get_locations(role, secondary)
    is_us = any(c.lower() in ('united states','us','usa') for c in countries)
    has_non_us = any(c.lower() not in ('united states','us','usa') for c in countries)
    remote_place = bool(matches(' | '.join(locs), REMOTE_US, 1))
    remote_words = matches(body, REMOTE_US, 2)
    reloc = positive_relocation_evidence(body)
    days = matches(body, OFFICE_DAYS, 2)
    workplace, remote_flag = role['workplace_type'], None if role['is_remote'] is None else bool(role['is_remote'])
    if remote_place and workplace == 'Remote' and not days:
        category = 'US_REMOTE_ADVERTISED'
    elif remote_place and not days:
        category = 'US_REMOTE_LOCATION_REVIEW'
    elif workplace == 'Remote' and is_us and not days:
        category = 'US_REMOTE_ELIGIBILITY_UNCONFIRMED'
    elif is_us and reloc:
        category = 'US_RELOCATION_ASSISTANCE_STATED'
    elif is_us and (workplace in ('Hybrid','OnSite') or days):
        category = 'US_OFFICE_RELOCATION_NOT_STATED'
    elif is_us:
        category = 'US_WORK_ARRANGEMENT_UNKNOWN'
    elif has_non_us:
        category = 'NON_US_LOCATIONS_ONLY'
    else:
        category = 'LOCATION_UNKNOWN'
    # A boolean API remote flag never by itself establishes Utah-remote eligibility.
    if category == 'US_REMOTE_ADVERTISED':
        policy = 'REVIEW_ELIGIBILITY' if profile['allow_us_remote'] else 'OUTSIDE_PROFILE'
    elif category in ('US_REMOTE_LOCATION_REVIEW','US_REMOTE_ELIGIBILITY_UNCONFIRMED'):
        policy = 'REVIEW_ELIGIBILITY' if profile['allow_us_remote'] else 'OUTSIDE_PROFILE'
    elif category == 'US_RELOCATION_ASSISTANCE_STATED':
        policy = 'RELOCATION_DEPENDENT' if profile['allow_us_relocation'] else 'OUTSIDE_PROFILE'
    elif category.startswith('US_'):
        policy = ('RELOCATION_NOT_CONFIRMED' if profile['allow_us_relocation'] and profile['require_relocation_assistance']
                  else 'REVIEW_ELIGIBILITY' if profile['allow_us_relocation'] else 'OUTSIDE_PROFILE')
    elif category == 'NON_US_LOCATIONS_ONLY':
        policy = 'REVIEW_ELIGIBILITY' if profile['allow_non_us'] else 'OUTSIDE_PROFILE'
    else:
        policy = 'REVIEW_ELIGIBILITY'
    return {'category':category,'policy':policy,'primary_location':role['location'], 'secondary_locations':locs[1:],
            'countries':sorted(set(countries)),'workplace_type':workplace,'is_remote':remote_flag,
            'remote_us_location':remote_place,'remote_text_evidence':remote_words,
            'relocation_evidence':reloc,'office_requirement_evidence':days,
            'remote_metadata_conflict': remote_flag is True and workplace == 'Hybrid'}


def classify(role, secondary, profile):
    # Restrict description-based classifications to the company-specific pre-boilerplate portion.
    text = role['description_plain'] or ''
    markers = [m.start() for p in END_HEADINGS[:2] for m in re.finditer(p, text, REGEX_FLAGS)]
    body = text[:min(markers)] if markers else text
    duties, duties_method, quals, quals_method = role_sections(body)
    title, team = role['title'] or '', role['team'] or ''
    sale_title = matches(title, STRONG_SALES_TITLE)
    sale_role = matches(duties, SALES_RESPONSIBILITIES)
    sale_context = matches(title+' '+duties, SALES_CONTEXT)
    if sale_title or team.strip().lower() == 'sales' or sale_role:
        sales_label = 'SALES_PRIMARY_EVIDENCE'
    elif sale_context:
        sales_label = 'SALES_CONTEXT_REVIEW'
    else:
        sales_label = 'NO_STRONG_SALES_EVIDENCE'
    technical_title = matches(title, TECH_TITLE, 2)
    technical_duties = matches(duties, HANDS_ON, 4)
    if technical_title or technical_duties:
        tech_label = 'HANDS_ON_EVIDENCE'
    elif duties_method == 'heading_not_found':
        tech_label = 'RESPONSIBILITIES_UNPARSED'
    else:
        tech_label = 'TECHNICAL_CORE_UNCONFIRMED'
    domain_text = title+'\n'+duties+'\n'+quals
    domains = {domain: hits for domain, pats in DOMAIN_PATTERNS.items() if (hits:=matches(domain_text,pats,2))}
    preferred = sorted(set(domains) & set(profile['preferred_domains']))
    loc = location_evidence(role, secondary, body, profile)
    requirements_text = quals if quals_method == 'heading_detected' else ''
    year_mentions = matches(requirements_text, [YEARS.pattern], 5)
    degree_mentions = matches(requirements_text, EDUCATION, 4)
    # No automatic required/preferred labels or résumé fit claims.
    blockers=[]
    if profile['exclude_sales'] and sales_label == 'SALES_PRIMARY_EVIDENCE': blockers.append('sales_primary')
    if profile['require_technical_core'] and tech_label == 'TECHNICAL_CORE_UNCONFIRMED': blockers.append('technical_core_unconfirmed')
    if loc['policy'] == 'OUTSIDE_PROFILE': blockers.append('geography_outside_profile')
    if loc['policy'] == 'RELOCATION_NOT_CONFIRMED': blockers.append('relocation_support_unconfirmed')
    review_flags=[]
    if duties_method != 'heading_detected': review_flags.append('responsibilities_heading_missing')
    if quals_method != 'heading_detected': review_flags.append('qualification_heading_missing')
    if sales_label == 'SALES_CONTEXT_REVIEW': review_flags.append('sales_context_ambiguous')
    if loc['remote_metadata_conflict']: review_flags.append('remote_true_but_hybrid')
    if loc['policy'] in ('REVIEW_ELIGIBILITY','RELOCATION_DEPENDENT','RELOCATION_NOT_CONFIRMED'): review_flags.append('location_or_relocation_confirmation_required')
    if year_mentions: review_flags.append('experience_duration_requires_human_interpretation')
    if degree_mentions: review_flags.append('education_requirement_requires_human_interpretation')
    if not preferred: review_flags.append('no_preferred_domain_evidence')
    critical = {'sales_primary','technical_core_unconfirmed','geography_outside_profile'}
    if any(b in critical for b in blockers):
        band='HOLD_WITH_REASONS'
    elif preferred and tech_label == 'HANDS_ON_EVIDENCE' and loc['policy'] in ('REVIEW_ELIGIBILITY','RELOCATION_DEPENDENT'):
        band='DEEP_REVIEW_PRIORITY'
    elif preferred and tech_label == 'HANDS_ON_EVIDENCE' and loc['policy']=='RELOCATION_NOT_CONFIRMED':
        band='STRETCH_OR_LOGISTICS_REVIEW'
    else:
        band='MANUAL_REVIEW'
    seniority = ('PRINCIPAL_STAFF' if re.search(r'\b(principal|staff|distinguished)\b',title,re.I) else
                 'SENIOR_LEAD' if re.search(r'\b(senior|lead|director|head of|chief)\b',title,re.I) else
                 'UNSPECIFIED_OR_OTHER')
    return {
        'seniority_title_signal':seniority,
        'id':role['id'], 'title':title, 'team':team, 'department':role['department'],
        'job_url':role['job_url'], 'apply_url':role['apply_url'], 'source_index':role['source_index'],
        'snapshot_sha256':role['source_sha256'], 'published_at':role['published_at'],
        'band':band,'blockers':blockers,'review_flags':review_flags,
        'location':loc,
        'sales':{'classification':sales_label,'title_evidence':sale_title,'responsibility_evidence':sale_role,'context_evidence':sale_context},
        'technical':{'classification':tech_label,'title_evidence':technical_title,'responsibility_evidence':technical_duties, 'domains':domains,'preferred_domains_detected':preferred},
        'qualification_screen':{'section_method':quals_method,'years_evidence':year_mentions,'education_evidence':degree_mentions,
                                'required_vs_preferred':'NOT_CLASSIFIED_AT_BROAD_STAGE'},
        'responsibility_section_method':duties_method,
        'compensation_summary': json.loads(role['compensation_json']).get('compensationTierSummary'),
        'compensation_visibility':None if role['should_display_compensation'] is None else bool(role['should_display_compensation'])
    }


def choose_review(dossiers, maximum):
    # Broad triage deliberately reserves space for technically relevant jobs
    # with relocation uncertainty, without asserting that relocation is feasible.
    # Seniority is a caution marker, not proof of ineligibility.
    def order(d):
        loc=d['location']['category']
        loc_n=(0 if loc=='US_REMOTE_ADVERTISED' else
               1 if loc=='US_RELOCATION_ASSISTANCE_STATED' else
               2 if loc.startswith('US_REMOTE') else 3)
        title_n=0 if matches(d['title'],TECH_TITLE,1) else 1
        senior_n={'UNSPECIFIED_OR_OTHER':0,'SENIOR_LEAD':1,'PRINCIPAL_STAFF':2}[d['seniority_title_signal']]
        return (loc_n,title_n,senior_n,-len(d['technical']['preferred_domains_detected']),
                d['title'].casefold(),d['id'])
    primary=sorted([d for d in dossiers if d['band']=='DEEP_REVIEW_PRIORITY'],key=order)
    stretch=sorted([d for d in dossiers if d['band']=='STRETCH_OR_LOGISTICS_REVIEW'],key=order)
    manual=sorted([d for d in dossiers if d['band']=='MANUAL_REVIEW'],key=order)
    quota_primary=max(1,round(maximum*0.7))
    first=primary[:quota_primary]
    remaining=maximum-len(first)
    chosen=first+stretch[:remaining]
    if len(chosen)<maximum:
        chosen+=primary[len(first):maximum-len(chosen)+len(first)]
    if len(chosen)<maximum:
        chosen+=stretch[len(stretch[:remaining]):len(stretch[:remaining])+(maximum-len(chosen))]
    if len(chosen)<maximum:
        chosen+=manual[:maximum-len(chosen)]
    return [{'id':d['id'],'title':d['title'],'band':d['band'],'seniority_title_signal':d['seniority_title_signal'],
             'review_flags':d['review_flags'], 'location_policy':d['location']['policy'],
             'job_url':d['job_url'],'source_index':d['source_index']} for d in chosen]


def md_report(r):
    overview=r['counts']
    out=['# ProofLoop Stage 5 — Broad Role Analysis','',f"- **Status:** {r['status']}",f"- **Board:** `{r['board']}`",
         f"- **Analyzed:** {overview['total']} postings",f"- **Database SHA-256:** `{r['inputs']['db_sha256']}`",
         f"- **Profile SHA-256:** `{r['inputs']['profile_sha256']}`",f"- **Review pool:** {len(r['deep_review_pool'])} (maximum {r['max_deep_candidates']})",'',
         '## Triage bands','', '| Band | Count |','|---|---:|']
    out += [f'| {k} | {v} |' for k,v in sorted(overview['bands'].items())]
    out += ['', '## Location classifications','', '| Category | Count |','|---|---:|']
    out += [f'| {k} | {v} |' for k,v in sorted(overview['locations'].items())]
    out += ['', '## Sales and technical classifications','', '| Classification | Count |','|---|---:|']
    out += [f'| {k} | {v} |' for k,v in sorted(overview['sales'].items())]
    out += [f'| {k} | {v} |' for k,v in sorted(overview['technical'].items())]
    out += ['', '## Candidate review queue (not a ranking)','', '| Job | Band | Source |','|---|---|---|']
    for p in r['deep_review_pool']:
        title=html.escape(p['title'].replace('|','\\|').replace('\n',' '))
        out.append(f"| {title} | {p['band']} | [posting]({p['job_url']}) |")
    out += ['', '## Boundaries','',
            'All source roles are preserved in the JSON report; the review queue is a deterministic triage subset, not the five best opportunities.',
            'An API isRemote=true flag does **not** prove Utah-remote eligibility, especially where workplaceType=Hybrid.',
            'Relocation wording is an advertisement, not confirmed personal financial coverage.',
            'Sales and technical classifications are heuristic and contain false positive/negative risk.',
            'Qualification section extraction is incomplete when headings vary; experience years are not automatically required or satisfied.',
            'This stage does not compare a verified résumé or select final application targets.','']
    return '\n'.join(out)


def run(db, store_report, validation_report, profile_path, output_dir):
    paths=(db,store_report,validation_report,profile_path)
    for path in paths:
        if not path.is_file(): raise ValueError('Missing input: '+path.name)
    if db.stat().st_size > MAX_DB: raise ValueError('Database exceeds safety limit')
    if output_dir.exists(): raise FileExistsError('Output exists; choose new output directory: '+str(output_dir))
    profile=check_profile(jload(profile_path))
    store=jload(store_report); validation=jload(validation_report)
    digest=sha(db)
    if store.get('status')!='PASS' or validation.get('status')!='PASS' or validation.get('failed')!=0 or validation.get('passed')!=24:
        raise ValueError('Store and Stage 4 reports must indicate validated success (24/24)')
    if store.get('database',{}).get('sha256')!=digest or validation.get('files',{}).get('sqlite_sha256')!=digest:
        raise ValueError('DB SHA does not match the store and independent validation reports')
    if validation.get('files',{}).get('jsonl_sha256')!=store.get('input',{}).get('jsonl_sha256'):
        raise ValueError('Upstream JSONL fingerprints disagree')
    with closing(sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True)) as conn:
        conn.row_factory=sqlite3.Row
        integrity=conn.execute('PRAGMA integrity_check').fetchone()[0]
        fks=conn.execute('PRAGMA foreign_key_check').fetchall()
        if integrity!='ok' or fks: raise ValueError('Database integrity/foreign key failure')
        tables={x[0] for x in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {'roles','secondary_locations','compensation_tiers','compensation_components','compensation_summary_components'}.issubset(tables):
            raise ValueError('Unexpected Stage 3 database schema')
        rows=[dict(r) for r in conn.execute('SELECT * FROM roles ORDER BY source_index')]
        children=defaultdict(list)
        for row in conn.execute('SELECT role_id, location, address_json FROM secondary_locations ORDER BY role_id, ordinal'):
            children[row[0]].append({'location':row[1],'address':json.loads(row[2])})
    if len(rows)!=store.get('input',{}).get('records') or len(rows)!=validation.get('details',{}).get('source_records'):
        raise ValueError('Database and source counts disagree')
    boards={row['board'] for row in rows}
    if len(boards)!=1 or next(iter(boards))!=store.get('board') or store.get('board')!=validation.get('details',{}).get('board', store.get('board')):
        raise ValueError('Board identity mismatch')
    dossiers=[classify(row,children[row['id']],profile) for row in rows]
    counts={'total':len(dossiers),'bands':dict(Counter(d['band'] for d in dossiers)),
            'locations':dict(Counter(d['location']['category'] for d in dossiers)),
            'location_policies':dict(Counter(d['location']['policy'] for d in dossiers)),
            'sales':dict(Counter(d['sales']['classification'] for d in dossiers)),
            'technical':dict(Counter(d['technical']['classification'] for d in dossiers)),
            'review_flags':dict(Counter(f for d in dossiers for f in d['review_flags']))}
    pool=choose_review(dossiers,profile['max_deep_candidates'])
    report={'stage':'broad_analysis','program_version':VERSION,'status':'PASS',
            'generated_at_utc':datetime.now(timezone.utc).isoformat(), 'board': next(iter(boards)),
            'inputs':{'db_sha256':digest,'store_report_sha256':sha(store_report),
                      'validation_report_sha256':sha(validation_report),'profile_sha256':sha(profile_path),
                      'source_snapshot_sha256':store['input']['source_sha256']},
            'max_deep_candidates':profile['max_deep_candidates'], 'counts':counts,
            'methodology':{'triage_is_not_ranking':True,'human_confirmation_required':True,
                           'profile_policy':{k:profile[k] for k in profile if k!='preferred_domains'},
                           'preferred_domains':profile['preferred_domains']},
            'deep_review_pool':pool,'roles':dossiers,
            'limitations':['Snapshot presence is not current job availability','Remote eligibility and relocation funding require confirmation',
                           'Sales and technical rules are heuristic','No numerical experience-duration fit assertion',
                           'Role requirements and candidate experience not yet matched']}
    # Preflight before writing; do not replace existing directories.
    output_dir.mkdir(parents=True,exist_ok=False)
    try:
        (output_dir/'broad_analysis_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (output_dir/'broad_analysis_report.md').write_text(md_report(report),encoding='utf-8')
        (output_dir/'deep_review_candidates.json').write_text(json.dumps({'board':report['board'],'database_sha256':digest,
             'candidate_ids':[d['id'] for d in pool], 'candidates':pool},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    except BaseException:
        for file in output_dir.glob('*'):
            if file.is_file(): file.unlink()
        output_dir.rmdir()
        raise
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--store-report',type=Path,required=True)
    p.add_argument('--validation-report',type=Path,required=True)
    p.add_argument('--profile',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args(argv)
    try:
        result=run(args.db,args.store_report,args.validation_report,args.profile,args.output_dir)
    except (OSError, ValueError, sqlite3.Error) as e:
        print(f'FAIL: {e}', file=sys.stderr)
        return 1
    print(f"PASS: analyzed {result['counts']['total']} jobs; {len(result['deep_review_pool'])} for deep review")
    print(f"Bands: {result['counts']['bands']}")
    print(f'Output: {args.output_dir}')
    print('Reports: broad_analysis_report.json and .md; deep_review_candidates.json')
    return 0

if __name__ == '__main__':
    sys.exit(main())
