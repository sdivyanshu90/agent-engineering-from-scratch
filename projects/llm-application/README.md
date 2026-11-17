# Milestone 3 — reliable model boundary

[models.py](../../forgeagent/models.py) and [llm_app.py](../../forgeagent/llm_app.py)
extend the same ForgeAgent package. They add typed provider requests/replies,
strict classification, version identity, normalized stream assembly, bounded
recovery, local admission and configurable accounting. No agent loop exists yet.

```sh
python -m unittest tests.integration.test_llm_app -v
python labs/week-05/checks.py --day 4
```

Core tests are offline. The optional Pydantic comparison uses:

```sh
uv sync --locked --extra schemas
uv run python -m unittest tests.integration.test_llm_app.SchemaComparisonTests -v
```

Attempt the first-principles validator before reading the library comparison.
The strict raw parser rejects duplicates; Pydantic's raw JSON behavior is distinct.

A live nonstreaming adapter is available only by explicitly constructing
OpenAIResponses(key,allow_live=True) and supplying a currently accessible model.
Never commit a key. This may incur charges and was not exercised in the build;
ordinary tests inject a transport and never call a paid model. The endpoint is
fixed HTTPS, redirects reject, reads are bounded and error bodies are not logged.
Socket timeout/thread cancellation do not guarantee remote computation stopped.

Streaming here uses a normalized async delta/done protocol, not a live provider
SSE bridge. RateGate is local request spacing, not distributed/token quota.
Cost uses hypothetical caller-supplied rates, not current provider pricing or
spend enforcement. Classification shape does not establish correct labels or
permission to execute anything. Those boundaries are taught in the six chapters.
