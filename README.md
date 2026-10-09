# Building My Way Into AI

> **Breaking into the AI industry one real application at a time.**

I'm investigating the AI industry while actively trying to enter it: researching real companies and their roles, comparing requirements to my actual experience, learning missing technical capability, building the software to support the campaign, and publishing evidence of what changes. This is a human-directed, AI-assisted project. It starts with genuine prior experience, incomplete skills, imperfect early work, corrections, and real application decisions—not a claim that I was already an AI engineer.

**First case:** **Attempt #001 — OpenAI**, physically preserved in the original [`Day1/`](Day1/) directory. That attempt spans multiple calendar days; the folder name remains `Day1` because existing Windows scripts and reports reference it. **Five targets are selected for consideration; no submissions are yet verified in this baseline.**

## One experiment, three engineering/presentation layers

| Layer | What exists today | What grows later |
|---|---|---|
| **Engineering** | HTML/SQLite prototype; eight-stage Ashby API ingestion, JSONL, SQLite, validation, 231 reported passing Windows tests, audits, AI handoff | AI evaluation/testing, richer requirements, cross-company ingestion |
| **Product / interface** | Local read-only searchable Role Explorer with real SQLite source records | Integrated requirements, missing evidence, application states and metrics |
| **Proof / portfolio** | Technical README/docs, architecture, tests, change lessons, historical original scripts, build logs and templates; Git preparation | True Git commits, public demonstrations, Case Files, Observatory insights, actual applications and results |

**Distinct historical datasets:** the original `Day1/proofloop.db` HTML-derived experiment contains **817 roles**; `Day1/FinalVersion` preserves a separate **816-role frozen Ashby API snapshot**. These numbers aren't combined or represented as current vacancies.

## How the framework connects

- **[ProofLoop](framework/README.md)** — job/source → requirements → current qualifications and evidence → real gaps → just-in-time learning and Proof Sprint → applications → outcome.
- **[AI Observatory](observatory/README.md)** — companies and sources → observations → evidence-classified claims → relationships and unknowns → case reports and industry learning.
- **Shared infrastructure** — the Application Ledger, skills, Proof Graph, time and build logs, technical decisions, field notes, Case Files, AI-review records and Proof Capsules. See [workflow](docs/WORKFLOW.md) and [42-section coverage map](docs/FRAMEWORK_COVERAGE.md).

## Current case and engineering

- [Attempt #001 — OpenAI](Day1/ATTEMPT_OVERVIEW.md) — three original core application targets; two U.S.-remote-advertised but highly specialized stretch targets. No false submission claims.
- [FinalVersion source and full technical guide](Day1/FinalVersion/README.md) — Stage 1–8 code, SQL, validations, test history, corrective cases, Stage 9 prompt, and Role Explorer.
- [OpenAI Case File](observatory/companies/openai/CASE_FILE.md) — actual source-based investigation, not an invented industry map.

From `Day1/FinalVersion`, run the local demonstration with Python:

```powershell
python .\app\proofloop_explorer.py --db '.\examples\openai_snapshot_25.sqlite3' --open
```

The small database contains real excerpted rows, not manufactured sample positions. The full 816-role local database is a separate preserved output.

## Starting point and continuity

[Honest baseline](framework/BASELINE.md) · [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Application workflow](docs/WORKFLOW.md) · [Evidence rules](docs/EVIDENCE.md) · [Longitudinal measurement](docs/MEASUREMENT.md) · [Historical Git plan](docs/GIT_AND_HISTORY.md)

**Core principle:** Every application creates reusable software, sources, learning or proof, while a real submission remains the central objective. Today’s root framework is a first coherent system, not the finished Observatory or a published public series.
