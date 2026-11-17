"""Scalar reverse-mode automatic differentiation for CPU-sized teaching graphs.

Original implementation. backward() clears the reachable graph first; separate
backward calls do not accumulate batches. Rebuild the graph after parameter edits.
"""
import math


class Value:
    def __init__(self, data, parents=(), operation=""):
        self.data = float(data)
        self.grad = 0.0
        self.parents = tuple(parents)
        self.operation = operation
        self._pullback = lambda: None

    @staticmethod
    def wrap(other):
        return other if isinstance(other, Value) else Value(other)

    def __add__(self, other):
        other = self.wrap(other)
        output = Value(self.data + other.data, (self, other), "+")
        def pullback():
            self.grad += output.grad
            other.grad += output.grad
        output._pullback = pullback
        return output

    __radd__ = __add__

    def __mul__(self, other):
        other = self.wrap(other)
        output = Value(self.data * other.data, (self, other), "*")
        def pullback():
            self.grad += other.data * output.grad
            other.grad += self.data * output.grad
        output._pullback = pullback
        return output

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -self.wrap(other)

    def __rsub__(self, other):
        return self.wrap(other) + -self

    def __pow__(self, power):
        if not isinstance(power, (int, float)):
            raise TypeError("only constant numeric powers are supported")
        output = Value(self.data ** power, (self,), f"**{power}")
        def pullback():
            if power != 0:
                self.grad += power * self.data ** (power - 1) * output.grad
        output._pullback = pullback
        return output

    def __truediv__(self, other):
        return self * self.wrap(other) ** -1

    def __rtruediv__(self, other):
        return self.wrap(other) / self

    def exp(self):
        output = Value(math.exp(self.data), (self,), "exp")
        def pullback():
            self.grad += output.data * output.grad
        output._pullback = pullback
        return output

    def log(self):
        if self.data <= 0:
            raise ValueError("log requires positive input")
        output = Value(math.log(self.data), (self,), "log")
        def pullback():
            self.grad += output.grad / self.data
        output._pullback = pullback
        return output

    def tanh(self):
        output = Value(math.tanh(self.data), (self,), "tanh")
        def pullback():
            self.grad += (1 - output.data ** 2) * output.grad
        output._pullback = pullback
        return output

    def relu(self):
        output = Value(max(0.0, self.data), (self,), "relu")
        def pullback():
            self.grad += (1.0 if self.data > 0 else 0.0) * output.grad
        output._pullback = pullback
        return output

    def backward(self):
        ordered, visited = [], set()
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for parent in node.parents:
                visit(parent)
            ordered.append(node)
        visit(self)
        for node in ordered:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(ordered):
            node._pullback()

    def __repr__(self):
        return f"Value(data={self.data:.6g}, grad={self.grad:.6g})"


def cross_entropy(logits, target):
    """Stable log-sum-exp minus selected logit; positive finite normalization."""
    if not logits or type(target) is not int or not 0 <= target < len(logits):
        raise ValueError("target must index a nonempty logit vector")
    if any(not math.isfinite(value.data) for value in logits):
        raise ValueError("finite logits required")
    maximum = max(value.data for value in logits)
    total = sum((value - maximum).exp() for value in logits)
    return total.log() + maximum - logits[target]
