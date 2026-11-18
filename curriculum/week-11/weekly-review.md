# Week 11 review — authenticated, bounded, recoverable service

Review each invariant without opening the reference implementation. Your service
has an HTTP identity boundary, a durable admission boundary, worker concurrency,
queue lease and recovery rules, telemetry, rate/cost controls, and deployment
storage. These layers compose; passing one does not imply another is correct.

## Retrieval prompts

1. Starting from `Authorization: Bearer ...`, trace how the owner becomes trusted
   and where SQL must repeat the ownership predicate.
2. Explain why a session ID or random job ID cannot serve as authorization.
3. State the meaning of HTTP 202 and the fields a status response should omit.
4. Contrast rate tokens, owner pending quota, worker count, input size, and
   agent token budget.
5. Draw all legal job states and identify which transitions are terminal.
6. Explain lease expiry, heartbeat renewal, and why a fencing token is required
   for late completion.
7. Distinguish job recovery from replaying an external effect with Week 8's
   pending/unknown receipt.
8. Choose one event, counter, histogram, and trace span. Name their cardinality
   and privacy constraints.
9. Derive `L=λW`, capacity `c/S`, bucket refill, and estimated per-job cost.
10. Describe the single-host SQLite container topology, persistent volume, secret
    source, and limitations of multiple replicas.

## Practical review

Run the six public lab checks and the optional service integration tests. Then
inspect the service with a fake `run_handler`; do not add provider credentials.
Submit a trace from accepted request to terminal result that includes the trusted
owner label, job transition, lease token generation (redacted in ordinary logs),
and response status. Explain which parts of that trace are persisted and which
are in-memory telemetry. Calculate an overload example using your measured
handler mean and p95, then explain why p95 per replica should not be averaged.

## Mastery checklist

- Every API read/cancel/list operation derives the owner from the configured
  credential and scopes database access by owner.
- Repeated idempotency keys with matching input return the same job; changed
  input conflicts.
- Worker and pending bounds are enforced at their actual shared/local scope.
- Cancellation is observable; it does not claim to reverse a remote effect.
- Expired jobs are reclaimable, stale lease tokens cannot complete them, and
  service shutdown does not falsely mark them user-cancelled.
- Logs, metrics, and spans exclude credentials and user text; labels remain
  finite.
- Missing token usage is unknown, not zero. Cost is labeled as an estimate.
- Deployment docs identify the persistent data path and single-host boundary.

Use the [weekly examination](../../assessments/weekly/week-11.md) and compare
your reasoning with the [answer key](../../solutions/examinations/week-11.md).
