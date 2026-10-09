# Changelog

All notable changes to **Building My Way Into AI / ProofLoop** are documented here.

This changelog records the actual development history of **Attempt #001 — OpenAI** as reconstructed from the versioned scripts, generated artifacts, validation reports, test results, and decisions made during the build.

The project did not begin with formal semantic versioning or Git history. Early versions such as `v0.3.1`, `v0.5.1`, and `v0.7.2` are therefore preserved as part of the real implementation history rather than rewritten into a cleaner fictional sequence.

---

## Documentation review update — after Stages 1–8

This entry records an **editorial and evidence-audit update**, not a new ProofLoop software release. The original 817-role HTML and 815-role API snapshots, databases, program code, reports and user-approved three-target shortlist are unchanged. The README was supplied for review, resolving the earlier *unavailable-for-inspection* question; its prior absence among uploads was never evidence that it had not been written.

### Documentation files revised

- `README.md`: navigation, historical-versus-planned boundaries, testing claims, field-projection omission, algorithmic limits and output-safety cautions.
- `docs/data_model.md`: projected API-field coverage, full location-category taxonomy, v0.16 year/requirement semantics, complete decision-band counts, schema-state versus validation-state, and replacement behavior.
- `docs/attempt_001.md`: accepted selection kept intact, with tighter 001-C seniority/degree interpretation, transparent 001-A/001-B/001-C risk levels, and explicit absence of evidence for submission outcomes.
- `docs/lessons_learned.md`: original 103 lessons preserved; evidence-audit lessons appended without retroactively renumbering the historical record.
- `CHANGELOG.md`: this documentation-only change and corrected historical summary details.

The `docs/` links are the **intended repository paths**, not proof the local working folder was previously reorganized. `docs/architecture.md` and `docs/validation_and_testing.md` were reviewed as source references but are **not rewritten in this five-file delivery**. They may need a final synchronization pass before publication.

### Audited findings

- The historical v0.16 `A_TOP5_REVIEW` (1), `B_SERIOUS_REVIEW` (48), and `C_STRETCH_REVIEW` (122) counts do not exhaust the 224 candidates; `C_REQUIREMENTS_INCOMPLETE` (23) and `D_BACKGROUND` (30) also exist. The separately emitted decision-review pool contains 30 roles.
- The v0.15 source retains `is_remote` for evidence, but `classify_location()` does not use that variable in its branches. The code defines `B_REMOTE_US_LOCATION_AMBIGUOUS`, which was unpopulated in the frozen report.
- The frozen raw Ashby record includes `shouldDisplayCompensationOnJobPostings`, omitted from the normalized JSONL/database projection. Raw snapshot preservation remains intact.
- The v0.16 `expectation_strength()` can mark a whole requirement `PREFERRED` because it contains `ideally`. For 001-C, this does **not** establish the 8+ years expectation as optional; the `DIRECT_MATCH` tag also does not verify cumulative duration.
- The original and enriched SQLite builders can remove an existing output before a successful `--overwrite` rebuild is secured. Historical output correctness and replacement safety are separate claims.
- The current enriched database has no implemented application ledger, formal Target/Attempt tables, Proof Graph, skill-state tables or Observatory service. Those remain planned.
- Recorded PASS results are historical: the six principal reports show **137 passing validation checks** and **22 passing formal tests**. This editorial update did not rerun them.

### Historical code and datasets

**No changes** to source scripts, data sources, original archived reports, database files, or their recorded outcomes. The corrections concern explanatory claims and limitations.

---

# Unreleased

## Documentation phase

### Added

- `README.md`
  - Public-facing overview of Building My Way Into AI.
  - Explains the project as a real job-search attempt that generated technical work rather than as a prebuilt "job-analysis framework."
  - Documents the major pipeline stages, validation results, Attempt/Target model, and final Attempt #001 targets.

- `docs/architecture.md`
  - Documents the full source-to-decision architecture.
  - Covers HTML ingestion, API ingestion, normalization, JSONL/CSV/SQLite, reconciliation, enriched storage, validation, analysis, and final decision boundaries.

