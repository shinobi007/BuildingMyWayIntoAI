# Validation and Testing

## Building My Way Into AI — Attempt #001 / ProofLoop

This document describes how **Attempt #001 — OpenAI** was validated and tested.

The project did not treat a successful script run as proof that the data was correct.

Instead, validation was added as a separate layer and formal tests were introduced to exercise both successful and failing paths.

The central principle is:

> **A pipeline is only trustworthy if it can detect when it is wrong.**

That includes obvious structural failures, subtle control-flow failures, database constraint failures, source-count mismatches, regeneration differences, and platform-specific behavior.

---

# 1. Validation Strategy

The project uses several distinct forms of checking.

```text
input validation
        ↓
artifact validation
        ↓
database validation
        ↓
cross-artifact consistency validation
        ↓
negative-path testing
        ↓
synthetic tests
        ↓
full-pipeline regeneration
```

These checks overlap intentionally.

The goal is not to minimize the number of checks.

The goal is to make it difficult for one flawed component to certify its own bad output.

---

# 2. Why Validation Is Separate From Parsing

The parser is responsible for transformation.

The validator is responsible for asking whether the transformation result is acceptable.

Those are different jobs.

A parser can contain a bug and still produce syntactically valid output.

For that reason, the architecture separates:

```text
producer
```

from:

```text
independent validator
```

where practical.

This pattern appears repeatedly in the project:

```text
HTML parser
    ↓
JSONL validator

JSONL → SQLite importer
    ↓
SQLite validator

API normalization
    ↓
API artifact validator

enriched DB builder
    ↓
enriched DB validator
```

---

# 3. Types of Checks Used

The project currently uses several categories of checks.

## 3.1 Structural checks

Examples:

```text
required field exists
required field is non-empty
expected columns exist
expected tables exist
expected indexes exist
JSON record has expected keys
```

## 3.2 Cardinality checks

Examples:

```text
expected number of roles
expected number of source rows
expected union size
expected matched / source-only counts
```

## 3.3 Identity checks

Examples:

```text
role IDs are sequential
Ashby UUID is extractable
duplicate URLs are rejected
stable cross-source IDs match
```

## 3.4 Integrity checks

Examples:

```text
PRAGMA integrity_check
UNIQUE constraint enforcement
CHECK constraint enforcement
foreign-key-like relationship expectations
```

## 3.5 Equality checks

Examples:

```text
JSONL == regenerated JSONL
JSONL == CSV contents
JSONL == SQLite contents
baseline role IDs == database role IDs
```

## 3.6 Negative-path checks

Examples:

```text
wrong expected count must fail
duplicate unique value must fail
overwrite without permission must fail
invalid source status must fail
```

## 3.7 CLI behavior checks

Examples:

```text
success returns zero
validation failure returns non-zero
failure does not write a misleading success artifact
```

## 3.8 Platform behavior checks

The Windows SQLite locking issue is the most important example.

A script can be logically correct and still fail in real execution because a resource remains open.

---

# 4. Original HTML Pipeline

The original pipeline was built around:

```text
OpenAI Careers.zip
        ↓
HTML parser
        ↓
openai_roles.jsonl
        ↓
openai_roles.csv
        ↓
proofloop.db
```

The expected HTML role count was:

```text
817
```

The parser run itself reported:

```text
Parsed roles: 817
Expected:     817
Issues:       0
```

This was necessary, but not sufficient.

Independent validators and tests were then added.

---

# 5. v0.3 JSONL Validator

The first independent validator was:

```text
proofloop_openai_validate_v0_3.py
```

Its purpose was to validate:

```text
openai_roles.jsonl
```

without depending on the parser's internal success state.

Validation areas included:

```text
record count
required fields
record structure
URL shape
duplicate detection
role ID behavior
```

---

# 6. v0.3 Failure-Propagation Bug

The first validator contained an important bug.

When the user supplied the wrong expected count, the validator could visibly print:

```text
FAIL
```

for the count check.

However, the mismatch was not added to the final `problems` collection used to decide the overall result.

That meant the script could still produce:

```text
RESULT: PASS
```

and exit with:

```text
0
```

even though an expected-count validation had failed.

This was not merely cosmetic.

It meant automation calling the validator could treat a failed validation as success.

---

# 7. v0.3.1 Fix

The corrected version is:

```text
proofloop_openai_validate_v0_3_1.py
```

