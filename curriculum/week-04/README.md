# Week 4 — Transformer internals

Prerequisite: [Week 3 mastery gate](../../assessments/weekly/week-03.md). Build
an inspectable decoder independently, using scalar autograd to expose central
operations before adopting optimized libraries. This supports the ForgeAgent
specialization; training a competitive language model is outside the program.

| Day | Chapter | Independent artifact |
|---|---|---|
| 1 / D19 | [Tokens and embeddings](day-01/README.md) | Reversible ranked BPE |
| 2 / D20 | [Positions and Q/K/V](day-02/README.md) | Shape-checked projection |
| 3 / D21 | [Causal multi-head attention](day-03/README.md) | Stable weighted mixing |
| 4 / D22 | [Decoder block](day-04/README.md) | Per-token normalization |
| 5 / D23 | [Loss and training](day-05/README.md) | Stable categorical NLL |
| 6 / D24 | [Sampling and caching](day-06/README.md) | Candidate selection/cache invariants |

Use [labs](../../labs/week-04/README.md), then [review](weekly-review.md),
[weekly exam](../../assessments/weekly/week-04.md), and
[Phase 2 defense](../../assessments/phase-examinations/phase-02.md).
Allow 42–54 hours and additional days for shape/gradient remediation. No GPU,
paid API or third-party training runtime is required. The
[tiny transformer project](../../projects/tiny-transformer/README.md) documents
exact simplifications and executable commands.
