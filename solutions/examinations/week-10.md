# Week 10 examination — answer key and remediation

## 1. Protocol and contamination — 20 points

An acceptable contract specifies a task, a single `lookup(field)` call, an exact
answer, completed status, zero writes, and bounded steps/tokens. Award 8 points
for measurable independent outcomes. The scripted provider checks runtime
dispatch, parsing, budgets, and tool effects, but not whether a model can select
the right call; 4 points. The flag requires deliberate invocation and the digest
verifies exact fixture bytes, but source visibility means it is not secret or
independent after tuning; 4 points. After a heldout failure, label the result,
return that case to development, and use a new versioned final fixture for a
fresh independent estimate; 4 points.

## 2. Functional and trajectory grading — 20 points

The answer can match, but task completion status is failed; exact tool sequence
fails because of the extra store proposal; policy denies the effect and the
side-effect count is zero; strict case fails. Up to 8 points for separated
verdicts. Answer-only grading misses extra actions, authorization and resource
violations; 4 points. A valid partial order lets two independent reads happen
in either order but requires both before finalization; invalid dependency names
a missing predecessor and checks that no tool handler executes because graph
preflight occurs before dispatch; 8 points.

## 3. Uncertainty and grader calibration — 20 points

Observed rate is 4/4=1. Wilson interval is approximately [0.51,1.00] for z=1.96;
small n leaves substantial uncertainty; 6 points. Judge agreement is 2/4=0.5.
With human pass as positive, one human fail has judge pass (FP=1) and one human
fail judge fail (TN=1); false-accept rate is 1/(1+1)=0.5; 6 points. Repeating
one task measures within-task variability, not independent user/task coverage;
report unique tasks separately. Blind reviewers to judge scores; 4 points.
Supplied labels let learners practice arithmetic, while an actual model grade
requires a live judge call, version record, and calibration evidence; 4 points.

## 4. Telemetry and route economics — 15 points

Safe default record is `{"event":"tool_start","step":2}`; omit tool name and
arguments unless explicitly reviewed; 4 points. Latency: seconds from measured
run wall time; provider tokens: provider-reported count; known cost: USD from
caller-supplied per-million rates, not invoice; 5 points. B is faster and cheaper
on this fixed sample but fails a hard authorization gate, so do not select it
based on utility tradeoff; investigate/fix boundary before comparing. Mention
small n and matched cases; 6 points.

## 5. Security boundary reasoning — 25 points

An indirect injection arrives as untrusted tool output; model may propose a
write, while Registry/host policy checks allowlist and write permission before
handler execution; 6 points. Make handler append a sentinel and assert it stays
empty when write is disallowed; 5 points. Registered means implementation
exists, allowed means task/session scope admits the name, effect-permitted means
read/write policy admits that operation; 5 points. Timeout/cancellation stops
waiting but a remote service may already have accepted the operation; use
idempotency or reconciliation; 5 points. Limitations: source-visible scripted
responses, small case set, no stochastic model, synthetic tools, no real remote
state, or limited attack coverage; any two; 4 points.

## Remediation plan

If protocol scope was weak, rewrite one case with independent expected values.
If trajectory checks collapsed to answer equality, add exact calls and effect
evidence. If the interval or false-accept denominator was wrong, redo the
arithmetic with a confusion table. If telemetry kept payload fields, implement
allowlist-by-omission. If security relied on a phrase test, move the assertion
to the actual handler boundary. Re-attempt missed sections using new examples.
