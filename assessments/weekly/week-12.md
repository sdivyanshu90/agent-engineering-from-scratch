# Week 12 mastery examination — ForgeAgent capstone

Attempt independently before [reference criteria](../../solutions/examinations/week-12.md).
Use only the local deterministic fixtures. No live provider or execution backend
is required. Suggested effort: one focused day.

## System implementation — 30 points

Implement bounded repository search/read and report path, line, and content
revision (8). Build a validated plan and trajectory with causal event ordering
(7). Propose a patch bound to before/after digests and keep approval outside the
provider tool registry (8). Route fixed tests only through an injected backend
and refuse without one (7).

## State and recovery — 20 points

Select/compact context with explicit lossy provenance and a stated token
heuristic (5). Persist a complete runtime snapshot, including pending decisions
and counters (5). Demonstrate restart in a new session object without replaying
the initial provider call (5). Restore a patch proposal unapproved and
reconcile pending apply from operation status and before/after hashes (5).

## Verification and security — 20 points

Reject wrong session, changed source, altered replacement, and repeated apply
(8). Demonstrate that a test result is tied to the post-apply revision and that
a backend timeout remains uncertain (6). Explain path/symlink, test execution,
MCP output, context, and log disclosure boundaries (6).

## Evaluation and defense — 30 points

Run all fixed development cases and preserve per-case results (8). Run the
frozen held-out cases and report the exact denominator (5). Separate protocol
integration, task success, and safe refusal measures (5). Defend one failure,
one uncertainty, one tradeoff, and one known limitation using a real trace (7).
Offer a concrete next experiment without claiming unmeasured model quality (5).

Pass80/100 and all critical boundaries: no model-accessible approval tool, no
general shell, no host execution fallback, no stale or replayed write, no
provider-only claim of passing tests, and no false statement that a scripted
fixture proves autonomous coding quality. Remediate failed invariants with new
regression cases and preserve the original failure report.
