# Week 4 reference reasoning

Attempt independently first. Solution adapters return ordinary numbers while
reusing the actual differentiable project mechanism; inspect the linked source
rather than expecting unexplained omitted code.

1. [BPE](../../../forgeagent/tokenization.py): pair selection is deterministic;
   merge application consumes nonoverlapping operands and preserves reconstruction.
   This is Unicode-character toy BPE, not a provider tokenizer or billing estimator.
2. [Projection](projections.py): content/position addition requires equal widths;
   matrices store output rows. The isolated lab omits normalization explicitly,
   while the full pre-normalized decoder includes it.
3. [Attention](../../../forgeagent/transformer.py): scale by head-width square root,
   shift scores, normalize eligible support, preserve key/value alignment. The
   caller enforces causality by supplying only permitted prefixes.
4. [Normalization](../../../forgeagent/transformer.py): population variance across
   one token's feature coordinates. Epsilon prevents zero denominator; finite
   inputs and positive finite epsilon reject invalid domains. No learned gains
   or offsets are hidden in the helper.
5. [Loss](../../../forgeagent/autograd.py): log-sum-exp minus target score avoids
   taking log of an underflowed probability. Its gradient is p−one_hot_target.
   Shifted numerical form preserves the intended function and derivatives.
6. [Sampling](../../../forgeagent/transformer.py): temperature → top-k → normalize
   survivors → nucleus threshold → renormalized random choice. T=0 is an explicit
   deterministic branch. The cache must belong to one sequence/model revision;
   numeric equality with full execution is the correctness check.

The complete decoder is one block, multiple causal heads, learned absolute
positions, ReLU FFN and scalar autograd, without dropout/biases/learned norm gain.
Its cache retains Python graph objects for teaching and is not a production
memory-efficient tensor cache. Training on a three-symbol pattern demonstrates
mechanics, not useful language or coding performance.
