# Screening methodology and known limits

This document separates the **historical v0.14/v0.15 analysis experiments** from the current **eight-stage API pipeline**. A role's analytical classification is a discovery aid, not a final hiring assessment.

## Why the filtering evolved

Early matching overreacted to substring collisions (such as `commissioning` containing `commission`) and to job-location fields that used `is_remote=true` even for hybrid positions. Overlap with résumé topics was also easy to mistake for actual qualifications. These were substantive product and evaluation problems—not merely text formatting.

## Principles tested during the historical analysis work

- **Sales:** Use word-boundary-aware detection; distinguish strong sales-primary signals from phrases that require context review (`EXCLUDE_STRONG_SALES` versus `REVIEW_SALES_CONTEXT`). Being customer-facing or working with a revenue product does not by itself make a role sales-primary.
- **Location:** Interpret primary and secondary locations, workplace type, remote boolean, actual text about remote arrangements and required office days, and relocation-assistance wording together. Keep Utah eligibility distinct from technical fit; a U.S. remote designation is not a guaranteed Utah arrangement.
- **Technical substance:** Distinguish hands-on technical work from job descriptions that merely mention familiar tools. Do not treat title alone as a decisive technical criterion.
- **Requirements:** Prefer the employer's explicit qualifications section when reading experience years, education and credentials. Detect compound obligations, OR alternatives, and required vs preferred wording.
- **Résumé overlap:** Useful for discovering leads; not a qualification score or proof that every requirement is met.
- **Compensation:** Preserve currency and interval; do not equate hourly compensation with annual salaries without an explicit assumption.
- **Deep review:** Transparent rules produce candidates for human/AI consideration, **not** a guaranteed final ranking.

## How the current system handles this

`proofloop_broad.py`, `proofloop_deep.py` and `proofloop_advanced.py` use their own audited, frozen-dataset implementation. Their outputs include 816 broad records, 100 deep dossiers and 175 additional reconsideration leads. Do not assume every detail of the older `v0.15` experiment was copied into the new modules; check the source modules and their tests if verifying a particular behavior.

The source records stay authoritative. Stage 8 packages original postings, candidate evidence, analysis reports and warnings for an AI-assisted independent review; Stage 9 is the human-controlled prompt and subsequent application-selection process.
