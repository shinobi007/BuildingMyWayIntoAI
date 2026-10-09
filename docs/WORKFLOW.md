# One complete, repeatable application workflow

The system is not a list of separate to-do items. **One real role generates work that contributes to every layer.**

1. **Select target** (stable ID `001-A`, employer posting ID/URL). Add to `applications.csv` as selected; no submission timestamp yet.
2. **Investigate employer** using public sources, `observatory/.../sources.csv`, observations and claim states; maintain unresolved questions.
3. **Interpret posting** with source-quoted requirements in `requirements.csv`, not only keyword matches; distinguish required, preferred and alternatives.
4. **Compare candidate evidence**: `evidence.csv` + `proof_graph.csv`. Distinguish work-history self-reports from inspected project code/tests. Identify missing ability *versus* missing evidence.
5. **Determine just-in-time learning**: `learning_log.csv` and a bounded `PROOF_SPRINT.md` when a genuine shared project improvement is warranted.
6. **Build and verify** only as far as necessary: log actual tests, errors, decisions and AI assistance; save work product and demonstrable proof.
7. **Prepare and submit** role-appropriate materials. Submission happens on the employer site, not automatically through this scaffold. Record timestamp and confirmation only when real.
8. **Log outcome** and changes of state in `application_events.csv`; treat abandoned, submitted, interview, offer, rejection as real observed events, not predictions.
9. **Produce evidence**: link Git commit, README/demo, Case File or short Proof Capsule when useful. An episode is optional, not a blocker.
10. **Measure & carry forward**: record approximate time if known; update skill evidence, lessons, reusable artifacts and the next attempt's plan.

## Status model

`selected_not_submitted → preparing → submitted → [interview / rejected / offer / withdrawn]`, or `selected_not_submitted/preparing → abandoned` with a reason. `selected_not_submitted` means **no application has been submitted**, not an employer decision.

## ID and source conventions

- Attempt: `001`, `002` …; physical first folder: `Day1`.
- Target: `001-A`, `001-B` …; can point to one company/role posting ID.
- Employer source: `SRC001`; observation: `OBS001`; claim: `CLM001`; relationship: `REL001`.
- Requirement: `REQ001`; evidence: `EV001`; Proof Graph link: `PG001`; learning entry: `LRN001`; application event: `APP-E001`.
- Git commit is a technical change provenance marker, not a fake historical date.

Do not infer current job eligibility solely from frozen source metadata. The requirement→evidence joins have explicit source and limitation fields so later AI evaluations can challenge decisions instead of inheriting previous heuristics.