The fix made expected-count mismatches part of the actual failure state.

The intended behavior became:

```text
correct expected count
    → PASS
    → exit 0

wrong expected count
    → FAIL
    → non-zero exit
```

This was regression-tested.

The lesson was important enough to influence later scripts:

> **Printed output and process success are separate things. Both must be tested.**

---

# 8. CSV Conversion Validation

The JSONL-to-CSV converter evolved through:

```text
proofloop_jsonl_to_csv_v0_4.py
proofloop_jsonl_to_csv_v0_4_1.py
```

The converter produces:

```text
openai_roles.csv
```

with the six expected fields:

```text
role_id
title
team
display_location
career_url
apply_url
```

---

# 9. v0.4 Expected-Count Bug

The first CSV converter had the same conceptual failure class as the early JSONL validator.

An expected-count mismatch could be detected, but the script could still behave as if conversion had succeeded.

That included the risk of writing output even when the expected count was wrong.

---

# 10. v0.4.1 Fix

The corrected converter:

```text
proofloop_jsonl_to_csv_v0_4_1.py
```

enforces the expected count as a real precondition.

The intended behavior is:

```text
input count matches expectation
    → write CSV
    → exit 0

input count does not match expectation
    → do not produce misleading successful output
    → exit non-zero
```

Both positive and negative behavior were later included in the formal test suite.

---

# 11. SQLite Import Validation

The original SQLite importer evolved through:

```text
proofloop_jsonl_to_sqlite_v0_5.py
proofloop_jsonl_to_sqlite_v0_5_1.py
```

It creates:

```text
proofloop.db
```

with the schema:

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

The database layer introduces constraints that the flat-file layers do not enforce as naturally.

---

# 12. Manual SQLite Sanity Checks

Before the full validator existed, several direct SQL checks were used.

Examples included:

```sql
SELECT COUNT(*) FROM roles;
```

Expected result:

```text
817
```

Other exploratory checks examined:

```text
distinct teams
team counts
support-title counts
schema
indexes
sqlite_master
PRAGMA integrity_check
```

A deliberate duplicate `career_url` insert was also attempted.

Expected behavior:

```text
UNIQUE constraint failure
```

The database row count remained unchanged after the failed insert.

This confirmed that the constraint was active rather than merely documented.

---

# 13. Windows SQLite Connection-Lifecycle Failure

The initial v0.5 importer used:

```python
with sqlite3.connect(db_path) as conn:
    ...
```

The important detail is that the SQLite connection context manager handles transaction behavior:

```text
commit
rollback
```

but does not necessarily close the connection immediately when leaving the block.

On Windows, this became visible during temporary-database testing.

The temporary database file could remain locked during cleanup.

That caused test failures such as:

```text
PermissionError
```

even though the SQL operations themselves had succeeded.

---

# 14. v0.5.1 Connection Fix

The corrected importer explicitly manages the connection:

```text
open connection
try
    perform work
    commit
except
    rollback
    re-raise
finally
    close connection
```

This became:

```text
proofloop_jsonl_to_sqlite_v0_5_1.py
```

The fix was not made because explicit `close()` merely looked cleaner.

It was made because the platform behavior caused real test failures.

---

# 15. Original SQLite Validator v0.6

The database validator is:

```text
proofloop_sqlite_validate_v0_6.py
```

It checks the real database independently from the importer.

The real validation result was:

```text
22 / 22 PASS
```

---

# 16. v0.6 Validation Areas

The validator covers areas including:

```text
database can be opened
SQLite integrity is valid
expected roles table exists
expected schema exists
unique indexes exist
expected role count matches
role IDs are sequential
required text fields are present
URLs are unique
URL shapes are plausible
JSONL can be compared against DB
invalid duplicate inserts are rejected
```

Some tests use in-memory or synthetic databases so that destructive checks do not modify the real database.

---

# 17. Why Constraint Testing Matters

A schema declaration such as:

```sql
career_url TEXT NOT NULL UNIQUE
```

should not simply be trusted because the SQL text contains `UNIQUE`.

The validator actively tests bad inserts.

This makes the claim stronger:

```text
schema says the value is unique
```

becomes:

```text
the database actually rejected a duplicate value during testing
```

---

# 18. Full Pipeline Validator v0.7

The first large end-to-end validator was:

```text
proofloop_pipeline_validate_v0_7.py
```

