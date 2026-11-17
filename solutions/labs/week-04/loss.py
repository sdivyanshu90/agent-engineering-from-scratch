from forgeagent.autograd import Value,cross_entropy


def loss(logits,target):
    return cross_entropy([Value(value) for value in logits],target).data
