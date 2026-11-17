from dataclasses import dataclass


@dataclass(frozen=True)
class Hit:
    path: str
    count: int


def rank(hits, limit=5):
    if type(limit) is not int or limit < 0:
        raise ValueError("limit must be a nonnegative integer")
    positive = [hit for hit in hits if hit.count > 0]
    return sorted(positive, key=lambda hit: (-hit.count, hit.path))[:limit]
