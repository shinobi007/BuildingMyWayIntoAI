# Architecture

## Building My Way Into AI — Attempt #001 / ProofLoop

This document describes the architecture that emerged during **Attempt #001 — OpenAI**.

It is not a description of a system that was designed completely in advance.

The architecture grew in layers as the job-search problem became more demanding:

1. preserve the original OpenAI role list
2. extract structured records from semi-structured HTML
3. normalize those records
4. create portable intermediate formats
5. persist them in SQLite
6. validate every transformation
7. add a second structured source
8. reconcile the sources without overwriting either one
9. build a richer provenance-preserving database
10. analyze the role population
11. map individual qualifications against available evidence
12. use the result to choose real application targets

The architecture therefore reflects both the **data pipeline** and the **decision pipeline**.

---

# 1. System Goals

The system is designed around a few practical goals.

## 1.1 Reproducibility

A result should be regenerable from preserved inputs rather than existing only because it was produced once in an interactive session.

Where practical:

```text
input
  ↓
script
  ↓
output
  ↓
independent validation
```

is preferred over:

```text
manual manipulation
  ↓
result with no reproducible path
```

---

## 1.2 Provenance

The system should preserve the difference between:

```text
what the source said
what normalization changed
what the database stores
what the analysis inferred
what a human finally decided
```

These are separate evidence layers.

The system should not silently collapse them into one value.

---

## 1.3 Inspectability

Intermediate artifacts are intentionally visible.

JSONL, CSV, SQLite tables, JSON reports, Markdown reports, and validation output all exist because they make different parts of the system easier to inspect.

The project does not treat a single opaque end-to-end command as automatically superior.

---

## 1.4 Failure Visibility

A pipeline is only trustworthy if it can fail correctly.

The project therefore added:

- expected-count checks
- schema checks
- URL checks
- duplicate detection
- source-to-source equality checks
- SQLite integrity checks
- negative tests
- CLI exit-code tests
- regenerated-output comparisons
- database constraints
- synthetic test fixtures

Several architecture changes came directly from failures that these checks exposed.

---

## 1.5 Decision Support, Not Automated Judgment

The final system does **not** attempt to let a numeric score choose a job.

Instead, it exposes evidence such as:

```text
location
remote ambiguity
relocation support
technical content
sales risk
experience requirements
education requirements
resume evidence
unproven domains
compensation
source contradictions
```

and then leaves the final role decision to human review.

---

# 2. Architectural Overview

At the highest level, Attempt #001 contains two connected pipelines.

## 2.1 Data Pipeline

```text
Google Docs HTML export
        │
        ▼
HTML parsing
        │
        ▼
structured extraction
        │
        ▼
normalization
        │
        ▼
JSONL
        │
        ├──────────────► CSV
        │
        ▼
SQLite
        │
        ▼
validation + tests
```

A second source was then introduced:

```text
Ashby public job-board API
        │
        ▼
frozen API snapshot
        │
        ▼
API normalization
        │
        ▼
HTML/API reconciliation
        │
        ▼
enriched SQLite database
```

The enriched database then feeds the decision pipeline.

---

## 2.2 Decision Pipeline

```text
proofloop_enriched.db
        │
        ▼
broad role analysis
        │
        ▼
location / sales / technical classification
        │
        ▼
candidate funnel
        │
        ▼
qualification-level analysis
        │
        ▼
manual finalist review
        │
        ▼
Attempt #001 targets
```

The system therefore moves from:

```text
raw source
```

to:

```text
structured evidence
```

to:

```text
human decision
```

without pretending that the final decision is simply another database transformation.

---

# 3. Source Layer

Attempt #001 currently uses two primary role-data sources.

---

## 3.1 Source A — Google Docs HTML Export

The original OpenAI careers list was collected into Google Docs.

A plain-text export was not sufficient because it discarded the hyperlinks associated with the listings.

The document was therefore exported as:

```text
Web Page / HTML ZIP
```

The working source artifact is:

```text
OpenAI Careers.zip
```

This preserved enough HTML structure and link information to reconstruct the role list programmatically.

The HTML source produced:

```text
817 roles
```

This source became the original canonical input for the first pipeline.

---

## 3.2 Source B — Ashby Job-Board API

OpenAI's public Ashby job-board endpoint exposed richer structured records.

The endpoint used during development was:

```text
https://api.ashbyhq.com/posting-api/job-board/openai?includeCompensation=true
```

A frozen snapshot used for the reproducible reconciliation branch is:

```text
openai_ashby_snapshot_2026-10-07.json
```

That snapshot contained:

```text
815 roles
```

The API exposed additional fields including:

```text
id
title
department
team
employmentType
location
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

The API branch adds information to the system.

It does **not** overwrite the HTML source.

---

## 3.3 Acquisition Note

The original frozen Ashby snapshot was captured during the working session before the dedicated acquisition script was introduced.

The project later added:

```text
proofloop_ashby_fetch_v0_8.py
```

to make future API acquisition reproducible and to preserve exact HTTP response bytes together with provenance information.

The current frozen snapshot remains a valid project input, but its acquisition history should remain documented honestly rather than being retroactively rewritten.

---

# 4. HTML Ingestion Layer

The HTML ingestion branch began with:

```text
proofloop_openai_ingest_v0_1.py
```

and evolved into:

```text
proofloop_openai_ingest_v0_2.py
```

The parser uses the Python standard library.

Its major responsibilities are:

```text
open ZIP
find HTML
parse document
identify role records
unwrap URLs
extract fields
normalize records
validate expected structure
write JSONL
```

---

## 4.1 Initial Role Model

The original normalized HTML role model contains six fields:

```text
role_id
title
team
display_location
career_url
apply_url
```

Conceptually:

```python
Role(
    role_id,
    title,
    team,
    display_location,
    career_url,
    apply_url
)
```

The model is intentionally small because it reflects what the HTML source reliably provides.

---

## 4.2 URL Unwrapping

Google-generated exports can wrap outbound URLs.

The parser therefore includes URL-unwrapping logic before storing the career and application URLs.

This normalization is important because later validation and reconciliation depend on stable URLs and Ashby identifiers.

---

## 4.3 Deterministic Role IDs

The original HTML records use sequential integer role IDs:

```text
1
2
3
...
817
```

These IDs represent position in the parsed source.

They are useful inside the HTML pipeline but are **not** treated as the global identity of a job.

Later reconciliation uses the Ashby UUID instead.

---

# 5. JSONL Layer

The first durable normalized artifact is:

```text
openai_roles.jsonl
```

JSONL was chosen because it provides:

- one complete record per line
- straightforward streaming
- human inspectability
- easy Python parsing
- stable field boundaries
- easy conversion to other representations

The v0.2 pipeline produced:

```text
817 JSONL records
```

Each line contains one normalized HTML role.

---

# 6. Independent JSONL Validation

The independent JSONL validator evolved from:

```text
proofloop_openai_validate_v0_3.py
```

to:

```text
proofloop_openai_validate_v0_3_1.py
```

This separation is deliberate.

The parser should not be the only component deciding whether its own output is valid.

The validator checks areas including:

```text
record count
required fields
field structure
URL shapes
duplicate URLs
role ID behavior
expected counts
```

---

## 6.1 Failure Discovered in v0.3

The first validator contained an important control-flow defect.

An expected-count mismatch could print:

```text
FAIL
```

while the overall result could still become:

```text
PASS
```

with a successful exit code.

The mismatch was being displayed but was not included in the final problem state used to determine the process exit status.

This produced:

```text
v0.3
    ↓
failure-path test
    ↓
bug discovered
    ↓
