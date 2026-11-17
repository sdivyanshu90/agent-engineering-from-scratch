# Week 3 mastery examination

Attempt independently; [reference criteria](../../solutions/examinations/week-03.md)
are separate. Suggested one focused day including the coding task; extend as
needed. Use standard-library documentation, not copied/generated solutions.

## Concepts — 20 points

Five questions, four points each: correct distinction (2), causal mechanism (1),
example/limitation (1). Explain: training versus inference; parameter versus
activation; validation versus test; autograd versus finite differences; count-
model generation versus fitting. A definition without a trace earns partial credit.

## Implementation — 30 points

Implement six daily contracts, five points each: normal behavior (2), boundary
behavior (1), independent reasoning/tests (2). Use [the lab contracts](../../labs/week-03/README.md).
For autograd include a+a where a=x*x. For optimization require one update per
unique parameter and fresh graph per training iteration. Importing the reference
into a learner solution earns no independent implementation points.

## Debugging — 20 points

Four cases, five points each: minimal failure (1), first wrong state (2), fix and
regression (2). Diagnose: duplicate-content tasks across splits; updating bias
from residuals after updating weight; assigning instead of accumulating a shared
node gradient; retaining a mutable reference as the best-model checkpoint.

## Mathematics — 20 points

Five derivations, four points each: MSE gradients for x=[1,2], y=[3,5], w=b=0;
parameter count for 2→4→1; x*x+x derivative at x=3; L2 contribution at θ=.5,
λ=.1; mean NLL for `aba` after fitting `abab` over ab with α=1. Define every
symbol and denominator. Numeric answers without mechanism receive at most half.

## Integration and judgment — 10 points

Train the fixed-seed XOR network and preserve its measured loss history (3).
Explain why the full truth-table fit is not a held-out benchmark (2). Compare
bigram held-out NLL with a uniform predictor under identical vocabulary/units (3).
Defend a declared train/validation/test selection boundary (2).

Pass at 80/100 and all critical invariants: no evaluation leakage, all shared
gradient paths counted, parameter update after backward, finite training budget,
and honest metric scope. Retest changed inputs after remediation; do not adjust
rubrics to force a pass or discard unfavorable seeds.
