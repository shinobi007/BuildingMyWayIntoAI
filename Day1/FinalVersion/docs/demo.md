# Local Role Explorer demonstration

## Run

**Immediately runnable with the included 25-role excerpt:**

```powershell
python .\app\proofloop_explorer.py --db .\examples\openai_snapshot_25.sqlite3 --open
```

**Full 816-role local dataset (if available):**

Open PowerShell 7 in the existing `Day1/FinalVersion` directory and run:

```powershell
python .\app\proofloop_explorer.py --db '.\runs\openai_live_sqlite_001\db\jobs.sqlite3' --open
```

The browser opens at `http://127.0.0.1:8765/`. If it does not automatically open, paste that address into your browser. The app stays running until Ctrl+C. Python 3.10+ standard library only; no pip install needed. The app makes no network request to fetch job data, but its “Open Source” links lead to external employer pages when clicked.

## What to demonstrate

1. **Overview:** show the recorded 816 jobs and distinct workplace arrangements from the live database.
2. **Search:** enter “Support” and show results changing, then filter by team, location or work arrangement.
3. **Remote caution:** filter raw `is_remote=true` and demonstrate that `Hybrid` can still appear. Explain why this prevents false Utah-remote assertions.
4. **Inspect:** select a role, show its exact description, canonical normalized record and provenance fields. Open the employer source link separately.
5. **Database:** run read-only SQL examples on the same Stage 3 database.
6. **Testing:** run the explorer test suite and show the output, noting its separate scope from Stages 1–8 tests.

## Screenshots to capture after Windows verification

- `docs/screenshots/explorer-overview.png` — overview and source count.
- `docs/screenshots/explorer-filter.png` — technical-support query and work arrangement filters.
- `docs/screenshots/explorer-provenance.png` — selected role details and traceable source.
- `docs/screenshots/sqlite-query.png` — SQL query using read-only connection.
- `docs/screenshots/tests.png` — the full test pass output (crop irrelevant local paths/usernames).

These screenshots have not yet been captured for this package. They can be added after the first GitHub publication and applications; there is no need to delay submissions for them.

## Limits

- Localhost only; **no authentication**, so do not expose the port externally.
- Read-only database. No application status editing, Proof Graph visualization, fit scores or live synchronization yet.
- Remote flag is raw employer metadata, not a legal work-location decision.
- Current job availability must be checked separately.

## Public demo with genuine excerpt

Run `python .\app\proofloop_explorer.py --db '.\examples\openai_snapshot_25.sqlite3' --open` for **25 original archived OpenAI records**, not fabricated demo jobs. The larger local 816-role source DB is excluded from ordinary commits to avoid duplicating a large regenerable dataset.
