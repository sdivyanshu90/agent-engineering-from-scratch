# Milestone 1: deterministic repository inspection

This working reference is the first component of ForgeAgent. Search turns an
unstructured directory into explicit evidence (a path and a count). Later retrieval
must preserve this inspectable evidence contract. The implementation is in
[documents.py](../../forgeagent/documents.py) and [cli.py](../../forgeagent/cli.py).
Read these after attempting the [Week 1 lab](../../labs/week-01/README.md).

Run from the repository root:

```sh
python -m forgeagent.cli datasets/sample-data agents
python -m unittest discover -s tests -v
```

The first command prints `[{"path": "agents.txt", "count": 2}]` and exits 0.
A missing directory, invalid query, decoding error or size violation exits 2 and
writes an error on stderr. No results is a successful `[]`, not an error.

Architecture: CLI parser → bounded loader → tokenizer → frequency counter →
sort → JSON serializer. The loader accepts only UTF-8 `.txt` and `.md` files,
rejects discovered symbolic links, and reads at most one byte beyond each size
limit before rejecting. Paths are relative POSIX-style strings for reproducible
output. This avoids platform-specific separators in fixtures.

Time is proportional to text inspected plus hit sorting. Every query rereads all
files and recomputes counts. An index will improve repeated-query latency in
Week 6; introducing one now would hide the loop beginners must understand.

Limitations: a caller can select any root they can read; this is not an access
control system. Symlink checks are vulnerable to concurrent filesystem changes.
There is no OS sandbox, corpus-wide byte limit, multi-token ranking, semantic
retrieval, persistence, model adapter or agent loop yet. Do not expose this CLI
to untrusted users as a server. The capstone has not been implemented.
