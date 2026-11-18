# Week 10 mastery examination — agent evaluation and boundaries

Attempt before [answer key and remediation](../../solutions/examinations/week-10.md).
Suggested one focused day. Use only local fixtures; no paid inference or network
service is required. Explain assumptions and units in every result.

## 1. Protocol and contamination — 20 points

Define a task-level contract for an agent that reads a record and reports one
field. Include expected calls, answer, status, side effects, and a budget (8).
Explain what a fixed scripted provider does and does not measure (4). The
heldout fixture is source-visible; explain what its final flag and SHA-256 digest
establish and what they cannot establish (4). Describe how to handle a heldout
failure before making a new final claim (4).

## 2. Functional and trajectory grading — 20 points

Expected trajectory is `[lookup]`, answer “Mira,” no writes, two steps maximum.
Observed trace calls lookup then attempts denied store, answer “Mira,” status
failed, effects 0. Give completion, tool-sequence, policy, and overall strict
case verdicts (8). Explain why answer-only grading is insufficient (4). Design
one partial-order contract for two independent reads and one invalid-dependency
case that checks preflight atomicity (8).

## 3. Uncertainty and grader calibration — 20 points

Compute pass rate and interpret a Wilson 95% interval for 4/4; explain why the
lower limit is not 1 (6). Human labels are `[1,1,0,0]`; supplied judge scores
are `[1,0,1,0]`. Calculate exact agreement and binary false-accept rate (6).
Explain why repeated calls to the same task are not independent task samples
and name one practice to reduce reviewer anchoring (4). Distinguish supplied
scores in a calibration exercise from an actual model-graded result (4).

## 4. Telemetry and route economics — 15 points

An event has `event=tool_start`, `step=2`, `tool=send_email`, and
`arguments={...}`. Give a safe default exported record (4). State units and
provenance for p50/p95 latency, provider token counts, and known cost (5). Route
A passes 9/10 at p50 0.8 s and $0.010; B passes 8/10 at p50 0.5 s and $0.006,
but B fails a hard authorization gate. Give a defensible decision (6).

## 5. Security boundary reasoning — 25 points

Trace how an injected tool observation can result in a proposed write and name
where code enforces denial (6). Give one test that proves handler non-invocation
rather than checking injection wording (5). Explain the difference between
registered, allowed, and effect-permitted tools (5). State why timeout or
cancellation cannot establish remote rollback (5). Name two limitations of the
fixed benchmark's security evidence (4).

**Pass:** 80/100 and full credit on the security invariant that denied or
unauthorized writes have zero observed side effect. Repair any missed concept
before the Phase 5 cumulative defense.