v0.3.1
```

v0.3.1 makes an expected-count mismatch a real validation failure.

---

# 7. CSV Layer

JSONL is converted to CSV by the converter that evolved from:

```text
proofloop_jsonl_to_csv_v0_4.py
```

to:

```text
proofloop_jsonl_to_csv_v0_4_1.py
```

The generated artifact is:

```text
openai_roles.csv
```

The CSV contains the same six core fields as the HTML JSONL:

```text
role_id
title
team
display_location
career_url
apply_url
```

CSV is not the canonical source of truth.

Its purpose is interoperability:

- spreadsheet inspection
- simple manual review
- import into external tools
- transparent comparison with JSONL

---

## 7.1 CSV Failure-Path Fix

The initial v0.4 converter inherited a problem similar to the earlier validator:

an expected-count failure could be reported without being enforced correctly.

v0.4.1 corrected the failure behavior and prevents writing a supposedly successful output when the expected count is wrong.

---

# 8. Original SQLite Layer

The JSONL records are imported into:

```text
proofloop.db
```

using the importer that evolved from:

```text
proofloop_jsonl_to_sqlite_v0_5.py
```

to:

```text
proofloop_jsonl_to_sqlite_v0_5_1.py
```

The original schema is intentionally simple:

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

The database therefore adds enforceable constraints that the flat files cannot provide as naturally.

---

## 8.1 SQLite Connection-Lifecycle Bug

The original importer used a SQLite connection context manager.

That correctly handled:

```text
commit
rollback
```

but did not guarantee the connection was closed immediately.

On Windows, this became visible when test-created temporary databases remained locked during cleanup.

The corrected architecture explicitly performs:

```text
open
try
commit
except
rollback
finally
close
```

This fix became:

```text
v0.5 → v0.5.1
```

The change is important because it came from platform behavior observed during testing rather than from a theoretical style preference.

---

# 9. Original Database Validation

The original database validator is:

```text
proofloop_sqlite_validate_v0_6.py
```

It validates the database independently of the importer.

Checks include areas such as:

```text
database opens successfully
SQLite integrity
expected schema
unique indexes
expected role count
sequential IDs
required field presence
URL uniqueness
URL structure
optional JSONL/database equality
constraint behavior
negative insert behavior
```

The real database validation completed with:

```text
22 / 22 PASS
```

Its report is stored separately as JSON.

---

# 10. Full Original Pipeline Validation

The first complete orchestration validator evolved through:

```text
proofloop_pipeline_validate_v0_7.py
proofloop_pipeline_validate_v0_7_1.py
proofloop_pipeline_validate_v0_7_2.py
```

Its purpose is different from the individual validators.

Instead of asking:

```text
Is this JSONL valid?
```

or:

```text
Is this database valid?
```

it asks:

```text
Does the entire transformation chain remain internally consistent?
```

The final v0.7.2 validation covers areas including:

```text
source ZIP presence
ZIP content
JSONL structure
CSV structure
SQLite contents
report files
script syntax
regeneration
byte-identical JSONL regeneration
expected-count negative paths
fresh CSV generation
fresh SQLite generation
fresh validation report generation
cross-format equality
```

The completed real run reported:

```text
45 / 45 PASS
```

---

# 11. Original Formal Test Suite

Formal tests evolved through:

```text
test_proofloop_pipeline_v0_7.py
test_proofloop_pipeline_v0_8.py
test_proofloop_pipeline_v0_8_1.py
```

The v0.8.1 suite contains ten tests covering both units and integration behavior.

Examples include:

```text
Google URL unwrapping
synthetic HTML parsing
JSONL roundtrip behavior
SQLite row creation
duplicate career URL rejection
SQLite validator behavior
validator positive path
validator negative expected-count path
CSV positive path
CSV negative expected-count path
```

The final run completed:

```text
10 tests
10 passed
0 failed
0 errors
0 skipped
```

Testing is therefore a distinct architecture layer rather than merely a command executed at the end.

---

# 12. Ashby Normalization and Reconciliation

The second source branch starts from the frozen API snapshot.

The first reconciliation implementation is:

```text
proofloop_ashby_reconcile_v0_9.py
```

and the refined version is:

```text
proofloop_ashby_reconcile_v0_9_1.py
```

The branch produces:

```text
openai_ashby_roles.jsonl
```

plus reconciliation reports.

---

## 12.1 Stable Reconciliation Key

The most important architectural choice in this layer is the use of the Ashby UUID.

Example:

```text
49ae54dc-3d33-4107-8112-63fac1ee86ca
```

This identifier is preferred over:

```text
title
team
display text
source row number
```

because those values can change cosmetically or semantically over time.

The UUID can be obtained from:

```text
API id
```

or extracted from the Ashby application URL.

---

## 12.2 Reconciliation Result

The source comparison produced:

```text
HTML roles:            817
API roles:             815
matched:               814
HTML-only:               3
API-only:                1
canonical union:        818
```

This is not treated as an error.

It is evidence that the source populations were captured at different moments.

---

## 12.3 Cosmetic vs Substantive Changes

The first reconciliation reported many raw title/team changes.

Closer inspection showed that the differences were cosmetic whitespace differences rather than real semantic changes.

v0.9.1 therefore normalizes whitespace **for comparison only** while preserving the original values.

The refined result was:

```text
cosmetic title/team differences:      56
substantive title/team differences:    0
```

This illustrates the system's general provenance rule:

```text
normalize enough to compare
do not rewrite the preserved source
```

---

# 13. Ashby Artifact Validation

The API/reconciliation branch has its own validator:

```text
proofloop_ashby_validate_v0_10.py
```

It validates the real frozen snapshot and derived artifacts rather than depending on the original HTML tests.

The real validation result was:

```text
36 / 36 PASS
```

This keeps the API branch independently auditable.

---

# 14. Enriched Database

The enriched database builder is:

```text
proofloop_build_enriched_db_v0_11.py
```

and produces:

```text
proofloop_enriched.db
```

This database is **separate** from the original:

```text
proofloop.db
```

The original database is not upgraded in place.

That is intentional.

The original database remains evidence of the first HTML pipeline, while the enriched database represents the later multi-source architecture.

---

# 15. Enriched Database Schema

The enriched database currently contains:

```text
build_metadata
roles
html_roles
api_roles
api_secondary_locations
api_compensation_components
```

Each table has a distinct responsibility.

---

## 15.1 `roles`

`roles` is the canonical union view.

Its primary identity is:

```text
ashby_id
```

It includes fields used for unified analysis such as:

```text
canonical title
canonical team
display location
source status
source-presence flags
job/application URLs
workplace metadata
descriptions
```

Possible source statuses include:

```text
matched
html_only
api_only
```

---

## 15.2 `html_roles`

This table preserves the normalized HTML-source records.

Its purpose is provenance.

The existence of a canonical value does not erase the value observed in the original HTML branch.

---

## 15.3 `api_roles`

This table preserves API-specific values.

It stores both source-level and normalized information where needed, including richer job metadata.

Examples include:

```text
raw title/team
normalized title/team
department
employment type
location
published timestamp
remote/workplace fields
address JSON
compensation JSON
description text
description HTML
```

---

## 15.4 `api_secondary_locations`

Secondary locations are one-to-many data.

They are therefore stored relationally instead of being flattened into a single text column.

Conceptually:

```text
one role
    │
    ├── secondary location 0
    ├── secondary location 1
    └── secondary location 2