Its purpose was to validate the chain as a system rather than as independent files.

The validator exercises:

```text
source artifacts
derived artifacts
script availability
script syntax
artifact structure
cross-format equality
regeneration behavior
negative expected-count paths
fresh database generation
fresh report generation
```

---

# 19. v0.7 Windows Cleanup Failure

The first full-pipeline validator exposed another Windows file-locking problem.

A connection used to inspect a temporary database remained open long enough to prevent cleanup.

This produced another:

```text
PermissionError
```

on Windows.

The important point is that the validator itself needed validation.

---

# 20. v0.7.1 Fix

The validator's own SQLite connection lifecycle was corrected in:

```text
proofloop_pipeline_validate_v0_7_1.py
```

After that correction, the validator itself could complete its cleanup successfully.

However, the test suite then exposed that the same class of lock still existed inside the v0.5 importer.

That led to the v0.5.1 importer correction.

---

# 21. v0.7.2 Final Full-Pipeline Validator

The final original-pipeline validator is:

```text
proofloop_pipeline_validate_v0_7_2.py
```

It uses the corrected SQLite importer.

The completed real run reported:

```text
45 / 45 checks PASS
```

---

# 22. What v0.7.2 Validates

The full validation battery includes areas such as:

```text
OpenAI Careers.zip exists
source ZIP contains expected HTML
JSONL exists
JSONL has exact expected fields
JSONL contains expected record count
CSV exists
CSV matches JSONL
SQLite database exists
SQLite contents match JSONL
expected reports exist
expected scripts exist
scripts compile successfully
source ingest can regenerate expected records
v0.2 JSONL regeneration is byte-identical
v0.3.1 positive path passes
v0.3.1 negative expected-count path fails
v0.4.1 CSV regeneration succeeds
v0.4.1 negative expected-count path fails
v0.5.1 can regenerate SQLite
v0.6 can generate a fresh validation report
temporary resources clean up correctly
```

The battery therefore checks both:

```text
artifact correctness
```

and:

```text
behavior of the tooling that creates the artifacts
```

---

# 23. Byte-Identical Regeneration

One particularly strong check is that the v0.2 JSONL can be regenerated from the source ZIP and compared byte-for-byte against the existing canonical JSONL.

This tests more than semantic equality.

It checks deterministic serialization for that stage.

Conceptually:

```text
OpenAI Careers.zip
        │
        ▼
regenerate JSONL
        │
        ▼
byte comparison
        │
        ├── identical → PASS
        └── different  → investigate
```

Deterministic outputs make later auditing much easier.

---

# 24. Original Test Suite v0.7

The first formal `unittest` suite was:

```text
test_proofloop_pipeline_v0_7.py
```

It exposed the Windows SQLite lock problem.

Three tests failed with:

```text
PermissionError
```

because temporary SQLite files remained locked.

This was useful.

The test suite found a real lifecycle bug that successful manual runs had not made obvious.

---

# 25. Original Test Suite v0.8

The suite was expanded to:

```text
test_proofloop_pipeline_v0_8.py
```

The same underlying importer lifecycle problem still caused:

```text
3 errors
7 passes
```

This helped confirm that the issue was not isolated to one test.

---

# 26. Final Original Test Suite v0.8.1

After the importer fix, the test suite became:

```text
test_proofloop_pipeline_v0_8_1.py
```

It imports the corrected v0.5.1 importer and also emits a JSON report.

The completed real run reported:

```text
10 tests
10 passed
0 failed
0 errors
0 skipped
```

The report is:

```text
proofloop_test_report.json
```

---

# 27. v0.8.1 Test Inventory

The ten tests cover:

1. Google URL unwrapping
2. synthetic HTML parsing
3. JSONL roundtrip behavior
4. SQLite row creation
5. duplicate career URL rejection
6. SQLite validator behavior on synthetic data
7. v0.3.1 validator positive path
8. v0.3.1 validator negative expected-count path
9. v0.4.1 CSV positive path
10. v0.4.1 CSV negative expected-count path

These tests intentionally mix:

```text
unit behavior
integration behavior
negative behavior
constraint behavior
CLI behavior
```

---

# 28. Why Negative Tests Matter

A test that only proves:

```text
good input succeeds
```

does not prove that the validator is useful.

For validation code, this is equally important:

```text
bad input fails
```

The early v0.3 bug is the clearest example.

