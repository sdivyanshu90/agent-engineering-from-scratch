# Phase 3 cumulative defense — reliable grounded application

Prerequisite: Weeks5–6. Attempt independently before
[reference criteria](../../solutions/examinations/phase-03.md). Allow one or two
focused days. Use local fixtures and FakeProvider; no paid inference required.

## Application boundary — 25 points

Construct typed role-separated/versioned requests, strict output and usage (10).
Implement complete normalized stream assembly with truncation/cancellation
failures (10). Show finite classified recovery under one deadline (5). Central
mechanisms must be independently implemented from their contracts.

## Evidence and retrieval — 30 points

Ingest a fixed authorized document snapshot into revision-aware chunks (5),
implement postings/BM25 and exact cosine baselines with stated conventions (10),
fuse/rerank while preserving IDs and candidate limits (5), and compute retrieval
metrics from independent graded judgments (10). Authored fixture vectors must
not be described as pretrained semantic evaluation.

## Grounded answer integration — 25 points

Run retrieval→provider quote selection→strict support verification (10). Deny
invented ID, stale revision, altered quotation and extra uncited claim (10).
Abstain without calling the model on absent evidence and grade that separately
from vacuous citation validity (5). Use only selected authorized evidence in prompts.

## Measurement and defense — 20 points

Report quality denominators, known/unknown usage and hypothetical cost units (5).
Preserve visible benchmark rows and explain why they are not held out (5).
Reproduce candidate-recall loss and a real-source false-relevance case (5).
Present a diagram separating model/transport/schema/evidence/authorization and
identify production limitations (5).

Pass80/100 plus all critical boundaries: no source role promotion, no partial
success, no unbounded retries, no unauthorized evidence exposure, no unsupported
answer text and no invented live/held-out measurements. Correct and retest
changed fixtures after delay. This gate measures application foundations; it
is not yet a durable or secure coding-agent implementation.
