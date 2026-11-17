from dataclasses import dataclass


@dataclass(frozen=True)
class Hit:
    path: str
    count: int


def rank(hits, limit=5):
    return list(hits)
