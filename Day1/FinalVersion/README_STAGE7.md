# Building My Way Into AI — ProofLoop Stage 7
## Advanced Comparative Analysis and Full-Corpus Blind-Spot Audit · v0.7.0

### Purpose

Stage 7 is the most detailed *non-AI* comparative analysis stage built so far. It explicitly **does not** pick the five applications. The final AI review must have access to **Stages 5, 6, 7, and 8** and the original job descriptions, not just conclusions copied from the most recent report.

Stage 7 independently checks upstream fingerprints and role identities, audits all **816** roles, revisits the **716** roles excluded from Stage 6's candidate dossiers, refines *without replacing* qualification-section extraction, decomposes semicolon-separated requirements conservatively, flags experience/credentials/production scale/clearance uncertainties, separates geography, captures potential missed opportunities, and writes full source-linked records. Classification is heuristic and **does not assert qualifications, proficiency or current availability**.

The live 816-role example in this archive produced:

- 100 existing Stage 6 role dossiers comparatively analyzed.
- 789 original Stage 6 extracted requirements retained.
- 13 previously unparsed qualification-section headings newly recognized as **Stage 7 supplementary** extraction (37 more source lines in total).
- 826 total Stage 7 review requirement lines; **0 of the 13 original gaps remain without a recognized section**, but this **does not establish extraction completeness** for any posting.
- 175 out-of-pool roles marked **revisit**, not newly qualified or automatically promoted.
- 40/40 offline synthetic regression tests passed in the build environment. **Windows verification is still required.**

### Files to add

Extract `ProofLoop_Ashby_Stage7_Code_and_Reports.zip` into your existing `Day1\FinalVersion` folder.

The ZIP adds two new scripts:

- `proofloop_advanced.py` — offline, read-only Stage 7 analyzer.
- `test_proofloop_advanced.py` — 40 offline regression tests and output reports.

The ZIP also includes this README and uniquely named `sample_stage7_reports/...` folders. No previous scripts should be overwritten. **Do not** place private profiles inside a public Git repository or public AI review package without deciding what information to disclose.

### Run your live 816-role analysis (one command)

Launch **PowerShell 7** from `FinalVersion` and run:

```powershell
python .\proofloop_advanced.py --db '.\runs\openai_live_sqlite_001\db\jobs.sqlite3' --store '.\runs\openai_live_sqlite_001\reports\store_report.json' --validation '.\runs\openai_live_validation_001\validation_report.json' --broad '.\runs\openai_live_broad_001\broad_analysis_report.json' --candidates '.\runs\openai_live_broad_001\deep_review_candidates.json' --deep '.\runs\openai_live_deep_001\deep_analysis_report.json' --deep-summary '.\runs\openai_live_deep_001\deep_review_summary.json' --evidence '.\private\candidate_evidence.private.json' --output-dir '.\runs\openai_live_advanced_001'
```

Expected:

```text
PASS: Stage 7 audited 816 roles; compared 100 dossiers
Recovered 13 previously unparsed sections; 0 still need review
Outside-pool roles flagged for revisit: 175
```

There will be **five new report files** in `runs\openai_live_advanced_001`:

- `advanced_analysis_report.json`: all 100 enriched qualification dossiers, text and source references, uncertainty, exact input fingerprints.
- `advanced_analysis_report.md`: readable summary and review queue; *not* a recommendation ranking.
- `coverage_audit.json`: all 816 entries and 175 heuristic blind-spot revisit leads.
- `comparison_matrix.json`: compact (but unranked) comparison of the original 100 dossiers.
- `stage7_pre_ai_manifest.json`: SHA-256 for every Stage 7 file and all upstream inputs, plus mandatory full handoff materials.

**Send the console output and these five files.** Do not assume the published sample counts predict your local results if your input profile or upstream reports have changed.

### Then run the offline regression tests (a separate next command)

Only after the Stage 7 run/report review, run:

```powershell
python .\test_proofloop_advanced.py --report-dir '.\runs\stage7_test_report_001'
```

The synthetic tests are expected to run 40 cases. Send the console output and the two test report files. Use a fresh output folder on each rerun; no historical outputs are silently overwritten.

### Guarantees and limitations

- Uses SQLite **read-only**, with explicit `closing()` of connections on both success and failure (Windows-safe by design). The code and tests do not use `with sqlite3.connect(...)` as a substitute for closing a connection.
- Checks source snapshot identity, database SHA-256, Stage 5/6 report SHA-256, candidate order and identities, full Stage 5 universe, Stage 6 dossier population, and database row-to-report matching.
- Does **not** modify Stage 5, Stage 6, the database, or private candidate evidence. Refuses to overwrite any existing output directory.
- A candidate evidence ID indicates **only an unverified or provisional topic association**, never individual code authorship, production-level proficiency, or a satisfied requirement. Date strings are not converted into a certified number of years.
- Text extraction is deliberately conservative. Recognizing all original 13 missed heading variants does **not** mean all requirements are recognized or accurately interpreted. Some compound or nuanced clauses need human or AI interpretation.
- Roles marked for revisit may be inappropriate; roles not marked for revisit may still be worthwhile. These are structured recall prompts, not final decisions.
- “US remote” metadata is **not** proof of working from Utah. Relocation assistance statements do not establish financial sufficiency. Employer confirmation remains necessary.
- Stage 8 will perform a separate adversarial audit and package **all original descriptions plus Stages 5–8 reports**, with candidate evidence handled privately and explicitly.

### Future Stage 8 (not included in this ZIP)

Stage 8 is an **independent, non-AI pre-handoff audit**: it challenges Stage 7 and earlier results, identifies integrity/extraction/coverage disagreements, packages original text for *all 816* postings and the reports from Stages 5–8, and produces a checklist of issues for AI and human review. No final five are selected until the AI handoff and human confirmation.