- `docs/data_model.md`
  - Documents the original HTML role model.
  - Documents the enriched relational model.
  - Separates source facts, normalized values, derived evidence, and human decisions.
  - Documents evidence tiers and future Attempt/Target data concepts without pretending they are already implemented.

- `docs/validation_and_testing.md`
  - Documents validation philosophy, negative-path testing, regression behavior, SQLite locking failures, formal test suites, and current guarantees/limitations.

- `docs/attempt_001.md`
  - Documents the OpenAI attempt, the user's criteria and résumé evidence, the analysis funnel, the assistant-led final comparative selection, and the three locked targets.

- `docs/lessons_learned.md`
  - Captures engineering, analytical, workflow, repository, and AI-collaboration lessons from Attempt #001.

- `CHANGELOG.md`
  - Adds the first chronological project history.

### Changed

- Reframed the project unit from:

  ```text
  Application #001
  ```

  to:

  ```text
  Attempt #001
      ├── Target 001-A
      ├── Target 001-B
      └── Target 001-C
  ```

- Established **Attempt** as the company/opportunity-level unit and **Target** as the individual role-level unit.

### Planned

Before the first Git milestone, the project is expected to move through:

```text
finish documentation
        ↓
repository cleanup
        ↓
streamlined / presentable implementation pass
        ↓
.gitignore and repository structure
        ↓
Git initialization
        ↓
intentional first commit
```

The streamlined version is intended to make the project usable by another person rather than leaving them with only the historical development files.

The target experience is roughly:

```text
clone / obtain project
        ↓
read setup
        ↓
provide supported input
        ↓
run pipeline
        ↓
validate outputs
        ↓
inspect reports
        ↓
see whether the workflow works for them
```

This streamlined version is **planned but not yet implemented**.

The existing Attempt #001 implementation should remain preserved as development history rather than being silently replaced.

---

# 2026-10-08 — Attempt #001 final role selection

## Added

Locked the first three canonical targets for **Attempt #001 — OpenAI**.

### Target 001-A — IT Support Specialist

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

Selection rationale:

- strongest overall balance of demonstrated experience and practical plausibility
- strong technical-support / IT / systems alignment
- no strong sales signal
- explicit relocation assistance
- no detected explicit years-of-experience floor
- main gaps concentrated in AV/event-production and deeper endpoint/device-management tooling

### Target 001-B — Dedicated Support Engineer - San Francisco

Team:

```text
Support Delivery
```

Ashby ID:

```text
2348230a-295f-434d-9b16-653e01ddbd0b
```

Apply URL:

```text
https://jobs.ashbyhq.com/openai/2348230a-295f-434d-9b16-653e01ddbd0b/application
```

Selection rationale:

- strongest work-content alignment with the desired technical-support direction
- strong overlap with API/integration troubleshooting
- incident handling
- logs / metrics / traces / reproduction / hypothesis testing
- technical customer communication
- no detected explicit multi-year requirement
- main risks are distributed-systems/cloud depth and unresolved San Francisco relocation feasibility

### Target 001-C — AI Support Engineer - San Francisco

Team:

```text
Support Delivery
```

Ashby ID:

```text
1a979fd4-1bce-484e-a416-aed2810677a6
```

Apply URL:

```text
https://jobs.ashbyhq.com/openai/1a979fd4-1bce-484e-a416-aed2810677a6/application
```

Selection rationale:

- strong bridge from existing SaaS/support evidence into AI-native technical support
- direct support/troubleshooting/customer-communication alignment
- Python/API/automation relevance
- v0.16 reported no major domain gaps under its rule set; this is **not** proof of fully satisfied qualifications
- the posting's 8+ years expectation was over-softened to `PREFERRED` by the model's sentence-wide `ideally` detection, and `DIRECT_MATCH` did not verify actual years
- larger unresolved risks are genuine seniority/production-depth competitiveness and San Francisco location

## Decision process

The final top three were **not** produced by simply taking the three highest automatic analysis bands.

The selection combined:

```text
user-defined criteria
resume evidence
v0.15 broad analysis
v0.16 qualification-level analysis
manual finalist comparison
assistant judgment
user acceptance
```

Notable roles deliberately not selected included:

- `Product Engagement Manager, User Operations`
  - received a strong automated review band
  - rejected from the final three because the technical core did not satisfy the user's requirement for genuinely technical work

- `Technical Systems Program Manager, User Operations`
  - strong CRM/API/automation/system alignment
  - downgraded because of an explicit 8+ year technical-program-management expectation

- several remote Security roles
  - stronger geographic feasibility
  - downgraded because specialized security/threat-intelligence requirements were not adequately supported

---

# v0.16 — Qualification-level deep role analysis

## Added

Created:

```text
role_deep_analysis.py
```

Corresponding analysis version:

```text
ProofLoop Role Deep Analysis v0.16
```

Generated:

```text
proofloop_role_deep_analysis_report_v0_16.md
proofloop_role_deep_analysis_report_v0_16.json
```

## Purpose

Moved the analysis from:

```text
role-level signals
```

to:

```text
qualification-by-qualification evidence mapping
```

## Added evidence tiers

```text
DIRECT_WORK_EVIDENCE
RESUME_SKILL_CLAIM
ADJACENT_EVIDENCE
NOT_EVIDENCED
UNKNOWN
```

## Added requirement classifications

```text
DIRECT_MATCH
CLAIMED_SKILL_MATCH
ADJACENT_MATCH
MODERATE_GAP
MAJOR_GAP
UNCLASSIFIED_REQUIREMENT
```

## Added analysis concepts

- qualification-section extraction
- responsibility-section extraction
- preferred/bonus-section handling
- domain detection
- technology extraction
- experience-year extraction
- seniority burden
- career lane
- title alignment
- location path
- major/moderate gap tracking
- decision-review bands

## Improved

- qualification headings are matched at the line level rather than by loose prose matching
- missing qualification extraction no longer behaves like a perfect zero-gap role
- programming-language résumé entries remain skill claims rather than being promoted to production-engineering evidence
- location paths preserve:
  - remote now
  - remote needs confirmation
  - relocation supported
  - US location dependency

## Validation

Recorded run:

```text
Baseline current roles:      815
Deep candidate seed:         224
A_TOP5_REVIEW:                 1
B_SERIOUS_REVIEW:             48
C_STRETCH_REVIEW:            122
C_REQUIREMENTS_INCOMPLETE:   23
D_BACKGROUND:                30
Deep candidate total:       224
Decision pool emitted:        30
RESULT: PASS
```

Baseline consistency:

```text
baseline roles:          815
database current roles:  815
role IDs exact match:    True
SQLite integrity:        ok
```

## Design decision

The v0.16 decision bands are intentionally:

```text
manual review aids
```

not:

```text
final automated rankings
```

---

# v0.15 — Revised role-selection transparency battery

## Added

Created:

```text
proofloop_role_analysis_v0_15.py
```

Generated:

```text
proofloop_role_analysis_report_v0_15.md
proofloop_role_analysis_report_v0_15.json
```

## Purpose

Refined the first exploratory role-analysis battery into a more defensible baseline for:

```text
location feasibility
sales filtering
technical-core analysis
resume-evidence discovery
candidate funneling
```

## Fixed

### Sales false positives

The v0.14 substring approach could match:

```text
commission
```

inside:

```text
commissioning
```

v0.15 replaced broad substring matching with more contextual regular-expression logic.

### Sales-state overcompression

Introduced distinct outcomes:

```text
EXCLUDE_STRONG_SALES
REVIEW_SALES_CONTEXT
NO_SALES_SIGNAL_FOUND
```

instead of treating every sales-adjacent word as equivalent.

### Remote interpretation

The location-analysis dossier retains multiple forms of evidence:

```text
primary location
secondary locations
workplace_type
is_remote (stored/displayed, not directly used in classify_location() branches)
description wording
office-day wording
relocation wording
```

The final v0.15 location-category branches use structured workplace type, location strings and description/office/relocation signals rather than treating any single Boolean as authoritative. This clarification describes the historical code, not a change to its output.

## Added location categories

```text
A_US_REMOTE_STRONG
B_US_REMOTE_AMBIGUOUS
B_REMOTE_US_LOCATION_AMBIGUOUS
C_US_RELOCATION_SUPPORTED
D_US_LOCATION_UNCLEAR
D_US_ONSITE_OR_HYBRID
E_NON_US_OR_JURISDICTION_MISMATCH
```