```

This distinction later became critical to remote-work analysis.

---

## 15.5 `api_compensation_components`

Compensation is also one-to-many.

Components preserve information such as:

```text
compensation type
interval
currency
minimum value
maximum value
component order
```

The interval must remain attached to the values.

For example:

```text
USD 60.58–108.17 / hour
```

cannot be meaningfully compared as raw numbers with:

```text
USD 180000–260000 / year
```

---

# 16. Enriched Database Validation

The enriched database validator is:

```text
proofloop_enriched_db_validate_v0_12.py
```

The real database completed:

```text
34 / 34 PASS
```

Validation includes the union population, source relationships, relational children, constraints, and expected source counts.

---

# 17. Enriched Database Tests

Formal synthetic tests are implemented in:

```text
test_proofloop_enriched_db_v0_13.py
```

The suite covers twelve areas including:

```text
whitespace normalization
Ashby ID extraction
union construction
source-status assignment
canonical values
source-value preservation
raw/normalized API values
secondary-location relationships
compensation-component relationships
invalid source-status rejection
overwrite refusal
wrong expected-count rejection
CLI report behavior
```

The completed run reported:

```text
12 tests
12 passed
0 failed
0 errors
0 skipped
```

---

# 18. Role Analysis Layer

Once the enriched database was trustworthy enough to query, the project moved from data engineering into decision support.

The first large consolidation script became:

```text
proofloop_role_analysis.py
```

corresponding to the v0.14 analysis battery.

The improved baseline is:

```text
proofloop_role_analysis_v0_15.py
```

It produces:

```text
proofloop_role_analysis_report_v0_15.json
proofloop_role_analysis_report_v0_15.md
```

---

# 19. Why Role Analysis Is a Separate Layer

The database stores observed facts.

The role-analysis layer creates interpretations.

For example:

```text
database fact:
workplace_type = Hybrid

