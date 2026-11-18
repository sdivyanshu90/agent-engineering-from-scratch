# Phase 6 cumulative technical defense — ForgeAgent

Prerequisite: Weeks 7–12. Attempt independently before the
[reference rubric](../../solutions/examinations/phase-06.md). Present the
artifact and trace from your implementation, not a hypothetical production
system. Suggested effort: two focused days.

## Agent boundary and planning — 20 points

Show closed read/search tools, runtime allowlisting, dependency validation, and
bounded loop behavior (8). Walk a task from initial observation through exact
proposal and verification, showing causal event order and one failure (8).
Explain why plan validity and provider completion do not prove task correctness
(4).

## Authorization and execution — 25 points

Demonstrate exact content-hash binding, wrong-session rejection, stale-file
rejection, and one-use apply (10). Show that the model registry contains no
approval or apply tool (5). Explain the injected executor contract, fixed argv,
no-backend refusal, cancellation uncertainty, and why a subprocess is not a
sandbox (10).

## Context and durability — 20 points

Explain deterministic context selection and lossy compaction (5). Restart a
new agent object from a pending decision snapshot (5). Recover an append versus
checkpoint crash and preserve counters/deadline (5). Reconcile proposal and
apply state by receipt, operation ID, and file hashes; request fresh approval
after restore (5).

## Measurement — 20 points

Report fixed dev and held-out case rows with denominators and split identity
(8). Separate protocol regression from coding quality and fake backend from
real isolation evidence (6). Explain at least one false positive, uncertainty,
and confidence interval limitation (6).

## Limitations and next step — 15 points

Name the actual path/symlink assumptions, unverified executor properties,
provider limitations, and visible-fixture contamination risk (8). Propose a
bounded next experiment with a measurable acceptance result (4). Do not claim
senior experience, production security, or live-model performance absent direct
evidence (3).

Pass80/100 plus all critical invariants: authorization remains human, tool
scope is bounded, test absence fails closed, pending effects are reconciled,
and held-out data is not represented as independent after tuning against it.