## Recorded run

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

---

# v0.14 — Consolidated role-analysis battery

## Added

Created the first large consolidated role-analysis implementation (historically labeled v0.14). Its **uploaded, directly inspectable file** is:

```text
proofloop_role_analysis.py
```

The changelog originally referenced `proofloop_role_analysis_v0_14.py`; that exact additional filename has not been supplied as a separate source file. Preserve the historical version label, but do not claim that a second distinct v0.14 source copy has been inspected.

Generated:

```text
proofloop_role_analysis_report.md
proofloop_role_analysis_report.json
```

## Added analysis areas

- source status
- work-arrangement behavior
- primary locations
- team distribution
- broad remote population
- actual `workplace_type=Remote` population
- remote/location contradictions
- `US - Remote` primary or secondary roles
- all secondary locations
- technical-family feature map
- résumé-keyword overlap
- sales-risk signals
- remote wording context
- relocation wording context
- experience-year language
- education language
- compensation with interval/currency
- data-quality checks
- exact SQL catalog

## Recorded run

```text
Current API roles:    815
US-Remote anywhere:    44
Remote text matches:   43
Relocation matches:   355
Sales-signal roles:   132
RESULT: PASS
```

## Learned

The v0.14 report exposed two major weaknesses:

1. broad sales substring matching produced false positives
2. generic technical-keyword overlap could overstate real fit

Those findings directly motivated v0.15.

---

# v0.13 — Enriched database formal tests

## Added

Created:

```text
test_proofloop_enriched_db_v0_13.py
```

Generated:

```text
proofloop_enriched_test_report.json
```

## Added tests

The formal synthetic suite covered:

1. whitespace normalization
2. Ashby ID extraction
3. union/source-status behavior
4. canonical value behavior
5. exact source preservation
6. raw and normalized API preservation
7. relational secondary locations
8. compensation-component relationships
9. invalid source-status rejection
10. overwrite refusal
11. incorrect expected-count rejection
12. CLI report generation

## Result

```text
12 tests
12 passed
0 failed
0 errors
0 skipped
```

Recorded runtime:

```text
~0.357 seconds
```

---

# v0.12 — Enriched database validator

## Added

Created:

```text
proofloop_enriched_db_validate_v0_12.py
```

Generated:

```text
proofloop_enriched_db_validation_report.json
```

## Validation areas

- SQLite integrity
- enriched table set
- canonical union counts
- HTML/API source counts
- source-status counts
- presence-flag consistency
- Ashby ID uniqueness
- source relationships
- secondary-location relationships
- compensation-component relationships
- required canonical values
- preservation of original database

## Result

```text
34 / 34 PASS
```

---

# v0.11 — Enriched multi-source SQLite database

## Added

Created:

```text
proofloop_build_enriched_db_v0_11.py
```

Generated:

```text
proofloop_enriched.db
proofloop_enriched_db_build_report.json
```

## Added tables

```text
build_metadata
roles
html_roles
api_roles
api_secondary_locations
api_compensation_components
```

## Added

- canonical union by Ashby UUID
- source status:
  - `matched`
  - `html_only`
  - `api_only`
- source-presence flags
- preserved HTML-source values
- preserved API-source values
- relational secondary locations
- relational compensation components
- raw and normalized API comparison fields
- overwrite protection

## Architectural decision

The enriched database does **not** replace:

```text
proofloop.db
```

The original HTML-only database remains a separate artifact.

## Recorded build

```text
HTML roles:                  817
API roles:                   815
canonical union roles:       818
roles table:                 818
html_roles table:            817
api_roles table:             815
secondary locations:         231
compensation components:    1320
matched:                     814
html_only:                     3
api_only:                      1
RESULT: PASS
```

---

# v0.10 — Ashby artifact validator

## Added

Created:

```text
proofloop_ashby_validate_v0_10.py
```

Generated:

```text
proofloop_ashby_validation_report.json
```

## Purpose

Added independent validation for:

```text
frozen API snapshot
normalized API JSONL
reconciliation report
cross-source counts
Ashby IDs
matched/source-only relationships
```

