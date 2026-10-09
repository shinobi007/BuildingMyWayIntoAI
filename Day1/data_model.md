# Data Model

## Building My Way Into AI — Attempt #001 / ProofLoop

This document describes the data model used in **Attempt #001 — OpenAI**.

It focuses on the shape of the data, the relationship between source artifacts, normalized records, SQLite tables, derived analysis, and final decision records.

The guiding rule is simple:

> **Observed source data, normalized data, derived interpretation, and human decisions should remain distinguishable.**

The project deliberately avoids collapsing all of those layers into one "clean" record.

---

## Reader orientation and audit status

This is the **full historical data-model reference**, amended after a static audit of the supplied source, SQLite databases, and generated reports. Original schema descriptions and future ideas are intentionally retained. A field included in a *conceptual* model is not evidence that a corresponding SQL table exists.

Related: [Project overview](../README.md) · [Architecture](architecture.md) · [Attempt #001](attempt_001.md) · [Validation and testing](validation_and_testing.md) · [Changelog](../CHANGELOG.md). These are intended repository paths, not a claim that the old Windows working directory already has this layout.

---

# 1. Data Model Goals

The model is designed to support five things at the same time:

```text
preservation
normalization
reconciliation
analysis
decision traceability
```

That leads to several design constraints.

## 1.1 Preserve source-specific values

If the HTML source says one thing and the Ashby API says another, both should remain recoverable.

## 1.2 Use stable identity where possible

The original HTML row number is useful within that source, but the Ashby UUID is the durable cross-source role identity.

## 1.3 Represent one-to-many relationships relationally

Secondary locations and compensation components should not be flattened into one lossy string.

## 1.4 Keep derived classifications separate from source facts

For example:

```text
workplace_type = Hybrid
```

is source data.

```text
REMOTE_NEEDS_CONFIRMATION
```

is derived interpretation.

Those are not the same kind of value.

## 1.5 Preserve enough structure for future attempts

The OpenAI-specific model should remain understandable while also pointing toward a more general ProofLoop model that can later support other companies and ATS providers.

---

# 2. Data Layers

The project currently has four conceptual data layers.

```text
Layer 1 — Source artifacts
Layer 2 — Normalized source records
Layer 3 — Canonical/reconciled relational data
Layer 4 — Derived analysis and decision evidence
```

They are related, but they should not be treated as interchangeable.

---

# 3. Layer 1 — Source Artifacts

The source layer preserves material as close as practical to how it was originally acquired.

Primary source artifacts include:

```text
OpenAI Careers.zip
openai_ashby_snapshot_2026-10-07.json
```

These answer questions such as:

```text
What did the source contain?
When was it captured?
Can later transformations be regenerated?
```

The source layer should not be modified merely because later analysis discovers a better normalization rule.

---

# 4. Layer 2 — Normalized Source Records

Each source is normalized independently before reconciliation.

Current normalized artifacts include:

```text
openai_roles.jsonl
openai_roles.csv
openai_ashby_roles.jsonl
```

The HTML-derived records and API-derived records are not merged immediately.

That separation is deliberate.

---

# 5. Original HTML Role Schema

The first normalized schema contains six fields.

```text
role_id
title
team
display_location
career_url
apply_url
```

Conceptually:

```json
{
  "role_id": 1,
  "title": "Example Role",
  "team": "Example Team",
  "display_location": "San Francisco",
  "career_url": "https://...",
  "apply_url": "https://jobs.ashbyhq.com/openai/..."
}
```

---

## 5.1 `role_id`

Type:

```text
integer
```

Meaning:

```text
sequential role position in the parsed HTML source
```

Properties:

```text
required
unique within HTML dataset
sequential in expected source population
```

Important limitation:

`role_id` is not the durable global identity for the role.

It is source-local.

---

## 5.2 `title`

Type:

```text
string
```

Meaning:

```text
role title as normalized from the HTML source
```

Normalization may remove structural noise while preserving the observed title text.

---

## 5.3 `team`

Type:

```text
string
```

Meaning:

```text
team/category shown in the HTML source
```

This is not assumed to be identical to every later API department or organizational field.

---

## 5.4 `display_location`

Type:

```text
string
```

Meaning:

```text
primary display location shown in the HTML source
```

Examples:

```text
San Francisco
Seattle
US - Remote
London, UK
```

This should not be interpreted on its own as a complete work-arrangement policy.

---

## 5.5 `career_url`

Type:

```text
string / URL
```

Meaning:

```text
career-detail URL associated with the HTML listing
```

Constraints in the original SQLite model:

```text
NOT NULL
UNIQUE
```

---

## 5.6 `apply_url`

Type:

```text
string / URL
```

Meaning:

```text
application URL associated with the HTML listing
```

Constraints in the original SQLite model:

```text
NOT NULL
UNIQUE
```

The Ashby UUID can later be extracted from this URL.

---

# 6. JSONL Representation

`openai_roles.jsonl` stores one normalized HTML role per line.

Example shape:

```json
{"role_id":1,"title":"Example Role","team":"Example Team","display_location":"San Francisco","career_url":"https://...","apply_url":"https://jobs.ashbyhq.com/openai/.../application"}
```

Properties:

```text
one complete JSON object per line
UTF-8 text
fixed expected field set
817 records in the original real run
```

Why JSONL is useful:

```text
easy streaming
easy line counting
easy diffing
machine-readable
human-inspectable
simple regeneration
```

---

# 7. CSV Representation

`openai_roles.csv` represents the same six-field HTML-derived dataset.

Column order:

```text
role_id
title
team
display_location
career_url
apply_url
```

The CSV is an interoperability format, not a separate source of truth.

The intended relationship is:

```text
openai_roles.jsonl
        │
        ▼
openai_roles.csv
```

with equality validation between them.

---

# 8. Original SQLite Schema

The first SQLite database is:

```text
proofloop.db
```

Its core table is:

```sql
CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    team TEXT NOT NULL,
    display_location TEXT NOT NULL,
    career_url TEXT NOT NULL UNIQUE,
    apply_url TEXT NOT NULL UNIQUE
);
```

This table contains the same logical records as the HTML JSONL and CSV.

Its role is persistence plus database-level constraints.

---

# 9. Original Database Invariants

The original HTML database is expected to satisfy:

```text
role count = expected source count
role_id values are sequential
required fields are non-empty
career_url values are unique
apply_url values are unique
database passes PRAGMA integrity_check
database contents equal normalized JSONL contents
```

The database is not considered correct merely because it can be opened.

---

# 10. Ashby API Record Model

The Ashby API exposes a richer source record.

Observed fields included:

```text
id
title
department
team
employmentType
location
shouldDisplayCompensationOnJobPostings
secondaryLocations
publishedAt
isListed
isRemote
workplaceType
address
jobUrl
applyUrl
descriptionHtml
descriptionPlain
compensation
```

The project does not assume that every field is populated for every role.

Nullability itself can be meaningful.

---

## 10.1 Raw-source fields omitted by the normalized API projection

The frozen API job object contains **18 fields**. The normalized `openai_ashby_roles.jsonl` maps **17 of those fields** under canonical names and adds its own source-position and snapshot-reference fields. The raw field `shouldDisplayCompensationOnJobPostings` is *not* projected into normalized JSONL or the current enriched SQLite API table. The top-level `apiVersion` is likewise available in the snapshot rather than on normalized per-role records.

That omission is **limited to the derived layer**: the original `openai_ashby_snapshot_2026-10-07.json` remains the authoritative archived source for the raw compensation-display flag. A future generalization should decide explicitly whether to preserve it as a normalized Boolean and explain the policy for public compensation display. Do not infer authorization to display compensation solely from a non-null `compensation` object.

---

# 11. Stable Role Identity

The most important identity field in the enriched architecture is:

```text
ashby_id
```

Example:

```text
49ae54dc-3d33-4107-8112-63fac1ee86ca
```

This UUID is used as the stable reconciliation key.

It can originate from:

```text
API field: id
```

or from:

```text
Ashby apply URL
```

Conceptually:

```text
HTML role
   │
   └── apply_url ──► extract UUID
                         │
                         ▼
                    ashby_id
                         ▲
                         │
API role ────────────────┘
```

This allows reconciliation without depending on mutable titles or location strings.

---

# 12. Raw vs Normalized API Values

The reconciliation process preserves source values while also creating normalized comparison values.

A conceptual pattern is:

```text
raw_title
normalized_title

raw_team
normalized_team
```

Normalization can be used for:

```text
comparison
whitespace handling
cosmetic-equivalence detection
```

without rewriting the preserved raw value.

This distinction allowed v0.9.1 to determine that 56 title/team differences were cosmetic rather than substantive.

---

# 13. Canonical Union

The HTML and API datasets reconcile into a canonical union.

Observed real counts:

```text
HTML roles:       817
API roles:        815
matched roles:    814
HTML-only roles:    3
API-only roles:     1
union roles:      818
```

Each canonical role therefore has a source state.

---

# 14. Source Status

The enriched model uses a source-status concept.

Known values:

```text
matched
html_only
api_only
```

Meaning:

## `matched`

The same Ashby UUID is present in both normalized sources.

## `html_only`

The UUID is present in the earlier HTML source but not the frozen API snapshot.

This may represent:

```text
a closed role
a removed listing
a timing difference
another source-state change
```

It should not automatically be interpreted more specifically without evidence.

## `api_only`

The UUID is present in the frozen API snapshot but not the HTML source.

This may represent:

```text
a newly added role
a timing difference
```

Again, the status records the source relationship, not the cause.

---

# 15. Presence Flags

The canonical enriched role model also uses source-presence flags.

Conceptually:

```text
present_in_html
present_in_api
```

These are useful because source status is categorical, while presence flags make filtering simple.

For example:

```sql
WHERE present_in_api = 1
```

is used as the current-role population for the frozen API analysis.

Important:

```text
present_in_api = 1
```

means:

```text
present in that frozen API snapshot
```

not:

```text
guaranteed to be open forever
```

---

# 16. Enriched Database

The multi-source database is:

```text
proofloop_enriched.db
```

It is deliberately separate from:

```text
proofloop.db
```

This preserves the original HTML-only pipeline as its own artifact.

The enriched database currently contains:

```text
build_metadata
roles
html_roles
api_roles
api_secondary_locations
api_compensation_components
```

---

# 17. Entity Relationship Overview

Conceptually:

```text
                         ┌──────────────────┐
                         │  build_metadata  │
                         └──────────────────┘

┌─────────────────┐
│   html_roles    │
│                 │
│ role_id         │
│ ashby_id        │
│ title           │
│ team            │
│ location        │
│ URLs            │
└────────┬────────┘
         │
         │ ashby_id
         │
         ▼
┌─────────────────────────────────┐
│              roles              │
│                                 │
│ ashby_id  PRIMARY IDENTITY      │
│ canonical title/team            │
│ canonical location              │
│ source status                   │
│ presence flags                  │
│ richer API-derived fields       │
│ descriptions / URLs             │
└──────────┬──────────────┬───────┘
           │              │
           │              │ ashby_id
           │              ▼
           │     ┌──────────────────────────┐
           │     │ api_secondary_locations  │
           │     │                          │
           │     │ location_index           │
           │     │ location                 │
           │     └──────────────────────────┘
           │
           │ ashby_id
           ▼
┌──────────────────────────────┐
│          api_roles           │
│                              │
│ raw/normalized source fields │
│ structured work metadata     │
│ descriptions                 │
│ address JSON                 │
│ compensation JSON            │
└──────────┬───────────────────┘
           │
           │ ashby_id
           ▼
┌────────────────────────────────┐
│ api_compensation_components    │
│                                │
│ component_index                │
│ compensation_type              │
│ interval                       │
│ currency_code                  │
│ min_value                      │
│ max_value                      │
└────────────────────────────────┘
```

This diagram is conceptual rather than a complete SQL DDL dump.

The exact schema should ultimately be generated directly from SQLite as part of repository documentation or tooling.

---

# 18. `build_metadata`

Purpose:

```text
record how the enriched database was built
```

This table exists to preserve build-level context rather than job-level facts.

Useful metadata may include concepts such as:

```text
builder version
source counts
expected counts
build timestamp
input artifact names
```

The exact stored columns should be treated as implementation-defined unless taken directly from the database schema.

---

# 19. `roles` — Canonical Role Table

Purpose:

```text
one canonical row per Ashby UUID in the union
```

Primary identity:

```text
ashby_id
```

Confirmed role-level concepts include:

```text
ashby_id
canonical title
canonical team
display / primary location
source_status
present_in_html
present_in_api
career URL
apply URL
job URL
department
employment type
published timestamp
is_remote
workplace_type
description text
```

Not every role necessarily has every richer API field.

The canonical table is optimized for cross-source querying.

It does not replace the source-preserving child tables.

---

# 20. Canonical Value Selection

When both sources contain the same role, the canonical table may prefer a richer API value for some fields while preserving the HTML value elsewhere.

The important design rule is:

```text
canonical selection != source destruction
```

If a canonical title is selected from one source, the other source's title remains available in its source-specific table.

This allows later auditing.

---

# 21. `html_roles`

Purpose:

```text
preserve the normalized HTML branch inside the enriched relational model
```

Key concepts:

```text
role_id
ashby_id
HTML-source title
HTML-source team
HTML display location
HTML career URL
HTML apply URL
```

This table lets the enriched database answer:

```text
What did the HTML branch say?
```

without reconstructing the answer from canonical fields.

---

# 22. `api_roles`

Purpose:

```text
preserve richer API-source role data
```

Confirmed concepts include:

```text
ashby_id
raw title
normalized title
raw team
normalized team
department
employment type
primary location
published timestamp
is_remote
workplace_type
is_listed
job URL
apply URL
description_plain
description_html
address_json
compensation_json
```

The JSON columns preserve source structures that have not yet been fully normalized relationally.

This is deliberate.

Not every nested structure needs to be decomposed immediately.

---

# 23. `api_secondary_locations`

Purpose:

```text
represent zero-to-many secondary locations per API role
```

Confirmed concepts:

```text
ashby_id
location_index
location
```

Relationship:

```text
api_roles 1 ──────── 0..N api_secondary_locations
```

Why a child table is necessary:

A role may have:

```text
primary: San Francisco

secondary:
    New York City
    Seattle
    US - Remote
```

Flattening those locations into one string would make exact location queries and ordering less reliable.

---

# 24. Secondary Location Semantics

Secondary locations are treated as evidence, not automatic permission.

For example:

```text
secondary_location = US - Remote
```

does not automatically mean:

```text
the candidate can work from any US state
```

The role may still have:

```text
workplace_type = Hybrid
```

or explicit office requirements in the description.

This is why location eligibility is derived later instead of stored as a direct source fact.

---

# 25. `api_compensation_components`

Purpose:

```text
represent zero-to-many structured compensation components
```

Confirmed fields:

```text
ashby_id
component_index
compensation_type
interval
currency_code
min_value
max_value
```

Relationship:

```text
api_roles 1 ──────── 0..N api_compensation_components
```

---

# 26. Compensation Model

A compensation amount is meaningless without its unit.

Therefore the logical compensation identity is closer to:

```text
type
+ currency
+ interval
+ min
+ max
```

than:

```text
min
+ max
```

Example:

```text
Salary
USD
1 HOUR
60.58
108.17
```

is not directly comparable to:

```text
Salary
USD
1 YEAR
180000
260000
```

without conversion.

The analysis preserves interval and currency instead of flattening raw numbers into a false ranking.

---

# 27. Description Fields

The API provides both:

```text
descriptionHtml
descriptionPlain
```

The plain-text version is the primary input for later parsing and signal extraction.

The HTML version is preserved because formatting and structural context may matter.

The model does not assume that plain text perfectly preserves all semantic structure.

This becomes important when extracting:

```text
responsibilities
qualifications
preferred items
office requirements
relocation wording
```

---

# 28. Work-Arrangement Fields

Observed structured work-arrangement fields include:

```text
is_remote
workplace_type
location
secondary_locations
```

These must remain separate.

Observed real combinations included:

```text
is_remote = 1
workplace_type = Hybrid
```

for hundreds of roles.

Therefore the model explicitly rejects this simplification:

```text
is_remote == true
    therefore
fully remote
```

The source field is stored as observed.

Interpretation happens later.

---

# 29. Derived Location Model

v0.15 derives a richer location classification using multiple forms of evidence. Distinguish the **source/report context** from variables actively used by the classification branches.

Evidence carried in the report includes:

```text
primary location
secondary locations
is_remote (retained for inspection; not directly used in classify_location() branches)
workplace_type
description wording
office-days wording
relocation wording
```

The actual v0.15 branch logic uses structured workplace type, primary/secondary-location strings, and textual office/relocation/remote context. It assigns no category solely because `is_remote = 1`, which is appropriate given the observed hybrid/remote contradiction. It would be inaccurate to describe the remote Boolean as an operative final-classification condition in v0.15.

Known categories include:

```text
A_US_REMOTE_STRONG
B_US_REMOTE_AMBIGUOUS
B_REMOTE_US_LOCATION_AMBIGUOUS
C_US_RELOCATION_SUPPORTED
D_US_LOCATION_UNCLEAR
D_US_ONSITE_OR_HYBRID
E_NON_US_OR_JURISDICTION_MISMATCH
```

These categories belong to the analysis layer. They are not source columns. The implemented `B_REMOTE_US_LOCATION_AMBIGUOUS` branch was present in code but had **zero roles** in the historical 815-role report; an unused branch still belongs in the complete implemented taxonomy.

---

# 30. Location Evidence Fields

Later analysis records concepts such as:

```text
location_category
location_confidence
location_reason
us_remote_primary
us_remote_secondary
remote_description_context
relocation_assistance
relocation_context
office_days_per_week
office_requirement_context
```

These fields are derived from source data and text extraction.

They should be understood as:

```text
analysis evidence
```

rather than:

```text
original ATS fields
```

---

# 31. Sales Classification Model

Sales classification is also derived.

Known final-style categories include:

```text
NO_SALES_SIGNAL_FOUND
REVIEW_SALES_CONTEXT
EXCLUDE_STRONG_SALES
```

Supporting evidence may include:

```text
sales_team
sales-title patterns
strong sales signals
context sales signals
sales reason
```

This allows the system to retain the difference between:

```text
hard sales evidence
```

and:

```text
commercial or go-to-market language that merely requires review
```

---

# 32. Strong Sales Signals

Examples of strong signals include patterns around:

```text
quota
sales cycle
pipeline generation
prospecting
closing deals
book of business
revenue targets
account expansion
commission compensation
```

These are not stored in the core role table as source truth.

They are derived from title/team/description evidence.

---

# 33. Contextual Sales Signals

Examples of weaker/context-required signals include:

```text
pre-sales
business development
commercial
go-to-market
customer expansion
revenue
territory
working with sales
```

These are intentionally separated from strong exclusion evidence.

A technical role can interact with GTM or sales teams without itself being a sales job.

---

# 34. Technical-Core Model

v0.15 derives a technical-core classification.

Observed levels:

```text
HIGH
MEDIUM
LOW
NONE_DETECTED
```

Supporting technical signal families include:

```text
hands-on troubleshooting
systems / infrastructure
API / integration
coding / scripting
automation workflows
testing / evaluation
technical support
security investigation
```

Again:

```text
technical_core_level
```

is analysis output, not a source field.

---

# 35. Resume-Evidence Overlap Model

The broad analysis maps role descriptions against evidence categories.

Examples:

```text
support
troubleshooting
api_integrations
automation
scripting_programming
sql_data
ticketing_itsm
network_identity_device
uat_testing
documentation
crm_saas
```

A role can then have:

```text
resume_evidence_overlap_count
resume_evidence_overlap_categories
```

This is a discovery mechanism.

It is explicitly not a fit score.

---

# 36. Deep Evidence Profile

v0.16 introduces a more explicit candidate-evidence model.

Evidence tiers:

```text
DIRECT_WORK_EVIDENCE
RESUME_SKILL_CLAIM
ADJACENT_EVIDENCE
NOT_EVIDENCED
UNKNOWN
```

The known evidence profile for Attempt #001 includes domains such as:

```text
technical_support
troubleshooting_incidents
api_integrations
automation_workflows
ticketing_itsm
documentation_training
uat_qa_bug
crm_saas
basic_network_dns
process_improvement
technical_customer_communication
python_scripting
javascript_scripting
sql_data
powershell_bash
web_frontend
systems_operations
identity_device_management
technical_program_delivery
enterprise_customer_delivery
vendor_management
professional_software_engineering
production_system_ownership
distributed_systems
cloud_infrastructure
security_engineering
threat_intelligence_ir
offensive_security
fraud_abuse_investigations
data_science_statistics
ml_ai_engineering
datacenter_facilities
hardware_electrical
audiovisual_event_technology
people_management
security_vendor_risk
product_management
mergers_acquisitions
government_clearance
```

Not every domain has the same evidence tier.

---

# 37. Why Evidence Tiers Matter

Without tiers, a system might incorrectly perform this transformation:

```text
resume contains "Python"
        ↓
candidate is a professional Python software engineer
```

The evidence model instead supports:

```text
python_scripting
    = RESUME_SKILL_CLAIM
```

while:

```text
technical_support
    = DIRECT_WORK_EVIDENCE
```

The difference is critical when mapping job requirements.

---

# 38. Requirement Record Model

The deep-analysis layer turns qualification text into requirement records.

Conceptually:

```json
{
  "text": "Can write code or scripts to reproduce issues...",
  "strength": "POSTED_EXPECTATION",
  "years": [],
  "domains": [
    {
      "domain": "python_scripting",
      "evidence_tier": "RESUME_SKILL_CLAIM"
    }
  ],
  "technologies": ["Python"],
  "classification": "MODERATE_GAP"
}
```

The exact stored structure can vary, but the important concepts are stable.

---

# 39. Requirement Strength

Known requirement-strength concepts include:

```text
POSTED_EXPECTATION
EXPLICIT_REQUIREMENT
PREFERRED
```

The analysis attempts to distinguish:

```text
required
expected
preferred / bonus
```

instead of treating every sentence in a job posting as equally binding.

---

### Audit qualification: the v0.16 `PREFERRED` classifier is sentence-wide

The current `expectation_strength()` returns `PREFERRED` when it finds words such as `preferred`, `bonus`, or `ideally` anywhere in a requirement item. That is a regex-level label, **not a verified interpretation of which clause is optional**. For the 001-C posting, “8+ years ... ideally within high-growth ... environments” was classified as preferred even though the *ideally* clause appears to qualify the environment, not the full eight-year experience expectation. Preserve the stored label as historical model output, but do not claim it establishes that the employer treats eight years as optional.

---

# 40. Requirement Domains

A single qualification can map to multiple domains.

Example:

```text
"expert-level troubleshooting across APIs,
 distributed systems, cloud infrastructure,
 and enterprise integrations"
```

can map to:

```text
troubleshooting_incidents
api_integrations
distributed_systems
cloud_infrastructure
```

This matters because the candidate may have strong evidence in some parts and weak evidence in others.

---

# 41. Requirement Technologies

Technology mentions are also extracted separately.

Examples:

```text
Python
JavaScript/TypeScript
REST APIs
Salesforce
Microsoft 365
Google Workspace
Intune
Jamf
Azure
macOS
```

A technology mention is not automatically equivalent to a domain-level requirement.

---

# 42. Requirement Classification

Known classifications include:

```text
DIRECT_MATCH
CLAIMED_SKILL_MATCH
ADJACENT_MATCH
MODERATE_GAP
MAJOR_GAP
UNCLASSIFIED_REQUIREMENT
```

These describe the current relationship between posted expectations and available evidence.

They do not describe permanent ability.

---

# 43. Deep Role Record

A role in the deep-analysis layer can contain fields conceptually grouped like this:

```text
identity
source context
location evidence
sales evidence
technical evidence
resume overlap
responsibilities
qualifications
preferred qualifications
requirement records
experience-year signals
education signals
compensation
career lane
decision band
decision reasons
```

This is a decision-support record rather than a source record.

---

# 44. Experience-Year Signals

The analysis extracts experience language such as:

```text
4+ years
5+ years
8+ years
10+ years
at least five years
```

The model stores those signals separately because:

```text
a number appearing in a description
```

is not always:

```text
a hard minimum requirement
```

Context and section membership matter.

---

## 44.1 Years detected are not years demonstrated

The v0.16 code records numeric year signals and derives `seniority_burden`, but its `classify_requirement_item()` does **not** calculate the candidate's qualifying professional tenure and compare it to the posted threshold before returning `DIRECT_MATCH`. This can overstate agreement when a familiar support/IT domain is detected alongside an 8+ years clause.

`DIRECT_MATCH` here means a **matching evidence-domain signal** was detected, not “every clause, duration, qualification and technology in the original requirement is independently proven.” Experience-duration verification needs distinct evidence and preferably clause-level classification in a future implementation.

---

# 45. Education Signals

Education language is also modeled separately.

Examples include:

```text
bachelor's degree
master's degree
PhD / doctorate
degree or equivalent experience
equivalent practical experience
```

Again, education mention is not automatically a hard gate.

---

# 46. Responsibility and Qualification Sections

The deep-analysis layer attempts to extract distinct text sections.

Conceptual fields:

```text
responsibilities_text
qualifications_text
preferred_text
```

It also records extraction provenance such as:

```text
responsibility_extraction_method
qualification_extraction_method
preferred_extraction_method
```

This is important because parser confidence depends partly on how the section was found.

---

# 47. Qualification Parse Completeness

The analysis can distinguish between:

```text
qualification section successfully extracted
```

and:

```text
no clean qualification section found
```

A role with incomplete parsing should not be rewarded as if it had zero gaps.

This is why the decision system includes concepts such as:

```text
C_REQUIREMENTS_INCOMPLETE
```

---

# 48. Seniority Burden

The deep-analysis layer derives a seniority burden.

Known categories:

```text
LOW
MODERATE
HIGH
VERY_HIGH
UNKNOWN
```

Inputs can include:

```text
explicit year requirements
senior/staff/lead wording
scope of responsibility
management expectations
```

This is derived evidence, not source truth.

---

# 49. Career Lane

v0.16 groups candidates into broad career lanes.

Observed categories:

```text
PRIMARY_SUPPORT_IT
ADJACENT_TECHNICAL
STRETCH_TECHNICAL
```

This helps prevent a highly technical but unrelated role from being treated as equivalent to a direct support/IT role.

---

# 50. Title Alignment

Role titles are also interpreted into alignment categories such as:

```text
DIRECT_ROLE_FAMILY
ADJACENT_PROGRAM_ROLE
SPECIALIST_ENGINEERING_STRETCH
OTHER_TECHNICAL_ROLE
```

These are decision-support labels.

They should not be confused with ATS job families.

---

# 51. Location Path

The deep-analysis layer derives a candidate-facing location path.

Known values include:

```text
REMOTE_NOW_STRONG
REMOTE_NEEDS_CONFIRMATION
RELOCATION_SUPPORTED
US_LOCATION_DEPENDENCY
```

This makes the practical meaning of location evidence easier to compare across finalists.

---

# 52. Decision Bands

The deep-analysis layer also derives manual-review bands.

Known values:

```text
A_TOP5_REVIEW
B_SERIOUS_REVIEW
C_STRETCH_REVIEW
C_REQUIREMENTS_INCOMPLETE
D_BACKGROUND
```

These bands reduce the review population.

They do **not** select the final target automatically.

---

## 52.1 Exact frozen v0.16 distribution

| Band | Frozen candidate count |
| --- | ---: |
| `A_TOP5_REVIEW` | 1 |
| `B_SERIOUS_REVIEW` | 48 |
| `C_STRETCH_REVIEW` | 122 |
| `C_REQUIREMENTS_INCOMPLETE` | 23 |
| `D_BACKGROUND` | 30 |
| **All deep candidates** | **224** |

The `decision_review_pool` separately contains **30 roles**; that number must not be confused with the 30 `D_BACKGROUND` candidates. The report also records 23 instances where no recognized qualification heading was found (`not_found`). Missing recognized headings represent incomplete extraction, not a perfect zero-gap record.

---

# 53. Decision Review Pool

The v0.16 run produced:

```text
815 baseline roles
224 deep-analysis candidates
30 decision-review roles
```

The review pool is therefore a derived dataset.

Its purpose is:

```text
make exhaustive human review feasible
```

not:

```text
replace human review
```

---

# 54. Attempt Model

After the role-selection process, the project introduced a higher-level job-search entity:

```text
Attempt
```

An Attempt represents a coordinated company/opportunity campaign.

Current instance:

```text
Attempt #001 — OpenAI
```

---

# 55. Target Model

An Attempt can contain multiple role Targets.

Current canonical targets:

```text
Target 001-A
IT Support Specialist
Ashby ID:
49ae54dc-3d33-4107-8112-63fac1ee86ca

Target 001-B
Dedicated Support Engineer - San Francisco
Ashby ID:
2348230a-295f-434d-9b16-653e01ddbd0b

Target 001-C
AI Support Engineer - San Francisco
Ashby ID:
1a979fd4-1bce-484e-a416-aed2810677a6
```

Conceptually:

```text
Attempt 1 ──────── 1..N Targets
```

---

# 56. Future Target Data

The project has not yet implemented a formal target-tracking database, but the intended model should eventually support fields such as:

```text
attempt_id
target_id
company
role_external_id
role_title
job_url
apply_url
selection_reason
selected_at
status
resume_variant
proof_sprint
application_submitted_at
application_outcome
notes
```

These are future-model concepts, not currently claimed as implemented fields.

---

# 57. Future Attempt Data

A future Attempt entity may contain:

```text
attempt_id
company
started_at
research_snapshot
target_count
status
summary
lessons
```

Again, this belongs to the future ProofLoop operational model rather than the current OpenAI SQLite schema.

---

# 58. Provenance Model

The project currently relies on several forms of provenance.

## File provenance

```text
source filename
snapshot date
generated report filename
versioned script name
```

## Record provenance

```text
present_in_html
present_in_api
source_status
raw source-specific values
```

## Analysis provenance

```text
analysis version
extraction method
classification reason
signal matches
decision reasons
```

Together these make it possible to trace:

```text
decision
    ↓
analysis result
    ↓
canonical record
    ↓
source-specific record
    ↓
preserved artifact
```

---

## 58.1 Enforced database constraints versus current-data validation

The v0.11 SQLite schema enforces primary keys, many NOT NULL/UNIQUE rules, foreign-key relations for child tables, permitted source-status values, and Boolean-shaped presence flags. The v0.12 validator **also examines existing rows** to ensure combinations such as `source_status='matched'` align with `present_in_html=1` and `present_in_api=1`.

These are different guarantees: the schema does **not** include a compound CHECK constraint making every source-status/presence-flag combination impossible to insert. `foreign_key_check` and recorded data comparisons demonstrate the state of the historical database, not the rejection of every possible logically inconsistent future row.

**Replacement safety:** Both original and enriched importers can unlink an existing database when `--overwrite` is used before a validated candidate replacement exists. Original v0.5.1 additionally checks the expected count after generating its database. These behaviors are implementation limitations, not evidence that the archived dataset was lost. A future importer should build in a temporary location, verify, then replace atomically when feasible.

---

# 59. Data Quality State

The model intentionally allows nulls and unknowns.

Examples:

```text
workplace_type = NULL
is_remote = NULL
office_days_per_week = not detected
qualification section = not found
```

This is preferable to inventing values.

The project treats:

```text
UNKNOWN
```

as a real state.

---

# 60. Important Non-Equivalences

Several pairs of values may look similar but must remain distinct.

```text
role_id
!=
ashby_id
```

```text
raw title
!=
normalized title
```

```text
HTML title
!=
API title
```

```text
primary location
!=
secondary location
```

```text
is_remote
!=
workplace_type
```

```text
US - Remote secondary
!=
confirmed work-from-anywhere eligibility
```

```text
relocation assistance
!=
permission to begin remotely
```

```text
resume skill claim
!=
direct work evidence
```

```text
keyword overlap
!=
job fit
```

```text
no detected sales signal
!=
proof of no sales responsibility
```

```text
analysis band
!=
final human decision
```

These distinctions are central to the model.

---

# 61. Artifact Relationships

A simplified artifact lineage is:

```text
OpenAI Careers.zip
        │
        ▼
proofloop_openai_ingest_v0_2.py
        │
        ▼
openai_roles.jsonl
        │
        ├──────────► openai_roles.csv
        │
        ▼
proofloop.db
        │
        │
        │              openai_ashby_snapshot_2026-10-07.json
        │                            │
        │                            ▼
        │                  openai_ashby_roles.jsonl
        │                            │
        └──────────────┬─────────────┘
                       ▼
            reconciliation reports
                       │
                       ▼
              proofloop_enriched.db
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
role analysis v0.15          validation / tests
          │
          ▼
deep analysis v0.16
          │
          ▼
Attempt #001 targets
```

---

# 62. Report Data Model

Analysis reports are emitted in two parallel forms.

## JSON

Purpose:

```text
structured continuation
machine-readable evidence
future scripting
exact field preservation
```

## Markdown

Purpose:

```text
manual review
human-readable transparency
GitHub inspection
documentation
```

The JSON should be treated as the more structured representation.

The Markdown is a presentation layer over substantially the same analysis.

---

# 63. Validation Reports

Validation reports are separate artifacts rather than fields inside the main database.

Examples:

```text
proofloop_db_validation_report.json
proofloop_pipeline_validation_report.json
proofloop_test_report.json
proofloop_ashby_validation_report.json
proofloop_enriched_db_validation_report.json
proofloop_enriched_test_report.json
```

This avoids mixing:

```text
business/domain data
```

with:

```text
evidence that the pipeline behaved correctly
```

---

# 64. Versioning and Data Interpretation

Versioned scripts matter because analysis semantics changed.

For example:

```text
v0.14 sales signal
```

does not mean exactly the same thing as:

```text
v0.15 sales classification
```

because v0.15 changed the matching model.

Similarly:

```text
role-level overlap
```

is not equivalent to:

```text
v0.16 qualification-level evidence mapping
```

Reports should therefore always retain their producing version.

---

# 65. Data Model Evolution

The model evolved roughly like this:

```text
v0.1–v0.2
HTML role records

v0.3–v0.8.1
validation and pipeline-test metadata

v0.9–v0.10
API-normalized records and reconciliation state

v0.11–v0.13
multi-source relational model

v0.14–v0.15
role-level analysis records

v0.16
qualification-level evidence model

next
Attempt / Target operational tracking
```

The project therefore contains both:

```text
data-model evolution
```

and:

```text
implementation evolution
```

---

# 66. What Is Canonical Today

For the original HTML source:

```text
openai_roles.jsonl
```

is the canonical normalized flat-file representation.

For multi-source role analysis:

```text
proofloop_enriched.db
```

is the canonical relational dataset.

For broad role-selection analysis:

```text
proofloop_role_analysis_report_v0_15.json
```

is the current baseline structured analysis artifact.

For qualification-level analysis:

```text
proofloop_role_deep_analysis_report_v0_16.json
```

is the current deep structured analysis artifact.

For actual job-search selection:

```text
Attempt #001
Targets 001-A / 001-B / 001-C
```

represent the human decision state.

No one file replaces all of the others.

---

# 67. What Is Historical Today

Examples of historical-but-useful artifacts include:

```text
proofloop_openai_ingest_v0_1.py
proofloop_openai_validate_v0_3.py
proofloop_jsonl_to_csv_v0_4.py
proofloop_jsonl_to_sqlite_v0_5.py
proofloop_pipeline_validate_v0_7.py
proofloop_pipeline_validate_v0_7_1.py
test_proofloop_pipeline_v0_7.py
test_proofloop_pipeline_v0_8.py
proofloop_ashby_reconcile_v0_9.py
proofloop_role_analysis.py
```

Historical does not mean worthless.

Some exist specifically because they capture a bug that later versions corrected.

---

# 68. What Should Not Be Inferred From the Model

The current model does **not** prove:

```text
that a role is still open now
that a remote role permits every US state
that a candidate definitely qualifies
that relocation assistance covers all moving costs
that absence of a requirement mention means the requirement does not exist
that an analysis classification is objectively correct
that a resume skill is production-level evidence
```

The system is designed to reduce ambiguity, not erase reality.

---

# 69. Generalization Beyond OpenAI

The current source adapter is OpenAI/Ashby-specific, but the logical model already suggests a more general future shape.

Potential future source adapters:

```text
Ashby
Greenhouse
Lever
Workday
company HTML
manual role capture
```

All could normalize into a shared role identity model:

```text
company
external_provider
external_role_id
title
team / department
primary_location
secondary_locations
employment_type
workplace metadata
job URL
apply URL
description
compensation
snapshot timestamp
```

Then company-specific data can remain in source-specific structures.

---

# 70. Future Shared Role Schema

A future cross-company canonical role model might conceptually contain:

```text
company
provider
external_role_id
canonical_title
canonical_team
canonical_department
employment_type
primary_location
source_status
current_snapshot_presence
job_url
apply_url
published_at
description
```

with children for:

```text
secondary locations
compensation components
source snapshots
analysis results
attempt targets
```

This is a design direction, not yet implemented.

---

# 71. Future Proof Graph

The broader ProofLoop concept will eventually need a model that connects:

```text
requirement
    │
    ▼
evidence
    │
    ├── prior work
    ├── project artifact
    ├── test
    ├── documentation
    └── Proof Sprint
```

Conceptually:

```text
Role Requirement
      │
      ├──── DIRECTLY PROVEN BY ────► Evidence
      │
      ├──── ADJACENT TO ───────────► Evidence
      │
      └──── GAP ───────────────────► Proof Sprint
```

That is not yet part of the SQLite implementation, but v0.16 is the first practical step toward it.

---

# 72. Future Skill-State Model

The broader project already uses the following conceptual skill states:

```text
UNEXPLORED
LEARNING
EXPERIMENTED
APPLIED
TESTED
DOCUMENTED
REPEATED
PROVEN
```

A future Proof Graph could attach those states to evidence rather than treating skill ownership as binary.

Again, this is part of the project architecture but not yet an implemented table in Attempt #001.

---

# 73. Future Research-Evidence State

The wider ProofLoop / AI Observatory design also distinguishes research confidence states such as:

```text
DOCUMENTED
CORROBORATED
REPORTED
INFERRED
HYPOTHESIS
UNKNOWN
SUPERSEDED
```

These are useful for future company intelligence and market research.

They should remain separate from:

```text
job requirement evidence tiers
```

because they answer different questions.

---

# 74. Recommended Future Database Separation

As the project grows, it may become useful to separate:

```text
source ingestion
role intelligence
candidate evidence
attempt tracking
research observatory
```

into distinct logical domains.

A possible future structure:

```text
sources
roles
role_snapshots
role_locations
role_compensation
role_requirements

candidate_evidence
skills
proof_artifacts
proof_sprints

attempts
targets
applications
outcomes

research_claims
research_sources
research_states
```

This is not needed for Attempt #001 yet.

The current model should remain smaller until real usage earns the additional complexity.

---

# 75. Data Model in One View

```text
SOURCE LAYER
─────────────────────────────────────────────

OpenAI Careers.zip
        │
        ▼
HTML normalized roles
        │
        ├── openai_roles.jsonl
        ├── openai_roles.csv
        └── proofloop.db


Ashby snapshot
        │
        ▼
API normalized roles
        │
        └── openai_ashby_roles.jsonl


RECONCILIATION LAYER
─────────────────────────────────────────────

HTML roles ──┐
             ├── Ashby UUID ──► source status
API roles ───┘                  matched/html_only/api_only
                                      │
                                      ▼
                             proofloop_enriched.db


RELATIONAL LAYER
─────────────────────────────────────────────

roles
 │
 ├── html_roles
 ├── api_roles
 │     ├── api_secondary_locations
 │     └── api_compensation_components
 └── build_metadata


ANALYSIS LAYER
─────────────────────────────────────────────

source facts
   │
   ▼
location evidence
sales evidence
technical-core evidence
resume overlap
   │
   ▼
qualification extraction
   │
   ▼
requirement records
   │
   ├── direct match
   ├── claimed skill
   ├── adjacent
   ├── moderate gap
   ├── major gap
   └── unclassified
   │
   ▼
decision review pool


HUMAN DECISION LAYER
─────────────────────────────────────────────

Attempt #001 — OpenAI
   │
   ├── 001-A IT Support Specialist
   ├── 001-B Dedicated Support Engineer
   └── 001-C AI Support Engineer
```

---

## 75.1 Verified source and analytical lineage (documentation-only audit)

The preserved frozen dataset has **817 HTML**, **815 API**, **814 matched**, **3 HTML-only**, **1 API-only**, and **818 union** identities; the enriched database contains **231 secondary-location** and **1,320 compensation-component** child rows. Independent read-only comparison across the preserved files found agreement for all major projected records and their intended fields. This verification establishes *historical internal consistency*, not source completeness or live posting availability.

The analysis considers the **815 API-present** roles rather than the full 818-role union, expands the v0.15 75-role shortlist to a v0.16 population of 224, and emits 30 for manual review. The accepted three-target judgment lives in the Attempt #001 document; **no `applications`, `targets`, `proof_graph`, or outcome-tracking SQL tables are demonstrated by the current enriched database**.

Documentation audit clarifications here do **not** revise or rerun historical code, report values, or source snapshots.

---

# 76. Final Data Principle

The project should always be able to answer four different questions separately:

```text
1. What did the source say?
2. What did the software normalize or derive?
3. What evidence supports the interpretation?
4. What did the human decide?
```

If those four answers become indistinguishable, the model has lost too much provenance.

The purpose of this data model is to prevent that.
