# Week 8 labs — context and durable work

Copy `starter/` into `learner-work/week-08/`. Implement each contract without
importing the reference module. Start with `python labs/week-08/checks.py --day 1`;
pass `--module learner-work/week-08/workflow.py` (or the named file for the day).
The contract checks boundaries and crash states, not production readiness.

| Day | Starter/API | Required contract |
|---|---|---|
| D43 | `workflow.py`: `plan(steps)`, `verify(steps,layers)` | deterministic topological batches; reject duplicate IDs, missing edges, cycles before any side effect; verify exact coverage and dependencies |
| D44 | Extend `workflow.py`: `evaluate(candidate,evidence)` | bounded, explicit evaluator result that distinguishes accepted/revise/reject and records evidence; avoid self-graded hidden quality claims |
| D45 | `context.py`: `estimate_tokens`, `select` | item role/provenance/trust/revision/time/TTL, stale removal, stable relevance order, budget and reserved policy context |
| D46 | `context.py`: `compact` | visibly lossy bounded text plus source IDs/revisions; summary does not inherit source authority; demonstrate stale-memory rejection |
| D47 | `journal.py`: append/checkpoint | owner/session event scope, monotonically increasing revision, compare-and-swap append and checkpoint, JSON validation |
| D48 | `journal.py`: resume/operation ledger | restore exact counters/state, expose event tail, bind operation ID to canonical payload digest, preserve pending/unknown status after simulated crashes |

Add your own concurrent revision race, other-owner read, expired-memory, cycle,
budget edge, crash-before-effect and effect-before-result fixtures. A pending
operation is ambiguous after a crash; do not blindly repeat an irreversible
external call. Read [hints](hints.md), then compare with [reference reasoning](../../solutions/labs/week-08/explanation.md).
