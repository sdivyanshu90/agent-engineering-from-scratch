# Week 6 reference decisions

Attempt first. Reference adapters reuse [retrieval.py](../../../forgeagent/retrieval.py)
and [grounding.py](../../../forgeagent/grounding.py), whose mechanisms are implemented
explicitly rather than delegated to search/agent frameworks.

1. Preserve source text/newlines and full-source revision. Positive stride and
   stopping at the first final slice prevent zero-progress/redundant tails.
2. Unique query terms, chunk-level df and documented positive IDF make scores
   reproducible. BM25 conventions differ across engines; score is not probability.
3. Exact cosine is the correctness baseline. Sign filtering intentionally loses
   an almost-parallel cross-boundary vector. Fixtures/TF-IDF do not establish
   learned semantic quality, and same dimensions do not ensure model compatibility.
4. RRF uses one-based ranks and raw-score invariance. Duplicate within-list IDs
   reject rather than inflate contributions. Reranking cannot recover absent candidates.
5. Fixed cutoff and exponential gain define the metric. Empty-relevance zeros
   and separate abstention grading prevent denominator ambiguity. Source-path
   de-duplication belongs before document-level metrics when search returns chunks.
6. Exact selected-snapshot citations plus answer-equals-quotes establish the
   narrow mechanical support contract. Occurrence still does not prove relevance,
   source truth or authorization. Extra paraphrased claims reject by design.

The visible benchmark is a regression fixture with fixed labels, not a secure
held-out agent or real-model evaluation. Report observed metrics and all no-answer
rows; never change judgments merely to obtain a pass. Optional provider quote
selection uses the existing interface; FakeProvider tests are not live inference.
