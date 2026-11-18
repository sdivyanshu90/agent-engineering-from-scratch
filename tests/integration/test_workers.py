"""Persistence, worker concurrency, quotas, lease fencing, and restart tests."""
import asyncio
import tempfile
import time
import unittest
from pathlib import Path

try:
    from forgeagent.service import AdmissionError, JobStore, create_app
except ImportError:
    AdmissionError = JobStore = create_app = None


@unittest.skipIf(JobStore is None, "install the optional service extra")
class WorkerStoreTests(unittest.TestCase):
    def test_admission_is_atomic_and_lease_is_fenced(self):
        with tempfile.TemporaryDirectory() as directory:
            store = JobStore(Path(directory) / "queue.sqlite3")
            first = store.enqueue("alice", "s", "one", 1, "key")
            self.assertEqual(store.enqueue("alice", "s", "one", 1, "key").job_id,
                             first.job_id)
            with self.assertRaises(AdmissionError):
                store.enqueue("alice", "s", "two", 1, "other")
            job1, lease1 = store.claim(0.04)
            self.assertEqual(job1.state, "running")
            time.sleep(0.06)
            job2, lease2 = store.claim(2)
            self.assertEqual(job1.job_id, job2.job_id)
            self.assertNotEqual(lease1, lease2)
            self.assertFalse(store.finish(job1.job_id, lease1, result={"stale": True}))
            self.assertTrue(store.finish(job2.job_id, lease2, result={"ok": True}))
            self.assertEqual(store.get_for_owner(first.job_id, "alice").result,
                             {"ok": True})
            self.assertIsNone(store.get_for_owner(first.job_id, "mallory"))

    def test_running_job_survives_service_shutdown_and_restarts(self):
        async def scenario():
            with tempfile.TemporaryDirectory() as directory:
                database = Path(directory) / "queue.sqlite3"
                entered = asyncio.Event()
                first_run = True

                async def handler(owner, session, text):
                    nonlocal first_run
                    if first_run:
                        first_run = False
                        entered.set()
                        await asyncio.Event().wait()
                    return {"recovered": True}

                app1 = create_app(database_path=database, tokens={"secret": "alice"},
                                  run_handler=handler, lease_seconds=0.2,
                                  poll_seconds=0.01)
                async with app1.router.lifespan_context(app1):
                    await asyncio.to_thread(app1.state.job_store.enqueue,
                                             "alice", "s", "payload", 3)
                    await asyncio.wait_for(entered.wait(), timeout=1)
                # Shutdown cancels in-process work but must not mark it as user
                # cancelled; the durable running lease is recoverable.
                status_after_shutdown = app1.state.job_store.session_jobs("alice", "s")[0].state
                self.assertEqual(status_after_shutdown, "running")

                app2 = create_app(database_path=database, tokens={"secret": "alice"},
                                  run_handler=handler, lease_seconds=0.2,
                                  poll_seconds=0.01)
                async with app2.router.lifespan_context(app2):
                    for _ in range(200):
                        job = app2.state.job_store.session_jobs("alice", "s")[0]
                        if job.state == "succeeded":
                            break
                        await asyncio.sleep(0.01)
                    self.assertEqual(job.state, "succeeded")
                    self.assertEqual(job.attempts, 2)

        asyncio.run(scenario())


if __name__ == "__main__":
    unittest.main()
