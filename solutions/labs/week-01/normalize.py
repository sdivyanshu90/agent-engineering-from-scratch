def normalize(text):
    result = []
    for token in text.lower().split():
        cleaned = token.strip(".,!?")
        if cleaned:
            result.append(cleaned)
    return result