Without a negative expected-count test, the defect could have remained invisible.

---

# 29. API Branch Validation

The Ashby/API branch begins from the frozen snapshot:

```text
openai_ashby_snapshot_2026-10-07.json
```

and produces normalized/reconciled artifacts including:

```text
openai_ashby_roles.jsonl
openai_ashby_reconciliation_report_v0_9_1.json
```

The API branch has its own validator:

```text
proofloop_ashby_validate_v0_10.py
```

The real validation result was:

```text
36 / 36 PASS
```

---

# 30. API Validation Responsibilities

The API validator checks the real frozen artifacts rather than assuming that a successful reconciliation run is sufficient.

Validation areas include concepts such as:

```text
snapshot structure
API role count
presence of Ashby IDs
uniqueness of Ashby IDs
normalized API JSONL structure
reconciliation count consistency
matched/source-only arithmetic
missing-ID detection
source relationships
reconciliation report integrity
```

The exact set is version-specific, but the principle is stable:

```text
API ingestion
!=
API validation
```

---

# 31. Reconciliation Consistency

The refined reconciliation produced:

```text
API roles:     815
HTML roles:    817
matched:       814
HTML-only:       3
API-only:        1
```

The union arithmetic is therefore:

```text
814 + 3 + 1 = 818
```

and both source-count relationships must remain internally consistent.

These counts become validation expectations for the enriched database.

---

# 32. Cosmetic vs Substantive Difference Validation

The first reconciliation reported:

```text
56 changed title/team records
```

Closer inspection showed those differences were cosmetic whitespace differences.

The refined v0.9.1 logic performs normalized comparison while preserving original values.

Its result was:

```text
cosmetic changes:     56
substantive changes:   0
```

This is a good example of validation improving the interpretation model rather than merely rejecting data.

---

# 33. Enriched Database Build Validation

The enriched database builder is:

```text
proofloop_build_enriched_db_v0_11.py
```

It creates:

```text
proofloop_enriched.db
```

without modifying:

```text
proofloop.db
openai_roles.jsonl
openai_ashby_roles.jsonl
```

The real build reported:

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

# 34. Overwrite Protection

The v0.11 builder refuses to overwrite an existing enriched database unless explicitly permitted.

Conceptually:

```text
target DB absent
    → create

target DB exists
    → fail unless --overwrite
```

This protects provenance and prevents accidental destruction of an existing build.

The behavior is also formally tested.

---

# 35. Enriched Database Validator v0.12

The enriched database validator is:

```text
proofloop_enriched_db_validate_v0_12.py
```

The real validation result was:

```text
34 / 34 PASS
```

Its report is:

```text
proofloop_enriched_db_validation_report.json
```

---

# 36. Enriched DB Validation Areas

The validator checks concepts including:

```text
SQLite integrity
expected table set
canonical union count
HTML-source count
API-source count
source-status counts
presence-flag consistency
Ashby ID uniqueness
matched/source-only relationships
secondary-location relationships
compensation-component relationships
required canonical fields
original DB preservation
```

The validator verifies the multi-source relational model rather than only checking that the file opens.

---

# 37. Enriched Database Formal Tests v0.13

The formal enriched-database test suite is:

```text
test_proofloop_enriched_db_v0_13.py
```

The completed run reported:

```text
12 tests
12 passed
0 failed
0 errors
0 skipped
```

Runtime during the recorded run was approximately:

```text
0.357 seconds
```

The report is:

```text
proofloop_enriched_test_report.json
```

---

# 38. v0.13 Test Inventory

The twelve formal tests cover:

1. whitespace normalization
2. Ashby ID extraction
3. canonical union and source-status assignment
4. canonical value selection
5. exact source preservation
6. raw and normalized API preservation
7. relational secondary-location storage
8. relational compensation-component storage
9. invalid source-status rejection
10. overwrite refusal
11. wrong expected-count rejection
12. CLI report generation

These tests exercise both the data model and protective behavior.

---

# 39. Invalid Source-Status Test

The canonical role model accepts known source states such as:

```text
matched
html_only
api_only
```

The test suite deliberately attempts to use an invalid state.

Expected behavior:

```text
invalid value rejected
```

This proves that the allowed state space is enforced rather than merely described.

---

# 40. Source Preservation Tests

One of the enriched model's most important promises is:

```text
normalization does not erase source values
```