## Result

```text
36 / 36 PASS
```

---

# v0.9.1 — Refined Ashby reconciliation

## Added

Created:

```text
proofloop_ashby_reconcile_v0_9_1.py
```

Generated:

```text
openai_ashby_reconciliation_report_v0_9_1.json
```

## Changed

Whitespace normalization is now used **for comparison only**.

Original source values remain preserved.

## Result

```text
API roles:                          815
HTML roles:                         817
matched:                            814
HTML-only:                            3
API-only:                             1
cosmetic title/team differences:    56
substantive title/team differences:  0
missing IDs:                          0
RESULT: PASS
```

## Fixed

The earlier reconciliation described 56 title/team differences too broadly as "changed."

v0.9.1 distinguishes cosmetic whitespace differences from substantive changes.

---

# v0.9 — Initial Ashby reconciliation

## Added

Created:

```text
proofloop_ashby_reconcile_v0_9.py
```

Generated:

```text
openai_ashby_roles.jsonl
openai_ashby_reconciliation_report.json
```

## Added

- normalization of the frozen Ashby API snapshot
- Ashby UUID extraction
- HTML/API reconciliation by UUID
- source-only role reporting
- comparison of title/team values

## Initial reconciliation

```text
API roles:      815
HTML roles:     817
matched:        814
HTML-only:        3
API-only:         1
```

Initial raw comparison reported:

```text
56 title/team differences
```

which later proved cosmetic.

## Source-state discovery

HTML-only roles:

```text
Trust & Safety Ads Operations Analyst, Data
Strategic Delivery Lead, Intelligence Community
Product Policy Research and Advisory Partnerships
```

API-only role:

```text
Accounting Manager
```

The population difference demonstrated that the two source snapshots represented different moments in time.

---

# Ashby API acquisition branch

## Added

Created:

```text
proofloop_ashby_fetch_v0_8.py
```

## Purpose

Added a reproducible acquisition path for OpenAI's public Ashby job-board endpoint.

The script was designed to:

- use the Python standard library
- fetch the public endpoint
- validate the JSON/jobs structure
- preserve exact HTTP response bytes
- calculate SHA-256
- write provenance
- use atomic writes
- refuse accidental overwrite by default
- support an optional expected role count
- timestamp acquisition in UTC
- retry transient failures

## Important provenance note

The original frozen snapshot:

```text
openai_ashby_snapshot_2026-10-07.json
```

had already been captured before this dedicated fetch script was added.

The script therefore improves future acquisition reproducibility but does not retroactively change the acquisition history of the original snapshot.

---

# v0.8.1 — Final original-pipeline formal tests

## Added

Created:

```text
test_proofloop_pipeline_v0_8_1.py
```

Generated:

```text
proofloop_test_report.json
```

## Changed

Updated the test suite to use the corrected:

```text
proofloop_jsonl_to_sqlite_v0_5_1.py
```

importer.

## Tests

1. URL unwrapping
2. synthetic HTML parsing
3. JSONL roundtrip
4. SQLite row creation
5. duplicate career URL rejection
6. synthetic SQLite validator behavior
7. v0.3.1 positive validation
8. v0.3.1 negative expected-count validation
9. v0.4.1 positive CSV conversion
10. v0.4.1 negative expected-count conversion

## Result

```text
10 tests
10 passed
0 failed
0 errors
0 skipped
RESULT: PASS
```

---

# v0.8 — Expanded original-pipeline test suite

## Added

Created:

```text
test_proofloop_pipeline_v0_8.py
```

Expanded the earlier formal tests to ten cases.

## Result

The suite exposed the same underlying Windows SQLite connection-lifecycle problem.

Recorded result before the importer fix:

```text
7 passed
3 errors
```

The failing tests produced Windows:

```text
PermissionError
```

during temporary database cleanup.

---

# v0.7.2 — Final original full-pipeline validator

## Added / Changed

Created:

```text
proofloop_pipeline_validate_v0_7_2.py
```

Updated the full validator to use the corrected:

```text
proofloop_jsonl_to_sqlite_v0_5_1.py
```

importer.

## Validation scope

The battery validates:

- source ZIP presence and content
- JSONL structure
- exact JSONL fields
- CSV equality
- SQLite equality
- script/report presence
- script syntax
- parser regeneration
- byte-identical JSONL regeneration
- validator success path
- validator failure path
- CSV success path
- CSV failure path
- SQLite regeneration
- fresh database validation report
- temporary resource cleanup

## Result

```text
45 / 45 PASS
```

---

# v0.7.1 — Full-pipeline validator cleanup fix

## Changed

Corrected SQLite connection handling inside the validator itself.

## Fixed

The original v0.7 validator could leave a temporary database inspection connection open long enough for Windows cleanup to fail.

After the validator's own connection was fixed, the broader test suite revealed that the same underlying lifecycle issue still existed in the v0.5 importer.

---

# v0.7 — Initial full-pipeline validator

## Added

Created:

```text
proofloop_pipeline_validate_v0_7.py
```

## Purpose

Added the first end-to-end validation layer across:

```text
source ZIP
JSONL
CSV
SQLite
validators
reports
scripts
regeneration
```

## Discovered

A Windows temporary-database cleanup failure exposed incomplete SQLite connection lifecycle management.

This led to:

```text
v0.7.1
```

and later:

```text
v0.5.1
v0.7.2
```

---

# v0.6 — Original SQLite validator

## Added

Created:

```text
proofloop_sqlite_validate_v0_6.py
```

Generated:

```text
proofloop_db_validation_report.json
```

## Validation areas

- database opens successfully
- `PRAGMA integrity_check`
- expected schema
- unique indexes
- expected role count
- sequential role IDs
- required fields
- URL uniqueness
- URL shape
- optional JSONL equality
- invalid insert behavior

## Result

```text
22 / 22 PASS
```

## Manual verification

A deliberate duplicate `career_url` insert failed as expected and did not change the final row count.

---

# v0.5.1 — SQLite importer connection fix

## Added

Created:

```text
proofloop_jsonl_to_sqlite_v0_5_1.py
```

## Fixed

Explicitly manages SQLite connection lifecycle:

```text
open
try
commit
except
rollback
finally
close
```

This corrected Windows temporary-file locking observed during formal tests.

## Important note

The original existing:

```text
proofloop.db
```

did not require rebuilding solely because of this importer lifecycle fix.

The data itself had been written correctly; the defect affected connection cleanup behavior.

---

# v0.5 — Initial JSONL → SQLite importer

## Added

Created:

```text
proofloop_jsonl_to_sqlite_v0_5.py
```

Generated:

```text
proofloop.db
```

## Added schema

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

## Added

- SQLite persistence
- primary-key enforcement
- unique URL constraints
- relational querying

## Discovered later

The connection context manager handled transaction behavior but did not guarantee immediate connection closure.

On Windows, this caused temporary-database cleanup failures during tests.

---

# v0.4.1 — Corrected JSONL → CSV conversion

## Added

Created:

```text
proofloop_jsonl_to_csv_v0_4_1.py
```

## Fixed

Expected-count mismatch now causes a real failure.

The corrected behavior is:

```text
correct count
    → write CSV
    → exit success

wrong expected count
    → fail
    → do not write misleading successful output
```

## Regression tested

Both positive and negative count behavior were later included in the formal test suite.

---

# v0.4 — Initial JSONL → CSV conversion

## Added

Created:

```text
proofloop_jsonl_to_csv_v0_4.py
```

Generated:

```text
openai_roles.csv
```

## Added fields

```text
role_id
title
team
display_location
career_url
apply_url
```

## Discovered

The first implementation inherited a failure-state problem similar to v0.3:

an expected-count mismatch could be reported without being enforced strongly enough.

---

# v0.3.1 — Corrected independent JSONL validator

## Added

Created:

```text
proofloop_openai_validate_v0_3_1.py
```

## Fixed

Expected-count mismatches now enter the actual error state and produce a non-zero process exit.

Correct behavior:

```text
correct expected count
    → RESULT: PASS
    → exit 0

wrong expected count
    → RESULT: FAIL
    → non-zero exit
```

## Regression tested

Both success and failure paths were later included in formal tests.

---

