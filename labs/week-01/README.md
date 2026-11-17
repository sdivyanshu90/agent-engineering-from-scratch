# Lab sequence: build a document search CLI

Work in `learner-work/week-01/`; that directory is ignored by Git. Each day's
starter runs and returns a baseline result, but does not yet meet its contract.
A failing learner check is expected before you implement the requirement.
Ordinary repository tests run references, not unfinished learner submissions.

| Day | Independent artifact | Contract and acceptance |
|---|---|---|
| 1 | `summary.py` | Return a dictionary with character and whitespace-word counts; empty input has two zeros; preserve the caller's text. |
| 2 | `normalize.py` | Return lowercase whitespace tokens with only leading/trailing `.,!?` removed; omit empty tokens; internal punctuation stays. |
| 3 | `counts.py` | Count supplied tokens without mutating the input; return a fresh dictionary each call. |
| 4 | `loader.py` | Read sorted immediate `.txt` files as UTF-8; return `(filename, text)` pairs; propagate decoding and missing-directory errors. Do not recurse. |
| 5 | `rank.py` | Implement the frozen `Hit` data class and sort hits by descending count then path; retain only positive counts and validate nonnegative integer limit. |
| 6 | `cli.py` | Integrate Week 1 references or your equivalents; stdout JSON, stderr errors, status 0/2; reject invalid queries; deterministic ties. |

Every exercise's fixed inputs and expected outputs are in
[checks.py](checks.py). Use them as a public contract, then add your own tests.
Run a single reference check: `python labs/week-01/checks.py --day 1`.
Run your implementation: `python labs/week-01/checks.py --day 1 --module learner-work/week-01/summary.py`.
Day 6 additionally needs the integration tests under `tests/integration/`.

Starter files are in [starter](starter/summary.py). Copy the selected file; do
not edit the reference. After a sincere attempt use [hints](hints.md), then
compare with [solutions](../../solutions/labs/week-01/explanation.md).

Requirements: no network, no third-party libraries, no shell execution from
Python. Use local fixtures and a temporary directory for file tests. Submit the
source, one traced execution, two additional edge cases, observed outputs,
and a brief explanation of a failure you caused and fixed. Passing public tests
is necessary, but the explanation and unseen input gate must also pass.
