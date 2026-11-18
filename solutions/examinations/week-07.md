# Week 7 examination answer guide and scoring rubric

Attempt the questions in the six daily chapter examinations before using this
guide. This is a reference for reasoning and evidence, not an answer to memorize.

## Daily answer checkpoints

- D37: the adaptive call expectation is 1.8 and maximum is 4. Workflows may
  include branches; an agent loop is still bounded by authored state transitions.
- D38: `True` is not an integer argument under exact-type validation. `ééé`
  consumes six UTF-8 bytes. Unknown keys fail before handler invocation.
- D39: the example sends two requests, records one tool observation, and ends
  completed. The observation is data with a call ID, not a new authority grant.
- D40: DAG layers are `{A,B}`, `{C}`, `{D}`. Serial cost is 1.1 seconds;
  ideal read-layer latency is 0.8 seconds. Preflight rejects cycles before effects.
- D41: for 9 input and 2 output tokens at $2/M and $8/M, total usage is 11,
  overshoot is 1 token, and call cost is $0.000034. The response may already
  be billed when the runtime notices the overrun.
- D42: one safe tool failure can become an observation and a new decision;
  unexpected RuntimeError propagates. Retry after uncertain writes needs idempotency.

## Weekly assessment — 100 points

1. **Architecture and state (15):** distinguish fixed workflow routing from
   model-selected actions; draw explicit states and terminal transitions.
2. **Tool contract (15):** accurately implement the closed scalar schema,
   exact boolean/integer behavior, byte bounds, discovery allowlist and write grant.
3. **Loop and trace (20):** demonstrate request, JSON decision, preflight,
   handler call, bounded observation, next state and termination with correlation IDs.
4. **Scheduling (15):** construct layers for a DAG, handle failures and show
   independent read overlap without claiming writes are transactional.
5. **Resource accounting (15):** calculate tokens and Decimal cost, explain
   post-call overshoot and distinguish per-tool timeout from run deadline.
6. **Recovery and evaluation (20):** separate expected errors from programming
   defects; propose safe idempotent recovery; define metrics with denominators and
   assert a safety invariant over traces, not only final text.

Score each criterion proportionally. Passing requires 80/100 and no critical
authority or side-effect error. A critical error includes executing denied or
invalid calls, running malformed batches before preflight, or claiming a hard
spend guarantee from local usage checks.

## Remediation

Below 12/15 in architecture: redraw the D37 state graph and identify who owns
each guard. Below 12/15 in tool contracts: complete D38 boundary fixtures and
prove the side-effect counter stays zero. Below 16/20 in loop tracing: replay
D39 from request history and annotate each event. Below 12/15 in scheduling:
implement D40's DAG, then add a failed parent. Below 12/15 in budgets: redo the
D41 arithmetic with a different reported usage. Below 16/20 in recovery: replay
D42's ValueError and RuntimeError separately and write an idempotency condition.
Reattempt with a new fixture after remediation; do not award points solely for
reproducing these reference numbers.
