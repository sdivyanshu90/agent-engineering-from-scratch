# Week 8 examination — context and durable execution (100 points)

Allow 120 minutes. Closed notes for the first 60 minutes; then use only local
fixtures. No live model call is needed. Submit code, numerical traces and
failure analysis. A passing score is 80/100 plus all critical safety gates.

## A. Workflow planning and evaluation — 20 points

For edges `inspect→patch`, `inspect→test`, `patch→verify`, `test→verify`, give
stable topological layers. (5) Write validation for duplicate IDs, missing
parents and cycles that completes before a fake executor sees a node. (7)
Define a fixed two-criterion evaluator record and explain why a candidate change
requires rerunning checks. (8)

## B. Context, provenance and memory — 20 points

Given a policy item (7 estimated units), fresh test result (9), stale memory (4),
and untrusted README (10), with budget 20, a query matching test and README,
show selected IDs/order under the stated policy and identify the preselection
authorization step. (8) Explain why a tool string cannot become a developer
instruction. (5) State one failure of the four-byte token heuristic and one
revision-based freshness check. (7)

## C. Lossy compaction — 15 points

A note says “integration tests skipped; only unit tests passed.” Explain the risk
of prefix truncation and propose a structured compaction record retaining source
IDs/revisions, uncertainty and authority. (10) Contrast item exclusion with
content compaction. (5)

## D. Event journal and checkpoint — 25 points

Two writers read revision 8. Trace a transactional compare-and-append outcome.
(8) A checkpoint at revision 9 is followed by events 10 and 11; specify resume
state. (5) Design owner/session isolation and a checkpoint bound/schema check.
(6) Name what SQLite local atomicity does not cover. (6)

## E. Resume, idempotency and recovery — 20 points

Trace crashes before remote effect, after remote effect but before local receipt,
and after immutable receipt. (9) Define operation-ID digest binding and behavior
for changed payload. (5) Explain why pending is ambiguous and propose a safe
recovery path with/without remote status lookup. (6)

## Critical gates and remediation

Any of these caps the score at 59 until corrected: promoting untrusted text to
developer/system role; executing an invalid partial DAG; accepting stale
checkpoint writes; resetting accumulated budgets on resume; overwriting a
completed receipt; or blindly retrying an ambiguous irreversible effect.

For each missed area, write a minimal counterexample, correct the code or state
machine, and rerun the corresponding Week 8 check. Reattempt the missed section
after 48 hours with altered IDs and revisions. Do not memorize only this exact
fixture.
