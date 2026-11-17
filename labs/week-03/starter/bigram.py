def distribution(text, vocabulary, current, alpha=1.0):
    return {char: 1 / len(vocabulary) for char in vocabulary} if vocabulary else {}
