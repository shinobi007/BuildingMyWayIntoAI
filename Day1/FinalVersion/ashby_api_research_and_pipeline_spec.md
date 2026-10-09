# Building My Way Into AI — Ashby Public API Research and Streamlined Search Specification

**Research date:** 2026-10-08  
**Purpose:** Pre-Milestone-0 research and scope specification for the shared Attempt #001 foundational technical build.  
**Source fixture:** `openai_ashby_snapshot_2026-10-07(1).json`, 815 jobs, `apiVersion: "1"`, SHA-256 `97bdd769266238538febac6448a9a1dd2502a8a6765d6feba2e22073b66e4ba5`.

## 1. Source documents

- Ashby official public endpoint: https://developers.ashbyhq.com/docs/public-job-posting-api
- Employer-authorized `jobPosting.list`: https://developers.ashbyhq.com/reference/jobpostinglist
- Employer-authorized `jobPosting.info`: https://developers.ashbyhq.com/reference/jobpostinginfo
- API authentication and permissions: https://developers.ashbyhq.com/reference/authentication
- Dedicated partner feeds: https://developers.ashbyhq.com/docs/dedicated-partner-job-feeds
- Employer careers-page integration guide: https://developers.ashbyhq.com/docs/creating-a-custom-careers-page

## 2. Public API contract

`GET https://api.ashbyhq.com/posting-api/job-board/{BOARD_NAME}?includeCompensation=true`

The public posting feed is read-only. It exposes the `jobs` list and `apiVersion`. The official guide documents the `includeCompensation` parameter; it does **not** document public server-side role filters, incremental sync, pagination/cursors, or an endpoint for privately stored recruiting records. Do not import these features from the separately authenticated ATS endpoints without supporting evidence.

The public board name is derived from a `jobs.ashbyhq.com/{BOARD_NAME}` careers-page URL. For the historical fixture, board name is `openai`.

## 3. Public job fields to preserve

| Source field | Normalized usage | Key detail |
| --- | --- | --- |
| `id` | Stable posting UUID | Observed in all 815 snapshot jobs; not separately listed in the public documentation field table. Validate UUID and keep original. |
| `title` | Search/display | Preserve source text; optionally derive a normalized comparison value. |
| `department`, `team` | Organizational filters | Keep separate; preserve original strings. |
| `location` | Primary display location | Not enough to prove geographic eligibility. |
| `secondaryLocations[]` | Additional location records | Preserve `location`, `address`, and nested `postalAddress` where present. |
| `address.postalAddress` | City, region, country, sometimes postal/street | Fields may be missing; never invent. |
| `isRemote` | Raw remote metadata | Nullable in the actual OpenAI fixture; never equate `true` with work-from-anywhere permission. |
| `workplaceType` | OnSite/Remote/Hybrid/unknown | Nullable in the actual fixture and may conflict with simplistic interpretation of `isRemote`. |
| `employmentType` | FullTime/PartTime/Intern/Contract/Temporary | Keep exactly as supplied; do not assume every board has the same distribution. |
| `descriptionHtml` | Raw formatted posting text | Essential for structure, evidence spans and future specialized parsing. |
| `descriptionPlain` | Initial NLP/regex analysis text | Keep alongside HTML, do not silently replace the publisher's plain text with our own derivation. |
| `publishedAt` | Publisher timestamp | Official description says last published; not proof of initial creation or last modification time. |
| `jobUrl`, `applyUrl` | Source and application page URLs | Validate scheme/domain without assuming all boards use identical paths. |
| `isListed` | Public-display eligibility | Do not recommend unlisted roles merely because an API response exposed them. |
| `shouldDisplayCompensationOnJobPostings` | Compensation display decision | Present in all fixture rows but omitted from the official public field table; treat as observed/optional. |
| `compensation` | Full structured compensation | Optional object with summaries, tiers, component types, currency, interval, min/max and tier-specific text. Preserve exact details, never simply collapse to annual USD salary. |

**Unknown-field policy:** All source keys remain recoverable in the immutable raw snapshot; the normalization stage explicitly reports previously unseen or missing paths. If future snapshots expose more public fields, add typed mappings only after review; do not discard them silently.

## 4. What richer Ashby APIs can contain but this project cannot presume access to

`jobPosting.list` and `jobPosting.info` require an employer-authorized key with `jobsRead`. They document data such as employer job identifiers, board associations, application deadlines, form definitions, structured linked data, and `updatedAt`. The public feed is **not** documented to supply these as comparable fields. Do not use undocumented unauthenticated calls to these authenticated endpoints. The job application form itself is outside the bounded search/recommendation pipeline.

Dedicated partner feeds are Ashby-provisioned opt-in integrations, not a generally available replacement for the public board endpoint. Their schema includes organization identifiers/name, per-location metadata, `updatedAt`, and other location/compensation structure; organizations choose whether to share with a given partner. This can inform future data-model extensibility but not the present fetch implementation.

Potential optional enrichment: published job pages may contain additional publicly visible text or structured data, but any such extraction should be a **separate documented source adapter** with its own evidence, legal/technical checks, and comparison report; no specific extra field is guaranteed by Ashby's public posting API documentation.

## 5. Findings from the frozen OpenAI snapshot

Machine-readable detailed counts and all 18 observed job keys: `ashby_snapshot_schema_audit.json`.

