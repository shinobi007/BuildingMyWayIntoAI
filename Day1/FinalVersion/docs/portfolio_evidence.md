# Proof / portfolio surface

## What a reviewer should be able to see in two minutes

1. **Problem:** More than 800 postings made manual review and traceability difficult.
2. **Decision:** Freeze source data, model it with provenance, store it in SQLite, and independently validate transformations.
3. **Working product:** Open the local explorer and filter a role, inspect its original description and normalized/provenance evidence.
4. **Verification:** Cite precise local test results (231 stage tests; new UI suite separately after Windows verification), including documented failure fixes.
5. **Judgment:** Explain why remote booleans, sales keywords and résumé keywords are insufficient for eligibility or qualification decisions.
6. **Scope:** One evolving ProofLoop system supports five applications; the user directs the work and AI assists.

## Evidence sources

- Source code and Stage 1–8 READMEs in the existing `FinalVersion` root.
- Frozen original input, normalization reports, SQLite build report, independent validation report and analysis snapshots in existing `runs/` (usually **not** public Git files).
- Tests and test reports, including the corrected Windows SQLite regression suite.
- Screenshots captured from the user's own machine after verification.
- AI handoff manifest and résumé-derived evidence, to the extent the repository owner wants to publish them.
- A real Git history **from the date Git is actually initialized**, plus a separately labeled pre-Git development log.

## Claim discipline

Say: “Built and tested an AI-assisted, provenance-preserving job-analysis pipeline and a read-only viewer.”

Do not say: “Personally hand-coded every module without assistance,” “all 816 roles individually proven suitable,” “five applications submitted,” or “all remote jobs can be performed from Utah.” Those claims are not supported by the archived evidence.

## Repository curation

Personal project details may be included at the project owner’s discretion. The default `.gitignore` excludes repeated bulk runs and generated archives to keep cloning practical; it is not a prohibition on publishing professional background. Check staged paths and ensure no API credentials or login secrets are included before pushing.
