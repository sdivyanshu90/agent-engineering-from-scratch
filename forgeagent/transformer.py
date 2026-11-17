"""Tiny trainable decoder: scalar autograd exposes each operation, CPU only.

One pre-normalized block, learned positions, multiple heads, ReLU FFN, untied
output embeddings. No dropout or learned normalization gains/biases. Cached
inference and full causal execution share parameters and must agree numerically.
"""
import math
import random
from .autograd import Value, cross_entropy
from .math_basics import softmax


def linear(inputs, weights):
    if not weights or any(len(row) != len(inputs) for row in weights):
        raise ValueError("linear shape mismatch")
    return [sum(w*x for w, x in zip(row, inputs)) for row in weights]


def normalize(inputs, epsilon=1e-5):
    if not inputs or not math.isfinite(epsilon) or epsilon <= 0 or any(not math.isfinite(value.data) for value in inputs):
        raise ValueError("nonempty input and positive epsilon required")
    mean = sum(inputs) / len(inputs)
    variance = sum((value-mean)**2 for value in inputs) / len(inputs)
    inverse = (variance + epsilon) ** -0.5
    return [(value-mean)*inverse for value in inputs]


def attention(query, keys, values):
    if not keys or len(keys) != len(values):
        raise ValueError("nonempty aligned keys and values required")
    width = len(query)
    if not width or any(len(row) != width for row in keys + values):
        raise ValueError("head shape mismatch")
    scores = [sum(q*k for q, k in zip(query, key)) / math.sqrt(width) for key in keys]
    maximum = max(score.data for score in scores)
    weights = [(score-maximum).exp() for score in scores]
    total = sum(weights)
    probabilities = [weight / total for weight in weights]
    return [sum(probability * value[j] for probability, value in zip(probabilities, values)) for j in range(width)]


class TinyDecoder:
    def __init__(self, vocabulary_size, width=4, heads=2, context=8, seed=7):
        if any(type(value) is not int or value < 1 for value in [vocabulary_size,width,heads,context]) or width % heads:
            raise ValueError("positive dimensions; width divisible by heads")
        self.vocabulary_size, self.width, self.heads, self.context = vocabulary_size,width,heads,context
        rng = random.Random(seed)
        def matrix(rows, columns):
            return [[Value(rng.gauss(0,0.2)) for _ in range(columns)] for _ in range(rows)]
        self.embeddings = matrix(vocabulary_size,width)
        self.positions = matrix(context,width)
        self.query, self.key, self.value, self.output = [matrix(width,width) for _ in range(4)]
        self.expand = matrix(2*width,width)
        self.contract = matrix(width,2*width)
        self.lm_head = matrix(vocabulary_size,width)

    def parameters(self):
        matrices = [self.embeddings,self.positions,self.query,self.key,self.value,self.output,self.expand,self.contract,self.lm_head]
        return [value for matrix in matrices for row in matrix for value in row]

    def _check_token(self, token, position):
        if type(token) is not int or not 0 <= token < self.vocabulary_size:
            raise ValueError("token outside vocabulary")
        if position >= self.context:
            raise ValueError("context exhausted; do not silently reuse positions")

    def _finish(self, hidden, query, keys, values):
        concatenated = []
        head_width = self.width // self.heads
        for head in range(self.heads):
            start, end = head*head_width, (head+1)*head_width
            concatenated.extend(attention(query[start:end], [row[start:end] for row in keys], [row[start:end] for row in values]))
        projected = linear(concatenated,self.output)
        residual = [a+b for a,b in zip(hidden,projected)]
        expanded = [value.relu() for value in linear(normalize(residual),self.expand)]
        contracted = linear(expanded,self.contract)
        result = [a+b for a,b in zip(residual,contracted)]
        return linear(normalize(result),self.lm_head)

    def __call__(self, tokens):
        if not tokens or len(tokens) > self.context:
            raise ValueError("nonempty tokens within context required")
        hidden, queries, keys, values = [],[],[],[]
        for position,token in enumerate(tokens):
            self._check_token(token,position)
            row = [a+b for a,b in zip(self.embeddings[token],self.positions[position])]
            hidden.append(row)
            normalized = normalize(row)
            queries.append(linear(normalized,self.query))
            keys.append(linear(normalized,self.key))
            values.append(linear(normalized,self.value))
        return [self._finish(row,query,keys[:i+1],values[:i+1]) for i,(row,query) in enumerate(zip(hidden,queries))]

    def cached_step(self, token, cache):
        """Cache is caller-owned for one sequence/model revision; inference only.

        Value nodes remain in memory here for clarity. A production inference
        cache stores numeric tensors with gradients disabled and eviction limits.
        """
        if set(cache) != {"keys","values"} or len(cache["keys"]) != len(cache["values"]):
            raise ValueError("aligned key/value cache required")
        position = len(cache["keys"])
        self._check_token(token,position)
        hidden = [a+b for a,b in zip(self.embeddings[token],self.positions[position])]
        normalized = normalize(hidden)
        query = linear(normalized,self.query)
        cache["keys"].append(linear(normalized,self.key))
        cache["values"].append(linear(normalized,self.value))
        return self._finish(hidden,query,cache["keys"],cache["values"])

    def loss(self, inputs, targets):
        if len(inputs) != len(targets):
            raise ValueError("one next-token target per input position")
        return sum(cross_entropy(logits,target) for logits,target in zip(self(inputs),targets)) / len(inputs)


def sample(logits, *, temperature=1.0, top_k=None, top_p=1.0, rng=None):
    if not logits or any(not math.isfinite(z) for z in logits):
        raise ValueError("finite nonempty logits required")
    if not math.isfinite(temperature) or temperature < 0 or not 0 < top_p <= 1:
        raise ValueError("temperature>=0; 0<top_p<=1")
    if top_k is not None and (type(top_k) is not int or not 1 <= top_k <= len(logits)):
        raise ValueError("top_k must index a nonempty candidate set")
    order = sorted(range(len(logits)),key=lambda i:(-logits[i],i))
    if temperature == 0:
        return order[0]
    candidates = order[:top_k] if top_k is not None else order
    probabilities = softmax([logits[i]/temperature for i in candidates])
    total, keep = 0.0, 0
    for probability in probabilities:
        total += probability
        keep += 1
        if total >= top_p:
            break
    rng = rng or random.Random()
    return rng.choices(candidates[:keep],weights=probabilities[:keep],k=1)[0]


def train_toy(steps=8, rate=0.05, seed=7):
    model = TinyDecoder(vocabulary_size=3,width=4,heads=2,context=6,seed=seed)
    inputs,targets = [0,1,2,0,1], [1,2,0,1,2]
    losses=[]
    for _ in range(steps):
        loss=model.loss(inputs,targets)
        loss.backward()
        losses.append(loss.data)
        for parameter in model.parameters():
            parameter.data -= rate*parameter.grad
    return model,losses