database fact:
secondary location = US - Remote

analysis interpretation:
remote eligibility is ambiguous
```

The interpretation should not be written back over the facts that produced it.

This is one of the most important architecture boundaries in the system.

---

# 20. Location Analysis

Location turned out to require multiple fields.

The system therefore considers evidence such as:

```text
primary location
secondary locations
is_remote
workplace_type
description wording
office-days language
relocation language
```

The analysis explicitly avoids treating:

```text
is_remote = 1
```

as equivalent to:

```text
workplace_type = Remote
```

because the real dataset contained:

```text
509 roles:
is_remote = 1
workplace_type = Hybrid
```

Only:

```text
21 roles
```

were structured as:

```text
workplace_type = Remote
```

at the time of analysis.

---

## 20.1 Location Categories

v0.15 introduced categories such as:

```text
A_US_REMOTE_STRONG
B_US_REMOTE_AMBIGUOUS
C_US_RELOCATION_SUPPORTED
D_US_LOCATION_UNCLEAR
D_US_ONSITE_OR_HYBRID
E_NON_US_OR_JURISDICTION_MISMATCH
```

These categories are derived interpretation.

They do not replace source fields.

---

# 21. Sales Classification

The user-defined hard constraint is:

```text
NO SALES
```

The first large analysis used broad substring matching.

That produced false positives.

A key example was:

```text
commission
```

matching:

```text
commissioning
```

which is common in technical infrastructure contexts.

v0.15 replaced that approach with more contextual regular expressions and two separate outcomes:

```text
EXCLUDE_STRONG_SALES
REVIEW_SALES_CONTEXT
```

alongside:

```text
NO_SALES_SIGNAL_FOUND
```

This reduces the chance that sales-adjacent vocabulary automatically removes a genuinely technical role.

---

# 22. Technical-Core Classification

The analysis separately estimates whether a role contains meaningful hands-on technical work.

Signals include areas such as:

```text
troubleshooting
systems / infrastructure
APIs / integrations
coding / scripting
automation
testing
technical support
security investigation
```

This classification exists because a role can contain familiar résumé words without actually being the kind of technical work being targeted.

---

# 23. Resume-Evidence Overlap

The analysis also maps description language against known evidence areas.

Examples include:

```text
support
troubleshooting
API integrations
automation
scripting/programming
SQL/data
ITSM/ticketing
networking
UAT/testing
documentation
CRM/SaaS
```

This is intentionally a **discovery aid**, not a final fit score.

The project observed that highly specialized engineering jobs could receive many generic keyword matches while still being poor real-world targets.

---

# 24. Deep Requirement Analysis

The second-stage analysis is implemented by:

```text
role_deep_analysis.py
```

corresponding to v0.16.

It consumes:

```text
proofloop_role_analysis_report_v0_15.json
proofloop_enriched.db
```

and produces:

```text
proofloop_role_deep_analysis_report_v0_16.json
proofloop_role_deep_analysis_report_v0_16.md
```

Its job is to move from:

```text
role-level signals
```

to:

```text
qualification-by-qualification evidence mapping
```

---

# 25. Evidence Tiers

v0.16 models evidence using explicit tiers.

```text
DIRECT_WORK_EVIDENCE
RESUME_SKILL_CLAIM
ADJACENT_EVIDENCE
NOT_EVIDENCED
UNKNOWN
```

These tiers prevent several common reasoning errors.

For example:

```text
Python appears in résumé skills
```

does not automatically mean:

```text
years of professional production Python engineering
```

Similarly:

```text
related operational experience
```

does not automatically mean:

```text
direct professional experience in a specialized domain
```

---

# 26. Requirement Classifications

Individual qualifications can then be mapped to classifications such as:

```text
DIRECT_MATCH
CLAIMED_SKILL_MATCH
ADJACENT_MATCH
MODERATE_GAP
MAJOR_GAP
UNCLASSIFIED_REQUIREMENT
```

The classification describes the current evidence relationship.

It does **not** mean that a gap is permanent or unlearnable.

---

# 27. Qualification Extraction

The deep-analysis parser originally had to distinguish real qualification sections from ordinary prose containing words like:

```text
requirements
```

The refined approach uses exact line-level headings such as:

```text
Qualifications
You might thrive in this role if you:
You might thrive in this role if you have:
What We're Looking For
```

This reduces accidental section capture and makes the evidence mapping more defensible.

---

# 28. Decision Funnel

The v0.16 deep-analysis run began with:

```text
815 current roles
```

and reduced the universe to:

```text
224 roles entering deep requirement analysis
```

The decision-review pool emitted:

```text
30 roles
```

Decision bands included:

```text
A_TOP5_REVIEW
B_SERIOUS_REVIEW
C_STRETCH_REVIEW
C_REQUIREMENTS_INCOMPLETE
D_BACKGROUND
```

These bands were intentionally not treated as final rankings.

---

# 29. Why the System Does Not Auto-Select the Winner

The project found a concrete example of why automated ranking should stop before the final decision.

`Product Engagement Manager, User Operations` initially received the strongest automatic decision band.

But manual inspection showed:

```text
technical_core = NONE_DETECTED
```

and responsibilities centered heavily on:

```text
management
launch coordination
team leadership
product enablement
performance management
```

That conflicted with the actual target constraint:

```text
the role must contain a genuine technical component
```

The architecture therefore intentionally ends automated analysis at:

```text
decision-review pool
```

not:

```text
final answer
```

---

# 30. Attempt and Target Model

The project originally assumed one application would equal one top-level unit.

Actual usage showed that this is too restrictive.

The model is now:

```text
Attempt
    │
    ├── Target
    ├── Target
    └── Target