The v0.13 tests verify that raw/source-specific values remain intact even when normalized values are also created.

This directly protects the provenance model.

---

# 41. Relational Child Tests

Secondary locations and compensation components are stored as child rows.

The test suite verifies that synthetic records produce the expected child relationships.

For example:

```text
one role
    ↓
multiple secondary locations
```

must remain multiple rows rather than a flattened string.

The same principle applies to compensation components.

---

# 42. Role Analysis Validation Philosophy

The role-analysis scripts are different from the ingestion pipeline.

They generate **derived interpretations**, not source truth.

That means validation has to focus on:

```text
internal consistency
transparent rules
known false-positive behavior
stable source population
clear distinction between fact and inference
```

rather than pretending that a classification such as:

```text
HIGH technical core
```

has an objective ground truth.

---

# 43. v0.14 Role Analysis Battery

The first consolidated analysis script was:

```text
proofloop_role_analysis.py
```

corresponding to v0.14.

It successfully ran against:

```text
proofloop_enriched.db
```

in:

```text
READ ONLY
```

mode.

The recorded run reported:

```text
Current API roles:    815
US-Remote anywhere:    44
Remote text matches:   43
Relocation matches:   355
Sales-signal roles:   132
RESULT: PASS
```

---

# 44. What v0.14 Exposed

The important result of v0.14 was not that every heuristic was correct.

It was that the consolidated report made weaknesses visible.

Two major examples emerged.

## Sales false positives

The substring:

```text
commission
```

could match:

```text
commissioning
```

which is common in technical infrastructure work.

## Resume-overlap overreach

Generic technical descriptions could accumulate many keyword matches while still being poor actual role fits.

Those findings were not treated as reasons to discard the analysis system.

They became requirements for v0.15.

---

# 45. v0.15 Role Analysis Improvements

The improved baseline script is:

```text
proofloop_role_analysis_v0_15.py
```

Its recorded run reported:

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

# 46. v0.15 Sales Validation Improvement

v0.15 replaced naïve substring checks with more contextual regular-expression rules.

It also separates:

```text
EXCLUDE_STRONG_SALES
```

from:

```text
REVIEW_SALES_CONTEXT
```

This prevents a weak commercial signal from acting as an automatic hard exclusion.

It also addresses the observed:

```text
commission → commissioning
```

false-positive class.

---

# 47. v0.15 Location Validation Improvement

v0.15 does not use one remote field as the final answer.

It combines:

```text
primary location
secondary locations
workplace_type
is_remote
description wording
office-day wording
relocation wording
```

This behavior was justified by observed source contradictions such as:

```text
is_remote = 1
workplace_type = Hybrid
```

for hundreds of roles.

---

# 48. v0.16 Deep-Analysis Validation

The deep-analysis script is:

```text
role_deep_analysis.py
```

corresponding to v0.16.

It consumes:

```text
proofloop_role_analysis_report_v0_15.json
proofloop_enriched.db
```

The recorded run reported:

```text
Baseline current roles:      815
Deep candidate seed:         224
A_TOP5_REVIEW:                 1
B_SERIOUS_REVIEW:             48
C_STRETCH_REVIEW:            122
Decision pool emitted:        30
RESULT: PASS
```

---

# 49. v0.16 Baseline Consistency Validation

Before performing deep analysis, v0.16 verifies the baseline against the database.

Recorded results:

```text
baseline battery:          v0.15
baseline roles:              815
database current roles:      815
role IDs exact match:       True
SQLite integrity:             ok
```

This prevents the deep report from silently analyzing a different role population than the broad report.

---

# 50. Qualification-Parser Validation

The deep-analysis parser initially needed to distinguish real section headings from ordinary sentences containing words like:

```text
requirements
```

The refined parser only starts qualification extraction from exact line-level headings.

Examples include:

```text
Qualifications
Qualifications:
You might thrive in this role if you:
You might thrive in this role if you have:
What We're Looking For
```

If a clean section is not found, the role is not rewarded as if it had zero requirements.

Instead, it can be placed in:

```text
C_REQUIREMENTS_INCOMPLETE
```

This is an important defensive behavior.

---

# 51. Analysis Validation Is Not Ground Truth

The role-analysis layers are validated for consistency and transparency.

They are not validated as if there were an objective answer to:

```text
Is this candidate a perfect fit?
```

The project therefore distinguishes:

```text
mechanical validation
```

