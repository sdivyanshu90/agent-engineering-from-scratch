# Phase 4 reference defense

## Runtime and tool boundary

Use strict closed JSON schemas, allowlists and effect policy before handlers.
Compute the complete dependency plan before any call. Reads can share a layer
only when explicitly safe; writes serialize. Failed parents block descendants.
Cancellation propagates and does not prove an external call did not complete.
Resume validates run identity and snapshot structure, then preserves accumulated
steps, tool calls, tokens, costs and absolute deadline.

## Context and evaluator quality

Context records preserve role, provenance, trust, revision and creation/expiry.
Authorization filters sources before retrieval; selection then applies a
versioned relevance policy and budget. Reserve policy through trusted caller
inputs; reject untrusted system/developer records. Evaluator results bind named
criteria and evidence to the exact candidate digest/rubric version. Independent
evidence comes from distinct methods or sources, not simply multiple prompts.

## Durable state and race safety

Scope all journal queries and primary keys by owner/session. In one SQLite write
transaction compare current revision, increment and append event. A stale writer
conflicts, rereads and reconciles. Checkpoints contain bounded finite JSON and a
schema version; resume loads snapshot plus ordered later events. SQLite controls
only its local file. Filesystem permissions, encryption, backup, retention and
database-level tenant isolation require deployment decisions.

## Long-running effects and defense

Canonical payload digest binds operation ID. Same key plus same digest returns
the current status; changed payload conflicts. Completed receipts are immutable.
Before-effect crash may leave safe-to-dispatch intent, after-effect/before-receipt
is ambiguous, and after-receipt replay returns the same local receipt. Query a
remote idempotency/status API when documented; otherwise surface unknown and
reconcile. An absolute deadline and accumulated budgets prevent restart resets.
No local SQLite transaction proves exactly-once remote execution.

Critical-gate rationale: role promotion and prevalidation are authorization
boundaries; revision conflicts prevent lost updates; persisted budgets prevent
restart evasion; immutable receipt and unknown state prevent invented certainty.
