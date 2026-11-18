"""Optional FastAPI ASGI tests; no network, model, container, or paid calls."""
import asyncio
import tempfile
import time
import unittest
from pathlib import Path

try:
    import httpx
    from forgeagent.service import create_app
except ImportError as error:  # core-only installs keep this module discoverable
    httpx = None
    create_app = None
    IMPORT_ERROR = error
else:
    IMPORT_ERROR = None


@unittest.skipIf(httpx is None, "install the optional service extra")
class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "jobs.sqlite3"

    def tearDown(self):
        self.temp.cleanup()

    def run_async(self, coroutine):
        return asyncio.run(coroutine)

    def test_auth_owner_isolation_and_idempotency(self):
        async def scenario():
            async def handler(owner, session, text):
                return {"owner": owner, "session": session, "length": len(text)}

            app = create_app(database_path=self.database,
                             tokens={"token-a": "alice", "token-b": "bob"},
                             run_handler=handler, poll_seconds=0.01)
            async with app.router.lifespan_context(app):
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),
                                             base_url="http://test") as client:
                    self.assertEqual((await client.get("/health")).status_code, 200)
                    denied = await client.post("/sessions/s1/jobs", json={"input": "x"})
                    self.assertEqual(denied.status_code, 401)
                    headers = {"Authorization": "Bearer token-a", "Idempotency-Key": "request-9"}
                    first = await client.post("/sessions/s1/jobs", headers=headers,
                                              json={"input": "private prompt"})
                    replay = await client.post("/sessions/s1/jobs", headers=headers,
                                               json={"input": "private prompt"})
                    self.assertEqual(first.status_code, 202)
                    self.assertEqual(first.json()["job_id"], replay.json()["job_id"])
                    conflict = await client.post("/sessions/s1/jobs", headers=headers,
                                                 json={"input": "changed prompt"})
                    self.assertEqual(conflict.status_code, 409)
                    job_id = first.json()["job_id"]
                    bob = {"Authorization": "Bearer token-b"}
                    self.assertEqual((await client.get(f"/jobs/{job_id}", headers=bob)).status_code, 404)
                    self.assertEqual((await client.delete(f"/jobs/{job_id}", headers=bob)).status_code, 404)
                    observed = None
                    for _ in range(100):
                        response = await client.get(f"/jobs/{job_id}", headers={"Authorization": "Bearer token-a"})
                        observed = response.json()
                        if observed["status"] in {"succeeded", "failed"}:
                            break
                        await asyncio.sleep(0.01)
                    self.assertEqual(observed["status"], "succeeded")
                    self.assertEqual(observed["result"], {"owner": "alice", "session": "s1", "length": 14})
                    self.assertNotIn("input", observed)
                    foreign_session = await client.get("/sessions/s1/jobs", headers=bob)
                    self.assertEqual(foreign_session.json()["jobs"], [])

        self.run_async(scenario())

    def test_handler_fault_and_running_cancellation(self):
        async def scenario():
            entered = asyncio.Event()
            release = asyncio.Event()

            async def handler(owner, session, text):
                if text == "explode":
                    raise RuntimeError("private prompt and traceback must not escape")
                entered.set()
                await release.wait()
                return {"done": True}

            app = create_app(database_path=self.database, tokens={"secret": "owner"},
                             run_handler=handler, poll_seconds=0.01)
            auth = {"Authorization": "Bearer secret"}
            async with app.router.lifespan_context(app):
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),
                                             base_url="http://test") as client:
                    failed = await client.post("/sessions/s/jobs", headers=auth,
                                               json={"input": "explode"})
                    failure = None
                    for _ in range(100):
                        failure = (await client.get("/jobs/" + failed.json()["job_id"], headers=auth)).json()
                        if failure["status"] == "failed":
                            break
                        await asyncio.sleep(0.01)
                    self.assertEqual(failure["error_code"], "handler_failed")
                    self.assertNotIn("private", str(failure))

                    running = await client.post("/sessions/s/jobs", headers=auth,
                                                json={"input": "wait"})
                    await asyncio.wait_for(entered.wait(), timeout=1)
                    cancelled = await client.delete("/jobs/" + running.json()["job_id"], headers=auth)
                    self.assertEqual(cancelled.status_code, 202)
                    final = None
                    for _ in range(100):
                        final = (await client.get("/jobs/" + running.json()["job_id"], headers=auth)).json()
                        if final["status"] == "cancelled":
                            break
                        await asyncio.sleep(0.01)
                    self.assertEqual(final["status"], "cancelled")
                    release.set()

        self.run_async(scenario())


if __name__ == "__main__":
    unittest.main()
