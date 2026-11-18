# Week 12 labs — constrained coding agent

Work in a copy of the repository or a disposable fixture. No lab gives the
provider arbitrary shell access. Testing a candidate requires an explicit
isolation backend; absent backend is a fail-closed result. For each day, copy
the matching starter to your submission directory and run the public contract:

```text
python labs/week-12/checks.py --day 1
python labs/week-12/checks.py --day 1 --module learner-work/week-12/search.py
```

| Day | File | Contract |
|---|---|---|
| D67 | `search.py` | Deterministic bounded lexical source search with path and line provenance |
| D68 | `trajectory.py` | Ordered proposal, matching approval, apply, and same-revision test acceptance |
| D69 | `approval.py` | Canonical review digest binds path and before/after hashes |
| D70 | `execution.py` | Test requests use injected backend and fixed argv; missing backend refuses |
| D71 | `resume.py` | Recover latest full checkpoint snapshot across append/checkpoint crash window |
| D72 | `benchmark.py` | Fixed case denominator, split separation, and per-case outcomes |

Public checks are minimum contracts and do not prove semantic understanding,
security, or broad coding success. Full references are in
`../../solutions/labs/week-12/`; hints are in `hints.md`. Preserve failing
fixtures, report limits, and do not call a visible deterministic benchmark
held-out evidence. The offline provider in the demo is a scripted protocol
fixture, not a real-model coding-quality evaluation.