```

For Attempt #001:

```text
Attempt #001 — OpenAI

001-A — IT Support Specialist
001-B — Dedicated Support Engineer - San Francisco
001-C — AI Support Engineer - San Francisco
```

The stable Ashby UUIDs are:

```text
001-A
49ae54dc-3d33-4107-8112-63fac1ee86ca

001-B
2348230a-295f-434d-9b16-653e01ddbd0b

001-C
1a979fd4-1bce-484e-a416-aed2810677a6
```

Using the external UUID as the durable role identity is safer than using mutable display titles.

---

# 31. Data vs Evidence vs Decision

The architecture can be summarized as three major layers.

## Layer 1 — Observed Data

Examples:

```text
source title
source location
description text
workplace_type
is_remote
salary component
secondary location
```

These come from source artifacts.

---

## Layer 2 — Derived Evidence

Examples:

```text
US remote strong
relocation supported
sales context
technical core high
direct qualification match
major evidence gap
```

These come from transparent analysis rules.

---

## Layer 3 — Human Decision

Examples:

```text
keep role
reject role
build Proof Sprint
apply now
apply despite stretch
ask recruiter about relocation
```

These decisions should remain distinguishable from the underlying facts.

---

# 32. Current File Families

The working directory currently contains several categories of files.

## 32.1 Source / provenance artifacts

Examples:

```text
OpenAI Careers.zip
openai_ashby_snapshot_2026-10-07.json
```

---

## 32.2 Core normalized data

Examples:

```text
openai_roles.jsonl
openai_roles.csv
openai_ashby_roles.jsonl
```

---

## 32.3 Databases

```text
proofloop.db
proofloop_enriched.db
```

---

## 32.4 Validation and test reports

Examples include:

```text
proofloop_db_validation_report.json
proofloop_pipeline_validation_report.json
proofloop_test_report.json
proofloop_ashby_validation_report.json
proofloop_enriched_db_validation_report.json
proofloop_enriched_test_report.json
```

---

## 32.5 Analysis reports

Examples:

```text
proofloop_role_analysis_report.md
proofloop_role_analysis_report.json

