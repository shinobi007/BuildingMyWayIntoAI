# ProofLoop Stage 8 — Independent Pre-AI Audit

**Integrity: PASS** · **Review flags: 10** · **No top-five decision**

## Verified coverage
- Original source postings: **816**
- Stage 5 roles: **816**
- Stage 6/7 detailed dossiers: **100**
- Outside-pool roles flagged for review: **175**
- Requirements reviewed: Stage 6 **789**, Stage 7 **879**

## Independent review flags

| Flag | Count | Why it matters |
|---|---:|---|
| `OUTSIDE_100_REVISIT` | 175 | Heuristic recall leads—not qualified recommendations |
| `EMBEDDED_HEADING_ARTIFACTS` | 3 | Requirement extraction may include a subsequent heading |
| `EXTRACTION_COMPLETENESS_UNVERIFIED` | 816 | Recognized headings are not assurance that all requirements were extracted |
| `UNVERIFIED_CANDIDATE_EVIDENCE` | 100 | Candidate résumé evidence is included without contact details, but claims remain provisional and require user confirmation |
| `EXPERIENCE_DURATION_UNKNOWN` | 44 | Number of years in job descriptions is not years established for candidate |
| `RELOCATION_FUNDING_UNKNOWN` | 30 | No demonstrated relocation funding for these roles |
| `REMOTE_METADATA_AMBIGUITY` | 56 | isRemote=true can coexist with hybrid attendance |
| `STAGE7_DOC_STALE_EXAMPLE` | 1 | Stage 7 README example states 826 lines; actual run reports 879. Use the reports as authoritative, update docs. |
| `POSTING_AVAILABILITY_NOT_REFRESHED` | 816 | Source is a time-stamped snapshot, not real-time confirmation |
| `ZERO_MISSING_DOES_NOT_MEAN_ZERO_EXTRACTION_RISK` | 3 | Zero missing headings coexists with embedded heading issues |

## Boundaries

- **All 816 original postings and all Stage 5–8 reports are in the handoff archive.**
- The 175 revisit leads must not be treated as qualified matches.
- The full structured candidate-evidence profile is included with contact details removed; claims remain unverified.
- Verify relocation funding, remote eligibility, and current openings directly with the employer.
- The AI should audit the entire corpus, challenge previous labels, and present recommendations only after evidence review.
