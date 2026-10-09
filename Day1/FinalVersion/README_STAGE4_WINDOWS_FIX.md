# Stage 4 Windows SQLite connection-lifecycle correction

## Root cause

The prior `test_proofloop_validate.py` used `with sqlite3.connect(...) as conn:` in two test mutation paths. Python's SQLite connection context manager commits or rolls back transactions, but **does not close the connection**. Windows prevents temporary SQLite files from being removed while a connection is open, yielding `[WinError 32]` during `TemporaryDirectory.cleanup()`.

## Changes (test harness only)

- Centralized test database mutation in `Stage4Tests.mutate_db()`.
- Wrapped SQLite connections in `contextlib.closing(...)` **outside** the transaction `with conn:` block, closing the handle on success or exception.
- Routed the orphan-record foreign-key test through the same safely closing helper.
- Added two tests that spy on database connection creation and verify that the connection is **actually closed** after successful and failed modifications.
- No changes to `proofloop_validate.py`, `proofloop_store.py`, original snapshots, normalized JSONL, or production databases.

## Installing

Copy **only** the new `test_proofloop_validate.py` into your `Day1\FinalVersion` folder, replacing the previous Stage 4 test file. Preserve all other scripts and run folders. You may copy this README alongside it.

## PowerShell 7 — one command

Run this from `Day1\FinalVersion`:

```powershell
python .\test_proofloop_validate.py --report-dir '.\runs\stage4_test_report_fixed_001'
```

Use a **new** report directory because the scripts refuse to overwrite existing reports. A corrected run should report **26 tests**, not 24.

## Verification limitation

The corrected suite was verified in a Linux container. The connection-close behavior is also directly tested. The user must rerun the suite on Windows to confirm that the `[WinError 32]` cleanup problem is resolved on their host.
