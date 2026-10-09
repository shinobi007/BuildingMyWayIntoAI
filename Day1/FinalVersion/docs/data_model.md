# Data model — ProofLoop Stage 1–8

## Data representations

| Artifact | Purpose | Contract |
| --- | --- | --- |
| Frozen Ashby JSON | Exact source response; provenance root | Acquired by Stage 2; do not edit in place |
| Normalized JSONL | Portable, one-record-per-line staging | `provenance`, `canonical`, and `raw` evidence kept together |
| SQLite database | Searchable relational and JSON evidence store | Stage 3 verifies completeness, constraints and transformations |
| Stage 4 validation reports | Independent checks | Must refer to the same source and database identities |
| Stage 5–7 JSON/Markdown | Analysis/audit, with uncertainty | Derived and challengeable, not source truth |
| Stage 8 archive | Portable full AI handoff | Full source descriptions, reports, verified fingerprints, sanitized candidate evidence |
| Stage 9 prompt | Instructions to interpret material | No additional deterministic database structure is required |

CSV existed in the **earlier HTML learning branch** but is not a required current Stage 1–8 output. The old `proofloop.db` (817 HTML-derived rows) and current `runs/openai_live_sqlite_001/db/jobs.sqlite3` (816 API-derived rows) are distinct.

## SQLite schema (current Stage 3)

`roles` is the primary entity. `id` is a primary key; `(board, source_index)` is unique. Core fields include `title`, `department`, `team`, `employment_type`, `location`, `published_at`, `workplace_type`, `is_remote`, `is_listed`, `job_url`, `apply_url`, and original textual descriptions.

The primary table also stores `source_sha256`, `address_json`, `compensation_json`, `canonical_json`, `raw_json`, and `provenance_json`. These prevent a useful filtered view from discarding evidence required for later review.

Other tables:
- `secondary_locations`: additional places linked to a role.
- `compensation_tiers`: salary/compensation tier entries.
- `compensation_components`: components belonging to a tier.
- `compensation_summary_components`: separate summary-level components.
- `build_metadata`: source and software build metadata.
- `role_overview` (view): convenient selection of job id, title, team, department, location, workplace type, remote flag, published date, URLs.

The verified October 2026 live database contained 816 roles, 227 secondary locations, 667 compensation tiers, 1,346 tier components and 1,320 summary-level compensation components. Those are snapshot-specific observations, not permanent schema assumptions.

## Critical semantic cautions

- `is_remote = 1` may appear with `workplace_type = 'Hybrid'`. This does **not** prove work-from-Utah eligibility.
- A null remote field is **unknown**, not automatically false.
- Salary currency and pay interval matter (hourly vs annual and location-specific ranges). Do not combine them without normalization and explicit rationale.
- Requirement years must be traced to the employer's qualification section, not an unrelated number in the posting.
- Candidate résumé statements are self-reported; role-topic overlap does not satisfy a complex experience requirement.
- Jobs can be updated or removed after the frozen snapshot; current availability is never implicit.

See [`../examples/schema_queries.sql`](../examples/schema_queries.sql) for demonstration queries.
