from forgeagent.learning import affine


def forward(x, w1, b1, w2, b2):
    hidden = [max(0, value) for value in affine(x,w1,b1)]
    return affine(hidden,w2,b2)
