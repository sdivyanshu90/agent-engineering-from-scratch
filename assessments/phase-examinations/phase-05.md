# Phase 5 cumulative defense — evaluated and contained agents

Prerequisite: Weeks 9–10. Attempt independently before
[reference criteria](../../solutions/examinations/phase-05.md). Use local
fixtures only. This assessment joins tool protocol/security with measured agent
behavior; it does not certify a deployed system.

## Protocol, lifecycle, and policy — 25 points

Draw host/client/tool lifecycle and identify trusted capability ownership (5).
Show discovery, allowlist, closed-argument validation, and effect check as
distinct stages (8). Explain one version/protocol fault and one timeout or
cancellation case with uncertain remote outcome (6). Specify a side-effect
counter/idempotency or reconciliation strategy (6).

## Evaluation protocol and trajectory — 25 points

Define task-level expected answer/status, calls, side effects, and budgets (8).
Grade a correct answer reached through a forbidden extra tool proposal (5).
Explain dev vs fixed final split, exact digest, source-visible contamination,
and what a failure does to the claim (7). State scope of scripted provider
evaluation and one class it cannot measure (5).

## Security fault injection — 20 points

Construct an indirect injection trajectory in a tool result and test the actual
write boundary (8). Exercise unknown tool, malformed argument, and invalid
dependency preflight while checking zero effects (6). Explain why a string
heuristic, timeout, or cancellation alone does not prove containment/rollback
(6).

## Measurement, calibration, and decision — 20 points

Report task pass denominator and small-sample interval (5). Present human vs
supplied judge calibration with disagreement and false-accept analysis (5).
Provide p50/p95 latency in seconds and known cost in USD with rate provenance
(5). Make a decision using a hard security gate before quality/latency/cost
tradeoffs, and name a limitation (5).

## Reproducibility and review — 10 points

Freeze protocol/fixture hashes and preserve raw per-case checks without
conversation payloads (5). Run a mutation or independent reviewer exercise
that can expose a weak grader (5).

**Pass:** 80/100 plus critical boundaries: no unauthorized handler invocation,
no side effect on invalid preflight, exact split disclosure, units/provenance on
metrics, and no live-model or hidden-set claims from scripted fixtures.