proofloop_role_analysis_report_v0_15.md
proofloop_role_analysis_report_v0_15.json

proofloop_role_deep_analysis_report_v0_16.md
proofloop_role_deep_analysis_report_v0_16.json
```

---

## 32.6 Implementation history

Historical scripts currently remain beside the latest scripts.

Examples:

```text
proofloop_openai_ingest_v0_1.py
proofloop_openai_ingest_v0_2.py

proofloop_openai_validate_v0_3.py
proofloop_openai_validate_v0_3_1.py

proofloop_jsonl_to_csv_v0_4.py
proofloop_jsonl_to_csv_v0_4_1.py

proofloop_jsonl_to_sqlite_v0_5.py
proofloop_jsonl_to_sqlite_v0_5_1.py

proofloop_pipeline_validate_v0_7.py
proofloop_pipeline_validate_v0_7_1.py
proofloop_pipeline_validate_v0_7_2.py
```

Repository cleanup will decide whether all historical implementations should remain directly in Git or whether some should be represented through commits, tags, releases, and documentation instead.

No history should be rewritten merely to make the project appear cleaner than it actually was.

---

# 33. Reproducibility Boundaries

Not every stage currently has the same level of reproducibility.

The original HTML branch is strongly reproducible from:

```text
OpenAI Careers.zip
```

through:

```text
JSONL
CSV
SQLite
validation
tests
```

The enriched branch is reproducible from the preserved:

```text
openai_ashby_snapshot_2026-10-07.json
```

plus the HTML artifacts.

Future API acquisition can use:

```text
proofloop_ashby_fetch_v0_8.py
```

but a live API request made at a future date should not be expected to return the exact same role population as the frozen 2026-10-07 snapshot.

That is why the frozen snapshot is part of the provenance story.

---

# 34. Technology Choices

The project currently relies heavily on the Python standard library.

Major technologies include:

```text
Python
HTMLParser
json
csv
sqlite3
urllib
hashlib
unittest
argparse
dataclasses
pathlib
```

Development has been performed with:

```text
Windows
PowerShell 7
Python virtual environment
SQLite
```

This approach keeps the project:

```text
low-cost
portable
inspectable
dependency-light
```

It also forces the implementation to make the underlying transformations explicit.

---

# 35. Why SQLite

SQLite fits Attempt #001 well because it provides:

- relational structure
- constraints
- indexes
- joins
- aggregations
- portability
- zero external server requirement
- direct Python standard-library support

It also makes the transition from flat files to relational thinking visible without introducing unnecessary infrastructure.

For the current scale:

```text
hundreds of roles
thousands of related records
```

SQLite is more than sufficient.

---

# 36. Why Both JSON and Markdown Reports

The analysis layers produce both:

```text
JSON
Markdown
```

for different reasons.

## JSON

Used for:

```text
machine-readable continuation
future scripts
exact structured values
repeatable downstream analysis
```

## Markdown

Used for:

```text
human inspection
documentation
manual comparison
decision review
GitHub readability
```

The same analysis therefore supports both the machine and human sides of ProofLoop.

---

# 37. Architectural Lessons From Real Failures

Several architecture decisions are direct consequences of observed failures.

## 37.1 Never trust a displayed failure alone

A script can print:

```text
FAIL
```

and still return success.

Exit behavior and final state must be tested.

---

## 37.2 Context-manager semantics matter

A resource can commit correctly while still remaining open long enough to break Windows cleanup.

Resource lifetime must be explicit where platform behavior matters.

---

## 37.3 Structured metadata can still be semantically misleading

A field named:

```text
is_remote
```

does not guarantee the interpretation:

```text
can work remotely from anywhere
```

Real source behavior must be measured.

---

## 37.4 Keyword matching is evidence, not understanding

Substring rules can confuse:

```text
commission
```

with:

```text
commissioning
```

and generic technical vocabulary can make highly specialized jobs appear superficially aligned.

Context and manual review remain necessary.

---

## 37.5 A clean score can hide a bad assumption

The role with the strongest rule-based band was not necessarily the strongest real-world target.

Transparent decomposition is more valuable than a single unexplained score.

---

# 38. Current Architectural Boundary

The project is currently transitioning from:

```text
build and analyze
```

to:

```text
document and package
```

The implemented technical path is:

```text
Python
→ HTML parsing
→ data extraction
→ normalization
→ JSON / JSONL
→ CSV
→ SQLite
→ validation
→ testing
```

and has expanded through:

```text
API acquisition
→ source reconciliation
→ enriched relational storage
→ role analysis
→ qualification analysis
→ Attempt #001 target selection
```

The next architecture work is **not** to add another analysis layer.

The next work is to make the existing architecture easier for another person to understand and reproduce.

---

# 39. Planned Documentation Around This Architecture

This file describes the system shape.

Other documents will separate concerns:

```text
README.md
    public project overview and entry point

