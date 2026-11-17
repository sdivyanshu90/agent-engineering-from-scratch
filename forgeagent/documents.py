"""Week 1 reference: deterministic, bounded, local document inspection.

This is not an operating-system sandbox. Only use a workspace you control.
"""
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Document:
    path: str
    text: str


@dataclass(frozen=True)
class Hit:
    path: str
    count: int


def tokenize(text: str) -> list[str]:
    """Case-fold then extract Unicode letter/digit runs, excluding underscores."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return re.findall(r"[^\W_]+", text.casefold())


def frequencies(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in tokenize(text):
        counts[word] = counts.get(word, 0) + 1
    return counts


def load_documents(root: Path, *, max_bytes: int = 1_000_000) -> list[Document]:
    """Load sorted UTF-8 .txt/.md files; reject symlinks, oversize, bad UTF-8.

    Root must be an existing directory. max_bytes applies per file. Errors are
    surfaced rather than silently returning an apparently complete corpus.
    This walk has no total-corpus limit; it is a teaching implementation.
    """
    if type(max_bytes) is not int or max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise NotADirectoryError(str(root))
    result = []
    for path in sorted(root.rglob("*")):
        # Check ancestor links as well: traversal behavior can differ by platform.
        relative = path.relative_to(root)
        parents = [root.joinpath(*relative.parts[:i]) for i in range(1, len(relative.parts) + 1)]
        if any(p.is_symlink() for p in parents):
            raise ValueError(f"symbolic links are not accepted: {relative.as_posix()}")
        if not path.is_file() or path.suffix.lower() not in {".txt", ".md"}:
            continue
        # Read at most limit+1 to enforce the bound even if the file grows.
        with path.open("rb") as handle:
            raw = handle.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise ValueError(f"file exceeds byte limit: {relative.as_posix()}")
        result.append(Document(relative.as_posix(), raw.decode("utf-8")))
    return result


def search(documents: list[Document], query: str, *, limit: int = 5) -> list[Hit]:
    """Single-token exact search; descending frequency then ascending path."""
    terms = tokenize(query)
    if len(terms) != 1:
        raise ValueError("query must contain exactly one token")
    if type(limit) is not int or limit < 0:
        raise ValueError("limit must be a nonnegative integer")
    hits = []
    for document in documents:
        count = frequencies(document.text).get(terms[0], 0)
        if count:
            hits.append(Hit(document.path, count))
    return sorted(hits, key=lambda hit: (-hit.count, hit.path))[:limit]
