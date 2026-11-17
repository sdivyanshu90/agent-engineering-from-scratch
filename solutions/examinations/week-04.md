# Week 4 reference criteria

Daily exams each have five points: correct explanation, worked trace, independent
implementation, debugging evidence, and defensible design alternative. Require
four including coding. The weekly 20/30/20/20/10 rubric is fixed before results.

## D19

Text/code points differ from bytes, pieces, IDs and embedding rows. `aaa` under
(a,a) becomes [aa,a], preserving reconstruction. Apply merge ranks sequentially;
lexical reordering changes the tokenizer. ID 1 selects row 1, not a scaled version
of row 0. Vocabulary and weights must remain compatible. Toy counts cannot be
reported as a hosted model's billing units.

## D20

Add content and position vectors, then project through separate matrices.
Fixture h=[1,1], q=[1,2], k=[1,1], v=[2,0]. The isolated exercise omits normalization;
full decoder includes it. Q/K widths must agree; payload width depends on output
layout. Three d×d maps have 3d² parameters. Aliased rows/matrices can make roles
identical accidentally even though shapes pass.

## D21

For q=[1], keys [0],[1], values [2],[6], output is (2+6e)/(1+e)≈4.92423.
With only first location eligible it is 2. Causal eligibility is before score
normalization. Masking after softmax without renormalization loses unit mass;
future keys can affect allowed weights even if future values are zeroed. Heads
are distinct projected subspaces, not agents or proven interpretable functions.

## D22

For [1,3], mean=2,var=1, normalized values ±1/sqrt(1.00001). Population denominator
is d. Constant vectors normalize to zeros. Wrong temporal axes can leak future
content outside attention. Residual derivative is identity plus sublayer Jacobian.
Toy parameter count is 2Vd+Cd+8d²=176 at V=3,C=6,d=4. Gains, offsets and biases
are omitted explicitly; adding them changes counts and tests.

## D23

Inputs exclude last token, labels exclude first. At position i predict original
position i+1. Loss is logsumexp(z)−z_target, derivative p−one_hot. [1000,1001],
target 1 gives log(1+exp(-1))≈.31326, gradients [.26894,-.26894]. Training must
build a fresh graph and update only after backward. Low loss with current-token
labels or future leakage measures the wrong task.

## D24

T>0 divides logits before normalization; T=0 is greedy with smallest-index tie.
Reference order: top-k then normalize survivors then top-p prefix then sample.
[.6,.3,.1] at p=.8 keeps first two, renormalized [2/3,1/3]. Cache payload estimate
2Lndb counts numeric key/value elements, not Python object overhead. Cached/full
logits must agree under identical parameters/prefix/positions. Reusing after a
model or prefix edit is invalid even when output shapes remain correct.

## Weekly integration scoring

Award executed behavior with explanations, not predicted reports masquerading
as observed results. Require the future perturbation invariant across the whole
decoder, stable loss at large translated logits, and finite context/generation
limits. Toy pattern training demonstrates mechanics only. Do not waive a critical
boundary because the arithmetic score exceeds 80.
