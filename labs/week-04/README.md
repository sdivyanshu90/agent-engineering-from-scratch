# Week 4 labs — an inspectable causal decoder

Prerequisite: pass Week 3's gate. All reference mechanisms use the standard
library and run on CPU. Copy runnable baselines into `learner-work/week-04/`;
they intentionally do not yet meet the contracts. Try before using
[hints](hints.md) or [solutions](../../solutions/labs/week-04/explanation.md).

| Day / global | Starter | Assessed contract |
|---|---|---|
| 1 / D19 | [bpe.py](starter/bpe.py) | `merge(symbols,pair)` nonoverlapping left-to-right; `encode(text,merges)` applies ranked merges; no mutation; join pieces reconstructs input including whitespace/Unicode. |
| 2 / D20 | [projections.py](starter/projections.py) | `project(embedding,position,wq,wk,wv)` adds equal-width vectors, applies row-per-output maps without normalization for this isolated exercise, returns q/k/v; validate shapes and equal query/key widths. |
| 3 / D21 | [attention.py](starter/attention.py) | `attend(q,keys,values)` uses scaled dot scores, stable softmax, aligned weighted payloads; require nonempty equal-width rows; no framework. |
| 4 / D22 | [normalization.py](starter/normalization.py) | `layer_norm(vector,epsilon=1e-5)` uses per-vector population variance, finite inputs and finite positive epsilon; constant vector returns zeros, caller unchanged. |
| 5 / D23 | [loss.py](starter/loss.py) | `loss(logits,target)` stable categorical NLL via log-sum-exp; nonempty finite logits, genuine integer target in bounds; translated scores preserve loss. |
| 6 / D24 | [sampling.py](starter/sampling.py) | `choose(logits,temperature=1,top_k=None,top_p=1,seed=7)` stable temperature, then top-k, then nucleus on surviving normalized probabilities; greedy smallest-index ties, local RNG, explicit domain checks. |

Run `python labs/week-04/checks.py --day 1` against a reference. Append
`--module learner-work/week-04/bpe.py` for your own attempt, selecting the proper
local day/file. Run `python scripts/validate_exercises.py` for all authored
reference contracts. The public checks are necessary, not exhaustive.

Deliver each implementation, an unseen hand trace, two original boundary tests,
a reproduced/fixed defect and a tradeoff explanation. In addition integrate
already-mastered components into one decoder forward pass, one correctly aligned
training step, a three-prefix full/cached equivalence test and explicit context
exhaustion. Do not claim a logit-shape check proves causal correctness. The
weekly/phase defense requires future-perturbation and gradient evidence.
