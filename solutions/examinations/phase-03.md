# Phase 3 reference defense

Use fixed25/30/25/20 allocation and problem subpoints. References:
[model boundary](../../forgeagent/models.py), [application](../../forgeagent/llm_app.py),
[retrieval](../../forgeagent/retrieval.py), [grounding](../../forgeagent/grounding.py).
Attempt before reading; importing central solutions earns no independent code credit.

Request correctness preserves model/roles/settings/version. Strict output rejects
duplicate/extra/wrong fields; completed provider status does not prove content
truth. Stream success requires terminal evidence and exhaustion; cancellation
cleans up and propagates. Recovery encloses all attempts/backoff within one
deadline. Unknown HTTP outcome is not proof no effect or charge occurred.

Chunk IDs associate path/revision/span. BM25 uses exact declared tf/df/IDF/query
conventions; cosine requires compatible finite nonzero vectors. ANN recall loss
can occur before distance/reranking. Rank fusion must reject within-list duplicates.
Metric judgments use the declared document/chunk unit, cutoff and gain. Preserve
empty cases and fixed denominators rather than discarding inconvenient queries.

The quote-only model path accepts only supplied selected snapshot IDs, matching
revision and exact nonempty quote. Answer must consist entirely of those quotes;
a paraphrase is deliberately outside this mechanical contract. A correct-looking
citation to a real irrelevant passage exposes the difference between occurrence
and useful support. Neither source occurrence nor model instruction authorizes
an effectful command. No-evidence retrieval skips the provider and returns explicit
abstention; citation all(empty) alone cannot measure usefulness.

Hypothetical rates need per-million units and Decimal arithmetic; absent usage
on a failed attempt is unknown. Visible teaching fixtures are regression data,
not secure held-out evaluations. A complete diagram should mark local rate gate,
nonstreaming live adapter versus normalized stream, and missing production controls
such as multi-tenant authorization, total token budgets, durable execution, sandbox,
telemetry and deployment. All results must have execution evidence and scope.
