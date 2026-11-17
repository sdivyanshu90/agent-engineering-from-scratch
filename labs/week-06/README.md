# Week 6 labs — transparent retrieval and grounded evidence

Prerequisite: Week 5 gate. Work independently under `learner-work/week-06/`.
Copy runnable baselines; they intentionally do not meet full contracts. Use
[hints](hints.md) after attempting, then [reference reasoning](../../solutions/labs/week-06/explanation.md).
No embedding download, vector database, paid API or GPU is required.

| Day | Starter | Contract |
|---|---|---|
| 1 / D31 | [chunks.py](starter/chunks.py) | split_document(path,text,lines=8,overlap=1) returns Chunk records preserving newline text, one-based inclusive spans, full-text SHA-256 revision and hash(path,NUL,revision,NUL,span); require positive integer lines, 0≤overlap<lines; no redundant tail window. |
| 2 / D32 | [sparse.py](starter/sparse.py) | rank(query,chunks,k=5,k1=1.2,b=.75) implements positive-IDF BM25, unique normalized query terms, postings tf/df, mean chunk length; returns Scored IDs descending score/ascending ID; validate IDs/parameters/limit. |
| 3 / D33 | [dense.py](starter/dense.py) | nearest(vectors,query,k=5,approximate=False) exact cosine over equal-width finite nonzero vectors; optional sign-of-first-coordinate candidate filter explicitly demonstrates ANN loss; stable tie order, empty-index no results. |
| 4 / D34 | [fusion.py](starter/fusion.py) | combine(rankings,constant=60,k=5) sums 1/(constant+one_based_rank); absent zero, duplicate within-list rejection, stable ID ties and nonnegative limit. |
| 5 / D35 | [metrics.py](starter/metrics.py) | metrics(ranked,relevance,k=5) returns precision/recall/rr/ndcg with fixed-k precision, positive-grade relevance, exponential gain and log2(rank+1), ideal-zero→0; reject duplicate IDs, grade outside integer0..10, nonpositive cutoff. |
| 6 / D36 | [support.py](starter/support.py) | supported(text,chunks) strictly parses bounded answer/citations JSON; unique/exact fields, ≤5 citations, each ID/revision/exact nonempty quote exists in supplied evidence; answer equals newline-joined quotes or explicit Insufficient evidence. with empty citations. |

Run `python labs/week-06/checks.py --day 1` against a reference. Add
`--module learner-work/week-06/chunks.py` for your attempt; change local day/file
as appropriate. Run all authored references with `python scripts/validate_exercises.py`.
Public checks are minimum contracts, not semantic-quality certification.

Submit source, a hand numerical trace, two extra boundary cases, a reproduced/fixed
defect and the daily examination. Also run `python scripts/benchmark_retrieval.py`
without modifying its corpus/judgments after seeing scores. Report all per-query
rows, including no-evidence cases. The fixture is visible educational regression
data, not held-out. The toy sign bucket, TF-IDF and authored vectors are not a
pretrained semantic embedding system. Model quote selection is optional and tested
with FakeProvider; no live answer-quality result is claimed.
