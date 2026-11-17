# Week 5 reference reasoning

Attempt first. Adapters reuse the actual project source rather than duplicate
policies. [models.py](../../../forgeagent/models.py) implements typed interfaces,
canonical identity, optional HTTP translation and decimal accounting;
[llm_app.py](../../../forgeagent/llm_app.py) implements request construction,
strict output, bounded recovery, normalized streaming and local admission.

1. Parse completion before text; unsupported tools/refusal cannot disappear into
   success. Mocked translation is not live-model compatibility evidence.
2. Keep trusted template separate from source, version known recipes, and hash
   all request fields canonically. Hash identity neither anonymizes nor authorizes.
3. Bound bytes, reject duplicate/extra fields, validate exact types and nonblank
   content. Pydantic strict comparison is optional and raw duplicate-key policy
   must remain explicit. Valid structure does not establish correct labels.
4. Track collecting/completed state, count aggregate UTF-8 bytes, require terminal
   evidence and reject later events. Cleanup executes in finally; cancellation
   propagates. No provider SSE bridge is claimed by normalized-event tests.
5. One timeout encloses attempts and sleeps; only classified errors retry. A
   finite policy still cannot guarantee no duplicate remote cost or effects.
6. Decimal rates are hypothetical caller configuration. Per-million units matter;
   unknown failed-call usage is not zero. Preserve all evaluation denominators.

The live HTTP adapter requires explicit opt-in, uses a fixed HTTPS endpoint,
rejects redirects, bounds response reads and suppresses secret response-body
logging. Its thread/socket timeout does not forcibly cancel a remote operation.
Ordinary tests inject transport and never use API keys or external inference.
