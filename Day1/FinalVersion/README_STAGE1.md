# ProofLoop Ashby Search — Stage 1: Offline Validation and Normalization

**Project:** Building My Way Into AI / Attempt #001 — OpenAI  
**Implementation:** `proofloop_normalize.py`  
**Dependencies:** Python 3.10+ standard library only. No network, tokens, API keys, pip installs, or database writes.  
**Status:** Implemented and tested against the previously captured OpenAI Ashby snapshot.

## Purpose and boundary

This is the **first new streamlined script**. It reads one frozen JSON response from Ashby's public job-posting API, validates its structure, preserves every original job object, creates predictable normalized fields, and emits a JSON and Markdown report. It does **not** fetch fresh listings, build SQLite, select jobs, or conduct career analysis. Those stages follow after this contract is tested locally.

The historical `Day1` scripts and snapshot remain untouched. Use the empty `Day1\FinalVersion` directory for the new code, not for overwriting the historical source.

## Step 1 — Place the new files in FinalVersion

Copy these files from the downloaded Stage 1 package into `Day1\FinalVersion`:

- `proofloop_normalize.py`
- `test_proofloop_normalize.py`
- `README_STAGE1.md`

Keep your existing frozen JSON in **`Day1`** (the parent directory). No need to move or rename it.

## Step 2 — Identify your original snapshot filename

Open PowerShell 7 in `Day1\FinalVersion` and run:

```powershell
Get-ChildItem ..\*ashby*snapshot*.json | Select-Object Name, Length
```

The file shown in the command below is an example filename. Use the exact name reported on **your** machine.

## Step 3 — Normalize the historical snapshot

```powershell
python .\proofloop_normalize.py --snapshot '..\openai_ashby_snapshot_2026-10-07.json' --board openai --output-dir '.\runs\openai_oct07_stage1' --expected-count 815
```

Notes:

- `--snapshot` is read-only. Your original bytes remain unchanged.
- `--board openai` identifies the source board and populates normalized provenance fields.
- `--expected-count 815` deliberately applies to this **frozen October 7 fixture only**. For a future live snapshot, omit `--expected-count` unless you intentionally know the expected count.
- `--output-dir` must **not already exist**; each run gets a fresh name. An existing output is never overwritten.
- An invalid snapshot returns a nonzero exit status, does not publish a partial result directory, and writes a sibling `*.FAILED.<run_id>.json` report when possible.

### Output layout

```text
FinalVersion/
  proofloop_normalize.py
  test_proofloop_normalize.py
  README_STAGE1.md
  runs/
    openai_oct07_stage1/
      normalized/
        jobs.jsonl
      reports/
        normalization_report.json
        normalization_report.md
```

### JSONL record layout

One complete job object per line, with three top-level sections:

```json
{
  "provenance": {
    "provider": "ashby",
    "board": "openai",
    "snapshot_sha256": "<source-hash>",
    "source_index": 1
  },
  "canonical": {
    "id": "<posting-id>",
    "title": "<normalized-display-title>",
    "description_plain": "<original-plain-description>",
    "is_remote": null,
    "compensation": {}
  },
  "raw": {
    "id": "<posting-id>",
    "title": "<original-exact-title>",
    "<all other source keys>": "<preserved as given>"
  }
}
```

This JSON snippet is **illustrative** and abbreviated. Real rows include the full canonical field set and complete original job object. Unknown future job fields appear in `raw` and in the schema audit. The raw source snapshot remains the canonical byte-for-byte original.

We intentionally store the original job object again in JSONL, so the file is larger than a purely flattened representation. That favors auditability at this stage. Later SQLite tables can use typed columns while retaining raw source references.

## Step 4 — Run automated synthetic tests

From `FinalVersion`:

```powershell
python .\test_proofloop_normalize.py --report-dir '.\runs\stage1_test_report'
```

This exercises duplicate-ID rejection, field-type strictness, nullable remote values, URLs, nested compensation/location structures, invalid JSON, wrong expected counts, deterministic output, unknown-field preservation, and refusal to overwrite accepted output.

Outputs:

- `runs\stage1_test_report\test_report.json`
- `runs\stage1_test_report\test_report.md`

To run again, choose a new report directory (for example `stage1_test_report_2`).

## Historical fixture reference

The previously uploaded snapshot named `openai_ashby_snapshot_2026-10-07(1).json` produced:

| Metric | Recorded Stage 1 result |
|---|---:|
| Jobs / unique IDs | 815 / 815 |
| Secondary locations | 231 |
| Compensation tiers | 668 |
| Tier-level compensation components | 1346 |
| `isRemote`: true / false / null | 530 / 29 / 256 |
| `workplaceType`: Hybrid / Remote / OnSite / null | 509 / 21 / 29 / 256 |
| Synthetic tests | 17 passing |

Snapshot SHA-256: `97bdd769266238538febac6448a9a1dd2502a8a6765d6feba2e22073b66e4ba5`.  
Normalized JSONL SHA-256 for this exact uploaded fixture: `8d76cdde4c693d98d2a7798d1b8bced0d870ba78a87e60d9a47c694dfc7e7682`.

If the JSON was previously reformatted on your PC, its **byte-level hash may differ** even if the 815 parsed job objects match. Do not change a source file just to match the uploaded fixture hash.

## What Stage 1 verifies and does not verify

**Verified**: valid JSON, jobs-array structure, nonblank posting IDs and titles, ID uniqueness, types for known fields, valid HTTPS format for URLs when supplied, basic nested data structures, optional/null handling, and stable output hashing. All parsed source job objects were independently compared against the generated rows for the supplied fixture.

**Not verified**: live availability, employer permission to work remotely, accuracy of job descriptions, whether you meet qualifications, deeper compensation semantics, or correctness of future classifier decisions. The next stages will add independent JSONL/SQLite reconciliation and meaningful analytical checks.

## Next implementation

Stage 2: create the safe public Ashby fetcher using the same input contract. Then build transactional SQLite storage and source-to-database validation, followed by broad/deep analysis and AI comparison of five targets. Keep separate per-stage reports and tests.
