# Building My Way Into AI / ProofLoop Search
## Stage 2 — Public Ashby API snapshot acquisition

**Version:** `0.2.0`  
**Dependency:** Stage 1 `proofloop_normalize.py` must remain next to this script.  
**Runtime:** Python 3.10 or newer; Python standard library only.  
**Scope:** Fetch or replay one Ashby public job board; publish exact source bytes plus an acquisition report. This stage does **not** construct SQLite, analyze fit, or recommend jobs.

### Relationship to Stage 1

Stage 1 already validates and normalizes frozen snapshots. Stage 2 obtains new snapshots from Ashby's documented public job-board endpoint, **validates its response using the Stage 1 contract**, and publishes an immutable source artifact. Each stage publishes its own report. The primary pipeline is:

`Stage 2 fetch → raw JSON snapshot → Stage 1 normalize → JSONL + normalization report → future SQLite stage`

The two stage numbers reflect implementation order, not data-flow order. It was safer to verify the normalizer offline first.

### 1. Install

Extract `ProofLoop_Ashby_Stage2_Code_and_Reports.zip` into:

`Desktop\BuilidingMyWayIntoAI\Day1\FinalVersion`

Windows may show a slightly different project-folder spelling; keep the actual path used on your computer. Do **not** move or overwrite your original snapshot in `Day1`.

After extraction, `FinalVersion` should contain:

```text
proofloop_normalize.py        # existing Stage 1
 test_proofloop_normalize.py   # existing Stage 1
proofloop_fetch.py            # NEW Stage 2
 test_proofloop_fetch.py       # NEW Stage 2
README_STAGE2.md              # NEW instructions
sample_fetch_reports/         # NEW reference reports
sample_test_reports/          # NEW reference reports
```

### 2. First run: validate a frozen snapshot offline

From PowerShell 7 **in `FinalVersion`**, run:

```powershell
python .\proofloop_fetch.py --board openai --source-file '..\openai_ashby_snapshot_2026-10-07.json' --output-dir '.\runs\openai_oct07_stage2_fetch' --expected-count 815
```

Expected stdout begins:

```text
PASS: acquired and structurally checked 815 jobs
Mode: frozen_file
Output: runs\openai_oct07_stage2_fetch
Source SHA-256: 97bdd769266238538febac6448a9a1dd2502a8a6765d6feba2e22073b66e4ba5
Reports: reports/fetch_report.json and .md
```

Here, `--source-file` means **no network request**. It validates the old source using the new fetcher's acquisition pipeline and writes a **copy**, not an edited/reformatted JSON file. The original source remains untouched. The expected count of 815 applies only to this fixed historical file.

Generated:

```text
runs/openai_oct07_stage2_fetch/
  raw/ashby_snapshot.json
  reports/fetch_report.json
  reports/fetch_report.md
```

Output directories must be new; **nothing is overwritten automatically**. To rerun, choose a different `--output-dir` name.

### 3. Run the Stage 2 test suite

```powershell
python .\test_proofloop_fetch.py --report-dir '.\runs\stage2_test_report'
```

Expected based on local synthetic tests: **23 tests**, all PASS. The tests use simulated network responses and temporary files; they do not access Ashby.

Test cases include bad boards, retry on HTTP 429/503, no retry on 400, network outage, unexpected HTML responses, bad compression, redirected URLs, oversized responses, wrong counts, duplicates, malformed records, output refusal and safe failure sidecars.

### 4. Fetch a fresh public board (after frozen test succeeds)

```powershell
python .\proofloop_fetch.py --board openai --output-dir '.\runs\openai_live_fetch_001'
```

This **does contact** `https://api.ashbyhq.com/posting-api/job-board/openai?includeCompensation=true`, subject to normal internet access and public-endpoint availability. No Ashby employer API key or paid service is required for this public feed. An arbitrary numeric expected count is **not** applied to the live board; live vacancies change.

The program has bounded requests, retries for transient HTTP/network failures, a byte limit, response content-type and final-URL checks, and source JSON structural verification.

### 5. Normalize the new fetched file using Stage 1

After a successful live fetch:

```powershell
python .\proofloop_normalize.py --snapshot '.\runs\openai_live_fetch_001\raw\ashby_snapshot.json' --board openai --output-dir '.\runs\openai_live_normalize_001'
```

The Stage 1 source SHA-256 should equal the Stage 2 fetch report SHA-256. This is an explicit provenance chain across stages.

### What the reports do and do not establish

The fetch report contains run ID, mode (offline/live), date/time, endpoint only when contacted, final response URL, response HTTP status, fetch attempts, exact byte count, SHA-256, record count, unique job count, nested location and compensation counts, and warnings about unexpected fields.

`fetch_report.json` and `.md` are stored beside the snapshot in a single newly published directory. Failed validation does **not** publish a success directory. Where possible it generates `OUTPUT_NAME.FAILED.RUN_ID.json` alongside it instead.

Reports verify **acquisition and structure**, not current individual-job availability, eligibility to work from a given location, salary eligibility, or candidate qualifications.

The public Ashby job-board endpoint does not provide employer-only job-posting details and application-management data that require privileged credentials.

### Development evidence

The Stage 2 script was tested **offline**, using the historical 815-job snapshot and 23 independent synthetic tests; its successful snapshot bytes matched the frozen input. A subsequent normalization replay produced the exact same JSONL SHA-256 as the previously verified Stage 1 output:

`8d76cdde4c693d98d2a7798d1b8bced0d870ba78a87e60d9a47c694dfc7e7682`

**A new live API request has not been run in this development environment.** The live-fetch code has been exercised with controlled/mock responses, not independently verified against a fresh live server in this stage.
