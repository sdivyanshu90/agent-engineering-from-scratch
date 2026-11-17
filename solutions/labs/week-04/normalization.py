from forgeagent.autograd import Value
from forgeagent.transformer import normalize


def layer_norm(vector,epsilon=1e-5):
    return [value.data for value in normalize([Value(v) for v in vector],epsilon)]
