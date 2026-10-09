# Engineering lessons and judgment

1. **Preserve source evidence.** A normalization process is easier to audit when raw job objects and source IDs are retained alongside canonical fields. Snapshots are historical—not a guarantee that jobs still exist.
2. **Similar counts can refer to different products.** The old 817-role HTML-derived SQLite database, historic 815-role API snapshot, and new 816-role live API SQLite database must not be presented as interchangeable.
3. **The value of relational storage is queryability plus traceability.** JSONL is portable; SQLite adds indexing, constraints and joins, while JSON columns preserve detail not represented relationally.
4. **`with sqlite3.connect(...)` is not a safe close guarantee.** Python's connection context manager manages transactions, not connection lifetime. Windows test cleanup exposed this via `[WinError 32]`; explicit closure corrected it.
5. **Test counts must be grounded in actual runs.** The latest eight stage suites passed 231 tests on the user's Windows system. A separate 24-check live-data validator and the new explorer tests are distinct types of evidence, not numbers to add casually.
6. **Automated extraction needs provenance and uncertainty.** Seniority, years, degrees, compound employer wording and preferred criteria cannot be reduced to shared keywords. Recovering all missing headings did not eliminate every semantic parsing issue.
7. **Metadata is not the same as policy.** `is_remote=true` may coexist with `workplace_type=Hybrid`. A U.S.-remote job is not confirmed Utah-eligible without employer evidence.
8. **Sales filtering requires context.** Regex word boundaries prevent collisions such as `commissioning` versus `commission`, and sales-adjacent customers do not automatically mean a quota-driven job.
9. **A shortlist cap can hide opportunity.** Stage 5's 100-role boundary was useful for focused review, but Stage 7 found 175 outside-pool roles worth reconsidering. Recall flags are not proof of suitability.
10. **A complete handoff includes BOTH sides of a comparison.** The first Stage 8 archive omitted candidate qualifications, limiting independent AI review. The corrected revision includes the résumé evidence, still labeled self-reported.
11. **Engineering and demonstration are different deliverables.** A working 44+ MB SQLite database can be technically real but not visually compelling. A local Role Explorer and truthful README make it inspectable without pretending an enterprise product has been deployed.
12. **Commit evidence only after inspection.** Git cannot retroactively reconstruct authentic history. Preserve generated run reports and development notes, review staged files for unintended credentials, and create real commits as work progresses from now onward.
