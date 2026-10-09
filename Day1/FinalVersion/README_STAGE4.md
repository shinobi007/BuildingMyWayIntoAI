# ProofLoop Ashby — Stage 4: Independent Source-to-SQLite Validation

**Version:** 0.4.0  
**Requirements:** Python 3.10+; standard library only; existing Stage 1 and Stage 3 outputs.  
**No internet required.**

## Purpose

Stage 4 is a new, standalone, **read-only independent validator**. It does not import the Stage 1 normalizer or Stage 3 database builder. Instead, it separately examines five artifacts:

1. The exact Stage 2 public API snapshot (`raw/ashby_snapshot.json`).
2. The Stage 1 normalized JSONL (`normalized/jobs.jsonl`).
3. The Stage 3 SQLite database (`db/jobs.sqlite3`).
4. The Stage 1 normalization JSON report.
5. The Stage 3 storage JSON report.

It compares all 816 jobs and all their nested secondary locations, compensation tiers, tier components, and summary components to independently establish source → JSONL → SQLite data fidelity. It also checks SQL scalar columns, foreign keys, integrity, build metadata, report fingerprints/counts, source ordering, board identity, and permitted whitespace trimming.

### Important semantics

- `raw` JSON in each normalized record must exactly match the corresponding **parsed** source job. JSON byte formatting is preserved **only** by the Stage 2 snapshot artifact.
- For `title`, `team`, `department`, and `location`, the Stage 1 canonical projection deliberately strips leading/trailing whitespace; the validator allows exactly that transformation.
- Nullable `isRemote` and `workplaceType` fields retain unknown values, not false/onsite assumptions.
- The validator does not verify current job availability or candidate qualifications.
- An independent validator detects inconsistencies but cannot prove all source statements true or rule out every shared modeling error.

## Installation

Extract the Stage 4 ZIP into your existing `Day1\FinalVersion` folder. It includes **only new filenames and uniquely named sample report folders**:

```
proofloop_validate.py

test_proofloop_validate.py

README_STAGE4.md

sample_validation_reports/
  validation_report.json
  validation_report.md

sample_validation_test_reports/
  test_report.json
  test_report.md
```

Existing Stage 1, Stage 2, and Stage 3 scripts must remain in the folder. The Stage 4 test suite imports `proofloop_store.py` **only to create disposable synthetic fixture databases**. The actual validator does not import it.

## Step 1 — Independently validate your 816-job live run

Open PowerShell 7 in `Day1\FinalVersion` and run **one command**:

```powershell
python .\proofloop_validate.py --snapshot '.\runs\openai_live_fetch_001\raw\ashby_snapshot.json' --jsonl '.\runs\openai_live_normalized_001\normalized\jobs.jsonl' --db '.\runs\openai_live_sqlite_001\db\jobs.sqlite3' --normalization-report '.\runs\openai_live_normalized_001\reports\normalization_report.json' --store-report '.\runs\openai_live_sqlite_001\reports\store_report.json' --output-dir '.\runs\openai_live_validation_001'
```

Successful output should resemble:

```
PASS: independent checks 24 passed, 0 failed
Output: runs\openai_live_validation_001
Reports: validation_report.json and .md
```

Your reports will appear in `runs\openai_live_validation_001\` (not inside an additional `reports` subfolder).

**Do not reuse an existing output directory.** No existing outputs are overwritten. If an input is missing or structurally unreadable, the script will return a failure code and attempt to produce a FAILURE report at the requested new report directory.

## Step 2 — Run the Stage 4 synthetic tests

Do this after checking Stage 4's live-snapshot validation:

```powershell
python .\test_proofloop_validate.py --report-dir '.\runs\stage4_test_report'
```

Expected historical suite: 24 tests. They create disposable synthetic databases, deliberately introduce corruption, and check that validation fails for the correct reasons. Unlike the validator itself, these synthetic tests create and modify temporary fixture files and databases. They do **not** modify your live database or existing run outputs.

## Sample reports included in the ZIP

- `sample_validation_reports`: a **PASS 24/24** independent validation against the uploaded 816-job live snapshot, its normalized JSONL, the uploaded SQLite file, and both original reports.
- `sample_validation_test_reports`: **PASS 24/24** synthetic tests that included deliberate corruption cases.

Do not copy sample results over your locally generated results: your local run must independently establish its own PASS.

## What comes next

After Stage 4 passes locally, we have independently checked the fetch → normalize → SQLite data chain and can begin **initial broad role analysis**, followed by **deep qualification analysis** and the final **AI-assisted top-five decision packet**. Those later stages interpret posting content; Stage 4 does not.
