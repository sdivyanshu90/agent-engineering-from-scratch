# Supporting project — miniature learning mechanisms

Week 3 builds [autograd](../../forgeagent/autograd.py) and
[learning examples](../../forgeagent/learning.py). They support understanding
LLM internals; they are not dependencies required to orchestrate a production
model provider or an unrelated second capstone.

Run from the repository root:

```sh
python -m unittest tests.integration.test_learning -v
python labs/week-03/checks.py --day 4
```

Seven tests cover shared paths/reset, nonlinear finite differences, stable
cross-entropy gradients, data partitions, regression fitting, a network parameter
check plus XOR fitting, and bigram evaluation/read-only inference. The scalar
engine keeps a graph of Python Value objects; its backward clears reachable
grads and uses reverse topological pullbacks. Rebuild after parameter updates.

The train_xor helper returns a model and measured per-step training losses.
The data is the full four-row XOR truth table, so success demonstrates the
mechanism rather than generalization. Bigram vocabulary/boundary conventions
are explicit and CPU-sized. All ordinary checks use only the standard library.

Limitations: recursive topology traversal can exceed Python depth on large graphs;
scalar objects/closures are slow; numerical domains are limited to supported real
operations; no tensor kernels, dropout, GPU, batching infrastructure, or model-
scale optimizer is provided. The [Week 3 chapters](../../curriculum/week-03/README.md)
explain why and how these mechanisms work before introducing larger systems.
