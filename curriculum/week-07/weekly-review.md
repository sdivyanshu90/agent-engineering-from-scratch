# Week 7 review and remediation

Closed book, draw one state machine from task to terminal status. Then trace one
model call proposal through JSON parsing, permission and schema validation,
handler execution, bounded observation, next decision and final answer. Include
the call ID at every transition and mark tool output as untrusted data.

Re-derive the D37 adaptive expectation and maximum, D38 UTF-8 byte length and
exact bool/integer case, D40 topological layers and latency, and D41 token/cost
overshoot. For each derivation, write units and assumptions before checking the
reference. Compare a normal tool exception with an unexpected programming bug;
explain why they have different recovery paths.

Run all six [public lab contracts](../../labs/week-07/README.md) and the runtime
integration tests. Add one new input per lab and prove invalid preflight input
causes zero handler calls. For concurrency, use a barrier or active counter.
For cancellation, preserve the terminal trace while confirming cancellation
still propagates to the caller.

Complete the [weekly assessment](../../assessments/weekly/week-07.md) before
checking the [answer guide](../../solutions/examinations/week-07.md). Remediate
the first failed boundary: state ownership, tool allowlist, exact schema type,
call correlation, dependency edge, budget reconciliation, cancellation, or
idempotency. Reattempt with changed values; a memorized example is not evidence
of transfer. In one week, reconstruct one safe retry rule and one case where a
locally bounded run can still incur external cost.
