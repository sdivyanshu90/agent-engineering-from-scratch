class Scalar:
    def __init__(self, data):
        self.data = float(data)
        self.grad = 0.0

    def __add__(self, other):
        return Scalar(self.data + (other.data if isinstance(other, Scalar) else other))

    __radd__ = __add__

    def __mul__(self, other):
        return Scalar(self.data * (other.data if isinstance(other, Scalar) else other))

    __rmul__ = __mul__

    def backward(self):
        self.grad = 1.0
