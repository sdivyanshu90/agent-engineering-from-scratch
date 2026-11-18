# Week 12 hints

1. Normalize each line once, score each query term once, and sort ties by path.
2. Find event indices; require the sequence proposal → approval → apply → test.
3. Canonical JSON needs sorted keys and compact separators before hashing.
4. Let `TestExecutor` reject a missing backend; never add a local shell fallback.
5. The append event must carry enough snapshot data to recover if checkpoint
   persistence did not happen.
6. Keep development and held-out rows separately named, fixed, and visible.

The references show one acceptable approach. Your explanation must state the
assumptions that the code cannot enforce.
