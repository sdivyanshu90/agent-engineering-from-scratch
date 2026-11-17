"""Small CPU mathematical mechanisms; no NumPy hides shapes in Week 2."""
import math


def dot(a, b):
    if len(a) != len(b) or not a:
        raise ValueError("equal nonzero dimensions required")
    return math.fsum(x * y for x, y in zip(a, b))


def cosine(a, b):
    product = dot(a, b)
    denominator = math.sqrt(dot(a, a)) * math.sqrt(dot(b, b))
    if denominator == 0:
        raise ValueError("zero vector has no cosine direction")
    return product / denominator


def matvec(matrix, vector):
    if not matrix:
        raise ValueError("matrix needs at least one row")
    return [dot(row, vector) for row in matrix]


def softmax(logits):
    if not logits or any(not math.isfinite(value) for value in logits):
        raise ValueError("nonempty finite logits required")
    maximum = max(logits)
    weights = [math.exp(value - maximum) for value in logits]
    denominator = math.fsum(weights)
    return [weight / denominator for weight in weights]


def derivative(function, x, h=1e-5):
    if not math.isfinite(h) or h <= 0:
        raise ValueError("positive finite h required")
    return (function(x + h) - function(x - h)) / (2 * h)


def descend_square(x, learning_rate=0.1, steps=10):
    if not 0 < learning_rate < 1 or type(steps) is not int or steps < 0:
        raise ValueError("require 0<rate<1 and nonnegative integer steps")
    history = [x]
    for _ in range(steps):
        x = x - learning_rate * 2 * x
        history.append(x)
    return history
