# Phase 2 cumulative examination — learned computation

Build and defend mechanisms from Weeks 3–4. Attempt before consulting
[reference criteria](../../solutions/examinations/phase-02.md). Suggested two
focused days plus remediation. Use tiny CPU fixtures; no GPU, paid model,
framework-generated transformer, or externally trained artifact is necessary.

## Data and learning mechanisms — 25 points

Create a ten-example regression dataset with provenance IDs and fixed partitions.
Derive one MSE update, fit a line with finite steps, and report train/validation
results without consuming test for tuning (10). Implement two-operation reverse
mode, demonstrate shared operands/intermediates, and verify gradients numerically
(10). Explain a fitted XOR example's limited evaluation scope (5).

## Decoder architecture — 30 points

Implement or reconstruct a one-block decoder from explicit prior components:
embedding/position handling (5), projected causal multi-head mixing (10), residual
and per-token normalization/FFN (10), vocabulary logits and correct dimensions (5).
Document omissions such as biases or normalization gains rather than pretending
a framework supplies them. Correct shape alone earns no causality credit.

## Training and inference — 25 points

Derive categorical NLL and p−y (5). Train with shifted labels and a finite budget,
preserving measured losses and gradient evidence (5). Implement documented
sampling support/tie rules (5). Demonstrate full/cached equivalence over three
prefixes (5) and explicit context exhaustion plus stale-cache failure (5).

## Failure and architectural defense — 20 points

Reproduce four faults, five points each: evaluation leakage, lost shared gradient,
future-token leakage, and stale-cache reuse. For each provide minimal input (1),
first wrong state/cause (2), corrected regression evidence (2). Explain how a
fixed tokenizer/model version and cache owner/prefix are part of the contract.

Pass at 80/100 with all four failure boundaries corrected. A fabricated result,
use of held-out answers for tuning, copied central mechanism, or claim that toy
loss proves production agent capability is a critical failure. Repeat changed
fixtures after a delay. This gate establishes model-internals foundations;
application integration, tools, durable execution and security remain separate work.
