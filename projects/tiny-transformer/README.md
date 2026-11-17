# Supporting project — tiny trainable decoder

The [implementation](../../forgeagent/transformer.py) contains a complete one-block
decoder: token and learned position embeddings, per-token pre-normalization,
multiple causal attention heads, residuals, ReLU expansion/contraction, final
normalization, vocabulary logits, stable loss and finite training. It uses our
[scalar autograd](../../forgeagent/autograd.py), not a transformer/agent framework.

```sh
python -m unittest tests.integration.test_transformer -v
python labs/week-04/checks.py --day 5
```

Seven tests cover BPE reconstruction, attention arithmetic, normalization/residual
gradients, causal invariance/gradients, full/cached equivalence and limits, training/
parameter gradients, and sampling support/domain checks. Tests run on CPU without
external data, packages or model requests.

For an interactive educational run:

```python
from forgeagent.transformer import train_toy,sample
model,losses=train_toy(steps=8,rate=.05,seed=7)
print(losses)
tokens=[0]
cache={'keys':[],'values':[]}
for _ in range(5):
    logits=model.cached_step(tokens[-1],cache)
    tokens.append(sample([value.data for value in logits],temperature=0))
print(tokens)
```

Exact losses are measured when you run; do not copy documentation numbers as
your evidence. The model learns a three-symbol repeating fixture, not real
language or coding ability. Vocabulary and context limits are explicit.

Simplifications: one block, learned absolute positions, no dropout, linear biases
or learned normalization gain/offset, scalar Python arithmetic, and Value-node
cache storage instead of efficient numeric tensors. A production cache disables
gradients and needs layer-specific ownership, eviction and revision handling.
The toy rejects context exhaustion. Its purpose is to teach mechanics; the
primary capstone remains ForgeAgent application/runtime infrastructure.
