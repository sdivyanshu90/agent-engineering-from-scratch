# Week 11 examination — service, workers, and operations (100 points)

**Time:** 120 minutes. **Pass:** 80/100 and no critical ownership or recovery
misconception. Closed-book first attempt; then remediate with the listed lesson
and reattempt using changed names and values. Show calculations and state
transitions. Answers are in `solutions/examinations/week-11.md`.

1. **Identity boundary (10 points).** A valid bearer token maps to `owner-A`.
   A request body says `{"owner":"owner-B"}` and names session `s-9`. State
   which owner is used, the correct SQL predicate for reading job `j-3`, and the
   response for a foreign job. Name two values that must not be treated as proof
   of authority.

2. **Async admission (10 points).** Explain why a long handler should not run to
   completion in the POST request. State what 202 guarantees, list the status
   endpoint's responsibility, and describe one risk of an unbounded queue.

3. **Idempotency (10 points).** The client times out after submitting key `k`
   and retries with the same owner/session/key and same text. State the correct
   result. Then the same key is reused with changed text. Explain why it must
   conflict and what idempotency does not guarantee about a remote tool.

4. **Capacity (10 points).** A service has 4 workers and mean handler duration
   10 seconds. Arrival is 0.3 jobs/second. Calculate ideal capacity and `ρ`.
   Estimate in-system jobs with `L=λW` if observed end-to-end time is 18 seconds.
   State one reason p95 can still be high.

5. **Cancellation (10 points).** A running worker receives DELETE on another
   replica. Describe the persisted signal and how the worker observes it. State
   why `cancelled` does not prove a provider call or file write was undone.

6. **Lease fencing (10 points).** Worker A's lease expires; worker B claims the
   same job with a new token. Write the condition required for A's completion to
   be rejected. Explain why periodic renewal does not create exactly-once tool
   effects.

7. **Telemetry privacy (10 points).** Propose a safe event, metric, and span for
   a failed job. Identify two sensitive/high-cardinality fields to exclude and
   explain what an in-memory OTel exporter test proves and does not prove.

8. **Cost and rate limits (10 points).** A bucket has capacity 3 and refills at
   one token every 30 seconds. Explain immediate burst and next token timing. A
   job reports 2,000 input tokens at $0.50/M and 500 output tokens at $2/M;
   calculate estimated cost. State how missing token usage should be represented.

9. **Persistence and Week 8 (10 points).** Distinguish a job state row, a session
   event, and an external operation receipt. A remote effect timed out after it
   might have succeeded; identify the receipt status and safe next step.

10. **Deployment/recovery (10 points).** Describe the reference container's user,
    secret source, persistent SQLite volume, and topology. Give a restart drill
    that proves a running job can be reclaimed. Explain why separate local SQLite
    files on two replicas do not create a shared queue.

## Remediation map

| Question | Revisit |
|---|---|
| 1 | [D61](../../curriculum/week-11/day-01/README.md) |
| 2–5 | [D62](../../curriculum/week-11/day-02/README.md) |
| 6 and 9 | [D63](../../curriculum/week-11/day-03/README.md), Week 8 durable state |
| 7 | [D64](../../curriculum/week-11/day-04/README.md) |
| 4 and 8 | [D65](../../curriculum/week-11/day-05/README.md) |
| 10 | [D66](../../curriculum/week-11/day-06/README.md) |
