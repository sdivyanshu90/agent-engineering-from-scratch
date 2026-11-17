# Week 4 mastery examination

Attempt independently before [answers](../../solutions/examinations/week-04.md).
Suggested one focused day plus remediation. Standard-library docs are allowed;
copying a prebuilt transformer or reference source is not independent evidence.

## Concepts — 20 points

Five questions, four points each: correct distinction (2), mechanism (1), example
or limitation (1). Explain pieces/IDs/embeddings; Q/K/V roles; causal versus
padding mask; teacher forcing versus generation; KV/prompt/response/application
memory caches. Avoid inferring undocumented provider behavior.

## Coding — 30 points

Implement six [daily contracts](../../labs/week-04/README.md), five points each:
normal output (2), boundary/domain correctness (1), independent explanation/tests
(2). Test nonoverlap, nonsquare maps, stable attention, constant normalization,
translated-logit loss, and filter support. No external framework may hide the
assessed mechanism. Already-mastered Value objects may support later integration.

## Debugging — 20 points

Four cases, five points each: minimal failure (1), first wrong state (2), fix and
regression (2). Diagnose overlapping `aaa` merges; masking after softmax; normalizing
across time instead of features; cache reuse after model/prefix mutation. Show
numeric evidence, not merely changed generated text.

## Mathematics — 20 points

Five derivations, four points each: scaled two-key attention fixture from D21;
normalization [1,3] with epsilon; parameter count 2Vd+Cd+8d² at V=3,C=6,d=4;
cross-entropy gradient p−y; nucleus support for [.6,.3,.1] at p=.8 and tensor
cache estimate 2Lndb. State axes, symbols, units, and assumptions.

## Integrated decoder defense — 10 points

Execute one full forward pass and one finite training sequence with shifted
labels (3). Demonstrate future-token perturbation invariance (2), three-prefix
cached/full numeric equivalence (3), and context-limit termination (2). Label
training metrics as toy optimization evidence, not application quality.

Pass at 80/100 plus no critical failures: lossy reconstruction, future leakage,
unstable valid-input loss, wrong target alignment, stale cache described as valid,
or unbounded generation. Preserve failed evidence and retest changed inputs.
