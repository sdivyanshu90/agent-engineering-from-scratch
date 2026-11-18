# Phase 6 reference rubric

Full credit requires directly demonstrated behavior and a trace that a reviewer
can reproduce. The model-facing registry exposes search, bounded file reads,
patch proposals, fixed test requests, and only explicitly allowlisted read-only
MCP tools. It does not expose approval or patch application. Runtime budgets and
strict argument validation are visible in the trace.

Approval is a human action bound to exact original and replacement content.
Changed source, changed arguments, wrong session, wrong digest, and replay must
reject. A policy hash binds content; reviewer authentication is a separate
deployment responsibility. Test execution is injected, fixed-argv, and fail
closed. A recording fake validates adapter shape but cannot support an isolation
claim. Cancellation or uncertain external completion must remain explicit.

Checkpoint evidence demonstrates a new object resuming a pending call without
repeating the provider's initial decision. It restores full typed state and
budgets, recovers a full snapshot event past an older checkpoint, restores
proposals as unapproved, and reconciles apply by operation ID and file digest.

Benchmark evidence reports each frozen case, split, denominator, and failure.
Protocol fixture success is not live-model task quality. Confidence intervals
do not repair a biased or correlated fixture set. Full credit requires explicit
limitations and a next experiment that could falsify a claim. No score should
be filled in until the student's actual evidence has been graded.
