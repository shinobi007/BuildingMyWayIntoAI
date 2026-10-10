# Attempt #001 — OpenAI

## Building My Way Into AI / ProofLoop

This document records the first real company-level attempt in **Building My Way Into AI**.

Attempt #001 is important because it is where the project stopped being only a technical exercise and became part of an actual job-search decision.

The user did **not** manually choose the final three roles.

Instead, the process worked like this:

```text
user supplied:
    goals
    constraints
    relocation reality
    no-sales rule
    technical-role requirement
    resume / work-history evidence

system supplied:
    role ingestion
    normalization
    reconciliation
    database analysis
    location analysis
    sales filtering
    technical-role analysis
    qualification mapping
    evidence-gap analysis
    finalist comparison

assistant performed:
    final comparative judgment
    final top-3 selection

user then:
    reviewed the result
    accepted it
    locked the three targets
```

That distinction matters.

Attempt #001 is therefore not a record of a person manually browsing hundreds of jobs and picking favorites.

It is a record of **criteria-guided, evidence-based analysis producing a recommendation that the user then adopted**.

---

## Audit note — accepted shortlist versus verified qualifications

This document preserves the **original user-approved target selections** and the analyses that led to them. The appended and inline audit notes distinguish historical model outputs from the more cautious interpretation reached by independently reading the frozen postings and the v0.16 classifier code. This is not a second selection and does not retroactively change the 2026-10-08 approval.

The three roles are **selected targets**, not documented application submissions. Posting status, interview outcomes, specific relocation support terms, and present-day availability are **not established** by these archived files.

Related: [README](../README.md) · [Data model](data_model.md) · [Validation](validation_and_testing.md) · [Changelog](../CHANGELOG.md).

---

# 1. Attempt Identity

```text
Attempt:    #001
Company:    OpenAI
Primary product focus: ChatGPT / OpenAI platform
Status:     TARGETS SELECTED
Target count: 3
```

Canonical targets:

```text
001-A — IT Support Specialist
001-B — Dedicated Support Engineer - San Francisco
001-C — AI Support Engineer - San Francisco
```

The final three were selected after analysis of the full current role population, not from an arbitrary shortlist.

---

# 2. Why "Attempt" Instead of "Application"

The project originally assumed:

```text
Application #001
```

would mean:

```text
one company
one role
one application
```

That proved too artificial.

A real job search often involves multiple related roles at the same company at the same time.

The model was therefore changed to:

```text
Attempt #001 — OpenAI
    │
    ├── Target 001-A
    ├── Target 001-B
    └── Target 001-C
```

An **Attempt** is the broader company/opportunity campaign.

A **Target** is a specific role inside that attempt.

This allows one company attempt to include several strategically related applications without pretending each application is an unrelated project.

---

# 3. What the User Actually Controlled

The selection process was guided by user-defined constraints rather than an opaque automated score.

The user provided the important decision criteria.

Those included:

- **No sales**
- The role must contain a **real technical component**
- Strong preference for work connected to:
  - IT
  - support engineering
  - technical support
  - systems
  - automation
  - APIs
  - integrations
  - QA / UAT
  - technical operations
  - security / investigations where genuinely plausible
- Current location should not automatically disqualify a role
- Relocation is possible **only if the employment path makes relocation financially realistic**
- Employer-supported relocation is therefore materially different from "move first and hope"
- Remote work would be valuable, but remote metadata must be interpreted carefully
- The final role should be plausible based on actual evidence rather than title similarity alone
- A stretch can be acceptable if the gaps are bounded and defensible
- Missing ability and missing evidence should not be treated as the same thing

The user also supplied the résumé used as the primary evidence source.

---

# 4. Candidate Evidence Supplied by the User

The résumé establishes a work-history pattern centered on:

```text
technical support
Tier 1–3 troubleshooting
CRM / SaaS systems
Jira
Microsoft 365
DNS
workflow automation
REST APIs
Zapier
ticketing / escalation
documentation
UAT
bug tracking
user feedback
customer communication
```

The strongest directly documented experience includes:

## Zion HealthShare

Role:

```text
Billing & Systems Specialist
11/2024 – 05/2025
```

Documented work includes:

```text
templated communication automation
CRM ledger troubleshooting
user access troubleshooting
reimbursement workflow troubleshooting
internal SOPs
policy documentation
workflow guides
high-volume ticket management
```

## Baam LLC

Role:

```text
IT Support & Systems Specialist
06/2022 – 06/2024
```

Documented work includes:

```text
Tier 1–3 technical support
CRM troubleshooting
DNS
Jira
Microsoft 365
SaaS platforms
Jira Service Desk administration
custom workflows
SLAs
automation rules
escalation paths
Zapier automation
REST APIs
1,000+ SOPs / tooltips / KB / training documents
UAT
bug tracking
workflow optimization
end-user feedback
```

## Vivint SmartHome

Role:

```text
Technical Agent
07/2016 – 02/2018
```

Documented work includes:

```text
smart-home technical support
routers
firmware
sensors
mobile apps
remote access
system integration
device troubleshooting
network troubleshooting
software troubleshooting
```

The résumé also lists programming / scripting technologies including:

```text
Python
JavaScript
SQL
PowerShell
Bash
HTML/CSS
REST APIs
webhooks
```

The analysis intentionally treats many of those as:

```text
RESUME_SKILL_CLAIM
```

rather than automatically upgrading them to:

```text
years of professional production engineering
```

That distinction was important in the final role selection.

---

# 5. What the User Did Not Do

For transparency, the user did **not**:

```text
manually inspect all 815 current roles
assign numeric scores to every posting
choose the final top three directly
hand-classify every qualification
manually resolve every remote-location contradiction
```

The user defined the objective and supplied the evidence.

The system performed the large-scale role analysis.

The assistant then made the final comparative recommendation.

The user accepted the result and locked the targets.

This is closer to:

```text
human-defined objective
        +
machine-assisted exhaustive analysis
        +
assistant judgment
        +
human acceptance
```

than:

```text
automated job picker
```

or:

```text
manual browsing
```

---

# 6. Starting Population

The original HTML pipeline contained:

```text
817 roles
```

The frozen Ashby API snapshot contained:

```text
815 roles
```

Reconciliation produced:

```text
matched:      814
HTML-only:      3
API-only:       1
union:         818
```

For current-role selection, the system used:

```text
present_in_api = 1
```

which produced:

```text
815 current API roles
```

This became the role-selection population.

---

# 7. Broad Analysis — v0.15

The first defensible role-selection battery was:

```text
proofloop_role_analysis_v0_15.py
```

It operated against:

```text
proofloop_enriched.db
```

in read-only mode.

The recorded run reported:

```text
Current API roles:           815
US-Remote anywhere:           44
Strong US-Remote:             20
Relocation-supported US:     250
Strong sales exclusions:      84
Sales context review:        210
Deep-review pool emitted:     75
RESULT: PASS
```

The purpose of this stage was not to choose the winner.

Its purpose was to make the landscape tractable.

---

# 8. v0.15 Guardrails

The v0.15 report explicitly preserved several important rules.

```text
No role is selected solely by the battery.

Strong sales evidence and contextual sales evidence are separate.

US - Remote in a secondary location is not automatically remote permission.

Relocation assistance is not the same as permission to begin remotely.

Experience and education language should be read in qualification context.

Resume/evidence overlap is a discovery aid, not a fit score.

Compensation must preserve interval and currency.
```

This mattered because the source metadata contained real contradictions.

---

# 9. Location Discovery

One of the strongest findings was that:

```text
is_remote = 1
```

could not safely mean:

```text
remote from Utah
```

The current population included:

```text
509 roles:
is_remote = 1
workplace_type = Hybrid
```

while only:

```text
21 roles
```

were structured as:

```text
workplace_type = Remote
```

The final location analysis therefore used:

```text
primary location
secondary locations
workplace_type
is_remote (retained in evidence; not directly evaluated by v0.15 classify_location() branches)
description wording
office-days requirement
relocation wording
```

rather than one remote flag.

---

# 10. Sales Filtering

The user's rule was:

```text
NO SALES
```

The first role-analysis version generated false positives.

For example:

```text
commission
```

could match:

```text
commissioning
```

v0.15 corrected this by separating:

```text
EXCLUDE_STRONG_SALES
```

from:

```text
REVIEW_SALES_CONTEXT
```

and:

```text
NO_SALES_SIGNAL_FOUND
```

This allowed sales-adjacent technical work to remain reviewable without allowing real sales roles through the hard filter.

---

# 11. Technical-Role Filtering

The user did not want a role selected merely because it was at an AI company.

A role needed a meaningful technical component.

The broad analysis therefore measured technical signals such as:

```text
hands-on troubleshooting
systems / infrastructure
APIs / integrations
coding / scripting
automation
testing / evaluation
technical support
security investigation
```

This became important later when an automatically strong candidate turned out to have:

```text
technical_core = NONE_DETECTED
```

and was rejected during final review.

---

# 12. Deep Analysis — v0.16

The second-stage analysis was:

```text
role_deep_analysis.py
```

corresponding to v0.16.

It consumed:

```text
proofloop_role_analysis_report_v0_15.json
proofloop_enriched.db
```

Before deeper analysis, it verified:

```text
baseline roles:          815
database current roles:  815
role IDs exact match:    True
SQLite integrity:        ok
```

The recorded funnel was:

```text
815 baseline roles
224 deep-analysis candidates
30 decision-review roles
```

The report explicitly stated that it did **not** select the final top five automatically.

---

# 13. Evidence Mapping

v0.16 compared individual posted qualifications against evidence tiers.

The tiers were:

```text
DIRECT_WORK_EVIDENCE
RESUME_SKILL_CLAIM
ADJACENT_EVIDENCE
NOT_EVIDENCED
UNKNOWN
```

Individual requirements could then be classified as:

```text
DIRECT_MATCH
CLAIMED_SKILL_MATCH
ADJACENT_MATCH
MODERATE_GAP
MAJOR_GAP
UNCLASSIFIED_REQUIREMENT
```

This made the final comparison much more useful than raw keyword overlap.

---

## 13.1 Complete v0.16 candidate-band counts and selection-path nuance

The **224** v0.16 deep candidates were distributed as: `A_TOP5_REVIEW` **1**, `B_SERIOUS_REVIEW` **48**, `C_STRETCH_REVIEW` **122**, `C_REQUIREMENTS_INCOMPLETE` **23**, and `D_BACKGROUND` **30**. The separate **30-role decision-review pool** must not be confused with the `D_BACKGROUND` band.

The v0.16 candidate population contains all **75** v0.15 deep-review roles **plus 149 additional candidates**. 001-A was in the earlier shortlist, while 001-B and 001-C were added through the expanded deep-candidate selection. All three ultimately appear in the 30-role decision-review pool. This broadening materially affected what could be recommended.

---

# 14. Why the Automatic Ranking Was Not the Final Decision

The deepest analysis still stopped before final selection.

That was intentional.

A concrete example was:

```text
Product Engagement Manager, User Operations
```

which received:

```text
A_TOP5_REVIEW
```

from the rule-based funnel.

But manual inspection showed:

```text
technical_core = NONE_DETECTED
```

and the work emphasized:

```text
team leadership
product launch coordination
performance management
product enablement
```

That conflicted with the user's technical-role requirement.

The role was therefore not selected.

This is a useful demonstration of why:

```text
transparent automation
+
manual comparative reasoning
```

was preferable to:

```text
take highest score
```

---

# 15. Final Selection Method

After the 30-role review pool was produced, the assistant performed the final comparative analysis.

The comparison considered:

```text
actual work content
direct résumé evidence
adjacent evidence
unproven requirements
seniority burden
location feasibility
relocation support
remote ambiguity
sales risk
technical depth
ability to create bounded proof
whether a gap was realistically defensible
```

The assistant then selected the final top three.

The user did not instruct the assistant to choose those specific roles.

The user instructed the assistant to:

```text
exhaust the available evidence
give the final top three
```

The user then accepted the recommendation and locked the URLs.

---

# 16. Final Target 001-A

# IT Support Specialist

Team:

```text
IT
```

Ashby ID:

```text
49ae54dc-3d33-4107-8112-63fac1ee86ca
```

Apply URL:

```text
https://jobs.ashbyhq.com/openai/49ae54dc-3d33-4107-8112-63fac1ee86ca/application
```

Primary structured location:

```text
Seattle
```

Additional listed locations:

```text
Washington, DC
San Francisco
London, UK
```

Work arrangement:

```text
OnSite
5 days in office per week
```

Relocation:

```text
explicit relocation assistance
```

Sales classification:

```text
NO_SALES_SIGNAL_FOUND
```

Technical core:

```text
HIGH
```

---

# 17. Why 001-A Was Selected

This role had the best overall balance of:

```text
plausibility
technical relevance
documented work-history overlap
clear non-sales identity
relocation feasibility
lack of an explicit detected years floor
```

The actual work includes:

```text
frontline IT support
hardware troubleshooting
software troubleshooting
network troubleshooting
support-process improvement
repeatable workflows
cross-functional technical communication
vendor coordination
equipment management
```

Those responsibilities map closely to the résumé's support and systems history.

---

# 18. 001-A Evidence Strengths

The résumé supports substantial adjacent/direct evidence in areas including:

```text
technical support
troubleshooting
Microsoft 365
SaaS environments
Jira / Atlassian
networking / DNS
workflow improvement
vendor/process coordination
automation
technical communication
```

The role also lists scripting / low-code automation as added value, which aligns with documented Zapier/API automation and listed scripting skills.

---

# 19. 001-A Main Gaps

The deep analysis identified the largest unproven area as:

```text
audiovisual / high-production event technology
```

Additional weaker areas include depth with:

```text
macOS
Jamf
Intune
identity/device-management ecosystems
```

These are real gaps.

However, they are narrower than the specialized engineering gaps found in many other OpenAI roles.

---

# 20. 001-A Location Reality

This role is not remote.

It requires:

```text
5 days onsite
```

However, the posting explicitly offers:

```text
relocation assistance
```

That made it materially more realistic than an onsite role that assumes the candidate can independently finance relocation before employment.

This factor was important in ranking it first overall.

---

# 21. Final Target 001-B

# Dedicated Support Engineer - San Francisco

Team:

```text
Support Delivery
```

Department:

```text
User Operations
```

Ashby ID:

```text
2348230a-295f-434d-9b16-653e01ddbd0b
```

Apply URL:

```text
https://jobs.ashbyhq.com/openai/2348230a-295f-434d-9b16-653e01ddbd0b/application
```

Primary location:

```text
San Francisco
```

Work arrangement:

```text
Hybrid
```

Relocation evidence:

```text
not explicit in captured posting
```

Sales classification:

```text
REVIEW_SALES_CONTEXT
```

Technical core:

```text
HIGH
```

---

# 22. Why 001-B Was Selected

If ranked only by work-content alignment, this role may be the strongest of the three.

Its responsibilities center on:

```text
complex technical support
API failures
integration problems
authentication errors
unexpected product behavior
performance degradation
production incidents
logs
system behavior
error reproduction
hypothesis testing
root-cause isolation
technical escalation
incident ownership
customer technical communication
```

This aligns directly with the direction of the existing support/systems background.

---

# 23. 001-B Requirement Evidence

v0.16 found:

```text
5 direct qualification matches
1 major gap area
1 moderate gap area
```

Directly aligned areas included:

```text
hands-on technical support
complex troubleshooting
API / integration work
incident coordination
root-cause analysis
technical customer communication
support-system improvement
```

---

# 24. 001-B Main Gap

The strongest unproven requirement is depth across:

```text
distributed systems
cloud infrastructure
enterprise integrations
expert-level API troubleshooting
```

The role also expects the ability to write scripts or code to:

```text
reproduce issues
interrogate systems
automate repetitive work
improve internal tooling
```

The résumé lists relevant scripting languages, but the analysis intentionally does not treat that as proof of deep production engineering experience.

That is why scripting was treated as a smaller but still real evidence gap.

---

# 25. 001-B Location Risk

The major practical problem is location.

The captured posting is:

```text
San Francisco
Hybrid
```

with no explicit relocation assistance identified by the analysis.

The role therefore remains viable as an application target, but location is an unresolved dependency.

The system deliberately does **not** assume that:

