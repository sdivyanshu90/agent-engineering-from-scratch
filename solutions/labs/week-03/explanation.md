# Week 3 reference decisions

Attempt independently before following these source links. Thin solution modules
reuse tested implementations, so the evolving project and the references cannot
drift into different policies. Importing a reference into an assessed submission
does not demonstrate independent implementation.

1. [Partitioning](../../../forgeagent/learning.py): local seeded randomness avoids
   modifying global RNG state. Copy before shuffle and reject duplicate IDs.
   ID disjointness is necessary, not sufficient: related tasks can leak answers.
2. [Regression](../../../forgeagent/learning.py): one residual vector fixes the
   old parameter version for both gradients. Empty means are undefined, so reject
   empty input. Check both coordinates independently with finite differences.
3. [Forward pass](network.py): row-per-output shape is explicit. ReLU separates
   two affine maps; without nonlinearity they collapse into one affine function.
4. [Autograd](../../../forgeagent/autograd.py): visit nodes once topologically,
   propagate in reverse, add every operand contribution. The reachable graph is
   cleared before each backward. Shared x*x and shared a+a detect different bugs.
5. [Optimizer](optimizer.py): validate all configuration/identities before writing.
   Duplicate parameter references would otherwise apply the step twice. Keep
   gradients inspectable; construct a fresh graph after updating parameter data.
6. [Bigram](../../../forgeagent/learning.py): smoothing covers the whole fixed
   vocabulary. Unknown training input rejects before mutation. Generation reads
   counts; fit deliberately accumulates observations. Mean NLL divides by n−1
   transitions and is not comparable across different tokenization units.

The seed-7 XOR loop is a CPU optimization demonstration, not a held-out benchmark.
For performance claims, record split, metric, seed set and all outcomes before
selecting a design. The tested graph is scalar and intentionally limited in
recursion depth, numerical domains and throughput.
