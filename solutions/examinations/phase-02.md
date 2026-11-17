# Phase 2 reference defense

Use the examination's fixed 25/30/25/20 allocation. Reference mechanisms live in
[learning](../../forgeagent/learning.py), [autograd](../../forgeagent/autograd.py),
[tokenization](../../forgeagent/tokenization.py) and [decoder](../../forgeagent/transformer.py).
Consult after the independent attempt; importing them does not earn central-
implementation credit. Reusing already-mastered helpers is acceptable where
explicitly permitted by the problem.

Data defense needs disjoint/complete partitions plus duplicate-content awareness.
Regression gradients use simultaneous old parameters; finite differences vary
one coordinate at a time. Shared a=x*x,y=a+a+x has dy/dx=4x+1, equal 13 at 3.
The visited set processes a node once; pullbacks retain both operand contributions.
XOR full-table fitting is not a held-out generalization experiment.

Decoder defense requires explicit dimensions and causal eligibility. A future
perturbation test must cover the full block so wrong normalization axes cannot
hide behind correct attention masking. Tokenizer roundtrip and stable ID/weight
mapping are distinct checks. A one-block implementation may omit optional biases,
dropout and learned norm gains when those choices are documented; it must not
omit attention, residuals, FFN, positional information, output logits or training.

Cross-entropy is logsumexp minus target logit with gradient p−y. Derive shifted
labels from a concrete sequence. Record finite toy training losses and at least
one independent parameter-gradient check. Sampling changes selected output,
whereas caching must preserve logits. A cache belongs to one prefix and parameter
revision; test stale state deliberately, then clear/recompute. Context exhaustion
must reject rather than alias untrained positions.

For each failure case award the published reproduction/cause/regression points.
Do not award correctness to a handwave such as “the library handles it.” Do not
replace missing results with invented measurements or equate a learned toy pattern
with agent task success. Passing this phase permits moving to model integration;
it does not establish that production identity, tools, grounding or sandboxing exist.
