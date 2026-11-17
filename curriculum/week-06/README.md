# Week 6 — Retrieval and grounded applications

Prerequisite: [Week 5 gate](../../assessments/weekly/week-05.md). Build evidence
acquisition before agent execution. Preserve exact source provenance and evaluate
retrieval separately from answer support and usefulness.

| Day | Chapter | Independent artifact |
|---|---|---|
| 1 / D31 | [Chunking and provenance](day-01/README.md) | Revision-aware line windows |
| 2 / D32 | [Sparse retrieval](day-02/README.md) | Inverted BM25 scoring |
| 3 / D33 | [Vectors and approximation](day-03/README.md) | Exact cosine/ANN-loss fixture |
| 4 / D34 | [Fusion and reranking](day-04/README.md) | Reciprocal rank fusion |
| 5 / D35 | [Retrieval metrics](day-05/README.md) | Fixed-convention ranking measures |
| 6 / D36 | [Grounding and abstention](day-06/README.md) | Strict selected-snapshot support |

Use [labs](../../labs/week-06/README.md), [review](weekly-review.md),
[weekly exam](../../assessments/weekly/week-06.md) and
[Phase 3 defense](../../assessments/phase-examinations/phase-03.md).
Budget 42–54 hours, extending for metric/provenance remediation. All ordinary
code runs locally without a vector service, downloaded model, GPU or paid call.
The [retrieval](../../projects/retrieval-engine/README.md) and
[RAG](../../projects/rag-system/README.md) components extend the same package.
