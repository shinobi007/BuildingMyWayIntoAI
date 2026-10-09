# ProofLoop Stage 2 — Synthetic Test Report

**Result:** PASS

- Tests run: 23
- Passed: 23
- Failed: 0
- Errors: 0
- Skipped: 0

Tests include offline source fidelity, network retry/error handling (mocked), structural validation, publish safety and failure reporting.

## Individual cases

- PASS: `__main__.Stage2Tests.test_bad_nested_data_rejected_by_stage1_contract`
- PASS: `__main__.Stage2Tests.test_board_slug_rejects_injection`
- PASS: `__main__.Stage2Tests.test_duplicate_ids_no_partial_output`
- PASS: `__main__.Stage2Tests.test_empty_rejected_unless_acknowledged`
- PASS: `__main__.Stage2Tests.test_failure_sidecar_contains_no_secrets`
- PASS: `__main__.Stage2Tests.test_frozen_source_not_modified`
- PASS: `__main__.Stage2Tests.test_live_400_does_not_retry`
- PASS: `__main__.Stage2Tests.test_live_429_retries_then_succeeds`
- PASS: `__main__.Stage2Tests.test_live_503_retries_then_succeeds`
- PASS: `__main__.Stage2Tests.test_live_bad_content_type_rejected`
- PASS: `__main__.Stage2Tests.test_live_compressed_payload_rejected`
- PASS: `__main__.Stage2Tests.test_live_network_retry_exhaustion`
- PASS: `__main__.Stage2Tests.test_live_redirect_outside_allowed_host_rejected`
- PASS: `__main__.Stage2Tests.test_live_response_success`
- PASS: `__main__.Stage2Tests.test_malformed_json_no_partial_output`
- PASS: `__main__.Stage2Tests.test_maximum_response_size_enforced`
- PASS: `__main__.Stage2Tests.test_missing_file_rejected`
- PASS: `__main__.Stage2Tests.test_refuses_existing_destination_without_modifying`
- PASS: `__main__.Stage2Tests.test_successful_offline_preserves_bytes_and_generates_reports`
- PASS: `__main__.Stage2Tests.test_unknown_source_job_fields_preserved`
- PASS: `__main__.Stage2Tests.test_url_build_with_compensation`
- PASS: `__main__.Stage2Tests.test_url_build_without_compensation`
- PASS: `__main__.Stage2Tests.test_wrong_expected_count_no_partial_output`
