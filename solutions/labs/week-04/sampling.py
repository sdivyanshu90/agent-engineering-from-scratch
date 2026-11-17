import random
from forgeagent.transformer import sample


def choose(logits,temperature=1.0,top_k=None,top_p=1.0,seed=7):
    return sample(logits,temperature=temperature,top_k=top_k,top_p=top_p,rng=random.Random(seed))