```text
is_remote = 1
```

means the role can be performed from Utah.

---

# 26. Final Target 001-C

# AI Support Engineer - San Francisco

Team:

```text
Support Delivery
```

Department:

```text
User Operations
```

Ashby ID:

```text
1a979fd4-1bce-484e-a416-aed2810677a6
```

Apply URL:

```text
https://jobs.ashbyhq.com/openai/1a979fd4-1bce-484e-a416-aed2810677a6/application
```

Primary location:

```text
San Francisco
```

Relocation evidence:

```text
not explicit in captured posting
```

Technical core:

```text
HIGH
```

---

# 27. Why 001-C Was Selected

This role provides a strong bridge from:

```text
traditional technical support
```

toward:

```text
AI-platform support
API support
automation
technical incident handling
```

The deep analysis found:

```text
4 `DIRECT_MATCH` labels in the historical v0.16 output
1 `CLAIMED_SKILL_MATCH` label
0 automatically detected major gaps
0 automatically detected moderate gaps
```

before separately considering seniority and location. **These are model classifications, not four independently proven complete qualifications.** In particular, the eight-year requirement was labeled `DIRECT_MATCH` based on work-domain overlap without a verified duration comparison. The absence of automated major gaps must not be repeated as evidence that no substantial qualification gap exists.

The role nevertheless remained worth considering as a clearly labeled **stretch** because the technical direction was close to the career objective.

---

# 28. 001-C Evidence Strengths

Directly aligned areas include:

```text
SaaS troubleshooting
technical support
incident communication
enterprise customer communication
complex problem solving
cross-functional issue resolution
```

The posting also values:

```text
Python
OpenAI API
automation
tool integration
```

which align with the résumé at the skill-claim / automation-evidence level.

---

# 29. 001-C Seniority Risk

The major competitiveness issue is:

```text
8+ years
```

of experience in:

```text
User Operations
Engineering
Support Engineering
or similar technical roles
```

**Historical model output:** the v0.16 qualifier engine labeled the entire sentence `PREFERRED` and `DIRECT_MATCH`. Those labels do **not** establish that the eight-year experience expectation was fulfilled, or that the employer intended the eight years to be optional.

The captured wording is essentially “Have 8+ years of experience in User Operations, Engineering, Support Engineering or similar technical roles, *ideally* within high-growth tech startups or other fast-paced environments.” The word *ideally* more naturally qualifies the kind of environment rather than the 8+ years clause. The regex classifier marks the whole item preferred whenever it encounters that word, and its domain-match logic does not independently compare the stated years against the résumé.

The résumé documents significant support/IT experience but does **not independently establish eight years in those particular fields**. The posting also refers to a relevant bachelor's degree **or equivalent practical experience**; the submitted résumé does not establish the completed degree, and whether experience meets the alternative is an employer decision.

**Updated audited conclusion:** 001-C remains an approved, defensible *ambitious application target*, not a confirmed qualification match. The numeric seniority expectation and financially unresolved San Francisco location are material risks. Its approval is preserved, but the model's overbroad interpretation is no longer relied upon as justification.

---

# 30. 001-C Location Risk

Like 001-B, this target is tied to San Francisco in the captured role data.

The current evidence did not establish a reliable:

```text
remote-from-Utah path
```

or explicit relocation assistance.

That remains unresolved.

---

# 31. Near Miss — Technical Systems Program Manager, User Operations

This was one of the strongest roles not selected.

It had unusually strong alignment with:

```text
CRM systems
Salesforce
support workflows
APIs
integrations
enterprise SaaS
automation
QA
release processes
operational systems
```

v0.16 identified:

```text
4 direct matches
2 adjacent matches
0 major gaps
0 moderate gaps
```

and the posting included relocation assistance.

The reason it lost was seniority.

The role explicitly asks for:

```text
8+ years driving high-impact technical programs
```

The résumé does not cleanly establish eight years of technical program management.

Selecting it over the final three would have required stretching the interpretation of prior support/systems experience too far.

It remains a high-quality future comparison role.

---

# 32. Near Miss — Senior Support Specialist, Ads

This role also survived deep review.

Strengths included:

