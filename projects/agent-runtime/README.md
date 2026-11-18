# ForgeAgent bounded runtime

ForgeAgent is a small asynchronous reference implementation for Week 7. The
runtime accepts a `Provider`, a registry of local `Tool` handlers, an explicit
tool allowlist and finite `Budgets`. `FakeProvider` makes every educational
example deterministic and offline. The optional model adapter lives behind the
existing provider interface; importing the runtime does not make a network call.

## Run locally

From the repository root, install the project in its documented environment,
then run a selected Week 7 lab or `python -m unittest tests.integration.test_runtime`.
The exam and labs use only fake providers and local handlers. No real account or
credentials are needed.

## Runtime contract

Model output must be JSON in one of two exact forms: a finish answer or a list
of tool calls with unique IDs and explicit dependency IDs. The supported input
schema subset is a closed object with string, integer or boolean properties.
Unknown fields and Python bool-as-int coercion are rejected. Discovery filters
the declared tools, and the dispatcher checks authorization again before a
handler runs. Writes need a separate run-level grant.

The dispatcher validates the complete call graph before acting. Independent
read calls in one layer may run concurrently. Any layer containing a write is
serialized. Tool outputs are JSON encoded and bounded before becoming untrusted
observations. The model is asked not to emit private reasoning; observable
decisions and tool events are sufficient to reconstruct the control flow.

Budgets bound steps, proposed tools, reported tokens, known cost, total time and
per-tool time. A provider response may complete and report usage beyond the
remaining local allowance. The loop charges that usage and blocks subsequent
effects, but cannot undo a billed call or guarantee a hard spend limit. Caller
cancellation propagates. Expected tool failures become observations; unexpected
programming exceptions propagate for diagnosis.

## Limits

This is an instructional process-local dispatcher. A tool declaration is not
a sandbox, schema validation is not authorization, and a read label is not a
proof of purity. The runtime does not supply distributed transactions,
idempotency, provider-side spending limits, durable checkpoints, or isolation
from handler filesystem/network access. Production deployments must enforce
those boundaries outside this sample and review each handler independently.
