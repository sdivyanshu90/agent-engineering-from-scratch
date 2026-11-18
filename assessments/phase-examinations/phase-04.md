# Phase 4 cumulative defense — bounded agents and durable work

Prerequisite: Weeks 7–8. Attempt without browsing first, then implement against
local fake providers, tools and SQLite fixtures. This is cumulative across
runtime dispatch, context engineering and recovery; no paid service is required.
Allow one or two focused days. Passing requires 80/100 and every critical gate.

## Runtime and tool boundary — 25 points

Build a typed call with a dependency edge and closed argument schema (6). Prove
invalid tool, malformed JSON, denied write and cycle fail before effect (7).
Trace parallel reads versus serialized writes, failing-parent propagation,
cancellation and bounded outcomes (7). Preserve model identity, counters and
known costs across a valid resume (5).

## Context and evaluator quality — 20 points

Define evidence role, provenance, trust, revision and freshness (6). Select
context under a budget while reserving authoritative policy and excluding stale
or unauthorized records (6). Give one fixed evaluator rubric with candidate
digest and evidence pointers; explain why identical multi-agent reviewers do not
provide independent confidence (8).

## Durable state and race safety — 25 points

Implement owner/session event scope, atomic optimistic append and conflict
handling (8). Checkpoint bounded versioned JSON against a revision; restore
state and ordered event tail (7). Run two competing writers and a cross-owner
isolation check (5). Distinguish SQLite local atomicity from remote effects and
identify deployment controls outside the journal (5).

## Long-running effects and defense — 30 points

Bind operation IDs to canonical payload digests and preserve immutable receipts
(8). Reproduce crashes before effect, after effect/before receipt and after
receipt (9). Design safe handling for pending/unknown with and without remote
idempotency/status lookup (7). Explain timeout, cancellation, absolute deadline,
budget persistence and why exactly-once is not established locally (6).

Critical gates: untrusted context never gains system/developer role; invalid
graphs never partially execute; authorization is checked before dispatch;
checkpoint conflicts do not overwrite newer state; resumed budgets do not reset;
completed receipts cannot change; ambiguous irreversible effects are not blindly
retried. Any gate failure caps the score at 59 until corrected and retested.

## Defense packet

Submit source, test output, a state-transition diagram, one crashed-worker trace,
and a short limitations section. Mark fixture results as local observations;
do not claim provider behavior, exactly-once effects or model quality without
external evidence. Remediate missed gates with altered owners, IDs and payloads,
then repeat after 48 hours.
