# Week 1 mastery examination

Attempt independently before inspecting [answers](../../solutions/examinations/week-01.md).
Suggested 3–4 hours plus review; time is advisory, criteria are fixed. Allowed:
this problem statement, Python standard library documentation, your editor, and
a terminal. Record any assistance. Do not copy repository solutions.

## A. Conceptual examination — 20 points

Five questions, 4 points each: 2 for a correct claim, 1 for explaining its
mechanism, 1 for a counterexample or limitation.

1. Distinguish file, running process, in-memory value, and printed representation.
2. Explain why `b=a` can share a list but rebinding `a=[]` does not clear b.
3. Explain type hints versus validation, including `True` as an integer subtype.
4. Explain why invalid UTF-8 cannot honestly be reported as an empty corpus.
5. Distinguish a successful no-match result from an invalid query in a CLI.

## B. Independent coding — 30 points

Build a CLI over an owned local directory. Accept one-token query and a
nonnegative integer limit. Read UTF-8 `.txt` files, normalize with one documented
policy on both query and documents, rank positive token counts descending,
break ties by relative filename ascending, and emit JSON. Do not alter input.
For this examination immediate traversal is sufficient if documented.

Use fixtures `b.txt = "Agent agent"`, `a.txt = "agent tool"`, and `empty.txt = ""`.
For query agent, limit 2, expected records are b with count 2 then a with count 1.
For tool, only a with count 1. For absent term, `[]`. Create two tied documents
and show their output is independent of creation order. Reject multi-token
queries and negative limits visibly.

Points: reading/scope/encoding 6; compatible normalization/counts 6; ordering/
limit/nonmutation 6; process contract and errors 6; meaningful additional tests 6.
A copied solution or unexplained generated implementation earns no independent
coding credit; reconstruct from the contract instead.

## C. Debugging assessment — 20 points

For each flawed statement below: provide a minimal failing input (2 points),
first wrong state/cause (2), correction (2), and regression evidence (2).
The fifth item is worth 4 points for identifying and correcting the failure policy.

1. `result = result.append(cleaned)` inside a normalization loop.
2. `return counts` indented inside the token iteration.
3. A dictionary default argument carrying counts between calls.
4. Sorting hits by count alone while promising filename tie order.
5. Catching all exceptions and returning `[]` from a loader.

## D. Architectural reasoning — 15 points

1. Draw parsing → loading → pure search → serialization, marking the effectful
   boundaries and expected error path (5).
2. Explain cost for corpus size, query count, and matching document count.
   State assumptions and one measurement needed before adding an index (5).
3. Explain why symlink checks do not make an OS sandbox; define the trusted
   workspace assumption and one future isolation requirement (5).

## E. Practical integration — 15 points

Run success, no-match, invalid-query, missing-directory, and malformed-UTF-8 cases
from a fresh process. Record return code, stdout, stderr for each. Each case is
worth 3: correct status, correct channel/content, explanation. Success/no-match
must be status 0 with parseable JSON; operational failures must be nonzero and
not emit a success payload. Inspect a diff of your work and note one known limitation.

## Gate and remediation

Pass at 80/100 **and** all four critical invariants: fresh per-call state, valid
success JSON, nonzero operational-failure status, visible decoding failure.
These cannot be traded for conceptual points. No grading adjustments after
results. If failed, use the [review](../../curriculum/week-01/weekly-review.md),
then retest with changed filenames, token frequencies, and malformed input.
Retain the original failed evidence alongside the corrected attempt.
