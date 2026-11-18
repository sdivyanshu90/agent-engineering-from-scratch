# ForgeAgent capstone

ForgeAgent is a framework-free teaching system that composes the repository's
runtime, policy, context selection, durable journal, MCP client, evaluation,
telemetry, and service adapter. The coding module intentionally gives a model a
small interface: search, bounded file read, revision-bound evidence retrieval, exact patch
proposal, and a fixed test request. A human must review and authorize a proposal through a
separate callback. The agent has no generic shell or approval tool.

## Run

```text
python -m forgeagent --help
python scripts/demo_forgeagent.py
python labs/week-12/checks.py --day 1
python scripts/validate_exercises.py
```

The demo uses a scripted offline provider and a temporary repository fixture.
It demonstrates protocol flow and does not claim real-model autonomous coding
quality. Test execution requires an explicitly selected backend. The Linux
Bubblewrap backend is available for reviewed fixtures. See [architecture](ARCHITECTURE.md), [decisions](DECISIONS.md),
and [limitations](LIMITATIONS.md).

## Integration

`CodingSession(provider, Workspace(root), owner=..., session_id=...,
test_backend=..., journal=...)` assembles the registered tools. Pass a real
provider through the `Provider` protocol from `forgeagent.models`. Keep
`Workspace` rooted to a caller-authorized tree. Use `CodingSession.run(task)`
for a new run and `resume=True` only with the same task, model, registry, owner,
and session. Runtime snapshots preserve pending calls and budgets. Workspace
proposal receipts are stored in journal snapshots and restore without approval,
so the human must review again. Apply uses a durable intent and current before/
after hashes to avoid blind replay.

For an MCP server, create a `StdioClient` explicitly and call
`session.attach_mcp(client, allowlist=..., read_only=...)`. Only allowlisted
read-only schemas in the runtime's closed primitive subset are registered.
Close the client when the session ends. The provider sees tool output as
untrusted observations. See [system design](ARCHITECTURE.md) for limits.

## Verify execution and service integration

Use `python scripts/demo_forgeagent.py --interactive` to review the generated
fixture replacement yourself. On Linux with Bubblewrap and unprivileged
namespaces, add `--isolated` to run its actual unittest after approval.
`python scripts/verify_linux_isolation.py` tests the environment, mounts,
network namespace and read-only workspace using a disposable fixture.
Use both checks to distinguish behavior of the sandbox from behavior of the
scripted provider.

The authenticated API uses the Week 11 character-count handler by default.
An operator setting an absolute `FORGEAGENT_WORKSPACE` enables read-only
repository evidence mode. Jobs invoke the custom runtime and the Week 6
BM25 extractive baseline, returning the quote, file path, line range and
revision in the terminal job result. HTTP exposes no patch approval or
test operations. Use an owned corpus and configure its mount as read-only.

```sh
docker build -t forgeagent-mastery:validation -f deploy/Dockerfile .
bash scripts/verify_container.sh
```

The smoke uses an ephemeral container with no external network and a disposable
credential. It checks unauthenticated rejection, authenticated job admission,
and a revision-bound citation to the bundled public corpus. See the
[deployment drill](OPERATIONS.md) for the default container and persistence
setup.

For an optional hosted-model experiment, initialize the Week 5
`OpenAIResponses` provider with `allow_live=True` and pass it to
`CodingSession` with a model ID available to your account. Start with
`read_only=True` and the bundled public corpus. Source passages and user tasks
are sent to the provider, and usage can incur charges. Keep credentials outside
the workspace. The offline grader does not estimate hosted-model performance.
