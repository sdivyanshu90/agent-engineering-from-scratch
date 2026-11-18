# Week 11 — Authenticated services and operations

Prerequisite: Week 10's security and observability gate, plus Week 8 durable
state. This week creates the production-facing boundary around an injected async
agent runner. The included reference is optional: install `.[service]` for
FastAPI, ASGI tests, and the OpenTelemetry SDK. Core curriculum examples and
labs remain runnable with the Python standard library.

| Day | Chapter | Main artifact |
|---|---|---|
| D61 | [FastAPI, authentication, and session ownership](day-01/README.md) | Bearer identity and owner-scoped API |
| D62 | [Async APIs, queues, workers, and cancellation](day-02/README.md) | Bounded async job admission and execution |
| D63 | [Persistent execution and concurrency control](day-03/README.md) | SQLite transitions, leases, fencing, recovery |
| D64 | [Structured logs, traces, metrics, and OpenTelemetry](day-04/README.md) | Redacted telemetry and in-memory span |
| D65 | [Rate limits, performance, and cost observability](day-05/README.md) | Token bucket, capacity, estimate |
| D66 | [Docker, secrets, deployment, and recovery](day-06/README.md) | Nonroot container and operations runbook |

Use the [labs](../../labs/week-11/README.md), [weekly review](weekly-review.md),
[100-point exam](../../assessments/weekly/week-11.md), and answer reasoning
(../../solutions/examinations/week-11.md). The service accepts a trusted
token-to-owner mapping and an injected async handler. It does not import or
invoke a provider by itself. Use fake handlers for local tests; no model API,
container engine, or live telemetry collector is required to complete the core
learning outcomes.

Estimated effort: 42–54 hours, including a local recovery drill. The service
uses SQLite for a single-host reference deployment. A fleet requires shared
storage and shared rate limiting. A job lease makes recovery possible but does
not make remote effects exactly once; consult Week 8 operation receipts before
replaying uncertain tool actions.
