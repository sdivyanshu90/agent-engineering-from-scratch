# Week 2 mastery examination

Attempt independently; [solutions](../../solutions/examinations/week-02.md) are
separate. Suggested 4–6 focused hours including experiments. Notes and standard-
library docs are permitted; repository reference source and generated solutions
are not permitted for the independent coding portion. Record assistance.

## Conceptual — 20 points

Five questions, four points each: correct distinction (2), mechanism (1), example
or limitation (1).
1. Distinguish transport framing, JSON parsing, schema validation, and authorization.
2. Explain commit/rollback separately from connection closing.
3. Explain concurrency versus parallelism and why async code can block the loop.
4. Explain timeout versus cancellation versus uncertain effect completion.
5. Distinguish vector similarity, probability assignment, and empirical accuracy.

## Coding — 30 points

Implement owner-scoped persistent put/get, strict document-body validation, a
structured concurrent collector, selective retry, and stable softmax. Each is
worth six points: correct normal behavior (2), boundary/failure behavior (2),
independent tests and clear explanation (2). Use only the standard library.

Public contracts: [Week 2 labs](../../labs/week-02/README.md). Add unpublished-to-
yourself-before-coding fixtures by asking a reviewer to choose new filenames,
text, and failure order, or write them before implementing and do not tune them
after seeing output. These are practice checks, not a secure hidden benchmark.

## Debugging — 20 points

Four tasks, five points each: minimal reproduction (1), first wrong state/cause
(2), correction and regression (2).
1. A GET using only identifier returns another owner's row.
2. A “concurrent” collector awaits each operation before starting the next.
3. A retry loop catches cancellation and immediately starts another attempt.
4. A softmax implementation evaluates exp(1000) directly.

## Mathematics and architectural reasoning — 20 points

1. Compute dot, norms, and cosine of [3,4] and [0,5]; state zero-vector policy (4).
2. Derive d/dx (3x+1)² and evaluate at x=2; check numerically (4).
3. Derive softmax shift invariance and compute probabilities for [0,ln2] (4).
4. Derive retry delay sum for four attempts and base 0.1 seconds (4).
5. Critique a claimed 99.2% success rate from three attempts when failures share
   an invalid schema. Explain the failed independence assumption (4).

## Integration — 10 points

Use the application boundary to PUT and GET under two identities; restart
storage and repeat GET. Inject malformed input and a storage operational error.
Verify status, persistence, ownership, and that failures are not success payloads.
Five cases at two points each: executed result (1), explained expected behavior (1).

## Gate

Require 80/100 plus all critical invariants: other-owner reads denied, invalid
input does not write, cancellation propagates, no unbounded retry, shifted finite
softmax normalizes correctly. No score compensates for a critical failure.
Remediate and retest with new data. The cumulative phase exam remains a separate
requirement before starting machine learning.
