# Milestone 2: persistent asynchronous document service

This extends the same ForgeAgent codebase: [storage](../../forgeagent/storage.py)
retains owner-scoped document text, [application](../../forgeagent/api.py) validates
and authorizes requests, and [teaching transport](../../forgeagent/http_demo.py)
frames local HTTP messages. It does not expose filesystem search to strangers.
Stored documents can later feed the same Document representation used by search.
The custom agent runtime is still unimplemented.

Run tests without a server or external network:

```sh
python -m unittest tests.integration.test_api tests.integration.test_async_math -v
```

For the local transport demo on Linux/macOS:

```sh
export FORGE_DEMO_TOKEN=local-disposable-learning-secret
python -m forgeagent.http_demo
```

On PowerShell set `$env:FORGE_DEMO_TOKEN='local-disposable-learning-secret'`, then
run the same Python module. Do not use a real credential or expose this demo
beyond loopback. In a second terminal a standard-library client can PUT and GET:

```python
import json
import urllib.request
body = json.dumps({"text": "Agents inspect evidence."}).encode("utf-8")
headers = {"Authorization": "Bearer local-disposable-learning-secret", "Content-Type": "application/json"}
request = urllib.request.Request("http://127.0.0.1:8765/documents/notes", data=body, headers=headers, method="PUT")
with urllib.request.urlopen(request, timeout=5) as response:
    print(response.status, response.read().decode())
request = urllib.request.Request("http://127.0.0.1:8765/documents/notes", headers=headers)
with urllib.request.urlopen(request, timeout=5) as response:
    print(response.status, response.read().decode())
```

Expected: `200 {"id": "notes"}`, then `200 {"id": "notes", "text": "Agents inspect evidence."}`.
Ctrl+C stops the server; the ignored SQLite file remains for restart. Missing
authentication is 401; another owner cannot see this row. The local token map
has only the learner identity; multi-owner authorization is tested in-process.

Limits: 8192 header bytes, 4096 body bytes, 2000 text code points, one request
per connection, no transfer encoding, exact application/json media type, local
HTTP only, two-second read/dispatch scope. SQLite work runs in a thread and may
commit after task cancellation. No TLS, rate/admission control, production
identity provider, optimistic versioning, queue, OS sandbox or container is
implemented. The parser intentionally supports a small HTTP/1.1 subset and must
not be used as an Internet-facing server. FastAPI and maintained transport
infrastructure are introduced in the planned production phase.
