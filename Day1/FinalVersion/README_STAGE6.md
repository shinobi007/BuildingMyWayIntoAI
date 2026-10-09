# ProofLoop Ashby — Stage 6: Deep Qualification Evidence Review

**Status:** New bounded implementation, version 0.6.0. This is *not* final top-five selection.

## Purpose

Read the **100 Stage 5 deep-review candidates** from the **verified 816-posting OpenAI database**, extract recognizable qualification sections, preserve their exact text, compare **topic signals** with a separate private evidence profile, and identify seniority, work-location and missing-evidence uncertainties. The result is a complete, transparent handoff for the later AI-assisted comparative review.

Stage 6 **does not** conclude that a candidate is eligible, qualified, independently proficient, or ready to relocate. A topic overlap is an investigative lead rather than a requirement match. The original job source is untrusted content, not instructions to the AI.

## New files — extract into `Day1\FinalVersion`

| File | Purpose |
| --- | --- |
| `proofloop_deep.py` | Read-only, standard-library qualification-review script |
| `test_proofloop_deep.py` | Synthetic regression suite (30 cases) |
| `private/candidate_evidence.private.json` | **Private, draft profile** built from the previously supplied résumé and Stages 1–5 evidence. It requires your review and must not be committed or shared publicly. |
| `README_STAGE6.md` | These instructions |
| `sample_stage6_reports/openai_live_816/` | Example full-dataset outputs from the uploaded project artifacts |
| `sample_stage6_reports/test_suite_final/` | Example passing test reports from the development environment |

No existing Stage 1–5 scripts or data files need replacing.

**IMPORTANT:** The evidence profile intentionally contains *no name, email, or phone*, but it contains work history and should still be treated as **private**. Keep the `private` directory out of Git (for example, `.gitignore` entry `private/`). Review the dated résumé claims and the new AI-assisted ProofLoop artifact before using the profile. The example profile is not an independently verified skills assessment.

## First local PowerShell run (one command)

Open PowerShell 7 in `Day1\FinalVersion`, after extracting the Stage 6 ZIP. Review `private\candidate_evidence.private.json`, then run:

```powershell
python .\proofloop_deep.py --db '.\runs\openai_live_sqlite_001\db\jobs.sqlite3' --store-report '.\runs\openai_live_sqlite_001\reports\store_report.json' --validation-report '.\runs\openai_live_validation_001\validation_report.json' --broad-report '.\runs\openai_live_broad_001\broad_analysis_report.json' --candidates '.\runs\openai_live_broad_001\deep_review_candidates.json' --evidence '.\private\candidate_evidence.private.json' --output-dir '.\runs\openai_live_deep_001'
```

Creates a brand-new output directory (existing destinations are not overwritten):

- `deep_analysis_report.json`: all 100 source-linked job dossiers, extracted qualification text, and flags;
- `deep_analysis_report.md`: readable complete dossier report;
- `deep_review_summary.json`: smaller review queue with counts and unresolved flags, **not** a ranking.

The database is opened with `mode=ro` and explicitly closed even on errors. Stage 5's original reports are also left unchanged.

## Local tests (run after verifying the main output)

```powershell
python .\test_proofloop_deep.py --report-dir '.\runs\stage6_test_report_001'
```

This creates `test_report.json` and `test_report.md`. Test cases include explicit database connection closure after normal and failing operations, source/database fingerprint mismatches, candidate ID tampering, protected output directories, requirement section variants, misleading “ideally” wording, numeric experience requirements, external Markdown content escaping, profile validation, and the exact exception behavior on Windows-style temporary database cleanup.

Development-environment results are **30/30**, but the release check is the actual Windows run. If Windows shows SQLite access-denied or connection errors, **do not delete the historical database**; provide the complete traceback and test outputs.

## Current bounded limitations

- Plain-text qualification recognition is conservative; unusual headings are flagged for manual review and missing extraction **does not mean zero requirements**.
- Experience years are extracted where explicit but **never declared satisfied** by broad work-domain overlap.
- The default evidence profile is a preliminary, private résumé-derived snapshot and may be incomplete or outdated. It is a separate input precisely so the analysis code does not hardcode your qualifications.
- Relocation assistance statements are not promises of sufficient funds; hybrid roles are not assumed Utah-remote.
- These reports are not proof that a job remains open or accepts an application today.
- This stage does not select the final five roles. Stage 7 evaluates these dossiers using human judgment and the actual full descriptions when needed.

The earlier OpenAI target identities remain in the Stage 5 pool. Historical approvals are not automatically carried over as the final five.