- 815 jobs and 815 distinct observed `id` values; 18 distinct top-level job keys; `apiVersion: "1"`.
- All 815 were `isListed: true` in this historical snapshot. Future snapshots may differ.
- `isRemote`: 530 true, 29 false, 256 null.
- `workplaceType`: 509 Hybrid, 21 Remote, 29 OnSite, 256 null. All 509 Hybrid records also carried `isRemote: true`. Keep both metadata fields as-is.
- `shouldDisplayCompensationOnJobPostings`: 657 true and 158 false. All 657 true records had nonempty published compensation summaries/tiers; the 158 false records had empty summaries and tiers in this snapshot. `compensation` was still an object on all 815 rows.
- 231 additional-location records across 142 jobs.
- The primary `postalAddress` occasionally provided postal or street fields even though many did not. Preserve address dictionaries rather than projecting only three fields.
- Salary, equity cash value, and commission component types occurred; compensation is not simply a numeric salary field.

These counts apply to the **October 7, 2026 frozen file only**, not today's live availability. The fact a property is non-null in this file does not mean Ashby guarantees it for all boards.

## 6. Proposed streamlined data design

- Store original response body bytes unchanged (`raw/<board>/<run_id>/snapshot.json`) with SHA-256, HTTP status, URL, response headers where available, UTC fetch time, and declared job count.
- Write `normalized/jobs.jsonl` with one row per posting, original API `id`, stable source/run linkage, all useful scalar fields, nested location and compensation structures, and explicit unknown/null handling. Preserve raw description HTML and text. No fabricated qualifications.
- Build one search-specific SQLite database (`roles.db`) using transactions and foreign keys, with `snapshots`, `postings`, `posting_snapshots` or equivalent versioned observations, `secondary_locations`, and `compensation_components` as needed. Store source hashes and preserve prior snapshots rather than destructive in-place replacement.
- Expose current-snapshot queries without losing prior observations, so later research can compare changes and detect disappearance from the board **without claiming why a role disappeared**.
- Keep **candidate profile data separate and private**; the application search database should not contain unneeded personal résumé information.
- Preserve an inspectable, unranked role population and avoid irreversible filtering. Annotate exclusion/uncertainty decisions rather than deleting roles.

## 7. Required per-stage outputs and reports

| Stage | Data product | Evidence/report product |
| --- | --- | --- |
| Fetch | Raw immutable JSON response | `fetch_report.json` (URL, retrieved time, status, headers, response size, hash, count, API version, retries, failures) |
| Normalize | `jobs.jsonl` | `normalization_report.json` (row counts, schema paths, nulls, unexpected fields, invalid IDs, conversion decisions) |
| Store | `roles.db` | `database_build_report.json` (counts, constraints, source links, transaction status, SQLite integrity, schema version) |
| Validate | Read-only verification | `validation_report.json` + readable `.md` (source-to-JSONL-to-DB comparisons, missing records, sampled/full-field checks, exact tests and failures) |
| Test | Automated synthetic fixture suite | `test_report.json` + readable `.md` (case names, expected/actual results, negative-path outcomes) |
| Broad analysis | `broad_analysis.json` | `broad_analysis.md` (all/eligible counts, location/sales/technical signals, candidates, exclusion/unknown reasons) |
| Deep analysis | `deep_analysis.json` | `deep_analysis.md` (exact qualification source spans, evidence gaps, seniority, preferred vs required ambiguity, relocation dependencies) |
| AI handoff | `ai_review_packet.json` or `.md` | `ai_review_packet.md` (candidate profile constraints, source-backed dossiers, uncertainties, selection instructions) |
| Human-reviewed top five | Reviewed decision artifact | `top5_decision.md` (reasons, tradeoffs, human approval, alternatives, snapshot identity) |

Each report includes `run_id`, program/version, input/output hashes where feasible, UTC timestamp, counts, warnings, errors, and a clear success/failure status. JSON is authoritative for automation; Markdown is for reading and Git. Failure reports are also valuable, but must not claim success or overwrite earlier successful reports.

## 8. Analysis responsibilities and safeguards

**Broad analysis:** work type, location feasibility, sales/non-sales evidence, compensation where published, department, technical focus, job description coverage, work-history overlap, seniority requirements, role status and unknowns. Do not confuse `isRemote` with physical work location.

**Deep analysis:** parse qualifications in context; retain verbatim source evidence with job UUID; separate required, preferred, and ambiguous language **at clause level**; compare specific experience length and technologies against documented candidate evidence; do not equate domain overlap with years of experience. Keep unavailable proof and missing ability distinct.

**AI final judgment:** software prepares a transparent pool and an evidence packet; AI proposes five roles for the actual user; user retains final choice. Store prompts/version and corrected decisions with the selected snapshot. This bounded component **does not submit applications or implement the full career framework**; the larger Attempt #001 project uses the same completed build as shared technical proof for its five application targets.

## 9. API and transport safeguards

- Public GET requests only; configurable board slug; `includeCompensation=true` when public data available.
- Bounded timeouts, retries with capped exponential backoff for appropriate transient/HTTP 429/5xx failures; no uncontrolled loops.
- Validate the response type and payload shape before accepting the snapshot.
- Use atomic writes and fail-safe backups/transactional staging; never unlink the last good database before validating its replacement.
- Avoid hard-coded job totals, fixed currencies, fixed employment-type distributions, and implicit true/false conversion of nullable metadata.
- No public endpoint pagination is documented; treat pagination and incremental sync as separate authenticated API concepts unless official public documentation changes.
- Cache/freeze snapshots. Downstream normalize/validate/analyze work offline using the saved response.
- Redact secrets and personal records from generated public artifacts.

## 10. First implementation boundary

Start from the preserved October 7 snapshot. First implement and test a read-only snapshot schema validator/normalizer that produces complete reports from a frozen file. Then add fetch with identical schema checks, then SQLite persistence and tests, then broad/deep analysis and AI packet. Do not preserve obsolete HTML/CSV/reconciliation steps in the new Ashby-only path unless a future non-API source adapter needs them.

This research document and its companion audit are **planning and inspection artifacts**, not proof that the replacement pipeline has been implemented or tested.
