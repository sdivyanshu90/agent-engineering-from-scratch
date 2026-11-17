from forgeagent.autograd import Value
from forgeagent.transformer import attention


def attend(q,keys,values):
    return [value.data for value in attention([Value(v) for v in q],
        [[Value(v) for v in row] for row in keys],[[Value(v) for v in row] for row in values])]
