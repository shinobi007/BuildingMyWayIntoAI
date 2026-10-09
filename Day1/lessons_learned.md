# Lessons Learned

## Building My Way Into AI — Attempt #001 / ProofLoop

This document captures the practical lessons that emerged while building and using the first end-to-end ProofLoop workflow during **Attempt #001 — OpenAI**.

These are not abstract best practices added after the fact.

They came from:

- scripts that failed
- assumptions that turned out to be wrong
- source fields that were misleading
- validation that caught real defects
- heuristics that overreached
- platform behavior that mattered
- analysis that looked convincing until manually reviewed
- the final use of the system to choose real application targets

The purpose of this document is not to make the project look cleaner.

It is to preserve what actually changed our understanding.

---

## Reading this retrospective after the technical audit

The 103 numbered lessons below remain the historical retrospective. A **documentation-only audit addendum** follows Lesson 103, recording new findings without renumbering or erasing what was learned at the time. The audit did not rewrite earlier source versions, rerun the historical tests, reselect the jobs, or submit applications.

Related documents: [README](../README.md) · [Architecture](architecture.md) · [Data model](data_model.md) · [Attempt #001](attempt_001.md) · [Validation and testing](validation_and_testing.md) · [Changelog](../CHANGELOG.md).

---

# 1. A Real Problem Is Better Than a Fake Portfolio Prompt

The project became useful because it started with a real constraint:

```text
There are hundreds of OpenAI jobs.
Which ones are actually worth applying to?
```

That question created a natural need for:

```text
parsing
normalization
structured data
SQLite
validation
testing
analysis
documentation
```

Nothing had to be invented for the sake of a portfolio.

The work existed because the problem existed.

That made the project more coherent and made every technical decision easier to justify.

**Lesson:**

> Use real work as the curriculum whenever possible.

---

# 2. Start Small, Then Earn Complexity

The first task was not:

```text
build an AI job-intelligence platform
```

It was:

```text
parse a Google Docs HTML export into structured role records
```

That was small enough to finish.

The system became larger only when the data demanded it.

The progression was:

```text
HTML
→ JSONL
→ CSV
→ SQLite
→ validation
→ tests
→ API reconciliation
→ enriched database
→ analysis
→ qualification mapping
```

Each layer existed because the previous one exposed a concrete need.

**Lesson:**

> Complexity should be earned by the problem.

---

# 3. Preserve the Original Source

One of the strongest architectural decisions was not overwriting the original HTML-derived dataset when the richer Ashby API became available.

Instead:

```text
original HTML source
```

and:

```text
API source
```

remained distinct.

This made it possible to discover:

```text
3 HTML-only roles
1 API-only role
814 matched roles
```

Had the second source simply replaced the first, that history would have disappeared.

**Lesson:**

> A better source should usually add evidence, not erase earlier evidence.

---

# 4. Normalization Is Not the Same as Rewriting

The reconciliation stage initially reported:

```text
56 title/team changes
```

Closer inspection showed that they were cosmetic differences.

The correct response was not to rewrite the source values.

Instead:

```text
raw value
```

was preserved while:

```text
normalized value
```

was used for comparison.

That produced:

```text
56 cosmetic differences
0 substantive title/team differences
```

**Lesson:**

> Normalize for comparison; preserve for provenance.

---

# 5. Stable Identity Matters More Than Display Text

Titles change.

Spacing changes.

Teams can be renamed.

Locations can be formatted differently.

The Ashby UUID turned out to be a much safer role identity than:

```text
title
team
row number
URL text alone
```

Example:

```text
49ae54dc-3d33-4107-8112-63fac1ee86ca
```

became more useful than relying on:

```text
IT Support Specialist
```

as the identity.

**Lesson:**

> Use provider-stable external IDs whenever they exist.

---

# 6. A Script Printing "FAIL" Does Not Mean It Failed

The v0.3 validator exposed a subtle but important control-flow problem.

It could print an expected-count failure and still end with:

```text
RESULT: PASS
```

and:

```text
exit code 0
```

The visible message looked correct.

The process behavior was wrong.

That matters because automation relies on exit status, not human interpretation.

**Lesson:**

> Test the state transition, not just the message.

---

# 7. Failure Paths Need Their Own Tests

The same class of issue appeared again in the CSV converter.

That reinforced the point.

A validator or converter should be tested with:

```text
valid input
```

and:

```text
deliberately invalid input
```

The project improved only after asking:

```text
What happens when this should fail?
```

rather than only:

```text
Does this work when everything is correct?
```

**Lesson:**

> Negative-path tests are first-class tests.

---

# 8. Resource Lifetime Is Part of Correctness

The SQLite importer worked logically.

It wrote rows correctly.

It committed correctly.

But on Windows, temporary database files stayed locked because the connection lifecycle was not explicit enough.

The problem appeared only during test cleanup.

The fix was:

```text
open
try
commit
except
rollback
finally
close
```

rather than relying only on the connection context manager.

**Lesson:**

> Correct data is not enough if the program leaves resources in a broken state.

---

# 9. Platform Behavior Matters

The SQLite lock issue was not theoretical.

It mattered because the project was actually being developed on Windows.

Cross-platform assumptions can hide until:

```text
file deletion
locking
path handling
shell behavior
encoding
```

become visible.

**Lesson:**

> Test on the platform you are actually using.

---

# 10. One Validator Is Not Enough

The project became more trustworthy as validation was layered.

Examples:

```text
JSONL validator
SQLite validator
full-pipeline validator
API validator
enriched DB validator
formal unittest suites
```

This may look redundant.

It was not.

Different validators found different classes of problems.

**Lesson:**

> Independent validation catches failures that local validation misses.

---

# 11. Regeneration Is Strong Evidence

One of the most useful checks was regenerating the JSONL and comparing it against the existing artifact.

That moved confidence from:

```text
the script ran
```

to:

```text
the same source produces the same artifact
```

Byte-identical regeneration is especially powerful when the output format is deterministic.

**Lesson:**

> Reproducibility is stronger than plausibility.

---

# 12. A Database Should Enforce Something

Moving from JSONL/CSV into SQLite was useful because SQLite could enforce:

```text
PRIMARY KEY
UNIQUE
NOT NULL
```

But declaring a constraint is only half the work.

The duplicate URL insert test proved that the constraint actually behaved as intended.

**Lesson:**

> Constraints should be exercised, not merely declared.

---

# 13. Flat Files and Databases Serve Different Purposes

JSONL, CSV, and SQLite were all useful.

None made the others obsolete.

JSONL was good for:

```text
streaming
diffing
machine-readable source-like records
```

CSV was good for:

```text
spreadsheet inspection
interoperability
```

SQLite was good for:

```text
constraints
joins
aggregation
relational modeling
```

**Lesson:**

> Choose formats by function instead of searching for one universal format.

---

# 14. One-to-Many Data Should Stay One-to-Many

Secondary locations and compensation components initially could have been flattened into text.

That would have made later analysis much harder.

Representing them as child rows preserved:

```text
ordering
separate values
exact queryability
```

This became critical for remote-location analysis.

**Lesson:**

> Do not flatten structure prematurely.

---

# 15. Structured Data Can Still Be Misleading

The field:

```text
is_remote = 1
```

looked obvious.

It was not.

The dataset showed hundreds of roles with:

```text
is_remote = 1
workplace_type = Hybrid
```

That instantly invalidated the simplistic interpretation:

```text
is_remote = 1
therefore
work from anywhere
```

**Lesson:**

> A field name is not a semantic guarantee.

---

# 16. Use Multiple Signals for Ambiguous Real-World Concepts

Remote eligibility required reviewing:

```text
primary location
secondary locations
is_remote (retained for evidence, not directly used in v0.15 classification branches)
workplace_type
description language
office-day language
relocation wording
```

No single field was reliable enough. **Static implementation clarification:** v0.15 retained `is_remote` in role dossiers, but the `classify_location()` branches did not consult that Boolean directly. The general multi-evidence lesson remains correct; the operative code path is narrower than the original prose implied.

**Lesson:**

> Real-world concepts often need evidence synthesis rather than one-column logic.

---

# 17. Unknown Is a Valid State

Some roles did not provide enough information to determine:

```text
true remote eligibility
office requirement
relocation support
qualification structure
```

The system improved when it stopped forcing these into yes/no outcomes.

Useful states included:

```text
UNKNOWN
REMOTE_NEEDS_CONFIRMATION
US_LOCATION_DEPENDENCY
C_REQUIREMENTS_INCOMPLETE
```

**Lesson:**

> Unknown is better than fabricated certainty.

---

# 18. Keyword Matching Is Useful Until It Pretends to Understand

The sales classifier initially used broad substring matching.

That produced:

```text
commission
→ commissioning
```

as a false positive.

The same problem appeared in resume-overlap counts.

A role could contain many generic technical words and appear highly aligned while actually requiring a completely different specialty.

**Lesson:**

> Keywords are good discovery tools and bad final judges.

---

# 19. Word Boundaries Matter

Replacing naïve substring matching with contextual regex rules improved the sales classifier immediately.

This was a small implementation detail with a large interpretive effect.

**Lesson:**

> Simple text analysis still benefits from careful linguistic boundaries.

---

# 20. Separate Strong Evidence From Weak Context

The v0.15 sales model became much better when it stopped using one binary label.

Instead:

```text
EXCLUDE_STRONG_SALES
REVIEW_SALES_CONTEXT
NO_SALES_SIGNAL_FOUND
```

made the reasoning visible.

The same pattern applies broadly.

**Lesson:**

> Prefer graded evidence states over false binary certainty.

---

# 21. Resume Keywords Are Not Professional Depth

The résumé listed:

```text
Python
JavaScript
SQL
PowerShell
Bash
```

It would have been easy to map those directly to engineering requirements.

That would have been misleading.

v0.16 instead distinguished:

```text
RESUME_SKILL_CLAIM
```

from:

```text
DIRECT_WORK_EVIDENCE
```

This was one of the most important epistemic improvements in the system.

**Lesson:**

> A named skill is evidence of exposure, not automatically evidence of depth.

---

# 22. Missing Evidence Is Not the Same as Missing Ability

A gap classification means:

```text
the current evidence does not establish this requirement
```

It does not necessarily mean:

```text
the candidate cannot do this
```

That distinction is essential for deciding whether the response should be:

```text
reject role
```

or:

```text
build proof
```

**Lesson:**

> Diagnose whether the problem is capability or proof.

---

# 23. Requirements Should Be Parsed in Context

A number like:

```text
8+ years
```

is meaningless without context.

It may be:

```text
required
preferred
one of several alternatives
mentioned in a narrative example
```

The project improved when experience extraction moved closer to real qualification sections.

**Lesson:**

> Extract requirements from the section that gives them meaning.

---

# 24. Section Parsers Need Defensive Rules

The deep parser initially risked treating ordinary prose containing words like:

```text
requirements
```

as the start of a qualification section.

Restricting extraction to exact line-level headings made the parser more reliable.

**Lesson:**

> Loose section matching creates confident nonsense.

---

# 25. An Empty Parse Is Not a Perfect Match

If qualification extraction fails, the system must not conclude:

```text
zero gaps
```

That would reward parser failure.

The explicit:

```text
C_REQUIREMENTS_INCOMPLETE
```

state prevents that mistake.

**Lesson:**

> Missing analysis output should reduce confidence, not increase it.

---

# 26. A Fit Score Can Hide the Wrong Objective

The role-analysis system deliberately avoided reducing everything to one final score.

That decision was validated when:

```text
Product Engagement Manager, User Operations
```

received the strongest automatic review band but turned out to have:

```text
technical_core = NONE_DETECTED
```

The user had specifically required a meaningful technical component.

A single weighted score could easily have hidden that contradiction.

**Lesson:**

> Decomposition is often safer than optimization.

---

# 27. The Best Automatic Candidate May Still Be Wrong

The strongest rule-based result was not selected.

That is not a failure of the project.

It is evidence that the project stopped automation at the correct boundary.

The system narrowed the search.

The final comparison remained judgment.

**Lesson:**

> Automate search-space reduction; be cautious about automating final judgment.

---

# 28. Human Review Is Part of the System

The final selection was produced through:

```text
user criteria
+
structured analysis
+
assistant comparative reasoning
+
user acceptance
```

That is not a flaw.

For a judgment-heavy task, human review is a legitimate architecture layer.

**Lesson:**

> Human judgment should be explicit, not hidden behind pseudo-objective math.

---

# 29. The User Did Not Need to Know the Final Answer First

The user supplied:

```text
criteria
constraints
resume
```

but did not manually select the final three roles.

That is important.

The system was useful because the user could define the problem without knowing the answer.

**Lesson:**

> Good AI-assisted workflows let the human define the objective without having to precompute the solution.

---

# 30. Criteria Matter More Than Vague Preferences

The final role selection became much better once the criteria were explicit:

```text
NO SALES
real technical work
location feasibility
relocation reality
remote ambiguity
documented evidence
bounded gaps
plausibility
```

Without those constraints, any ranking would have been arbitrary.

**Lesson:**

> Make the objective function visible before ranking options.

---

# 31. Location Feasibility Is Not a Secondary Detail

A role can be an excellent skills match and still be unusable.

This became obvious with the strongest support roles.

The project therefore had to distinguish:

```text
remote now
remote unclear
relocation supported
location dependent
```

**Lesson:**

> Practical feasibility is part of fit.

---

# 32. Relocation Support Changes the Decision

The IT Support Specialist role was onsite five days per week.

Ordinarily that would be a major problem.

But it explicitly offered:

```text
relocation assistance
```

Given the user's financial reality, that changed the role from:

```text
probably inaccessible
```

to:

```text
plausible enough to pursue
```

**Lesson:**

> A constraint can change meaning when another field changes the feasibility path.

---

# 33. Remote Convenience Should Not Override Domain Fit

Several security roles were much easier geographically.

But they required:

```text
security engineering
vendor security risk
threat intelligence
offensive security
adversary tradecraft
```

The system correctly avoided ranking them above stronger support/IT fits merely because they were remote.

**Lesson:**

> Optimize across the whole problem, not the most convenient variable.

---

# 34. Seniority Is Different From Technical Gap

A role can be highly aligned technically but still be unrealistic because of experience expectations.

The Technical Systems Program Manager role was a good example.

It aligned strongly with:

```text
CRM
APIs
automation
support systems
QA
Salesforce
```

but asked for:

```text
8+ years driving high-impact technical programs
```

That is not the same problem as:

```text
learn one missing technology
```

**Lesson:**

> Separate learnable technical gaps from chronology/seniority gaps.

---

# 35. Some Gaps Are Proof-Sprint-Friendly

Examples of more bounded gaps include:

```text
Python support tooling
API troubleshooting demos
authentication failure reproduction
logging/tracing labs
endpoint-management lab work
```

These can potentially be strengthened with focused proof.

Other gaps such as:

```text
8 years of TPM experience
5 years of threat intelligence
10 years of SRE leadership
```

cannot be honestly created in a short sprint.

**Lesson:**

> Only build proof for gaps that proof can actually address.

---

# 36. Proof Work Should Not Become Avoidance

The project can easily become fascinating enough to delay applications indefinitely.

That is a real risk.

The purpose of ProofLoop is:

```text
improve the quality of the attempt
```

not:

```text
replace the attempt with endless system building
```

**Lesson:**

> Bound the engineering so it serves the employment goal.

---

# 37. Documentation Is Part of the Proof

The project contains meaningful engineering work, but without documentation another person would see:

```text
many Python files
many JSON files
two SQLite databases
several reports
```

and have no idea what happened.

The README, architecture, data model, validation/testing, and Attempt #001 documents convert raw work into inspectable evidence.

**Lesson:**

> Undocumented work is harder to evaluate than incomplete but well-explained work.

---

# 38. The Ugly Parts Are Valuable

It would be tempting to hide:

```text
v0.3 failure propagation bug
v0.4 failure behavior
v0.5 SQLite lock
v0.7 validator lock
v0.14 false sales positives
```

But those are some of the strongest parts of the project.

They show:

```text
observation
debugging
root cause
correction
regression testing
```

**Lesson:**

> A corrected failure can demonstrate more engineering ability than a clean-looking final file.

---

# 39. Version Numbers Became a Useful Development Log

The many versioned scripts initially looked messy.

But they preserved the actual evolution:

```text
v0.3
→ v0.3.1

v0.5
→ v0.5.1

v0.7
→ v0.7.1
→ v0.7.2
```

That history is useful now.

Long term, Git should carry more of this burden.

**Lesson:**

> Before Git exists, file versions preserve history; after Git exists, commits should increasingly take over that job.

---

# 40. Git Should Have Started Earlier

The project reached a surprisingly advanced state before Git initialization.

That means the filesystem currently contains many versioned files that Git history could otherwise have represented more elegantly.

This is not catastrophic.

It is a useful lesson.

**Lesson:**

> Initialize Git near the beginning of the next attempt, not after the first major build phase.

---

# 41. But Do Not Rewrite the History to Look Cleaner

It would be easy now to delete every older script and pretend the final versions appeared directly.

That would make the repository neater but less truthful.

Repository cleanup should reduce noise without erasing the actual engineering path.

**Lesson:**

> Clean presentation should not become historical falsification.

---

# 42. Source Data and Generated Data Need Different Repository Rules

The working folder currently contains:

```text
source snapshots
normalized artifacts
databases
validation reports
analysis reports
scripts
documentation
installers
resume files
virtual environment
cache files
```

Not all of those belong in Git.

The next cleanup step needs to distinguish:

```text
source/provenance worth preserving
code worth committing
small evidence reports worth committing
large reproducible outputs
local-only files
private/personal files
environment/cache files
unrelated installers
```

**Lesson:**

> Repository design is a data-governance problem, not just a folder-cleanup problem.

---

# 43. Personal Data Needs Deliberate Handling

The working directory contains a résumé and job-search materials.

A public repository should not blindly commit everything in the folder.

Before Git staging, the project needs to decide what personal information belongs publicly.

**Lesson:**

> `git add .` is not a documentation strategy.

---

# 44. Large Generated Reports Need a Policy

The role-analysis Markdown and JSON reports can be hundreds of kilobytes or several megabytes.

They are useful evidence.

They are also noisy.

A public repository may be better served by preserving:

```text
selected reports
small summaries
generation scripts
fixtures
```

while excluding some large regenerable artifacts.

**Lesson:**

> Commit evidence intentionally; do not confuse volume with transparency.

---

# 45. Frozen Snapshots Are Valuable but Potentially Large

The frozen Ashby snapshot makes the reconciliation reproducible.

That is valuable.

But source snapshots also increase repository size and may change over time.

A long-term design may use:

```text
data/
snapshots/
```

or release assets rather than leaving every snapshot at repository root.

**Lesson:**

> Provenance artifacts deserve a deliberate storage strategy.

---

# 46. Naming Should Become More Consistent

The current working directory includes both:

```text
proofloop_role_analysis_v0_15.py
```

and:

```text
role_deep_analysis.py
```

even though the latter corresponds to v0.16.

That happened because a shorter filename was needed after a ChatGPT download problem.

The filename worked.

The naming consistency suffered.

**Lesson:**

> Operational workarounds should eventually be normalized in repository structure.

---

# 47. Do Not Rename Historical Files Casually

At the same time, renaming every historical file can break:

```text
documentation
reports
commands
provenance
```

The better approach may be:

```text
preserve historical filename
introduce clean current entry point
document aliases/migration
```

**Lesson:**

> Cleanup should preserve traceability.

---

# 48. The Local Folder Is Not Yet the Repository

The current Day1 folder contains unrelated installers such as:

```text
ChromeSetup
Bitwarden installer
ShareX installer
```

It also contains:

```text
.venv
__pycache__
```

Those clearly do not belong in the final project repository.

**Lesson:**

> The working directory and the publishable repository are different objects.

---

# 49. A `.gitignore` Will Be Essential

At minimum, the repository will need to consider ignoring:

```text
.venv/
__pycache__/
*.pyc
temporary files
large generated analysis outputs
local caches
unrelated installers
possibly private resume artifacts
```

The exact rules should be decided after reviewing the full directory.

**Lesson:**

> Ignore rules should reflect the project model, not just a generic Python template.

---

# 50. The README Should Tell a Story, Not Dump Architecture

The README became stronger when framed as:

```text
a real application attempt that caused a technical system to emerge
```

rather than:

```text
a sophisticated job-analysis platform
```

The detailed architecture belongs elsewhere.

**Lesson:**

> The README is the front door, not the storage room.

---

# 51. Documentation Should Be Layered

The project now benefits from separate documents:

```text
README.md
architecture.md
data_model.md
validation_and_testing.md
attempt_001.md
lessons_learned.md
```

This avoids forcing one document to explain everything.

**Lesson:**

> Separate documents by question, not by arbitrary length.

---

# 52. "What Happened?" and "How Does It Work?" Are Different Questions

`architecture.md` answers:

```text
How is the system structured?
```

`attempt_001.md` answers:

```text
How was the actual OpenAI decision reached?
```

`validation_and_testing.md` answers:

```text
Why should anyone trust the pipeline?
```

`lessons_learned.md` answers:

```text
What changed our understanding?
```

**Lesson:**

> Good documentation separates mechanism, evidence, and narrative.

---

# 53. AI Can Be Part of the Engineering Process Without Hiding the Human Role

The user did not manually write every line.

The assistant helped:

```text
design
debug
analyze
write scripts
interpret outputs
select finalists
write documentation
```

The user:

```text
defined the objective
ran the code
provided outputs
caught mistakes
made constraints explicit
supplied evidence
accepted/rejected recommendations
```

That collaboration is part of the actual project.

**Lesson:**

> AI assistance should be documented as part of the workflow, not hidden or exaggerated.

---

# 54. AI Output Still Needs Verification

Several assistant suggestions were corrected during the project.

Examples included:

```text
PowerShell / SQLite shell behavior
file naming assumptions
remote-field interpretation
analysis heuristic weaknesses
```

The user caught issues and forced deeper verification.

That improved the project.

**Lesson:**

> AI can accelerate work, but verification remains part of the job.

---

# 55. The User's Corrections Were Valuable Signal

Some of the strongest refinements happened because the user said:

```text
that does not look right
```

or:

```text
you are overclaiming this
```

Those corrections pushed the system toward:

```text
better provenance
better remote logic
better sales logic
better role-selection logic
```

**Lesson:**

> Friction is useful when it exposes a false assumption.

---

# 56. Exhaustive Analysis Has Diminishing Returns

The project reviewed an enormous amount of role data.

That was valuable once because it established the landscape.

But after the top three were selected, continuing to refine the role-analysis engine would have produced diminishing returns.

The correct move was to stop and document.

**Lesson:**

> Know when the analysis is sufficient to act.

---

# 57. "Good Enough to Decide" Is a Real Milestone

The system is not finished.

The role classifier is not perfect.

The data model can improve.

The parser can improve.

The reports can improve.

But the system was good enough to support a defensible decision.

That is meaningful.

**Lesson:**

> Completion should be tied to the decision need, not theoretical perfection.

---

# 58. Attempt-Level Thinking Is Better Than Application-Level Thinking

The project originally used:

```text
Application #001
```

Then it became clear that several applications to one company might belong together.

The new structure:

```text
Attempt #001
    ├── Target A
    ├── Target B
    └── Target C
```

fits the real process much better.

**Lesson:**

> Model the real workflow, not the first abstraction that comes to mind.

---

# 59. Company-Level Research Can Be Reused Across Targets

The three OpenAI targets share:

```text
company research
source snapshots
role database
location analysis
application platform
organizational context
```

Treating them as one Attempt means that work does not need to be duplicated.

**Lesson:**

> Shared context belongs above the individual application.

---

# 60. Target-Specific Evidence Still Needs Separation

Even inside one Attempt, each target needs its own:

```text
gap analysis
resume variant
proof work
application materials
status
outcome
```

The shared company layer should not blur the role-specific differences.

**Lesson:**

> Reuse shared context without collapsing distinct decisions.

---

# 61. The Final Three Represent Different Risk Profiles

The final selection was stronger because the targets are not identical.

## IT Support Specialist

Strength:

```text
best conventional fit
```

Risk:

```text
onsite + AV/device-management gaps
```

## Dedicated Support Engineer

Strength:

```text
best technical work-content alignment
```

Risk:

```text
distributed/cloud depth + location
```

## AI Support Engineer

Strength:

```text
best AI-native bridge
```

Risk:

```text
seniority + location
```

**Lesson:**

> A portfolio of applications can be strategically diversified.

---

# 62. Compensation Should Not Drive Fit

Some roles had very high salaries.

That made them visually attractive.

But compensation did not erase:

```text
security-domain gaps
seniority gaps
location problems
specialist engineering requirements
```

**Lesson:**

> Compensation is a decision input, not a fit shortcut.

---

# 63. Preserve Units

The IT Support Specialist compensation was hourly.

Many other roles were annual.

Without preserving:

```text
interval
currency
```

raw compensation comparison would have been nonsense.

**Lesson:**

> Numbers without units are dangerous data.

---

# 64. A Database Query Can Be Correct and Still Answer the Wrong Question

Several early SQL queries were useful for exploration but not suitable as final classifiers.

For example:

```text
team <> 'Sales'
```

does not mean:

```text
not a sales role
```

Similarly:

```text
title contains support
```

does not mean:

```text
good fit
```

**Lesson:**

> Query correctness and question correctness are separate.

---

# 65. SQL Is Excellent for Transparency

Even though some queries were too crude for final classification, SQL was extremely useful because it made assumptions inspectable.

It allowed questions such as:

```text
How many roles are in each team?
What combinations of remote fields exist?
Which roles have US - Remote as a secondary location?
What compensation intervals appear?
```

**Lesson:**

> SQL is an excellent investigative language even when the final logic moves into Python.

---

# 66. Python and SQL Complement Each Other

SQL handled:

```text
filtering
grouping
relational joins
counting
```

Python handled:

```text
text parsing
regex
classification
report generation
multi-stage logic
```

Trying to force everything into either language would have made the system worse.

**Lesson:**

> Use each tool where its reasoning model is strongest.

---

# 67. Markdown Reports Were Surprisingly Valuable

The Markdown reports turned large amounts of structured data into something that could actually be reviewed manually.

They also made it possible to:

```text
inspect heuristics
compare roles
spot false positives
document rationale
```

**Lesson:**

> Human-readable output is a real engineering feature.

---

# 68. JSON Reports Preserve Continuity

The Markdown report was better for reading.

The JSON report was better for:

```text
the next script
structured continuation
exact fields
automation
```

Producing both prevented the project from choosing between human and machine readability.

**Lesson:**

> Separate presentation format from continuation format.

---

# 69. Read-Only Analysis Is a Good Default

The role-analysis scripts opened the enriched DB in:

```text
READ ONLY
```

mode.

This protects the core dataset from accidental mutation during exploratory analysis.

**Lesson:**

> Analytical layers should not modify source-of-truth data unless they explicitly need to.

---

# 70. Provenance Should Survive Every Layer

The strongest overall design principle became:

```text
source
→ normalized source
→ reconciled record
→ derived evidence
→ decision
```

Each layer should remain traceable backward.

**Lesson:**

> If a conclusion cannot be traced back to evidence, it is too opaque.

---

# 71. The First Attempt Should Not Become the Universal Schema

Attempt #001 revealed many useful fields and concepts.

But it would be a mistake to assume OpenAI/Ashby represents every future company.

Future sources may use:

```text
Greenhouse
Lever
Workday
custom career sites
```

The shared schema should emerge gradually.

**Lesson:**

> Generalize from repeated experience, not from one rich example.

---

# 72. Build Adapters Around a Common Core

The likely future direction is:

```text
source adapter
    ↓
common normalized role model
    ↓
shared analysis
```

rather than writing the whole pipeline again for each ATS.

But that should happen only after the second or third Attempt confirms what is truly common.

**Lesson:**

> Abstract after pattern recognition, not before.

---

# 73. The Future Proof Graph Is More Important Than a Bigger Classifier

The most valuable next conceptual layer is probably not another role-ranking model.

It is a graph connecting:

```text
requirement
→ evidence
→ artifact
→ gap
→ Proof Sprint
```

That would turn the current evidence mapping into a durable career-development system.

**Lesson:**

> The next useful abstraction should connect claims to proof, not add more scoring.

---

# 74. Evidence States Should Remain Rich

The broader project uses skill states such as:

```text
UNEXPLORED
LEARNING
EXPERIMENTED
APPLIED
TESTED
DOCUMENTED
REPEATED
PROVEN
```

That is more informative than:

```text
has skill / does not have skill
```

**Lesson:**

> Capability is developmental, not binary.

---

# 75. Research Confidence Should Also Be Explicit

Future AI Observatory work will benefit from states such as:

```text
DOCUMENTED
CORROBORATED
REPORTED
INFERRED
HYPOTHESIS
UNKNOWN
SUPERSEDED
```

This mirrors the same epistemic discipline used in role analysis.

**Lesson:**

> Confidence state is part of the data.

---

# 76. The System Should Eventually Track Outcomes

The current pipeline ends at selected targets.

It will become much more useful once it records:

```text
submitted
rejected
interview
screen
technical assessment
offer
withdrawn
abandoned
```

Then the system can learn from actual outcomes.

**Lesson:**

> A recommendation system without outcome feedback eventually stops learning.

---

# 77. Outcomes Should Feed the Next Attempt

If a role with a certain evidence pattern repeatedly gets interviews, that matters.

If another pattern repeatedly gets rejected, that matters too.

Future Attempts should use:

```text
actual application outcomes
```

as new evidence.

**Lesson:**

> The loop is not complete until outcomes modify future decisions.

---

# 78. The Project Name Fits Better After Attempt #001

**Building My Way Into AI** became more accurate as the work progressed.

The project is not:

```text
a static portfolio
```

It is:

```text
a repeated cycle of applying, building, learning, proving, and improving
```

Attempt #001 demonstrated that the name describes the process rather than only the aspiration.

**Lesson:**

> A good project identity should describe what the system actually does.

---

# 79. ProofLoop Is Best Treated as the Operational Layer

The larger project is:

```text
Building My Way Into AI
```

ProofLoop is the mechanism that handles:

```text
role
→ requirement
→ evidence
→ gap
→ proof
→ application
→ outcome
```

Keeping those levels separate helps avoid naming everything the same thing.

**Lesson:**

> Project identity and operational subsystem identity should remain distinct.

---

# 80. The AI Observatory Should Remain a Separate Research Layer

The role database naturally started accumulating information about:

```text
OpenAI teams
location policy
compensation
job families
technical expectations
hiring patterns
```

That broader intelligence belongs in the future:

```text
AI Observatory
```

rather than being mixed directly into ProofLoop's application state.

**Lesson:**

> Operational data and research intelligence can share evidence without becoming the same system.

---

# 81. The First Attempt Produced More Than Expected

The original goal was:

```text
find roles to apply to
```

The project also produced evidence of:

```text
Python
HTML parsing
data extraction
normalization
JSONL
CSV
SQLite
SQL
validation
testing
debugging
API ingestion
data reconciliation
relational modeling
regex
classification
technical writing
research
decision analysis
```

This is exactly the recursive effect the project was intended to create.

**Lesson:**

> A well-chosen real problem can generate proof across many skills at once.

---

# 82. But Proof Should Not Be Inflated

The existence of this project does not automatically prove:

```text
senior software engineering
production distributed systems
ML engineering
security engineering
```

The project should be described accurately.

Its strength is in what it genuinely demonstrates.

**Lesson:**

> Strong evidence becomes weaker when exaggerated.

---

# 83. Present the Work as an Evolution

A polished final repository should still show:

```text
initial approach
failure
correction
better model
real decision
```

That story is more credible than pretending the architecture appeared fully formed.

**Lesson:**

> Evolution is part of the artifact.

---

# 84. The Next Attempt Should Begin With Git

For Attempt #002, the ideal sequence should be closer to:

```text
mkdir attempt
git branch / structured folder
capture source
commit source metadata
build adapter
commit
validate
commit
analyze
commit
document
commit
```

rather than waiting until the end.

**Lesson:**

> Use version control as part of the working method, not only as publication packaging.

---

# 85. The Next Attempt Should Reuse, Not Copy-Paste

Attempt #002 should reuse the stable pieces:

```text
common role model
validation utilities
report helpers
evidence framework
Attempt / Target structure
```

while adding a new source adapter.

**Lesson:**

> Reuse the learned abstractions, not the accidental file layout.

---

# 86. The Next Attempt Should Be Faster

Attempt #001 was expensive because everything was being invented.

Attempt #002 should test whether the architecture actually reduces marginal work.

A successful framework should make the next company easier.

**Lesson:**

> Reusability is proven by the second use, not the first.

---

# 87. The Next Attempt Should Test the Generalization

Questions for Attempt #002:

```text
Does the role schema still work?
Does the location model generalize?
Do the sales rules generalize?
Does the evidence framework generalize?
Does Attempt → Target still fit?
What breaks when the ATS is not Ashby?
```

**Lesson:**

> The next real use is the real architecture test.

---

# 88. "Presentable to Another Person" Is Now a Requirement

The user explicitly identified that the system was powerful but not yet presentable enough for another person.

That means future work should optimize for:

```text
clarity
navigation
reproducibility
smaller entry points
good defaults
clean repo structure
clear commands
representative outputs
```

not only analytical depth.

**Lesson:**

> Internal usefulness and external usability are different milestones.

---

# 89. A Repository Should Have a Happy Path

Another person should eventually be able to understand:

```text
1. what this is
2. what to run
3. what input is required
4. what output is produced
5. where to read the result
```

without first understanding every historical script.

**Lesson:**

> Preserve history, but provide a clean current path.

---

# 90. Documentation Should Link to Evidence

The current documents explain the project well.

A later refinement should connect them directly to:

```text
scripts
reports
schemas
test outputs
sample artifacts
```

so readers can move from narrative to proof.

**Lesson:**

> Claims in documentation are stronger when the evidence is one click away.

---

# 91. The Repository Should Probably Gain a `docs/` Directory

The documentation structure naturally wants to become:

```text
README.md
docs/
    architecture.md
    data_model.md
    validation_and_testing.md
    attempt_001.md
    lessons_learned.md
CHANGELOG.md
```

The files are being created first before any disruptive repository cleanup.

**Lesson:**

> Write the documents before reorganizing the filesystem they describe.

---

# 92. Repository Cleanup Should Happen Before `git add`

The current directory includes too much local material to stage blindly.

The correct order is:

```text
document
inspect
classify files
create repository structure
create .gitignore
move/copy deliberately
git init
git status
stage intentionally
```

**Lesson:**

> Git staging should be the result of curation.

---

# 93. The First Commit Should Be Meaningful

The first commit should represent a coherent project state.

Something closer to:

```text
Initial documented ProofLoop pipeline for Attempt #001
```

than:

```text
stuff
```

The exact contents should be reviewed first.

**Lesson:**

> Commit history is another layer of documentation.

---

# 94. Generated Artifacts Should Have a Reproduction Story

For every generated artifact kept in the repository, another person should ideally be able to answer:

```text
What produced this?
From which inputs?
With which version?
Can I regenerate it?
```

**Lesson:**

> A generated file without lineage becomes unexplained baggage.

---

# 95. Large Source Artifacts May Need Release-Level Storage

If later Attempts contain increasingly large snapshots, committing all raw data directly to Git may become undesirable.

Possible future options:

```text
Git LFS
release assets
separate data package
compressed fixtures
hash + acquisition instructions
```

No change is needed yet, but the issue is now visible.

**Lesson:**

> Data growth needs its own version-control strategy.

---

# 96. The Project Should Eventually Have a Single Current CLI

Right now, the workflow is spread across many versioned scripts.

That is appropriate for the historical build phase.

A future presentable version may expose something like:

```text
proofloop ingest
proofloop validate
proofloop analyze
proofloop attempt
```

while the historical scripts remain available as provenance.

**Lesson:**

> Historical implementation and current interface do not have to be the same thing.

---

# 97. Do Not Build the CLI Yet

The project has not earned that abstraction yet.

Documentation and Git come first.

A CLI should be built only after the current behavior and boundaries are stable enough to justify it.

**Lesson:**

> Presentation improvements should follow understanding, not race ahead of it.

---

# 98. The Most Important Technical Lesson

The most important technical lesson from Attempt #001 is probably:

> **Correctness is not one check.**

It is a chain of evidence:

```text
source preserved
transformation deterministic
schema constrained
failure paths tested
relationships validated
regeneration checked
interpretations exposed
uncertainty preserved
```

---

# 99. The Most Important Analytical Lesson

The most important analytical lesson is probably:

> **A transparent imperfect model is more useful than an opaque confident model.**

The project repeatedly improved by exposing:

```text
why
```

a role received a label.

That allowed the user and assistant to challenge the model.

---

# 100. The Most Important Project Lesson

The most important project lesson is probably:

> **Do not wait to become qualified before building proof. Build proof while pursuing the real opportunity.**

That is the core of Building My Way Into AI.

Attempt #001 turned:

```text
job search
```

into:

```text
engineering work
research
documentation
technical evidence
```

while still ending in actual application targets.

---

# 101. What Should Change Immediately

Before Git initialization:

```text
finish documentation
write CHANGELOG.md
inspect the working directory
separate unrelated installers
decide treatment of the resume
decide treatment of large generated reports
decide treatment of source snapshots
create docs/
create a deliberate .gitignore
decide current-vs-historical script layout
```

Then:

```text
git init
git status
```

Only after that should files be staged.

---

# 102. What Should Stay the Same

Several principles are worth preserving unchanged:

```text
real problem first
no inflated evidence
preserve provenance
explicit unknowns
independent validation
negative-path testing
bounded Proof Sprints
transparent analysis
human final judgment
employment remains the primary mission
```

These principles survived contact with the real Attempt.

That is stronger evidence than simply writing them down in advance.

---

# 103. Final Lesson

Attempt #001 started as:

```text
a list of jobs
```

and ended as:

```text
a tested data pipeline
a provenance-preserving database
a role-analysis system
a documented decision process
three real application targets
```

The project succeeded not because every component is finished.

It succeeded because the system became useful before it became perfect.

That is the lesson worth carrying into Attempt #002.

---

# Post-analysis evidence audit addendum (documentation-only)

The entries below were identified while comparing the preserved artifacts, code, reports, documentation, and original role requirements. They supplement the historical lessons without claiming they were known at the time the original 103 lessons were written.

## A1. Detecting the failure is not enough; preserve the prior successful output

Versions v0.3.1 and v0.4.1 corrected false-success exit behavior, but the SQLite importers still permit destructive replacement in some `--overwrite` failure paths. A program can correctly return `FAIL` yet already have removed a valid earlier database. **Lesson:** build, validate, and only then replace; exit codes and preservation are separate correctness requirements.

## A2. One atomic file write is not an atomic multi-artifact release

The v0.8 Ashby fetcher takes valuable precautions for individual file writes, but a raw snapshot and its companion provenance report are saved independently. If the second write fails, the pair can be inconsistent. **Lesson:** define atomicity at the level of what consumers treat as one logical artifact set, not only one file.

## A3. A source field may be preserved while absent downstream

The frozen API retained `shouldDisplayCompensationOnJobPostings`, but the normalized JSONL and enriched DB did not project it. The source is preserved, but normalized consumers lose access to that specific field. **Lesson:** document intended omissions in field lineage; do not claim that all raw fields survive each normalization step.

## A4. Document the *operative* code path, not only the design intention

The location-analysis prose said v0.15 combined `is_remote` with other factors; in the actual `classify_location()` function the Boolean is assigned but not used by the classification branches. The flag remains report evidence. **Lesson:** distinguish fields carried, fields displayed, and fields used to make a classification.

## A5. A multi-clause requirement cannot safely be labeled preferred by one word

The 001-C posting's phrase “8+ years ... ideally within high-growth ... environments” was labeled wholly `PREFERRED` by v0.16 because `ideally` appeared in the text. The more defensible reading is that the environment is preferred; the years are a posted expectation. **Lesson:** clause-level interpretation is necessary before softening employer requirements.

## A6. Experience-domain overlap does not verify years or depth

The v0.16 `DIRECT_MATCH` label can follow from direct work-domain evidence while ignoring whether a numeric duration is met. Similarly, experience with APIs is not necessarily evidence of expert-level production distributed-systems diagnosis. **Lesson:** separate domain, recency, duration, scope, tool proficiency, and proof strength.

## A7. Test the most consequential interpretation rules

The data-ingestion pipeline has substantially stronger negative-path and synthetic coverage than the sales, location, technical-core, and qualification heuristics. **Lesson:** add grounded expected-result fixtures for ambiguous job language before trusting classifications across new companies or ATSs. Historical passing data checks cannot replace semantic validation.

## A8. A valid database row is not always a logically consistent row

The enriched validator confirms that historical `source_status` and `present_in_*` values agree. The SQL schema constrains their individual values but does not enforce all valid combinations in one compound constraint. **Lesson:** distinguish persisted-state checks from database-enforced impossible states.

## A9. Test-report fidelity and outcome truth are different questions

The six uploaded historical reports contain 137 passing validator checks and 22 passing formal tests; the original pipeline's five recorded file hashes match the uploaded artifacts. This gives useful traceability and consistency. It does not independently authenticate the first HTTP capture or establish today's vacancy status, and tests are not independent just because they are numerous. **Lesson:** state the narrowest defensible proposition each report establishes.

## A10. Keep the application decision coupled to real-world action

Target 001-A is the strongest documented conventional fit; 001-B offers high technical relevance with location and distributed-systems risks; 001-C is a genuine stretch because the 8+ years language and geographic path remain unresolved. Approval of three targets is a decision milestone, not application submission or an employment result. **Lesson:** establish the selected → prepared → submitted → outcome transitions separately, and do not let perfecting the classifier replace applying.

## A11. Do not let upload packaging rewrite development history

Chat upload systems can add `(1)` or `(2)` suffixes to Python source and artifacts. The original scripts imported unsuffixed module names and were developed in a Windows working directory that was not yet a curated Git checkout. **Lesson:** keep canonical local filenames, source hashes, and proposed repository paths distinguishable.

## A12. Preserve the positive historical findings alongside corrections

The audit independently corroborated the 817/815/814/3/1/818 source identity relationship, the preserved source tables, and the three approved targets' paths through the analysis pool. Correcting overbroad qualification labels is compatible with recognizing that the underlying data engineering and evidence trail are substantive. **Lesson:** being precise about limits strengthens the proof rather than diminishing it.

---

**Addendum status:** These findings are proposed for eventual engineering and public-documentation alignment. No source code or historical report has been altered, and no application action has been taken as part of writing this addendum.
