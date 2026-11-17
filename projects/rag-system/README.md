# Milestone 4b — quote-grounded application

[grounding.py](../../forgeagent/grounding.py) adds extractive answers, revision-
aware citations, strict quoted-answer validation and optional model-assisted
quote selection using the Week5 Provider interface. This is integrated evidence
acquisition for ForgeAgent, not a separate agent framework.

```sh
python scripts/benchmark_retrieval.py
python -m unittest tests.integration.test_retrieval.ModelGroundingTests -v
```

extract_answer uses lexical coverage and returns a supporting candidate's exact
text or explicit abstention. grounded_generate supplies at most three matching
chunks as untrusted data and asks a configured provider to select exact quotes.
Tests use FakeProvider; no paid/live call is needed. parse_grounded accepts only
answer/citations, verifies selected ID/revision/substring and requires the answer
to equal newline-joined quotes. Freeform paraphrases are outside this narrow
mechanically checkable contract and require semantic evaluation if added.

Limitations: occurrence does not establish source truth, authority or relevance.
A real irrelevant quotation can pass support syntax. No-hit abstention skips
the provider; always-abstain must not pass a usefulness benchmark through vacuous
citation validity. Corpus authorization must occur before retrieval/context;
this owned local fixture does not implement multi-tenant access. Total evidence
context budgets, durable updates, learned rerankers and production deployment
remain later work. No stochastic or held-out agent benchmark is claimed.
