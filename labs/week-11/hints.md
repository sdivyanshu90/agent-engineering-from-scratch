# Week 11 hints

For each day use the first hint before opening the next. The executable reference
is in `solutions/labs/week-11/`; compare it only after your independent attempt.

1. **Ownership.** Concept: identity comes from a trusted credential, never the job body. Algorithm: reject bad credentials before an owner-scoped lookup. Implementation: parse the bearer scheme and compare the mapped owner against the row owner.
2. **Workers.** Concept: admission and execution are different bounds. Algorithm: acquire a permit around each awaited handler. Implementation: use `asyncio.Semaphore` and `gather`, preserving order and allowing cancellation to propagate.
3. **Leases.** Concept: an expired worker may still return. Algorithm: assign a new fencing token to each claim and check it at finish. Implementation: update state, deadline and attempt count together; reject mismatched tokens.
4. **Telemetry.** Concept: logs are a separate data exposure surface. Algorithm: copy only approved fields and derive durations from timestamps. Implementation: use a fixed field allowlist and choose the first inclusive histogram boundary.
5. **Limits.** Concept: a token bucket refills over elapsed time up to its capacity. Algorithm: refill, clamp, and spend only if one token exists. Implementation: inject time for deterministic tests; express price per million tokens.
6. **Deployment.** Concept: secrets must exist before startup and durable files need a persistent path. Algorithm: reject missing credentials and relative database paths. Implementation: validate `FORGEAGENT_TOKEN` and `FORGEAGENT_DATABASE` without returning the token itself.
