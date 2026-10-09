# ProofLoop — Stage 5: Broad Role Analysis (v0.5.0)

**Purpose:** A transparent, heuristic **triage** pass over all roles in the previously verified Stage 3 SQLite database. Stage 5 does **not** make hiring decisions, assert candidate qualifications, or automatically select a top five. It supplies the evidence-backed handoff pool for Stage 6's deep analysis and AI-assisted final review.

## What to extract

Extract only these new files/folders from `ProofLoop_Ashby_Stage5_Code_and_Reports.zip` into `Day1\FinalVersion`:

- `proofloop_broad.py`
- `test_proofloop_broad.py`
- `config\search_profile.example.json`
- `README_STAGE5.md`
- `sample_stage5_reports\openai_live_816_final\...` and `sample_stage5_reports\test_suite_final_v2\...` (reference examples only)

No existing Stage 1–4 scripts, databases, reports, or directories need replacement.

## Step 1 — Run the broad analysis

In PowerShell 7 from `Day1\FinalVersion`, paste **one command**:

```powershell
python .\proofloop_broad.py --db '.\runs\openai_live_sqlite_001\db\jobs.sqlite3' --store-report '.\runs\openai_live_sqlite_001\reports\store_report.json' --validation-report '.\runs\openai_live_validation_001\validation_report.json' --profile '.\config\search_profile.example.json' --output-dir '.\runs\openai_live_broad_001'
```

Expected outputs in `runs\openai_live_broad_001`:

- `broad_analysis_report.json` — complete evidence dossier for **every** job, along with profile policy and fingerprints.
- `broad_analysis_report.md` — readable overview, classifications, and full proposed review pool.
- `deep_review_candidates.json` — ID-based candidate handoff for Stage 6.

Expected when run against the uploaded October 8 live snapshot: `PASS: analyzed 816 jobs; 100 for deep review`. Actual results may differ if you supply another database, profile, or snapshot.

## Step 2 — Run synthetic regressions

```powershell
python .\test_proofloop_broad.py --report-dir '.\runs\stage5_test_report_001'
```

The supplied version has 24 synthetic tests. The tests use **temporary independent databases** and explicitly close SQLite handles, including mutation/failure cases, to avoid the WinError 32 regression seen during Stage 4. A distinct new test report directory is required for subsequent reruns.

## Profile: a starting set of preferences, NOT a résumé

`config\search_profile.example.json` encodes a broad default corresponding to our previously stated search priorities: genuinely technical work; no sales-first roles; U.S. remote where advertised, or U.S. office roles with relocation assistance; and a set of favored technical areas. It does **not** assert that you have a given skill, degree, or years of professional experience. Stage 6 requires a separately reviewed private candidate evidence profile. Do not publish your real résumé or private profile by default.

You can create `config\search_profile_attempt001.json` later and change the preferences without editing Python. Keep personal details out of publicly committed files.

## Labels and interpretation

- `DEEP_REVIEW_PRIORITY`: technical signals, preferred domain overlaps, and a plausible geographic route to investigate further; **not** a job-fit finding.
- `STRETCH_OR_LOGISTICS_REVIEW`: technically interesting roles where financial relocation support was **not** verified. These are not assumed feasible.
- `MANUAL_REVIEW`: mixed/uncertain evidence, not automatically rejected. (May be zero for a particular input.)
- `HOLD_WITH_REASONS`: stronger contrary evidence, such as sales-first role, out-of-scope location, or technical responsibilities unconfirmed. **Not** a definitive rejection.

Stage 5 keeps all records in the complete JSON report, even if they are outside the bounded deep-review pool. The pool is deterministic triage and may miss a worthwhile role. For the sample profile, the pool holds up to 100, reserving approximately 70% for stronger geographic pathways and 30% for roles needing logistics review.

## Improvements over the older v0.15 analysis

- Uses the newly verified, single-source Stage 3 database, not the old two-branch enriched database.
- Requires matching store-report and independent-validation fingerprints before analysis.
- Reads SQLite using read-only mode and **always explicitly closes** the connection.
- Distinguishes `is_remote=True` + `workplace_type=Hybrid` from genuinely advertised U.S. remote positions.
- Leaves relocation funding and residency eligibility unconfirmed until employer evidence exists.
- Restricts sales/technical signals largely to role title, team, and the posting's duties, rather than company boilerplate.
- Excludes the `commissioning` false-positive and guards against obvious negated relocation language.
- Extracts qualification-years and education excerpts **without** treating them as verified requirements, preferences, or candidate matches.
- Reports missing section headings explicitly; does not silently treat a missing section as proof of no requirements.
- Retains the original database and produces new output directories; no destructive overwrite option.

## Limitations

This is heuristic classification. Patterns can miss or misinterpret novel language, work arrangements, sales responsibilities, and role seniority. Titles and declared skills are not proof of qualifications. The date a posting appears in this API snapshot does not verify present-day availability or application eligibility. Broad reports are intended for **private** investigation and should be reviewed before public release.

Stage 6 will parse the bounded candidates in depth, map requirements against a reviewed résumé/evidence profile, identify missing proof, and produce a handoff to AI review for a proposed top five; the user approves the final applications.