# v0.3 — Initial independent JSONL validator

## Added

Created:

```text
proofloop_openai_validate_v0_3.py
```

## Purpose

Separated validation from the parser.

Added checks for:

- expected record count
- required fields
- record structure
- URL shapes
- duplicate values
- role-ID behavior

## Discovered

An expected-count mismatch could print:

```text
FAIL
```

but fail to enter the final problem collection.

The process could therefore still report:

```text
RESULT: PASS
```

and exit successfully.

This was the first important negative-path validation bug discovered in the project.

---

# v0.2 — HTML ingestion with JSONL output

## Added

Created:

```text
proofloop_openai_ingest_v0_2.py
```

Generated:

```text
openai_roles.jsonl
```

## Added

- JSONL serialization
- deterministic normalized role records
- configurable output path
- expected-count checking

## Real run

```powershell
python .\proofloop_openai_ingest_v0_2.py ".\OpenAI Careers.zip" --expected 817 --output ".\openai_roles.jsonl"
```

Recorded result:

```text
Parsed roles: 817
Expected:     817
Issues:       0
```

The canonical local filename is:

```text
openai_roles.jsonl
```

A later chat-upload rename did not change the local canonical artifact.

---

# v0.1 — Initial OpenAI HTML parser

## Added

Created:

```text
proofloop_openai_ingest_v0_1.py
```

## Purpose

Parse the Google Docs Web Page export stored inside:

```text
OpenAI Careers.zip
```

## Added

Standard-library implementation using:

```text
HTMLParser
zipfile
dataclasses
urllib parsing
```

## Initial normalized role model

```text
role_id
title
team
display_location
career_url
apply_url
```

## Added behavior

- load HTML from ZIP
- parse role listing structure
- unwrap Google redirect URLs
- normalize role records
- validate required fields
- detect duplicates
- validate URL shapes
- check expected record count

## Real run

```powershell
python .\proofloop_openai_ingest_v0_1.py ".\OpenAI Careers.zip" --expected 817
```

Recorded result:

```text
Parsed roles: 817
Expected count: PASS
Validation issues: 0
```

---

# Initial source acquisition and project setup

## Source problem

The OpenAI careers list was first collected into Google Docs.

A plain-text export lost the role hyperlinks.

The source was therefore re-exported as:

```text
Web Page / HTML ZIP
```

which preserved the URLs required for programmatic extraction.

## Initial technical goal

The original planned chain was:

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
→ documentation
→ Git
```

Attempt #001 completed the chain through testing and then expanded beyond it into:

```text
Ashby API acquisition
→ reconciliation
→ enriched database
→ role analysis
→ deep qualification analysis
→ final target selection
```

Documentation is now being completed before repository cleanup and Git initialization.

---

# Project state at the documentation milestone

Completed:

```text
[complete] Python pipeline
[complete] HTML parsing
[complete] data extraction
[complete] normalization
[complete] JSON / JSONL
[complete] CSV
[complete] original SQLite database
[complete] independent validation
[complete] formal testing
[complete] Ashby/API reconciliation
[complete] enriched SQLite database
[complete] enriched validation
[complete] enriched formal tests
[complete] broad role analysis
[complete] qualification-level analysis
[complete] Attempt #001 target selection
[complete] README
[complete] architecture documentation
[complete] data-model documentation
[complete] validation/testing documentation
[complete] Attempt #001 documentation
[complete] lessons learned
[complete] changelog
```

Next:

```text
[next] repository cleanup
[next] streamlined / externally usable implementation pass
[next] docs/ directory organization
[next] .gitignore
[next] Git initialization
[next] intentional first commit
[next] GitHub repository
[next] target-specific application preparation
```

---

# Changelog philosophy

This changelog intentionally keeps the imperfect versions visible.

The history:

```text
v0.3 → v0.3.1
v0.4 → v0.4.1
v0.5 → v0.5.1
v0.7 → v0.7.1 → v0.7.2
v0.8 → v0.8.1
v0.9 → v0.9.1
v0.14 → v0.15 → v0.16
```

is part of the evidence.

The project is not stronger because the failed versions are hidden.

It is stronger because the failure, diagnosis, correction, and regression path can be explained.
