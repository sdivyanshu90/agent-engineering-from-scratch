# Week 2 — Review, integration, and retention

Reconstruct before rereading. Trace an authenticated PUT from bytes through
validation, storage, commit, and response. Draw an owner-mismatched GET and a
malformed JSON PUT; explain why neither can read/write another owner's data.
Reopen the database to verify persistence, and inject a failure before commit
to verify rollback. Then explain why task cancellation cannot reliably undo
an already-running worker write.

Rebuild the concurrent collector and selective retry from contracts. Use events
to prove task overlap and cleanup; use injected sleep to inspect backoff. Rebuild
dot, cosine, a matrix product, central differences, and stable softmax. Derive
an analytic chain-rule example and compare with the numerical check.

Take [the weekly exam](../../assessments/weekly/week-02.md). After corrections,
take the [cumulative Phase 1 exam](../../assessments/phase-examinations/phase-01.md).
Record independent evidence in [progress](../../PROGRESS_TRACKER.md).

## Targeted remediation

| Observed gap | Reconstruction task |
|---|---|
| Valid JSON mistaken for authorized action | Draw parser/schema/identity/ownership as four separate checks |
| Lost or partial state | Open a fresh file DB and prove commit/rollback on two rows |
| Async handler stalls | Run a heartbeat beside blocking work, then move I/O to a worker |
| Cancellation ignored | Event-synchronize start, cancel, prove cleanup and no retry |
| Wrong vector result | Annotate dimensions and multiply coordinates by hand |
| Cosine interpreted as probability | Construct same-feature documents with different truth/relevance |
| Chain rule memorized only | Expand a composite square and derive both ways |
| Softmax overflow | Derive maximum-shift invariance and test large translated scores |

Retry with a changed fixture after remediation. Do not lower criteria or count
an answer copied from a solution as independent evidence. One week later,
reconstruct one software mechanism and one mathematical mechanism without notes.
