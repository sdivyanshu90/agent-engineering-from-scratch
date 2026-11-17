import math


def update(parameters, rate):
    if not math.isfinite(rate) or rate <= 0:
        raise ValueError("positive finite rate required")
    if len({id(parameter) for parameter in parameters}) != len(parameters):
        raise ValueError("each parameter must appear exactly once")
    for parameter in parameters:
        parameter.data -= rate * parameter.grad
