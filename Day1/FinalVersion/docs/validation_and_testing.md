# Validation and testing — evidence and limits

## Verified Windows regression history

| Stage | Test script | Latest corrected suite passed |
| --- | --- | ---: |
| 1 | `test_proofloop_normalize.py` | 17 |
| 2 | `test_proofloop_fetch.py` | 23 |
| 3 | `test_proofloop_store.py` | 24 |
| 4 | `test_proofloop_validate.py` | 26 |
| 5 | `test_proofloop_broad.py` | 24 |
| 6 | `test_proofloop_deep.py` | 30 |
| 7 | `test_proofloop_advanced.py` | 40 |
| 8 | `test_proofloop_handoff.py` **v0.8.1** | 47 |
| **Total** | | **231** |

The Stage 4 suite originally raised Windows `[WinError 32]` on temporary SQLite cleanup. Some tests used `with sqlite3.connect(...) as con:`, which **does not close the connection**. The corrected suite explicitly closes handles and includes closure regression tests. The original failed report remains evidence of diagnosis and correction.

Stage 8 v0.8.0 passed earlier tests but its public handoff omitted full candidate evidence needed for proper comparison. Stage 8 v0.8.1 is the corrected revision and has 47 Windows-passed tests; the earlier version's reports were not overwritten.

The above total describes eight specific latest suites—not proof that every combination of environment, input, output or model interpretation has been tested.

## Stage 4 independent data validation

A separate real-data validation run completed 24 checks comparing the source, normalized JSONL and SQLite. This is **not** another 24 tests added to the 231 synthetic-suite total.

## Portfolio interface tests

`tests/test_role_explorer.py` adds **19 synthetic tests** of the new local explorer, covering read-only SQLite access, filters, correct treatment of hybrid/remote, injection resistance, paginated queries, role detail, HTTP endpoints, source data escaping and schema rejection. These passed in the development container. **Windows confirmation is pending** until the user runs the provided command on their own FinalVersion folder.

```powershell
python -m unittest discover -s tests -p test_role_explorer.py -v
```

## Repeatability versus current availability

The original frozen JSON, the normalized JSONL, the SQLite data, and the stage reports are linked by SHA-256 checksums. Hash verification demonstrates that the datasets correspond to their recorded sources. It does **not** prove that a job remains open, a person meets an employer's requirements, or relocation support is sufficient.

The UI is a read-only display of one frozen database. It deliberately cannot modify the application ledger or job evidence; those capabilities can be designed as later versions after clear contracts and tests.
