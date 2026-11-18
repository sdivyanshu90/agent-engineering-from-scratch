#!/usr/bin/env bash
# Smoke test for the local pinned ForgeAgent image. Run from the repository root.
set -euo pipefail
container=$(docker run --rm --detach --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --tmpfs /tmp --tmpfs /data:uid=10001,gid=10001,mode=700 \
  --mount type=bind,src="$PWD/datasets/sample-data",dst=/workspace,readonly \
  -e FORGEAGENT_OWNER=learner -e FORGEAGENT_TOKEN=disposable-fixture-token \
  -e FORGEAGENT_WORKSPACE=/workspace forgeagent-mastery:validation)
trap 'docker stop -t 3 "$container" >/dev/null 2>&1 || true' EXIT
docker exec -i "$container" /opt/forge/bin/python - <<'PY'
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

base = "http://127.0.0.1:8000"
def call(path, *, authorized=True, input=None):
    headers = {"Authorization": "Bearer disposable-fixture-token"} if authorized else {}
    body = None
    if input is not None:
        body = json.dumps({"input": input}).encode()
        headers["Content-Type"] = "application/json"
    with urlopen(Request(base + path, headers=headers, data=body), timeout=2) as response:
        return response.status, json.load(response)

for _ in range(25):
    try:
        assert call("/health", authorized=False)[0] == 200
        break
    except URLError:
        time.sleep(0.2)
else:
    raise AssertionError("service failed readiness")
try:
    call("/sessions/demo/jobs", authorized=False, input="agents")
except HTTPError as exc:
    assert exc.code == 401
else:
    raise AssertionError("unauthorized request entered service")
code, job = call("/sessions/demo/jobs", input="agents")
assert code == 202, job
for _ in range(25):
    _, job = call("/jobs/" + job["job_id"])
    if job["status"] == "succeeded":
        break
    assert job["status"] in ("queued", "running"), job
    time.sleep(0.2)
else:
    raise AssertionError(job)
evidence = job["result"]["evidence"]
assert evidence["citations"][0]["path"] == "agents.txt", evidence
assert len(evidence["citations"][0]["revision"]) == 64
print("Container smoke passed: health, unauthorized denial, queued run, revision-bound evidence.")
PY
