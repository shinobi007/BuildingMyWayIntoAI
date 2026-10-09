# Building My Way Into AI

> **Breaking into the AI industry one real attempt at a time.**

This project documents a real job search that is also becoming a technical project. The first work took place in a local development folder; the reorganized public repository and generalized reusable package are still future milestones.

Instead of waiting until I have a perfectly organized portfolio before applying to AI companies, I am building the portfolio **inside the application process itself**. Each real attempt creates a concrete reason to research a company, work with data, write code, test assumptions, document mistakes, and leave behind evidence of what I can actually do.

The first attempt started with a very ordinary problem: I had a large list of OpenAI jobs exported from Google Docs and needed a defensible way to understand which roles were actually worth applying to.

That turned into a reproducible data pipeline, a reconciled SQLite dataset, multiple validation and test layers, and a role-analysis system that was ultimately used to choose the first three application targets.

This is not a finished framework dropped into a repository after the fact. It is the record of building the system while using it.

**Evidence boundary:** The three positions below were *selected as targets*, not evidenced as submitted applications. Role descriptions and availability reflect preserved October 2026 snapshots, not live verification.

---

## Documentation map

The current documentation set separates the public story, architectural reference, data contracts, verification history, first attempt, and retrospective. Relative links describe the **intended** repository arrangement; they do not claim the original Windows folder has already been reorganized.

