# Week 11 labs — authenticated durable service

Work independently under `learner-work/week-11/`. Copy each starter, implement
the stated contract, run its public check, then read the reference and reasoning
after writing down your own expected result. `python labs/week-11/checks.py
--day N` checks the complete reference; `--day N --module
learner-work/week-11/name.py` checks your attempt. No paid API, network service,
database server, or GPU is required. Days 1–5 use only Python's standard
library. The optional API integration tests use an in-process ASGI transport.

| Day | Starter | Required contract |
|---|---|---|
| 1 | `ownership.py` | Trusted token lookup; owner-scoped row lookup; bounded session/input validation. |
| 2 | `worker.py` | Async ordered execution with a concurrency cap; propagate cancellation. |
| 3 | `leases.py` | Claim queued/expired work, increment attempts, fence stale finishes. |
| 4 | `telemetry.py` | Allowlist safe fields; calculate durations and histogram buckets. |
| 5 | `limits.py` | Deterministic token bucket, capacity arithmetic, known cost estimate. |
| 6 | `deployment.py` | Validate required secret/path and disclose single-host boundaries. |

Run `python -m unittest tests.integration.test_service
tests.integration.test_workers` with the optional `service` extra for API auth,
owner isolation, idempotency, worker faults, cancellation, lease recovery, and
restart behavior. The tests use only local fixtures. If no Docker/Podman binary
is available, do static Day 6 checks and explicitly mark the image drill
untested. Do not report a successful container build without actually building
and starting it.

Submission: completed source, one worked numerical capacity trace, two added
edge tests, and one reproduced/fixed failure. Explain what a lease can recover,
what a cancellation flag can request, and why neither reverses a completed
external effect.