```text
support
escalations
QA findings
workflow improvement
knowledge systems
automation
technical investigation
```

The analysis found several direct matches and no major detected technical gap.

However, it introduced:

```text
6+ years
ads-domain context
Trust & Safety / advertiser workflow context
San Francisco location dependency
```

The final three offered cleaner overall positioning.

---

# 33. Rejected Despite Automatic Strength — Product Engagement Manager

This role is important to document because it demonstrates the limit of the automated funnel.

The rule-based system gave it:

```text
A_TOP5_REVIEW
```

Yet manual comparison showed:

```text
technical_core = NONE_DETECTED
```

and responsibilities centered on:

```text
team leadership
launch readiness
management
performance coaching
product engagement
```

The user had explicitly required a real technical component.

The assistant therefore removed it from the final three.

This is evidence that the final selection was not simply:

```text
take the top three script outputs
```

---

# 34. Remote Security Roles

Several security roles offered stronger geographic feasibility.

Examples included:

```text
Senior Technical Program Manager - Security
Vendor Security Technical Program Manager
Technical Threat Investigator, Threat Intel Engineering
```

Some were genuinely:

```text
REMOTE_NOW_STRONG
```

But the deeper requirement mapping identified major unproven areas such as:

```text
security engineering
vendor security risk
threat intelligence
offensive security
incident-response specialization
adversary tradecraft
```

The final selection therefore did not allow remote convenience to outweigh domain mismatch.

---

# 35. Senior Support Engineer

This role initially looked attractive because it combined:

```text
support
API troubleshooting
automation
incident response
relocation assistance
```

Closer inspection showed much heavier requirements:

```text
8+ years technical operations / SRE / NOC
distributed systems
monitoring / observability
high-severity incident leadership
cloud infrastructure
stronger scripting / software engineering
```

It was therefore a meaningfully larger stretch than the Dedicated Support Engineer role.

---

## 35.1 Other relevant AI-support variants

The 30-role review pool also includes AI Support Engineer variants, including a weekend-shift role and a biosciences-focused role. The historical record does not contain equally extensive direct comparison notes for every such variant. The final shortlist is therefore an evidence-informed recommendation, **not** proof that every plausible alternative was evaluated under an identical formal head-to-head protocol. The 001-C recommendation should be presented with that uncertainty visible.

---

# 36. Why These Three Together

The final three are useful as a portfolio of applications because they represent three related but distinct paths.

## 001-A — IT Support Specialist

Best:

```text
probability / conventional fit
```

Primary story:

```text
existing IT support and systems experience
```

## 001-B — Dedicated Support Engineer

Best:

```text
work-content alignment with the direction of growth
```

Primary story:

```text
support + APIs + incidents + technical diagnosis
```

## 001-C — AI Support Engineer

Best:

```text
bridge from existing evidence into AI-native technical support
```

Primary story:

```text
SaaS support + automation + API + AI tooling
```

Together they provide a better Attempt than choosing three nearly identical jobs for the same reason.

---

## 36.1 Revised comparative risk summary

| Historical target | Main strength | Main unresolved issue | Audit interpretation |
| --- | --- | --- | --- |
| **001-A IT Support Specialist** | Best conventional documented support/IT overlap; explicit relocation assistance in captured description | Onsite five days and specialist AV/endpoint-management gaps | Strongest comparatively defensible conventional target |
| **001-B Dedicated Support Engineer** | Strong API/integration and technical customer problem-solving relevance | Distributed systems/cloud depth and SF financial/logistical feasibility | Serious technical-direction target; historical `DIRECT_MATCH` counts are not complete skill proof |
| **001-C AI Support Engineer** | Strongest direct AI-platform support trajectory | 8+ years expectation, qualification/depth and SF location | Deliberate stretch; v0.16 `PREFERRED` / `DIRECT_MATCH` on duration is overbroad |

**Shared risk:** 001-B and 001-C both depend on an unresolved San Francisco work-location path, so the three targets are strategically diverse in technical direction but not strongly diversified geographically.

---

# 37. Attempt #001 Final Structure