- [Architecture](docs/architecture.md) — the source-to-decision architecture (existing reference document; not rewritten in this revision)
- [Data model](docs/data_model.md) — source, normalized, canonical and derived evidence, with reviewed limitations
- [Validation and testing](docs/validation_and_testing.md) — historical checks and their scope (existing reference document; not rewritten in this revision)
- [Attempt #001](docs/attempt_001.md) — full OpenAI shortlist and selection provenance
- [Lessons learned](docs/lessons_learned.md) — preserved development lessons and audit addendum
- [Changelog](CHANGELOG.md) — historical versions and documentation-only updates

---

## Attempt #001 — OpenAI

**Attempt #001** begins with OpenAI and currently contains three targets:

| Target | Role | Team | Ashby ID |
| --- | --- | --- | --- |
| **001-A** | IT Support Specialist | IT | `49ae54dc-3d33-4107-8112-63fac1ee86ca` |
| **001-B** | Dedicated Support Engineer - San Francisco | Support Delivery | `2348230a-295f-434d-9b16-653e01ddbd0b` |
| **001-C** | AI Support Engineer - San Francisco | Support Delivery | `1a979fd4-1bce-484e-a416-aed2810677a6` |

Application URLs:

- **001-A:** https://jobs.ashbyhq.com/openai/49ae54dc-3d33-4107-8112-63fac1ee86ca/application
- **001-B:** https://jobs.ashbyhq.com/openai/2348230a-295f-434d-9b16-653e01ddbd0b/application
- **001-C:** https://jobs.ashbyhq.com/openai/1a979fd4-1bce-484e-a416-aed2810677a6/application

The point of the project is not that a script can decide which job I should apply to. It cannot.

The point is that the system can make the evidence visible enough that the final decision is deliberate, explainable, and reproducible.

---

## The Core Idea

The project currently follows this technical chain:

```text
Python
  ↓
HTML parsing
  ↓
data extraction
  ↓
normalization
  ↓
JSON / JSONL
  ↓
CSV
  ↓
SQLite
  ↓
validation
  ↓
testing
  ↓
documentation
  ↓
Git
```

The initial ingestion, normalization, JSONL/CSV/SQLite, validation, and testing stages have been implemented for the frozen OpenAI dataset. The further Ashby and analysis branches are also implemented as historical, project-specific workflows. Documentation drafts exist; consistency review and eventual repository organization precede Git initialization.

**This diagram records the historical learning sequence, not a single supported install-and-run command.**

The project then expanded beyond the original pipeline:

```text
Google Docs HTML export
        │
        ▼
HTML parser
        │
        ▼
normalized role records
        │
        ├──────────────► JSONL
        │                  │
        │                  ▼
        │                 CSV
        │                  │
        │                  ▼
        └──────────────► SQLite
                           │
                           │
Ashby job-board API        │
        │                  │
        ▼                  │
frozen API snapshot        │
        │                  │
        ▼                  │
API normalization          │
        │                  │
        └────► reconciliation
                    │
                    ▼
            enriched SQLite DB
                    │
                    ▼
        role-analysis battery
                    │
                    ▼
   qualification-level analysis
                    │
                    ▼
       human review and selection
                    │
                    ▼
             Attempt #001
```

---

## Where the Data Came From

The first source was a Google Docs document containing OpenAI careers listings.

A plain-text export lost the hyperlinks, so the document was exported as **Web Page / HTML ZIP** instead. That preserved the URLs and created the first useful engineering constraint: extract the role data from semi-structured HTML without manually rebuilding the list.

The HTML pipeline produced **817 roles**.

A second source was later added using OpenAI's public Ashby job-board endpoint. The frozen API snapshot contained **815 roles** at the time it was captured.

The sources did not match perfectly:

| Reconciliation result | Count |
| --- | ---: |
| HTML roles | 817 |
| API roles | 815 |
| Matched by Ashby UUID | 814 |
| HTML-only | 3 |
| API-only | 1 |
| Canonical union | 818 |

The reconciliation uses the **Ashby UUID** as the stable identity rather than relying on mutable titles or display text.

The original HTML-derived data is preserved rather than overwritten by the API-derived data.

---

## Why Two Sources Matter

The HTML export and Ashby API each expose different useful information.

The HTML source preserved the role list and application links from the original research session.

The API added structured fields such as:

- department and team
- primary and secondary locations
- workplace type
- remote flags
- publication timestamps
- plain-text and HTML descriptions
- compensation components

The two sources also demonstrated why structured data should not automatically be trusted as truth.

For example, a large number of roles had:

```text
is_remote = 1
workplace_type = Hybrid
```

So `is_remote=1` could not safely be interpreted as "this role can be performed remotely from Utah."

That discovery directly changed the later analysis methodology.

---

## Main Generated Artifacts

The pipeline has produced artifacts including:

| Artifact | Purpose |
| --- | --- |
| `openai_roles.jsonl` | Canonical normalized records from the HTML source |
| `openai_roles.csv` | Spreadsheet-friendly representation of the HTML records |
| `proofloop.db` | Original HTML-derived SQLite database |
| `openai_ashby_snapshot_2026-10-07.json` | Frozen API snapshot used for reproducible reconciliation |
| `openai_ashby_roles.jsonl` | Normalized API-derived role records |
| `openai_ashby_reconciliation_report_v0_9_1.json` | Source comparison and reconciliation evidence |
| `proofloop_enriched.db` | Union database preserving HTML and API provenance |
| `proofloop_role_analysis_report_v0_15.json` | Broad role-selection transparency analysis |
| `proofloop_role_analysis_report_v0_15.md` | Human-readable v0.15 analysis |
| `proofloop_role_deep_analysis_report_v0_16.json` | Qualification-by-qualification deep analysis |
| `proofloop_role_deep_analysis_report_v0_16.md` | Human-readable v0.16 deep analysis |

Not every generated artifact necessarily belongs in the final Git repository. Repository cleanup will decide what should be committed, regenerated, ignored, or preserved strictly for provenance.

---

## What the Database Preserves

The enriched database does not flatten everything into one lossy table.

It keeps the canonical role view while also preserving source-specific records and one-to-many data such as secondary locations and compensation components.

Current tables include:

```text
build_metadata
roles
html_roles
api_roles
api_secondary_locations
api_compensation_components
```

This makes it possible to distinguish:

```text
canonical value
source-specific value
derived interpretation
```

rather than silently replacing one with another.

That distinction became important when titles differed only cosmetically, when location metadata conflicted, and when a later API snapshot no longer contained jobs present in the earlier HTML source.

---

## Raw versus normalized API data — an explicit limitation

The original Ashby job records each contain 18 fields. The normalized JSONL maps 17 source-job fields and adds provenance fields; **`shouldDisplayCompensationOnJobPostings` is not propagated into the normalized JSONL or enriched database**. The flag remains recoverable from the preserved raw API snapshot. Top-level `apiVersion` also remains at the raw-snapshot layer. This does not change the reported union counts, but it means downstream normalized records alone cannot establish the source's compensation-display preference. See [data_model.md](docs/data_model.md).

---

## Validation and Testing

The project deliberately added independent validation instead of assuming that a successful script run meant correct output.

### Original HTML pipeline

The final full-pipeline validator reported:

```text
45 / 45 checks PASS
```

The formal test suite reported:

```text
10 tests
10 passed
0 failed
0 errors
0 skipped
```

### Ashby/API branch

The API artifact validator reported:

```text
36 / 36 checks PASS
```

### Enriched database

The enriched database validator reported:

```text
34 / 34 checks PASS
```

The enriched database test suite reported:

```text
12 tests
12 passed
0 failed
0 errors
0 skipped
```

The v0.16 deep-analysis layer additionally verified that:

```text
baseline roles:          815
database current roles:  815
role IDs exact match:    True
SQLite integrity:        ok
```

The goal is not to claim that the system is perfect. The goal is to make failures observable and prevent obvious errors from silently becoming data.

---

## The Useful Mistakes

Some of the most valuable parts of the project came from things that initially failed.

### v0.3 → v0.3.1

The validator could print an expected-count failure but still report an overall PASS and exit successfully because the count mismatch had not been added to the final problem collection.

The fix made the expected-count mismatch a real failure and returned a non-zero exit status.

### v0.5 → v0.5.1

The SQLite importer used a connection context manager that committed or rolled back correctly but did not explicitly close the connection.

That mattered on Windows: temporary databases remained locked during later validation and tests.

The corrected version explicitly manages the connection lifecycle and closes it in `finally`.

### v0.7 → v0.7.2

The first full-pipeline validator exposed another Windows SQLite cleanup lock.

The validator and importer were corrected, then the complete pipeline was rerun rather than assuming the local fix was sufficient.

### v0.14 → v0.15

The first role-analysis battery used broad substring matching for sales-related language.

That produced false positives such as:

```text
commission  →  commissioning
```

v0.15 replaced the naïve substring approach with more contextual regular-expression rules and separated:

```text
strong sales exclusion evidence
```

from:

```text
sales context requiring review
```

### v0.15 → v0.16

Role-level keyword overlap was useful for discovery but not defensible as a final fit score.

v0.16 moved deeper and began mapping individual posted qualifications against explicit evidence tiers:

```text
DIRECT_WORK_EVIDENCE
RESUME_SKILL_CLAIM
ADJACENT_EVIDENCE
NOT_EVIDENCED
UNKNOWN
```

This prevented a programming-language entry on a résumé, for example, from being silently treated as proof of years of production software engineering.

These failures are intentionally part of the project history. They show how the implementation changed after contact with real data and real tests.

---

## What the historical PASS results establish—and do not

The six principal reports record **137/137 passing validation checks** and **22/22 passing formal tests**. These are historical records, not claims that the tests were rerun for this documentation update. Their check counts are overlapping measures of specific invariants, not independent statistical confidence estimates. The audited archived datasets and SQLite relations agree on their primary record populations and identity mapping.

Known limitations include non-transactional *replacement* of some existing outputs when `--overwrite` is supplied, partial-update possibilities for generated file sets, and far less automated regression coverage of location/sales/qualification heuristics than of the data pipeline. No test certifies the external job board's completeness, present-day posting availability, employer acceptance of a résumé, or an application outcome.

---

## Role Analysis Philosophy

The analysis system is designed to assist judgment rather than hide it behind a score.

Some of the major rules that emerged are:

```text
current API presence != original HTML presence

is_remote = 1 != true remote work

US - Remote secondary location != permission to work from any US state

relocation assistance != permission to start remotely

keyword overlap != qualification

resume skill claim != demonstrated professional depth

missing evidence != proof that a skill cannot be learned

high salary != high fit

remote convenience != domain fit

no detected sales language != guaranteed non-sales role
```

The final role selection remains a human decision.

---

## Audited role-analysis limitations

The v0.15 analyst retains `is_remote` as source evidence in its reports, but the local `classify_location()` decision branches do **not** directly consult the flag. Categories derive from location text, workplace type, office-day and relocation language, and other context. This is narrower than saying that the flag is an active input to the final classification. The code additionally defines `B_REMOTE_US_LOCATION_AMBIGUOUS`, a valid category with zero observed records in the frozen run.

The v0.16 requirement analyzer can overstate a match when it identifies familiar technical domains but does not compare a numeric years-of-experience demand against actual verified tenure. Its `expectation_strength()` also treats a sentence containing *ideally* as wholly `PREFERRED` even if that word qualifies only one clause. This matters for target **001-C**, whose posting says **8+ years of relevant experience**, *ideally* in a high-growth/fast-paced environment. The eight-year expectation is **not proven satisfied** and should not be dismissed because the historical report marks that full sentence `PREFERRED` / `DIRECT_MATCH`.

The v0.16 population is 224 deep candidates across five bands: `A_TOP5_REVIEW` 1; `B_SERIOUS_REVIEW` 48; `C_STRETCH_REVIEW` 122; `C_REQUIREMENTS_INCOMPLETE` 23; `D_BACKGROUND` 30. The **30-role decision-review pool** is a distinct subset, not another name for the `D_BACKGROUND` band.

---

## From "Application" to "Attempt"

One structural lesson appeared only after using the system.

Originally the project assumed:

```text
Application #001
```

would refer to one job.

That is too artificial for a real job search.

A serious company-level effort may involve several related applications at the same time, so the model is now:

```text
Attempt #001 — OpenAI
    ├── Target 001-A
    ├── Target 001-B
    └── Target 001-C
```

An **Attempt** is the broader company or opportunity campaign.

A **Target** is one specific role inside that attempt.

Each target can eventually have its own:

```text
evidence map
gap analysis
Proof Sprint
resume variant
application material
submission record
status
outcome
lessons
```

This is likely to become the durable model for later companies as well.

---

## ProofLoop

The operational system emerging from this project is called **ProofLoop**.

Its basic idea is recursive:

```text
real role
  ↓
investigate
  ↓
compare requirements to evidence
  ↓
identify gaps
  ↓
learn or build
  ↓
produce bounded proof
  ↓
apply
  ↓
record outcome
  ↓
improve the system
  ↓
next role
```

A key distinction is:

```text
missing ability
```

versus:

```text
missing evidence of ability
```

Those are not the same problem and should not produce the same response.

The broader research layer that accumulates observations about companies, roles, hiring patterns, technologies, and the AI industry is intended to become the **AI Observatory**.

---

## Current Scripts Worth Knowing

Historical versions are intentionally retained while the project is being documented because they show the actual development path.

Some of the major current or final-stage scripts include:

| Script | Role |
| --- | --- |
| `proofloop_openai_ingest_v0_2.py` | HTML ZIP → normalized JSONL |
| `proofloop_pipeline_validate_v0_7_2.py` | Full original pipeline validation |
| `test_proofloop_pipeline_v0_8_1.py` | Formal original-pipeline tests |
| `proofloop_ashby_fetch_v0_8.py` | Reproducible Ashby API acquisition |
| `proofloop_ashby_reconcile_v0_9_1.py` | HTML/API reconciliation |
| `proofloop_ashby_validate_v0_10.py` | API artifact validation |
| `proofloop_build_enriched_db_v0_11.py` | Build provenance-preserving enriched SQLite DB |
| `proofloop_enriched_db_validate_v0_12.py` | Enriched DB validation |
| `test_proofloop_enriched_db_v0_13.py` | Formal enriched-DB tests |
| `proofloop_role_analysis_v0_15.py` | Broad transparent role analysis |
| `role_deep_analysis.py` | v0.16 qualification-level deep analysis |

Older versions are not automatically obsolete junk. Where a later version exists because a real bug was discovered, the earlier version is part of the engineering history.

Repository cleanup will determine which historical versions belong in Git and which should be represented only in documentation and release history.

---

## Running the Current Analysis

Development has been performed on Windows using PowerShell 7 and a Python virtual environment.

The environment used during this attempt included:

```text
PowerShell 7.6.6
Python 3.14.8
pip 26.2.1
SQLite through Python's standard library
```

The original HTML ingestion was run with:

```powershell
python .\proofloop_openai_ingest_v0_2.py ".\OpenAI Careers.zip" --expected 817 --output ".\openai_roles.jsonl"
```

With the original unsuffixed filenames and all required historical artifacts present, the original pipeline can be validated with:

```powershell
python .\proofloop_pipeline_validate_v0_7_2.py --root . --expected 817
```

The formal original-pipeline tests can be run with:

```powershell
python .\test_proofloop_pipeline_v0_8_1.py
```

With the frozen enriched database, matching v0.15 inputs, and the original filenames in place, the historical role-analysis layers can be run with:

```powershell
python .\proofloop_role_analysis_v0_15.py
python .\role_deep_analysis.py
```

The scripts are intentionally being built with the Python standard library where practical so the project remains inexpensive, inspectable, and easy to reproduce.

More precise end-to-end setup instructions will be separated into dedicated documentation as the repository is cleaned up.

---

### Execution and privacy cautions

The commands above describe the historical workflow; they have not been independently tested as a fresh, one-command installation guide. Uploaded copies sometimes acquire suffixes such as `(1)` or `(2)` and cannot be assumed to satisfy import statements until original filenames are restored. Some validators compile Python files and may create bytecode caches; some scripts overwrite generated reports directly. Never use `--overwrite` on a historical database unless the existing file is separately backed up and the replacement process is understood.

The original résumé, personal identifiers, virtual environment, caches, unrelated installers, and potentially bulky generated reports require explicit review before any public Git commit. The local folder is not automatically a curated Git repository.

---

## Project Principles

1. **Use real work as the curriculum.**  
   The project should solve an actual problem connected to a real role or company.

2. **Do not exaggerate evidence.**  
   A résumé claim, keyword match, experiment, and proven production skill are different evidence states.

3. **Preserve provenance.**  
   Raw source facts, normalized values, and derived interpretations should remain distinguishable.

4. **Make unknowns explicit.**  
   Missing information should remain `UNKNOWN` instead of being converted into confidence.

5. **Test failures, not only happy paths.**  
   A validator that cannot fail correctly is not much of a validator.

6. **Keep Proof Sprints bounded.**  
   Building should support applying, not become an elaborate way to avoid applying.

7. **Document mistakes.**  
   The path from a flawed implementation to a corrected one is part of the proof.

8. **Prefer transparent rules over opaque scores.**  
   A human should be able to see why a role was retained, downgraded, or rejected.

9. **Separate current state from historical state.**  
   Job listings change. The system should preserve what was observed and when.

10. **The primary mission is employment.**  
    The software exists to improve the quality of the attempt, not replace the attempt.

---

## Current Status

At the end of the first build phase:

```text
[complete] Python pipeline
[complete] HTML parsing
[complete] data extraction
[complete] normalization
[complete] JSON / JSONL
[complete] CSV
[complete] SQLite
[complete] validation
[complete] testing
[complete] Ashby/API reconciliation
[complete] enriched database
[complete] broad role analysis
[complete] qualification-level role analysis
[complete] Attempt #001 target selection

[complete] source documentation drafted and reviewed through Stage 8
[pending] synchronize remaining architecture/testing references if needed
[next] repository cleanup
[next] .gitignore
[next] Git initialization
[next] intentional first commit
[next] GitHub repository
[next] target-specific application work; submissions and outcomes not yet evidenced
```

The immediate documentation plan is:

```text
README.md
docs/architecture.md
docs/data_model.md
docs/validation_and_testing.md
docs/attempt_001.md
docs/lessons_learned.md
CHANGELOG.md
```

---

## Current versus future system boundaries

**Implemented for Attempt #001:** ingestion, normalization, JSONL/CSV/SQLite persistence, API reconciliation, enriched data storage, independent validators, synthetic tests, broad/deep analyses, and a documented user-approved three-target shortlist.

**Supported manually or in documentation:** company-level Attempt/Target organization, résumé evidence interpretation, assistant-led final comparison, target-specific gap/proof planning, and development notes.

**Not yet demonstrated as working software:** persistent application ledger, Proof Graph relationships and skill-state tracking, AI Observatory intelligence workflows, provider-independent ATS adapters, installable reusable package, single stable CLI, GitHub/CI pipeline, or automated application submission/outcome tracking.

The next goal is to turn the preserved historical work into an inspectable, externally usable system *without letting that delay real applications indefinitely*.

---

## Why This Project Exists

The most important artifact is not any one Python file.

It is the accumulated evidence that I can take an ambiguous real-world problem, break it into smaller technical problems, build something, discover where it is wrong, test it, repair it, document it, and then use the result to make a real decision.

That is the point of **Building My Way Into AI**.

The repository starts with a job search.

The goal is that, attempt by attempt, it becomes evidence of the person doing the searching.

---

## Disclaimer

This is an independent personal project created as part of a job search and technical learning process.

It is not affiliated with, endorsed by, or maintained by OpenAI. Job listings, compensation, locations, requirements, and availability can change after the snapshots used in this project were captured.
