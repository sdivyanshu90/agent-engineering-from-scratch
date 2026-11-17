# Phase 1 cumulative examination — foundations

Build independently before opening [the reference defense](../../solutions/examinations/phase-01.md).
Suggested one or two focused days; increase the time for a complete beginner.
Use a fresh work directory and a temporary database. Standard-library docs and
problem contracts are allowed; copied repository source does not demonstrate
independent implementation. Fix grading criteria before executing.

## System task — 40 points

Build a local document ingestion/search service without a framework. A request
contains an authenticated identity, a document ID, and UTF-8 JSON text. Validate
shape and bounds, persist under the owner/id pair, then allow that owner to
retrieve text and count an exact normalized query token. Search must return
reproducible path/identifier and count evidence. Do not execute document text.
A maintained transport is not required; an in-process async dispatch interface
with simulated request messages is sufficient for assessing application behavior.

Points: contracts and diagrams 5; strict parsing/validation 5; transactional
persistence 10; ownership and pure search integration 10; meaningful test cases
and non-success failures 10. Empty documents are valid; absent documents are distinct.

## Failure drill — 25 points

Demonstrate five controlled failures: malformed JSON, other-owner lookup,
transaction exception before commit, operation timeout, caller cancellation.
For each show expected behavior (1), executed result (2), mechanism/limitation
(2). Explain which operations may still complete after the caller stops waiting.
No live remote tools, paid models, or destructive shell commands are necessary.

## Mathematical defense — 25 points

1. Compute a 2×2 matrix-vector product and cosine, checking dimensions (5).
2. Derive a composite scalar derivative and compare central differences over
   three h values, explaining numerical error (5).
3. Show square-loss descent at η=.1 and explain nonconvergence at η=1 (5).
4. Derive and test stable softmax translation invariance (5).
5. Explain conditional versus independent retry failure with a shared-cause
   example and a numeric calculation (5).

## Engineering defense — 10 points

Present a five-minute explanation of state ownership, effect boundaries,
thread/event-loop interactions, and why the local service is not production-
secure. Show an inspectable diff and one measurement with units and assumptions.
Award 2 points per item with concrete evidence.

## Pass criteria

At least 80/100 and no critical failure: cross-owner leakage, SQL interpolation,
unbounded retry, swallowed cancellation, or fabricated validation evidence.
Reconstruct the weak mechanism and repeat with changed data after a delay.
Passing this exam demonstrates foundations for the next phase, not professional
production experience or readiness to expose the learning server publicly.