from:

```text
human interpretation
```

The analysis is allowed to say:

```text
UNKNOWN
REVIEW
AMBIGUOUS
```

instead of manufacturing certainty.

---

# 52. Manual Review as a Deliberate Validation Layer

The final target selection included manual review of the decision pool.

This exposed at least one important case where automatic ordering should not be trusted blindly.

`Product Engagement Manager, User Operations` received:

```text
A_TOP5_REVIEW
```

from the rule-based system.

However, manual inspection found:

```text
technical_core = NONE_DETECTED
```

and responsibilities centered heavily on management/product-launch work.

Because the actual target constraint required genuine technical work, the role was not selected.

This is effectively a human validation step over the derived analysis.

---

# 53. Final Attempt #001 Selection

After broad and deep analysis, the first three locked targets became:

```text
001-A — IT Support Specialist
001-B — Dedicated Support Engineer - San Francisco
001-C — AI Support Engineer - San Francisco
```

The selection was not produced by one score.

It used:

```text
source data
location evidence
sales classification
technical-core analysis
qualification mapping
resume evidence
gap analysis
manual judgment
```

This is the intended end state of the validation architecture.

---

# 54. Validation Reports

Current validation/test report artifacts include:

```text
proofloop_db_validation_report.json
proofloop_pipeline_validation_report.json
proofloop_test_report.json
proofloop_ashby_validation_report.json
proofloop_enriched_db_build_report.json
proofloop_enriched_db_validation_report.json
proofloop_enriched_test_report.json
```

Analysis reports include:

```text
proofloop_role_analysis_report_v0_15.json
proofloop_role_analysis_report_v0_15.md
proofloop_role_deep_analysis_report_v0_16.json
proofloop_role_deep_analysis_report_v0_16.md
```

These are separate because:

```text
validation result
```

and:

```text
domain analysis result
```

are different artifact classes.

---

# 55. Current Validation Summary

The major completed validation/test results are:

| Layer | Tool | Result |
| --- | --- | ---: |
| Original SQLite DB | `proofloop_sqlite_validate_v0_6.py` | **22 / 22 PASS** |
| Full original pipeline | `proofloop_pipeline_validate_v0_7_2.py` | **45 / 45 PASS** |
| Original formal tests | `test_proofloop_pipeline_v0_8_1.py` | **10 / 10 PASS** |
| Ashby/API artifacts | `proofloop_ashby_validate_v0_10.py` | **36 / 36 PASS** |
| Enriched database | `proofloop_enriched_db_validate_v0_12.py` | **34 / 34 PASS** |
| Enriched DB formal tests | `test_proofloop_enriched_db_v0_13.py` | **12 / 12 PASS** |
| v0.15 analysis run | `proofloop_role_analysis_v0_15.py` | **RESULT: PASS** |
| v0.16 deep analysis | `role_deep_analysis.py` | **RESULT: PASS** |

This summary should not be read as:

```text
everything is proven correct
```

It means:

```text
the implemented checks passed for the recorded artifacts and known test cases
```

---

# 56. What the Tests Actually Establish

The completed checks provide evidence that:

```text
the original HTML parser produced the expected role count
the normalized JSONL has the expected structure
the CSV reproduces the normalized records
the original SQLite database preserves those records
database uniqueness constraints are active
expected-count failures actually fail
the full pipeline can regenerate key artifacts
Windows SQLite connection bugs were corrected
the Ashby reconciliation counts are internally consistent
the enriched database preserves both source branches
one-to-many child data is relationally preserved
invalid enriched-model states can be rejected
the v0.15 and v0.16 analyses operate on the same 815-role current population
```

These are meaningful guarantees.

They are not universal guarantees.

---

# 57. What the Tests Do Not Establish

The current validation does **not** prove:

```text
every source field was semantically interpreted perfectly
every live OpenAI role is still open now
Ashby's remote metadata means what its name appears to mean
every role-analysis regex is perfect
every qualification was parsed correctly
the resume evidence map is complete
the candidate will pass recruiter review
the selected top three are objectively optimal
```

These remain areas of uncertainty or human judgment.

---

# 58. Snapshot vs Live-State Limitation

The project uses a frozen API snapshot.

Therefore:

```text
validated snapshot state
```

should not be confused with:

```text
current live careers state
```

A future live fetch can legitimately produce different counts.

That would not automatically mean the old validation failed.

