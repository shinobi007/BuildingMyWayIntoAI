# ProofLoop Stage 4 — Independent Validation Report

**Status:** PASS
- Checks: **24 PASS / 0 FAIL**
- Generated (UTC): `2026-10-09T05:38:32+00:00`

## Input fingerprints

- `snapshot_sha256`: `74e48a4cab6fabe9905403d4df91f86a700b148d253165b1507d58b28e8fab72`
- `jsonl_sha256`: `7314911915808975c5eabff35e5a8151f2c99f97c4b0c5d3c14976d59c0a1d31`
- `sqlite_sha256`: `abcfb60e1674a703a34c4e6613cc54552220bac32e313ca8baa13fa4ed447be3`

## Checks

| Check | Result |
| --- | --- |
| `normalization_report_status` | PASS |
| `store_report_status` | PASS |
| `normalization_report_hashes` | PASS |
| `store_report_hashes` | PASS |
| `report_run_identity` | PASS |
| `source_normalized_count` | PASS |
| `normalization_report_count` | PASS |
| `store_report_count` | PASS |
| `source_raw_exact_parsed` | PASS |
| `canonical_projection_exact` | PASS |
| `source_ordinal_exact` | PASS |
| `source_provenance_exact` | PASS |
| `source_unique_ids` | PASS |
| `sqlite_integrity` | PASS |
| `foreign_keys` | PASS |
| `required_tables` | PASS |
| `relational_row_counts` | PASS |
| `store_report_database_counts` | PASS |
| `build_metadata` | PASS |
| `db_source_raw_objects` | PASS |
| `db_canonical_objects` | PASS |
| `db_provenance` | PASS |
| `db_scalar_projection` | PASS |
| `db_all_child_rows` | PASS |

## Expected table counts

- `roles`: 816
- `secondary_locations`: 227
- `compensation_tiers`: 667
- `compensation_components`: 1346
- `compensation_summary_components`: 1320

## Boundaries

- Verifies source-to-database data consistency, not current job availability or employer statements.
- Source-to-canonical field checks cover the 18 known Ashby source fields; unknown source fields are preserved in raw JSON.
- Does not assess candidate qualifications, location eligibility, or semantic truth of text.
