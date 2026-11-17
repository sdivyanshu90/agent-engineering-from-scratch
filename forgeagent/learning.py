"""Week 3 first-principles regression, neural forward pass, and character model."""
from dataclasses import dataclass
import math
import random
from .autograd import Value


@dataclass(frozen=True)
class Example:
    identifier: str
    features: tuple[float, ...]
    target: float


def split_examples(rows, seed=7):
    if len(rows) < 5 or len({row.identifier for row in rows}) != len(rows):
        raise ValueError("need at least five uniquely identified rows")
    copy = list(rows)
    random.Random(seed).shuffle(copy)
    train_end, validation_end = int(0.6 * len(copy)), int(0.8 * len(copy))
    return {"train": copy[:train_end], "validation": copy[train_end:validation_end], "test": copy[validation_end:]}


def predict(x, weight, bias):
    return weight * x + bias


def mse(predictions, targets):
    if not predictions or len(predictions) != len(targets):
        raise ValueError("nonempty equally sized predictions and targets required")
    return math.fsum((prediction - target) ** 2 for prediction, target in zip(predictions, targets)) / len(targets)


def regression_step(xs, ys, weight, bias, rate=0.01):
    if not xs or len(xs) != len(ys) or not math.isfinite(rate) or rate <= 0:
        raise ValueError("valid nonempty pairs and positive finite rate required")
    residuals = [predict(x, weight, bias) - y for x, y in zip(xs, ys)]
    dw = 2 * math.fsum(error * x for error, x in zip(residuals, xs)) / len(xs)
    db = 2 * math.fsum(residuals) / len(xs)
    return weight - rate * dw, bias - rate * db


def affine(inputs, weights, biases):
    if not inputs or not weights or len(weights) != len(biases) or any(len(row) != len(inputs) for row in weights):
        raise ValueError("weights must be output-by-input, biases match outputs")
    return [sum(w*x for w, x in zip(row, inputs)) + b for row, b in zip(weights, biases)]


class MLP:
    """One tanh hidden layer, scalar output; topology is explicit."""
    def __init__(self, inputs=2, hidden=4, seed=7):
        if inputs < 1 or hidden < 1:
            raise ValueError("positive dimensions required")
        rng = random.Random(seed)
        self.first = [[Value(rng.uniform(-1, 1) / math.sqrt(inputs)) for _ in range(inputs)] for _ in range(hidden)]
        self.biases = [Value(0) for _ in range(hidden)]
        self.second = [Value(rng.uniform(-1, 1) / math.sqrt(hidden)) for _ in range(hidden)]
        self.output_bias = Value(0)

    def __call__(self, inputs):
        if len(inputs) != len(self.first[0]):
            raise ValueError("wrong input width")
        hidden = [sum(w*x for w, x in zip(row, inputs)) + b for row, b in zip(self.first, self.biases)]
        return sum(w*h.tanh() for w, h in zip(self.second, hidden)) + self.output_bias

    def parameters(self):
        return [value for row in self.first for value in row] + self.biases + self.second + [self.output_bias]


def train_xor(steps=300, rate=0.1, seed=7):
    """Tiny deterministic full-batch regression of XOR targets -1/+1."""
    model = MLP(seed=seed)
    rows = [([-1,-1],-1), ([-1,1],1), ([1,-1],1), ([1,1],-1)]
    losses = []
    for _ in range(steps):
        loss = sum((model(x) - y) ** 2 for x, y in rows) / len(rows)
        loss.backward()
        losses.append(loss.data)
        for parameter in model.parameters():
            parameter.data -= rate * parameter.grad
    return model, losses


class BigramModel:
    """Smoothed count-based P(next character | current character), not a neural LM."""
    def __init__(self, vocabulary, alpha=1.0):
        if not vocabulary or len(set(vocabulary)) != len(vocabulary) or not math.isfinite(alpha) or alpha <= 0:
            raise ValueError("unique nonempty vocabulary and positive finite smoothing required")
        self.vocabulary = tuple(sorted(vocabulary))
        self.counts = {char: {following: alpha for following in self.vocabulary} for char in self.vocabulary}

    def fit(self, text):
        if any(char not in self.counts for char in text):
            raise ValueError("training text contains unknown character")
        for current, following in zip(text, text[1:]):
            self.counts[current][following] += 1
        return self

    def distribution(self, current):
        row = self.counts[current]
        total = math.fsum(row.values())
        return {char: value / total for char, value in row.items()}

    def nll(self, text):
        if len(text) < 2 or any(char not in self.counts for char in text):
            raise ValueError("need at least two known characters")
        return -math.fsum(math.log(self.distribution(current)[following]) for current, following in zip(text, text[1:])) / (len(text)-1)

    def generate(self, start, count=20, seed=7):
        if start not in self.counts or type(count) is not int or count < 0:
            raise ValueError("known start and nonnegative integer count required")
        rng, output = random.Random(seed), start
        for _ in range(count):
            distribution = self.distribution(output[-1])
            output += rng.choices(self.vocabulary, weights=[distribution[c] for c in self.vocabulary], k=1)[0]
        return output