```text
Attempt #001 — OpenAI
│
├── Target 001-A
│   IT Support Specialist
│   49ae54dc-3d33-4107-8112-63fac1ee86ca
│
├── Target 001-B
│   Dedicated Support Engineer - San Francisco
│   2348230a-295f-434d-9b16-653e01ddbd0b
│
└── Target 001-C
    AI Support Engineer - San Francisco
    1a979fd4-1bce-484e-a416-aed2810677a6
```

---

# 38. Canonical Application URLs

## 001-A

```text
https://jobs.ashbyhq.com/openai/49ae54dc-3d33-4107-8112-63fac1ee86ca/application
```

## 001-B

```text
https://jobs.ashbyhq.com/openai/2348230a-295f-434d-9b16-653e01ddbd0b/application
```

## 001-C

```text
https://jobs.ashbyhq.com/openai/1a979fd4-1bce-484e-a416-aed2810677a6/application
```

The Ashby UUID is treated as the durable role identity.

---

# 39. What Happens Next

Target selection is not the end of Attempt #001.

Each target should now move through its own application path.

Conceptually:

```text
Target selected
      ↓
exact role re-check
      ↓
resume variant
      ↓
gap analysis
      ↓
bounded Proof Sprint if useful
      ↓
application material
      ↓
submission
      ↓
status tracking
      ↓
outcome
      ↓
lessons
```

The three targets may progress at different speeds. Before preparing any application package, re-check the live posting, whether it accepts applications, precise onsite/remote requirements and whether relocation assistance is available. Historical `present_in_api=1` proves presence only in the frozen October 2026 API snapshot.

No submission receipts, recruiter responses, or employment outcomes are established by the supplied Attempt #001 artifacts.

---

# 40. Target-Specific Proof Work

Not every target needs the same Proof Sprint.

Possible directions:

## 001-A

Potential proof emphasis:

```text
IT automation
endpoint / identity-management lab
device-management workflow
support documentation
incident/runbook work
```

## 001-B

Potential proof emphasis:

```text
API troubleshooting
authentication failures
logging / tracing
reproduction harness
incident diagnosis
Python support tooling
```

## 001-C

Potential proof emphasis:

```text
OpenAI API
support automation
Python
incident triage
SaaS troubleshooting
AI-assisted support workflows
```

These should remain bounded.

The purpose is to strengthen an application, not delay it indefinitely.

---

# 41. Selection Provenance

The final target selection can be traced backward.

```text
Targets 001-A / 001-B / 001-C
        │
        ▼
assistant comparative judgment
        │
        ▼
30-role decision-review pool
        │
        ▼
v0.16 qualification-level evidence mapping
        │
        ▼
224-role deep-analysis population
        │
        ▼
v0.15 broad role analysis
        │
        ▼
815 current API roles
        │
        ▼
proofloop_enriched.db
        │
        ▼
HTML + Ashby source reconciliation
```

The user-defined criteria and résumé evidence constrain the entire decision path.

---

# 42. Decision Ownership

The cleanest description of decision ownership is:

```text
User:
defined the goal and constraints
provided personal work-history evidence
decided whether to accept the recommendation

Software:
organized and exposed the evidence
reduced the search space
identified contradictions and gaps

Assistant:
performed the final cross-role reasoning
selected the top three recommendations

User:
locked the recommendations as Attempt #001 targets
```

This is important for presenting the project accurately to another person.

The top three were not preselected and then justified afterward.

They emerged from the analysis.

---

# 43. Why This Matters as Project Evidence

Attempt #001 demonstrates more than job-board scraping.

The chain is:

```text
real employment problem
        ↓
data acquisition
        ↓
parsing
        ↓
normalization
        ↓
multiple representations
        ↓
relational storage
        ↓
validation
        ↓
testing
        ↓
source reconciliation
        ↓
analysis
        ↓
heuristic failure discovery
        ↓
analysis refinement
        ↓
qualification-level evidence mapping
        ↓
final real-world decision
```

That final step matters.

The software was actually used.

---

# 44. What Attempt #001 Does Not Claim

This document does not claim that:

```text
the selected three are objectively the only correct choices
the user is guaranteed to qualify
OpenAI will interview the user
every posting remains live indefinitely
every relocation question is resolved
the analysis is free from error
```

The claim is narrower:

> Given the captured role population, the supplied résumé, the user's stated constraints, and the analysis performed, these three were judged to be the strongest targets to pursue first.

That is defensible.

---

# 45. Attempt Status

Current status:

```text
[complete] company selected
[complete] source data captured
[complete] HTML pipeline
[complete] API reconciliation
[complete] enriched database
[complete] broad role analysis
[complete] deep qualification analysis
[complete] top-three recommendation
[complete] user acceptance
[complete] canonical target URLs locked

[next] target-specific application preparation
[next] resume variants
[next] bounded proof work where justified
[next] submissions
[next] application ledger / status tracking
[next] outcomes
[next] Attempt #001 retrospective
```

---

## 45.1 Qualification and provenance corrections from the evidence audit

The Stage 1–8 audit distinguished historical output from independently supported semantics. `is_remote` was stored and displayed in v0.15 but not used as an operative condition by `classify_location()`. The v0.16 numeric-year extraction was **not** a duration-to-résumé verification. Treat `DIRECT_MATCH` as an evidence-domain tag; a multi-clause requirement may still include unproven depth or tenure. The strong-sales exclusion and contextual-sales review were separate, and the three selected positions were not evidenced as quota-driven sales roles.

The final selection was made by the assistant from the reduced pool and then accepted by the user. The database and report pipeline establishes traceability through the 30-role pool, but the comparison and acceptance are documented **decisions**, not rows in a currently implemented application ledger.

These clarifications are documentation-only: no historical role labels, source documents, tests or selection approvals were rewritten.

---

# 46. Final Attempt Principle

Attempt #001 established an important pattern for the rest of the project:

```text
The user does not need to manually know the answer first.

The user can define:
    the objective
    the constraints
    the evidence

The system can then:
    investigate
    organize
    compare
    expose uncertainty

The assistant can:
    make a reasoned recommendation

The user can:
    accept, reject, or revise the result
```

That is a much more interesting use of AI than simply asking:

```text
Which job should I apply to?
```

The value is in the evidence trail between the question and the decision.

---

# 47. Application Submission Milestone — October 9, 2026

## 47.1 Five real applications submitted

The candidate reported submitting five applications through OpenAI's application system:

| Target | Position | Location |
|---|---|---|
| 001-A | IT Support Specialist | Seattle |
| 001-B | Dedicated Support Engineer | San Francisco |
| 001-C | AI Support Engineer | San Francisco |
| 001-E | Security Program Manager | US Remote advertised; eligibility unverified |
| 001-F | Senior Support Specialist, Ads | San Francisco |

Target 001-D, Vendor Security Technical Program Manager, was investigated but not submitted. Its historical research and Proof Graph relationship remain preserved.

All five submitted applications have pending outcomes. Submission dates are recorded as 2026-10-09, based on the applicant's report. Official submission confirmation receipts have not been archived as evidence in the current ledgers.

## 47.2 ProofLoop operational tracking

The shared framework now records:

- Five submitted applications in applications.csv.
- Five submission events in application_events.csv.
- Employer sources through SRC010.
- Requirements REQ001 through REQ006.
- Proof Graph relationships PG001 through PG006.
- Existing evidence records EV001 through EV006.

The original evidence records remain intact. Proof Graph relationships explicitly preserve qualification gaps and limitations rather than treating transferable experience as proof of full qualification.

## 47.3 Published Git milestones

- 1b817d0 — Record five submitted OpenAI applications.
- a931acc — Record five application submission events.
- b1334db — Link the fifth application to employer source, requirement, and evidence.

These commits establish project-documentation provenance. They do not independently verify receipt of applications by the employer.

## 47.4 What remains open

Attempt #001 has reached the submission and tracking milestone, but the hiring cycle is not closed.

Remaining work includes preserving actual employer confirmation receipts when available, tracking interview or rejection events, maintaining accurate evidence and qualification states, and completing a retrospective as outcomes become known.

Further applications to other employers may proceed while Attempt #001 outcomes remain pending.

## 47.5 Historical continuity

Earlier sections describing application preparation and submission as future work are retained as records of the project's earlier state. This section supersedes those earlier progress labels without rewriting the historical engineering and selection narrative.

