# Building My Way Into AI — Stage 8 (replacement v0.8.1)
## Complete source, analysis AND candidate-evidence handoff

### What changed from v0.8.0
This is a **drop-in replacement** for the Stage 8 script and test suite. The previous Stage 8 handoff withheld the actual résumé-derived evidence. **This version includes it.** The generated `ai_handoff_bundle.zip` now contains:

- All 816 original Ashby posting records, with their full job descriptions, raw employer metadata, IDs, canonical fields and provenance.
- Every complete Stage 5, 6, 7 and 8 report and audit, with verified cross-stage IDs and SHA-256 manifest.
- `candidate/candidate_evidence_public.json` — **all** structured professional evidence records from the original Stage 6 profile (10 records in the supplied dataset), with contact-related content removed. Source fingerprint still points to the **unchanged** local original profile.
- `candidate/resume_professional_claims.md` — the fuller contact-redacted résumé source, if the recommended `--resume-claims` input is provided. A sanitized source transcription is included with this installation ZIP.
- `candidate/PROJECT_PROOFLOOP_UPDATE.json` — a clearly labeled, additive update of the current collaborative ProofLoop project **through Stage 8**, with explicit limitations about independent proficiency, production experience and sole authorship. The old source profile and Stage 6–7 reports remain intact.
- `AI_REVIEW_GUIDE.md` — an adversarial review protocol that asks AI to challenge earlier screenings, check the full corpus, reconcile résumé claims with requirements, and propose five applications only after human review.

Neither the private profile's original bytes nor the source résumé PDF is copied into the portable archive. The public candidate export uses an allowlist of professional evidence fields and redacts recognizable emails, US telephone numbers, common social-profile links and simple postal addresses. This is not a perfect anonymity guarantee: company names, employment dates, credential details and awards **can still identify a person**. Inspect the generated candidate evidence before publishing. The source résumé is unverified and contains the résumé's own self-assessed skill levels and metrics, not certifications of competence.

### IMPORTANT — overwrite the existing Stage 8 files when extracting

**Do not extract into a new `ProofLoop_Ashby_Stage8_Replacement` subfolder.** Open this ZIP and extract its **root contents directly into** your existing `Day1\FinalVersion` directory.

When Windows offers **Replace the files in the destination**, choose **Replace** for:

- `proofloop_handoff.py`
- `test_proofloop_handoff.py`
- `README_STAGE8.md`

The ZIP also adds `candidate_resume_claims.public.md`. **Do not replace or edit** `private\candidate_evidence.private.json`, or any Stage 1–7 script, database, job snapshot or report. Stage 6–7 hash checks depend on the existing original file being unchanged.

The `sample_stage8_reports` directory contains reference output only. Your actual reports will be regenerated from your Windows machine's existing `runs` artifacts.

### First PowerShell command: regenerate Stage 8, new versioned output

From `Day1\FinalVersion`, run **this one line**:

```powershell
python .\proofloop_handoff.py --snapshot '.\runs\openai_live_fetch_001\raw\ashby_snapshot.json' --db '.\runs\openai_live_sqlite_001\db\jobs.sqlite3' --store '.\runs\openai_live_sqlite_001\reports\store_report.json' --validation '.\runs\openai_live_validation_001\validation_report.json' --broad '.\runs\openai_live_broad_001\broad_analysis_report.json' --candidates '.\runs\openai_live_broad_001\deep_review_candidates.json' --deep '.\runs\openai_live_deep_001\deep_analysis_report.json' --deep-summary '.\runs\openai_live_deep_001\deep_review_summary.json' --advanced '.\runs\openai_live_advanced_001\advanced_analysis_report.json' --coverage '.\runs\openai_live_advanced_001\coverage_audit.json' --comparison '.\runs\openai_live_advanced_001\comparison_matrix.json' --stage7-manifest '.\runs\openai_live_advanced_001\stage7_pre_ai_manifest.json' --evidence '.\private\candidate_evidence.private.json' --broad-md '.\runs\openai_live_broad_001\broad_analysis_report.md' --deep-md '.\runs\openai_live_deep_001\deep_analysis_report.md' --advanced-md '.\runs\openai_live_advanced_001\advanced_analysis_report.md' --resume-claims '.\candidate_resume_claims.public.md' --output-dir '.\runs\openai_live_pre_ai_handoff_002'
```

The `_002` output is intentionally a new directory; it preserves your successful original `_001` for regression history. The executable code files **are overwritten by extraction**, whereas the original output report directories **are not overwritten**.

Expected main console messages with the same source corpus:

```text
PASS: Stage 8 audited 816 source roles; verified Stage 5-7 identities
Review flags: 10; recall leads: 175
Candidate evidence: INCLUDED, contact-sanitized; project update through Stage 8
Full résumé claims transcription: INCLUDED
Reports: stage8_audit_report.json/.md; stage8_handoff_manifest.json; ai_handoff_bundle.zip
```

### Next test command (only after reviewing the run output)

```powershell
python .\test_proofloop_handoff.py --report-dir '.\runs\stage8_test_report_002'
```

This revision has **47 synthetic tests** (the original 40, plus candidate-profile inclusion, sanitization, project-update and optional-résumé regression checks), and tests run with synthetic fixture résumés, not the real user profile. Windows verification is still pending.

### Output to share for review

`runs\openai_live_pre_ai_handoff_002\stage8_audit_report.json`, `.md`, `stage8_handoff_manifest.json` and **`ai_handoff_bundle.zip`**. Stage 9 must use the revised `_002` archive, **not** the old `_001` archive.

No qualification, geographical eligibility, employment availability, job selection or application submission is automatically established or authorized. The applicant should check the professional evidence before making recommendations or publishing the package.