docs/architecture.md
    system structure and data flow

docs/data_model.md
    fields, tables, schemas, relationships, provenance

docs/validation_and_testing.md
    validators, test suites, failures, fixes, guarantees

docs/attempt_001.md
    OpenAI attempt, selection process, final targets, evidence trail

docs/lessons_learned.md
    engineering and process lessons

CHANGELOG.md
    chronological implementation history
```

The goal is that no one document has to carry the entire project.

---

# 40. Architecture in One View

```text
┌──────────────────────────────────────────────────────────────┐
│                    SOURCE / PROVENANCE                       │
│                                                              │
│  OpenAI Careers.zip            Ashby API snapshot            │
│         │                              │                     │
└─────────┼──────────────────────────────┼─────────────────────┘
          │                              │
          ▼                              ▼
┌──────────────────┐          ┌──────────────────────┐
│ HTML parser      │          │ API normalization    │
│ v0.1 / v0.2      │          │ + reconciliation     │
└────────┬─────────┘          └──────────┬───────────┘
         │                               │
         ▼                               ▼
┌──────────────────┐          ┌──────────────────────┐
│ openai_roles     │          │ openai_ashby_roles  │
│ JSONL / CSV      │          │ JSONL                │
└────────┬─────────┘          └──────────┬───────────┘
         │                               │
         ▼                               │
┌──────────────────┐                    │
│ proofloop.db     │                    │
│ original SQLite │                    │
└────────┬─────────┘                    │
         │                               │
         └──────────────┬────────────────┘
                        ▼
              ┌──────────────────────┐
              │ source reconciliation│
              │ Ashby UUID identity │
              └──────────┬───────────┘
                         ▼
              ┌──────────────────────┐
              │ proofloop_enriched  │
              │ .db                 │
              └──────────┬───────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
┌──────────────────────┐      ┌──────────────────────┐
│ validation / tests   │      │ role analysis v0.15 │
│                      │      │                      │
│ 22/22 DB             │      │ location            │
│ 45/45 pipeline       │      │ sales               │
│ 10/10 tests          │      │ technical core      │
│ 36/36 API            │      │ evidence overlap    │
│ 34/34 enriched DB    │      └──────────┬───────────┘
│ 12/12 enriched tests │                 │
└──────────────────────┘                 ▼
                              ┌──────────────────────┐
                              │ deep analysis v0.16 │
                              │ qualification-level │
                              │ evidence mapping    │
                              └──────────┬───────────┘
                                         ▼
                              ┌──────────────────────┐
                              │ manual decision      │
                              │ review               │
                              └──────────┬───────────┘
                                         ▼
                              ┌──────────────────────┐
                              │ Attempt #001        │
                              │ 001-A / 001-B /     │
                              │ 001-C               │
                              └──────────────────────┘
```

---

# 41. Final Principle

The architecture is not valuable because it is elaborate.

It is valuable if another person can follow:

```text
where the data came from
what transformed it
what was preserved
what was inferred
what failed
what was tested
what remains uncertain
and how the final decision was reached
```

That is the standard this documentation is trying to establish.
