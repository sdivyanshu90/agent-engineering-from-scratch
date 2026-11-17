from forgeagent.learning import BigramModel


def distribution(text, vocabulary, current, alpha=1.0):
    model = BigramModel(vocabulary,alpha)
    if current not in model.counts:
        raise ValueError("unknown current character")
    return model.fit(text).distribution(current)
