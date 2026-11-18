# Week 11 deployment drill

The `deploy/` image starts a **demonstration handler**, not a coding agent. It
only returns the number of input characters. It therefore validates the service
boundary without performing tools or calling a paid model. The app requires a
bearer secret, an owner ID, and an absolute database path at startup. Never use a
real credential for this local drill.

From the repository root, with Docker Compose installed and running:

```sh
export FORGEAGENT_TOKEN='local-disposable-token'
export FORGEAGENT_OWNER='learner'
docker compose -f deploy/compose.yaml up --build -d
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/sessions/demo/jobs \
  -H "Authorization: Bearer $FORGEAGENT_TOKEN" -H 'Content-Type: application/json' \
  -d '{"input":"hello"}'
docker compose -f deploy/compose.yaml restart
```

Use the returned job ID with `GET /jobs/{job_id}` and the same authorization
header; check the record survives restart. Inspect only safe logs with
`docker compose -f deploy/compose.yaml logs`. Stop with `docker compose -f
deploy/compose.yaml down`; the named volume remains until deliberately removed.
The named volume must be writable by UID 10001. Secret environment variables are
visible to sufficiently privileged host users; use a managed secret mechanism in
a real deployment. Bind to loopback for this exercise. Production requires TLS,
credential rotation, durable backups, centralized shared admission controls,
monitoring, and a reviewed tool sandbox. SQLite here is a single-host example,
not a distributed queue. A recovered lease can retry a side effect; use
idempotency and reconciliation, not an assumption of exactly-once execution.
