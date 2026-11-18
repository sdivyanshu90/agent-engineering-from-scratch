# Week 8 — Context engineering and durable execution

Prerequisite: [Week 7 agent-runtime gate](../../assessments/weekly/week-07.md).
This week connects explicit planning and bounded agent loops to context
provenance, memory lifecycle, durable snapshots and honest recovery from
uncertain side effects.

| Day | Chapter | Practice focus |
|---|---|---|
| D43 | [DAG routing and verification](day-01/README.md) | Validate full graph before execution; deterministic layers |
| D44 | [Reflection and evaluator loops](day-02/README.md) | Fixed rubric, evidence, bounded revisions, useful delegation |
| D45 | [Provenance and context budgets](day-03/README.md) | Trust roles, freshness, deterministic selection |
| D46 | [Compaction and memory](day-04/README.md) | Lossy summaries, revision references, stale-memory rejection |
| D47 | [Events and checkpoints](day-05/README.md) | Owner/session scopes, SQLite CAS, snapshot plus tail |
| D48 | [Resume and idempotency](day-06/README.md) | Preserve budgets; reconcile pending/unknown operations |

Use the [labs](../../labs/week-08/README.md), [weekly review](weekly-review.md),
[100-point exam](../../assessments/weekly/week-08.md) and
[Phase 4 cumulative defense](../../assessments/phase-examinations/phase-04.md).
Allow 42–54 hours. Local code uses Python's standard library and fixtures; it
does not require a paid model or remote service. Token counts are character-based
estimates, and remote exactly-once effects are not claimed.
