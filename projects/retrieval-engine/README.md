# Milestone 4a — transparent retrieval

[retrieval.py](../../forgeagent/retrieval.py) extends ForgeAgent's local document
inspection with revision-aware chunks, in-memory postings/BM25, lexical TF-IDF,
exact cosine search, an intentionally crude approximate sign bucket, original
unweighted RRF and lexical-coverage reranking. No vector service or learned
semantic model is implicitly installed.

```sh
python -m unittest tests.integration.test_retrieval -v
python scripts/benchmark_retrieval.py
```

The [fixed fixture](../../datasets/evaluation-fixtures/retrieval.json) is original,
visible teaching material with three sources and four queries. Report every row,
including no-evidence behavior. Its mean reciprocal rank across all four is .75
under the declared convention, not a held-out or real-model quality claim.
Run the script for actual observed results; do not paste expectations as measurements.

The exact scan validates moderate finite nonzero compatible vectors. TF-IDF is
lexical; authored vectors test geometry. The sign-bucket approximation deliberately
misses an almost-parallel neighbor and does not claim to implement HNSW. RRF uses
one-based ranks with constant60, independent of a service's current defaults.
The implementation is an inspectable CPU baseline for later infrastructure work.
