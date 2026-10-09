# ProofLoop Ashby — Stage 3: Offline SQLite Storage

Version 0.3.0. This is the third step of the new streamlined pipeline:

`Stage 2 fetch → Stage 1 normalized JSONL → Stage 3 SQLite → analysis stages later`

## What this stage does

`proofloop_store.py` reads the Stage 1 JSONL, verifies its SHA-256 against the optional Stage 1 normalization report, validates record IDs and field structures, creates a new standalone SQLite database, and checks that the data stored can be recovered. It does not contact Ashby or change either upstream input.

### Tables

- `roles`: normalized query fields, full normalized JSON, full parsed raw source job JSON, provenance JSON.
- `secondary_locations`: per-job location/address records.
- `compensation_tiers`: salary/equity/etc. tier records.
- `compensation_components`: components inside each compensation tier.
- `compensation_summary_components`: separate summary-level compensation components.
- `build_metadata`: input data and software version references.
- `role_overview` SQL VIEW: convenient concise selection for later broad analysis.

The Stage 2 raw snapshot contains the original HTTP bytes. Stage 3 preserves data as parsed JSON, not original byte formatting. Field additions unknown to the normalizer remain accessible through `roles.raw_json`.

## Extract safely

Extract the Stage 3 ZIP into your existing `Day1\FinalVersion` folder. The ZIP adds **only**:

```
proofloop_store.py

test_proofloop_store.py

README_STAGE3.md

sample_store_reports/

sample_store_test_reports/
```

These filenames do not conflict with Stage 1 or Stage 2 files. The ZIP excludes bulky SQLite sample files and does not contain your private résumé.

## Run Stage 3 using your LIVE normalized output

In PowerShell 7 opened in `Day1\FinalVersion`:

```powershell
python .\proofloop_store.py --jsonl '.\runs\openai_live_normalized_001\normalized\jobs.jsonl' --normalization-report '.\runs\openai_live_normalized_001\reports\normalization_report.json' --output-dir '.\runs\openai_live_sqlite_001'
```

The command will create:

```
runs/openai_live_sqlite_001/
  db/jobs.sqlite3
  reports/store_report.json
  reports/store_report.md
```

Expected example from the uploaded October 8/9 live dataset: 816 roles, 227 secondary locations, 667 compensation tiers, 1346 tier components, 1320 summary components.

**Every output directory must be new.** The importer refuses to overwrite an existing directory and does not modify prior databases.

## Test Stage 3

Run **after** you have checked the successful import:

```powershell
python .\test_proofloop_store.py --report-dir '.\runs\stage3_test_report'
```

The synthetic test suite creates temporary databases and checks failures, constraints, JSON round trips, and overwrite safety. It does not require a network connection.

## Example SQL query (optional; not needed yet)

```sql
SELECT title, team, location, workplace_type, job_url
FROM role_overview
WHERE title LIKE '%Support%'
ORDER BY title;
```

## Verification and limitations

- The SQLite database is created in a temporary directory and is published only after verification succeeds.
- Reports include the normalized JSONL SHA-256, original snapshot SHA-256 from the records, input record counts, relational child-table counts, database digest, integrity check, foreign-key check, and JSON-equivalence roundtrip checks for all rows and children.
- If a build fails, no success bundle is published; a generic failure sidecar may be written near the requested output directory.
- SQLite `REAL` columns expose compensation amounts for querying; the exact JSON numeric values remain preserved in the JSON fields.
- This stage does not decide whether a posting is currently available, whether remote work is possible from Utah, or whether a candidate is qualified.
- Output SQLite binary bytes need not be identical across different builds; preserved field contents and reports are verified semantically.

## Next stage

Stage 4 will build **standalone validation** so the database and source can be checked independently of the builder. Then the role-analysis stages can consume the stable `role_overview` and underlying evidence fields.
