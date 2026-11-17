# Week 1 reasoning and reference solutions

Attempt each lab before opening its corresponding source. These are deliberately
small functions: independent implementation is possible with the day's concepts.

1. [summary.py](summary.py): `len(text)` includes whitespace. `split()` without
   an argument collapses whitespace and discards empty segments; splitting on
   the literal space would violate the newline contract. Complexity O(n).
2. [normalize.py](normalize.py): transformation order matters. Lowercase before
   counting so `Agent` and `agent` share a key; strip punctuation after splitting
   so internal punctuation remains. This tokenization differs intentionally
   from the final Unicode-aware project policy; a contract is more specific
   than the vague request to “clean text.” Complexity O(n).
3. [counts.py](counts.py): after k iterations, the sum of all stored counts is k.
   Allocating inside the function prevents accidental memory across calls.
   Average O(n) with Python dictionaries, not a promise of worst-case O(1)
   lookup for all possible workloads.
4. [loader.py](loader.py): immediate traversal and sorting make the scope and
   output reproducible. Errors propagate so the caller can choose a policy.
   The final project adds bounded reads and link checks; this introductory
   loader is for trusted small fixtures, not an adversarial filesystem.
5. [rank.py](rank.py): negative counts invert the primary order. Path order is
   an independent second key. `sorted` copies; `.sort` would mutate the caller's
   list. Reject booleans explicitly: `bool` is an `int` subclass in Python.
6. [cli.py](cli.py): the evolving implementation is composed from pure search
   and effectful loading. An expected operational failure becomes a concise
   error and status 2. Programming defects are allowed to show a traceback.

Do not collapse all failures into an empty list: that makes a broken corpus
indistinguishable from a genuine no-match result. Do not claim a passing test
suite proves absence of bugs. Explain one counterexample not covered by the
public checks, add a test, then justify its expected result independently.
