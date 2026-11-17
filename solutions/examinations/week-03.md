# Week 3 daily and weekly reference criteria

Each daily examination has five points: conceptual distinction, worked trace,
independent coding, debugging, judgment. Require four with coding mandatory.
Grade the demonstrated mechanism rather than a memorized answer.

## D13

Features are observed inputs; parameters are fitted coefficients. With w=2,b=1,
x=3 gives 7. Partition ten rows as 6/2/2 after copied seeded shuffle; require
coverage, disjoint IDs, no mutation. Duplicate content or target-derived features
can leak despite distinct IDs. Use grouped/time splits when deployment requires
new repositories/future observations rather than random related rows.

## D14

Residuals [-3,-5] give MSE 17, dw=-13 and db=-8. At η=.1, simultaneous new
parameters are 1.3,.8 and loss 1.685. Derive each chain-rule factor and averaging.
Computing bias residuals after changing weight implements a different update.
MSE emphasizes outliers; absolute error is less sensitive but has a corner at zero.
See [regression reference](../labs/week-03/regression.py) only after attempting.

## D15

An affine map includes bias. Given the lesson matrices, hidden preactivation
[-1,3] becomes [0,3] by ReLU and output is [3.5]. Two affine maps without nonlinear
activation collapse into another affine map. A 2→4→1 network has 17 scalar
parameters. A nonsquare test exposes matrix transposition that square fixtures
can hide. ReLU inactive gradients and tanh saturation are distinct limitations.

## D16

A graph records executed dependencies. Topological forward ordering becomes
reverse propagation order. For a=x*x,y=a+a at x=3, a.grad=2 and x.grad=12;
for y=a+a+x it is 13. Each operand contribution uses +=. Visiting nodes once
does not mean dropping duplicate operand roles. Root seed is one. Our reference
resets reachable gradients before backward, unlike accumulation semantics in
some libraries. Reverse mode gets many input derivatives for one scalar loss
with one backward traversal; finite differences require repeated evaluations.

## D17

Forward → scalar loss → backward → data update, then rebuild graph. Example:
θ=.5, data grad=.2, λ=.1 adds .1; rate .05 gives .485. Do not mutate parameters
before their forward-dependent pullbacks finish. Missing biases can leave part
of a model untrained. Validation may choose a checkpoint; test must not choose
hyperparameters. Save copied numerical parameter values. XOR on all four rows
is an optimization/expressivity demonstration, not held-out accuracy evidence.

## D18

With vocabulary ab and α=1, fitted `abab` yields row a counts [1,3] and row b
[2,1]. P(b|a)=.75, P(a|b)=2/3. `aba` mean NLL is -ln(.5)/2≈.34657 and
perplexity √2. Divide by two transitions, not three characters. Uniform NLL is
ln2 on the same vocabulary. Sampling does not update counts; fit accumulates.
The last-character state cannot distinguish longer histories with the same final
character, regardless of how attractive a sampled string looks.

## Weekly grading

Use the fixed 20/30/20/20/10 allocation from the problem. Conceptual points need
a mechanism and limitation. Coding requires independent source and executed
boundary tests; public contracts alone do not prove broader mastery. Debugging
must identify the first wrong state and retain the minimal failure. Numerical
answers above supply expected values but do not replace derivations. All critical
gates remain mandatory even if the total exceeds 80. Preserve every trial in
an experiment instead of selecting a seed after seeing results.
