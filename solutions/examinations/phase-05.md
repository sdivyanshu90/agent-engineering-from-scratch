# Phase 5 defense — reference criteria

## Protocol, lifecycle, and policy — 25 points

Full credit draws lifecycle ownership in host code, then distinguishes discovery
from enforcement. A valid tool requires registration, task/session allowlisting,
schema-valid closed arguments, and effect permission before handler entry. A
timeout or cancellation bounds waiting but may leave external acceptance
uncertain. A sound design records effects, uses idempotency keys, or queries
remote status before retrying.

## Evaluation protocol and trajectory — 25 points

Expected outcome includes answer/status, call trace, effects, and resource
limits. If an answer is right but an unapproved call was proposed, answer quality
may pass while trajectory/policy fails and strict task case fails. Dev cases are
for iteration; final cases are source-visible and hash-frozen but not secret.
After tuning on final, call it development evidence and construct a new versioned
final split. Scripted providers measure runtime orchestration and contract
behavior, not stochastic model choice or broad semantic quality.

## Security fault injection — 20 points

Place malicious instructions in a tool observation, script a proposed write,
and assert the real handler's effect counter stays zero because runtime policy
denies before invocation. Unknown tools, malformed arguments, and invalid
dependency graphs must reject before effects. A text denylist misses paraphrases;
timeouts do not guarantee that remote work stopped; cancellation does not roll
back durable changes.

## Measurement, calibration, and decision — 20 points

Show n, pass count, rate, and interval; note task sampling assumptions. Preserve
human and judge scores, disagreement direction, false accepts, and rubric
version. Latency is seconds from measured wall clock; cost is USD only under
declared caller-supplied rates. First enforce security invariants. Only compare
quality, latency, and cost across matched workloads when gates pass. State at
least one missing slice or environmental limitation.

## Reproducibility and review — 10 points

Record protocol version, fixture digest, command, exact case rows, and reviewed
redacted data fields. A useful mutation test changes one expected property or
creates a misleading successful answer with an unsafe trajectory. Independent
review should challenge case relevance and grader correctness, not simply rerun
the same assertions.

## Remediation

Repair one missing authorization gate and prove handler non-invocation. Replace
answer-only scoring with trajectory/effect checks. Recompute statistics with
the correct denominator and units. If final data was tuned on, stop making an
independent claim and version a fresh final set. Re-present the changed evidence
to a reviewer before claiming the phase complete.
