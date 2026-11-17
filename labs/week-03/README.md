# Week 3 labs — from data to a trainable neural network

Prerequisite: pass the Phase 1 examination. Work independently under
`learner-work/week-03/`; copy the runnable baseline for the selected day. Baseline
results are intentionally incomplete. Use [graduated hints](hints.md) after a
written attempt; [reference reasoning](../../solutions/labs/week-03/explanation.md)
is separate. Ordinary repository checks run references, not your unfinished work.

| Day | Starter and assessed contract |
|---|---|
| 1 / D13 | [partition.py](starter/partition.py): `partition(rows,seed=7)` on records with identifier; require ≥5 unique IDs; shuffle a copy with local Random, split floor(.6n)/floor(.8n), output train/validation/test lists; deterministic for fixed order/seed, no mutation. |
| 2 / D14 | [regression.py](starter/regression.py): `step(xs,ys,w,b,rate=.01)` returns new weight/bias using simultaneous full-batch MSE gradients; reject empty/mismatched lists, nonpositive/non-finite rate; no input mutation. |
| 3 / D15 | [network.py](starter/network.py): `forward(x,w1,b1,w2,b2)` uses row-per-output affine maps and ReLU hidden units, returns output list, validates both shapes/bias lengths, leaves inputs unchanged. |
| 4 / D16 | [scalar.py](starter/scalar.py): `Scalar(data)` supports +,* with scalars or Scalar; fields data/grad; backward computes reverse-mode derivatives, sums shared paths, resets reachable gradients before each call. |
| 5 / D17 | [optimizer.py](starter/optimizer.py): `update(parameters,rate)` subtracts rate*grad from each distinct parameter once, keeps grads available, rejects duplicate identities and nonpositive/non-finite rate before mutation. Integrate into a finite fresh-graph MLP training loop. |
| 6 / D18 | [bigram.py](starter/bigram.py): `distribution(text,vocabulary,current,alpha=1)` adds alpha to every possible following-symbol count, fits adjacent pairs, returns current row probabilities; reject unknown symbols/current and invalid alpha. |

Run `python labs/week-03/checks.py --day 1` for a reference contract. Append
`--module learner-work/week-03/partition.py` to assess your attempt, changing day
and filename as needed. Run `python scripts/validate_exercises.py` for all authored
reference contracts. These public checks are a minimum, not evidence of all concepts.

Deliver each source file, its hand-traced execution, at least two original boundary
tests, one intentionally reproduced and corrected defect, and the day's examination.
For Day 4 include shared operand/intermediate and numerical-gradient cases.
For Day 5 report architecture, seed, rate, steps, loss and scope: fitting all XOR
rows demonstrates optimization, not held-out generalization. For Day 6 include
NLL by hand and read-only inference evidence. No GPU, external data download,
paid service, or third-party training framework is required.
