# Stage 7 method, traceability, adversarial constraints

## Distinguish what the code knows from what it cannot know

1. **Snapshot truth:** SQL database rows and earlier source-linked reports can be checked for consistency by hashes and cross-source identity. They do not confirm jobs remain open in real time.
2. **Employer statements:** A job posting can state a location, arrangement or qualification. It does not establish the candidate's eligibility or proficiency.
3. **Qualification section recognition:** Stage 6's 789 original lines are preserved; Stage 7 adds clearly labeled supplementary lines only where Stage 6 found none. Source strings are preserved and common embedded-heading bleed-through is flagged rather than silently ignored.
4. **Professional evidence:** Current résumé-derived history is explicitly UNVERIFIED. An automated AI-assisted project demonstrates project artifacts and relevant exposure, but does not independently prove ownership of every line, years in production or senior-level authority.
5. **Requirement strength:** Preferred language is preserved; ambiguous headings stay expectations, never hard minimums by assumption. A combined requirement can contain several conditions. Semicolons are a conservative split, *not* a full logical parser.
6. **Blind-spot recall:** Stage 5's 100-dossier cap is a workflow constraint, not an evidence cutoff. Stage 7 audits the other 716 and flags domain/title/technical signs deserving a second look, while retaining blockers and uncertainty.
7. **Groups are categories, not numeric scores:** The comparison matrix is **unranked**. It does not force a false precision on incomplete experience evidence.
8. **Stage 8 design:** Validate independently before AI; give AI every report from Stages 5–8 and a complete source-text universe to challenge upstream preselection. Private candidate evidence requires an explicit sharing decision.

## Outputs

- `advanced_analysis_report.json`: detailed Stage 7 assessments, source text, requirement traces, evidence references and uncertainty.
- `coverage_audit.json`: one compact entry per posting and separate out-of-pool revisit entries.
- `comparison_matrix.json`: one entry per Stage 6 dossier; no rank.
- `stage7_pre_ai_manifest.json`: upstream hashes, output hashes and Stage 8 packaging requirements.

## Failure modes to test

- Windows SQLite locks after failed or successful query.
- Source SHA / altered upstream report.
- Candidate order or IDs drifting across Stage 5 and Stage 6.
- Role title or original source index mismatch.
- A job stating `isRemote=true` and `Hybrid`.
- Principal title or experience duration incorrectly certified from topic overlap.
- Stage 6 missing a variant `You Might Thrive Here If You` qualification heading.
- Broken or cross-contaminated qualification sections.
- HR boilerplate parsed as job qualifications.
- Summary report fabricated from a changed upstream report.
- An out-of-pool role receiving no possibility for retrospective inspection.
- Untrusted posting title placed unescaped into Markdown.

Human and AI review must continue after these tests. They do not make Stage 7's heuristic classifications objective facts.