It may simply mean the job board changed.

---

# 59. Source-Acquisition Limitation

The original frozen Ashby snapshot was captured before the dedicated reproducible fetch script was introduced.

The project later created:

```text
proofloop_ashby_fetch_v0_8.py
```

for future acquisition.

That improves future reproducibility, but it does not retroactively change how the original snapshot was captured.

This limitation should remain documented.

---

# 60. Test Isolation

Where practical, tests use:

```text
temporary directories
synthetic HTML
synthetic JSONL
synthetic SQLite databases
in-memory SQLite databases
```

rather than modifying the real project artifacts.

This reduces the risk that testing destroys the evidence it is meant to validate.

---

# 61. Why Synthetic Tests Are Necessary

Real-data validation answers:

```text
Does the current real artifact look correct?
```

Synthetic tests answer:

```text
Does this function behave correctly under controlled inputs?
```

Both are necessary.

For example, a real database may contain no duplicate URLs.

That does not prove the database would reject a duplicate.

A synthetic negative test can prove that behavior directly.

---

# 62. Why Real-Artifact Validation Is Necessary

Synthetic tests cannot prove that the actual project artifacts were generated correctly.

That is why the project also validates:

```text
the real 817-role JSONL
the real CSV
the real SQLite database
the real 815-role API snapshot
the real reconciliation report
the real enriched database
```

The two validation modes complement each other.

---

# 63. Failure Taxonomy

The project has encountered several useful classes of failure.

## Control-flow failure

Example:

```text
printed FAIL
but returned success
```

## Resource-lifecycle failure

Example:

```text
SQLite connection stayed open
temporary DB could not be deleted on Windows
```

## Semantic-classification failure

Example:

```text
commission
matched
commissioning
```

## Overgeneralization failure

Example:

```text
is_remote = 1
assumed to mean
true remote work
```

## Ranking-model failure

Example:

```text
high keyword overlap
assumed to mean
high real-world fit
```

Each class required a different kind of correction.

---

# 64. Regression Philosophy

When a bug is discovered, the preferred response is:

```text
reproduce
understand
fix
test the failure path
rerun broader validation
```

rather than:

```text
patch
assume
move on
```

This happened with:

```text
v0.3 → v0.3.1
v0.4 → v0.4.1
v0.5 → v0.5.1
v0.7 → v0.7.1 → v0.7.2
v0.8 → v0.8.1
v0.9 → v0.9.1
v0.14 → v0.15
v0.15 → v0.16
```

Not every version change is the same kind of change, but each records a real refinement.

---

# 65. Recommended Test Command Sequence

For the original HTML pipeline:

```powershell
python .\proofloop_openai_ingest_v0_2.py ".\OpenAI Careers.zip" --expected 817 --output ".\openai_roles.jsonl"
```

Then:

```powershell
python .\proofloop_pipeline_validate_v0_7_2.py --root . --expected 817
```

Then:

```powershell
python .\test_proofloop_pipeline_v0_8_1.py
```

For the enriched branch:

```powershell
python .\proofloop_ashby_validate_v0_10.py
python .\proofloop_enriched_db_validate_v0_12.py
python .\test_proofloop_enriched_db_v0_13.py
```

For the role-analysis layers:

```powershell
python .\proofloop_role_analysis_v0_15.py
python .\role_deep_analysis.py
```

Exact CLI arguments for some later validators may depend on the local script implementation and should be confirmed directly from `--help` before formal publication.

---

# 66. Recommended Pre-Commit Validation

Before the first intentional Git commit, the project should rerun the key stable checks.

Recommended minimum:

```text
full original pipeline validator
original formal tests
Ashby artifact validator
enriched DB validator
enriched DB tests
v0.15 analysis
v0.16 deep analysis
```

The purpose is to establish:

```text
the documented state
```

and:

```text
the committed state
```

as the same state.

---

# 67. Recommended Future CI

The project does not yet have CI configured.

A future GitHub Actions workflow could run:

```text
Python syntax checks
unittest suites
synthetic database tests
artifact-independent validators
```

without necessarily committing every large source snapshot.

The CI design should separate:

```text
tests that can run from repository fixtures
```

from:

```text
tests that require large or private/local source artifacts
```

This is future work, not currently implemented.

---

# 68. Recommended Future Test Organization

As the project grows, the tests could be reorganized into a structure such as:

```text
tests/
    test_html_ingest.py
    test_jsonl_validation.py
    test_csv_conversion.py
    test_sqlite_import.py
    test_reconciliation.py
    test_enriched_db.py
    test_role_analysis.py
    fixtures/
```

The current versioned standalone files are valuable because they document the actual build history.

Repository cleanup can later decide how much historical structure to preserve directly.

---

# 69. Recommended Future Validation Metadata

Each generated report would benefit from standard metadata fields such as:

```text
tool_name
tool_version
generated_at_utc
input_files
input_hashes
expected_counts
actual_counts
result
check_count
pass_count
fail_count
```

Some current reports already contain parts of this pattern.

Standardizing it would make future attempts easier to compare.

---

# 70. Recommended Future Hashing

Future provenance could be strengthened by storing SHA-256 hashes for:

```text
source ZIP
API snapshot
normalized JSONL
CSV
SQLite DB
analysis inputs
```

The Ashby fetch script already moves in this direction by preserving response bytes and hashing them.

A consistent artifact manifest would extend that idea across the project.

---

# 71. Recommended Future Schema Snapshot Tests

The project currently validates expected schema behavior.

A future addition could store machine-readable schema snapshots derived from:

```sql
PRAGMA table_info(...)
PRAGMA index_list(...)
sqlite_master
```

That would make accidental schema drift easier to detect.

---

# 72. Recommended Future Analysis Tests

The role-analysis layers would benefit from small synthetic text fixtures for known classification cases.

Examples:

```text
"commissioning engineer"
    → must NOT trigger commission compensation

"quota-carrying sales role"
    → should trigger strong sales exclusion

"US - Remote" + Hybrid
    → should remain ambiguous

workplace_type = Remote + US - Remote
    → should classify as strong remote evidence

"8+ years preferred"
    → should not be treated exactly like hard required 8+ years
```

These would turn observed heuristic failures into permanent regression tests.

---

# 73. Recommended Future Qualification-Parser Fixtures

The v0.16 section parser should eventually have fixtures for:

```text
Qualifications
Qualifications:
You might thrive in this role if you:
You might thrive in this role if you have:
What We're Looking For
ordinary prose containing "requirements"
posting with no qualification heading
posting with preferred section
```

This would make parser behavior less dependent on the live dataset.

---

# 74. Recommended Future Attempt Validation

Once Attempt/Target tracking is formalized, validation should include:

```text
target references a real canonical role ID
target URL matches canonical role
attempt IDs are unique
target IDs are unique within attempt
submission status transitions are valid
resume variant exists before submission
application timestamp exists when status = submitted
outcome cannot precede submission
```

This does not exist yet.

It is the natural next validation layer once the application-tracking model is implemented.

---

# 75. Testing Philosophy in One View

```text
                 ┌──────────────────┐
                 │   source input   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ transformation   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ output artifact  │
                 └────────┬─────────┘
                          │
              ┌───────────┴────────────┐
              ▼                        ▼
     ┌──────────────────┐    ┌──────────────────┐
     │ real validation  │    │ synthetic tests  │
     └────────┬─────────┘    └────────┬─────────┘
              │                       │
              └───────────┬───────────┘
                          ▼
                 ┌──────────────────┐
                 │ negative paths   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ regression run   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ documented state │
                 └──────────────────┘
```

---

# 76. The Most Important Lessons

The testing work produced several durable lessons.

## Lesson 1

A validator that cannot fail correctly is not a validator.

## Lesson 2

A successful happy-path run says very little about failure behavior.

## Lesson 3

Database resource lifetime matters, especially on Windows.

## Lesson 4

Constraints should be actively tested.

## Lesson 5

Real artifacts and synthetic fixtures answer different questions.

## Lesson 6

A classification heuristic should be treated as a hypothesis until real data challenges it.

## Lesson 7

Ambiguity should survive the pipeline when the source does not justify certainty.

## Lesson 8

Human review is part of validation when the final output is a judgment rather than a deterministic transformation.

---

# 77. Final Testing Principle

The goal of validation in ProofLoop is not to prove that the system can never be wrong.

The goal is to make wrongness:

```text
detectable
reproducible
localized
explainable
correctable
```

That is why the project keeps the failed versions, the regression tests, the validation reports, and the notes about what each check does **not** prove.

The testing history is part of the project evidence, not something to hide after the pipeline starts passing.
