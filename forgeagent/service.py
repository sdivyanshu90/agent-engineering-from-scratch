"""Optional authenticated ASGI service for durable, owner-scoped agent jobs.

Install the ``service`` extra before importing this module.  The SQLite job
store is intentionally independent of an agent implementation: applications
inject an async run_handler and may wrap Week 8's EventJournal around it.
"""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, closing
from dataclasses import dataclass
import hmac
import json
import logging
import math
from pathlib import Path
import secrets
import sqlite3
import time
from typing import Awaitable, Callable, Mapping
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from .workers import TokenBucket, WorkerGroup


LOGGER = logging.getLogger("forgeagent.service")
TERMINAL = {"succeeded", "failed", "cancelled"}


class JobInput(BaseModel):
    input: str = Field(min_length=1, max_length=4000)


@dataclass(frozen=True)
class Job:
    job_id: str
    owner: str
    session_id: str
    state: str
    created_at: float
    updated_at: float
    attempts: int
    result: object = None
    error_code: str | None = None


class AdmissionError(ValueError):
    """A bounded queue or per-owner quota rejected admission."""


class JobStore:
    """Small SQLite queue with atomic claims and renewable worker leases.

    Connections are per-operation and database transactions are short. A
    crashed worker's expired lease makes the job claimable again. Handler side
    effects still need Week 8 idempotency keys/reconciliation: leases alone do
    not promise exactly-once execution.
    """

    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path == ":memory:":
            raise ValueError("use a file-backed database for recovery")
        with closing(self._connect()) as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY, owner TEXT NOT NULL,
                    session_id TEXT NOT NULL, input_text TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN
                      ('queued','running','succeeded','failed','cancelled')),
                    created_at REAL NOT NULL, updated_at REAL NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0, lease_until REAL,
                    lease_token TEXT,
                    cancel_requested INTEGER NOT NULL DEFAULT 0,
                    result_json TEXT, error_code TEXT,
                    idempotency_key TEXT
                );
                CREATE INDEX IF NOT EXISTS jobs_owner_created
                  ON jobs(owner, created_at DESC);
                CREATE INDEX IF NOT EXISTS jobs_claim
                  ON jobs(state, lease_until, created_at);
                CREATE TABLE IF NOT EXISTS job_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL, state TEXT NOT NULL,
                    at REAL NOT NULL, detail TEXT
                );
            """)

    def _connect(self):
        connection = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _job(row):
        return Job(row["job_id"], row["owner"], row["session_id"], row["state"],
                   row["created_at"], row["updated_at"], row["attempts"],
                   json.loads(row["result_json"]) if row["result_json"] is not None else None,
                   row["error_code"])

    def enqueue(self, owner: str, session_id: str, input_text: str,
                max_pending: int, idempotency_key: str | None = None) -> Job:
        now = time.time()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            if idempotency_key is not None:
                existing = connection.execute("SELECT * FROM jobs WHERE owner=? AND session_id=? AND idempotency_key=?",
                                              (owner, session_id, idempotency_key)).fetchone()
                if existing is not None:
                    connection.commit()
                    if existing["input_text"] != input_text:
                        raise AdmissionError("idempotency_key_conflict")
                    return self._job(existing)
            pending = connection.execute(
                "SELECT count(*) FROM jobs WHERE owner=? AND state IN ('queued','running')",
                (owner,)).fetchone()[0]
            if pending >= max_pending:
                connection.rollback()
                raise AdmissionError("owner_pending_limit")
            identifier = uuid4().hex
            connection.execute("INSERT INTO jobs(job_id,owner,session_id,input_text,state,created_at,updated_at,idempotency_key) VALUES(?,?,?,?,?,?,?,?)",
                               (identifier, owner, session_id, input_text, "queued", now, now, idempotency_key))
            connection.execute("INSERT INTO job_events(job_id,state,at) VALUES(?,?,?)",
                               (identifier, "queued", now))
            connection.commit()
        return self.get_for_owner(identifier, owner)

    def claim(self, lease_seconds: float) -> tuple[Job, str] | None:
        now = time.time()
        lease_token = secrets.token_hex(16)
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("""SELECT * FROM jobs
                WHERE cancel_requested=0 AND
                  (state='queued' OR (state='running' AND lease_until < ?))
                ORDER BY created_at, job_id LIMIT 1""", (now,)).fetchone()
            if row is None:
                connection.commit()
                return None
            connection.execute("""UPDATE jobs SET state='running',updated_at=?,
                attempts=attempts+1,lease_until=?,lease_token=? WHERE job_id=?""",
                               (now, now + lease_seconds, lease_token, row["job_id"]))
            connection.execute("INSERT INTO job_events(job_id,state,at,detail) VALUES(?,?,?,?)",
                               (row["job_id"], "running", now, "lease_claimed"))
            claimed = connection.execute("SELECT * FROM jobs WHERE job_id=?",
                                         (row["job_id"],)).fetchone()
            connection.commit()
        return self._job(claimed), lease_token

    def renew(self, job_id: str, lease_token: str, lease_seconds: float) -> bool:
        now = time.time()
        with closing(self._connect()) as connection:
            cursor = connection.execute("UPDATE jobs SET lease_until=? WHERE job_id=? AND state='running' AND lease_token=?",
                                        (now + lease_seconds, job_id, lease_token))
        return cursor.rowcount == 1

    def cancellation_requested_for_lease(self, job_id: str, lease_token: str) -> bool | None:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT cancel_requested FROM jobs WHERE job_id=? AND state='running' AND lease_token=?",
                                     (job_id, lease_token)).fetchone()
        return None if row is None else bool(row[0])

    def finish(self, job_id: str, lease_token: str, *, result=None,
               error_code=None, cancelled=False):
        now = time.time()
        state = "cancelled" if cancelled else ("failed" if error_code else "succeeded")
        encoded = None if error_code or cancelled else json.dumps(
            result, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT state,cancel_requested FROM jobs WHERE job_id=? AND lease_token=?",
                                     (job_id, lease_token)).fetchone()
            if row is None or row["state"] != "running":
                connection.rollback()
                return False
            if row["cancel_requested"]:
                state, encoded, error_code = "cancelled", None, None
            connection.execute("UPDATE jobs SET state=?,updated_at=?,lease_until=NULL,lease_token=NULL,result_json=?,error_code=? WHERE job_id=?",
                               (state, now, encoded, error_code, job_id))
            connection.execute("INSERT INTO job_events(job_id,state,at,detail) VALUES(?,?,?,?)",
                               (job_id, state, now, error_code))
            connection.commit()
        return True

    def request_cancel(self, job_id: str, owner: str) -> Job | None:
        now = time.time()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT * FROM jobs WHERE job_id=? AND owner=?",
                                     (job_id, owner)).fetchone()
            if row is None:
                connection.rollback()
                return None
            if row["state"] == "queued":
                state, cancel_requested = "cancelled", 1
            elif row["state"] == "running":
                state, cancel_requested = "running", 1
            else:
                state, cancel_requested = row["state"], row["cancel_requested"]
            if state != row["state"] or cancel_requested != row["cancel_requested"]:
                connection.execute("UPDATE jobs SET state=?,cancel_requested=?,updated_at=? WHERE job_id=?",
                                   (state, cancel_requested, now, job_id))
                connection.execute("INSERT INTO job_events(job_id,state,at,detail) VALUES(?,?,?,?)",
                                   (job_id, state, now, "cancel_requested"))
            updated = connection.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            connection.commit()
        return self._job(updated)

    def cancellation_requested(self, job_id: str) -> bool:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT cancel_requested FROM jobs WHERE job_id=?",
                                     (job_id,)).fetchone()
        return bool(row and row[0])

    def get_for_owner(self, job_id: str, owner: str) -> Job | None:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM jobs WHERE job_id=? AND owner=?",
                                     (job_id, owner)).fetchone()
        return None if row is None else self._job(row)

    def session_jobs(self, owner: str, session_id: str, limit=50) -> list[Job]:
        with closing(self._connect()) as connection:
            rows = connection.execute("SELECT * FROM jobs WHERE owner=? AND session_id=? ORDER BY created_at DESC LIMIT ?",
                                      (owner, session_id, limit)).fetchall()
        return [self._job(row) for row in rows]


def _public(job: Job):
    return {"job_id": job.job_id, "session_id": job.session_id,
            "status": job.state, "created_at": job.created_at,
            "updated_at": job.updated_at, "attempts": job.attempts,
            "result": job.result, "error_code": job.error_code}


def _safe_log(event: str, *, state: str | None = None, attempt: int | None = None):
    """Emit only reviewed low-cardinality fields; omit owner/session/input/IDs."""
    fields = {"event": event}
    if state is not None:
        fields["state"] = state
    if attempt is not None:
        fields["attempt"] = attempt
    LOGGER.info(event, extra=fields)


def create_app(*, database_path: str | Path,
               tokens: Mapping[str, str],
               run_handler: Callable[[str, str, str], Awaitable[object]],
               worker_count: int = 2, max_pending_per_owner: int = 8,
               rate_per_minute: int = 30, lease_seconds: float = 60.0,
               poll_seconds: float = 0.1) -> FastAPI:
    """Create an authenticated jobs API. `tokens` maps secrets to owner IDs."""
    if not tokens or any(not secret or not owner for secret, owner in tokens.items()):
        raise ValueError("configure at least one token to owner mapping")
    if worker_count < 1 or max_pending_per_owner < 1 or rate_per_minute < 1:
        raise ValueError("worker and admission bounds must be positive")
    if not math.isfinite(lease_seconds) or lease_seconds <= 0 or poll_seconds <= 0:
        raise ValueError("lease and poll durations must be positive")
    store = JobStore(database_path)
    limiter = TokenBucket(rate_per_minute)
    active: dict[str, asyncio.Task] = {}
    stop = asyncio.Event()
    group = WorkerGroup(lambda index: worker(index), worker_count)

    async def worker(number: int):
        while not stop.is_set():
            claimed = await asyncio.to_thread(store.claim, lease_seconds)
            if claimed is None:
                try:
                    await asyncio.wait_for(stop.wait(), timeout=poll_seconds)
                except TimeoutError:
                    pass
                continue
            job, lease_token = claimed
            _safe_log("job_started", state="running", attempt=job.attempts)
            async def invoke():
                input_text = await asyncio.to_thread(_input_for_job, store, job.job_id)
                return await run_handler(job.owner, job.session_id, input_text)

            run_task = asyncio.create_task(invoke(), name="forgeagent-job-handler")
            active[job.job_id] = run_task
            async def renew_lease():
                while True:
                    await asyncio.sleep(max(0.05, lease_seconds / 3))
                    cancelled = await asyncio.to_thread(
                        store.cancellation_requested_for_lease, job.job_id, lease_token)
                    if cancelled is None:
                        run_task.cancel()
                        return
                    if cancelled:
                        run_task.cancel()
                        return
                    still_owned = await asyncio.to_thread(store.renew, job.job_id,
                                                          lease_token, lease_seconds)
                    if not still_owned:
                        run_task.cancel()
                        return

            heartbeat = asyncio.create_task(renew_lease(), name="forgeagent-job-lease")
            try:
                result = await run_task
                json.dumps(result, allow_nan=False)
                await asyncio.to_thread(store.finish, job.job_id, lease_token,
                                         result=result)
                _safe_log("job_finished", state="succeeded")
            except asyncio.CancelledError:
                if stop.is_set():
                    # A process shutdown is not a user cancellation. Leave the
                    # lease to expire so another replica can retry the job.
                    raise
                await asyncio.to_thread(store.finish, job.job_id, lease_token,
                                         cancelled=True)
            except (Exception,):
                # Don't put exception strings or user content into logs/API.
                _safe_log("job_failed", state="failed")
                await asyncio.to_thread(store.finish, job.job_id, lease_token,
                                         error_code="handler_failed")
            finally:
                heartbeat.cancel()
                await asyncio.gather(heartbeat, return_exceptions=True)
                active.pop(job.job_id, None)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        stop.clear()
        tasks = group.start()
        app.state.worker_tasks = tasks
        try:
            yield
        finally:
            stop.set()
            await group.stop()
            app.state.worker_tasks = []

    app = FastAPI(title="ForgeAgent Jobs API", version="1.0", lifespan=lifespan)
    app.state.job_store = store
    app.state.worker_tasks = []

    async def authenticate(authorization: str | None = Header(default=None)) -> str:
        scheme, _, credential = (authorization or "").partition(" ")
        if scheme.lower() != "bearer" or not credential:
            raise HTTPException(status_code=401, detail="authentication_required",
                                headers={"WWW-Authenticate": "Bearer"})
        owner = None
        for configured, configured_owner in tokens.items():
            if hmac.compare_digest(credential, configured):
                owner = configured_owner
        if owner is None:
            raise HTTPException(status_code=401, detail="invalid_credentials",
                                headers={"WWW-Authenticate": "Bearer"})
        return owner

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.post("/sessions/{session_id}/jobs", status_code=202)
    async def submit(session_id: str, body: JobInput, request: Request,
                     owner: str = Depends(authenticate)):
        if not 1 <= len(session_id) <= 128:
            raise HTTPException(status_code=422, detail="invalid_session_id")
        idempotency_key = request.headers.get("Idempotency-Key")
        if idempotency_key is not None and (not 1 <= len(idempotency_key) <= 128 or
                                             any(ord(ch) < 33 for ch in idempotency_key)):
            raise HTTPException(status_code=400, detail="invalid_idempotency_key")
        if not await limiter.take(owner):
            raise HTTPException(status_code=429, detail="rate_limit_exceeded",
                                headers={"Retry-After": "2"})
        try:
            job = await asyncio.to_thread(store.enqueue, owner, session_id,
                                          body.input, max_pending_per_owner,
                                          idempotency_key)
        except AdmissionError as error:
            if str(error) == "idempotency_key_conflict":
                raise HTTPException(status_code=409, detail="idempotency_key_conflict") from None
            raise HTTPException(status_code=429, detail="pending_job_limit") from None
        _safe_log("job_accepted", state="queued")
        return _public(job)

    @app.get("/sessions/{session_id}/jobs")
    async def list_jobs(session_id: str, owner: str = Depends(authenticate)):
        return {"jobs": [_public(job) for job in
                          await asyncio.to_thread(store.session_jobs, owner, session_id)]}

    @app.get("/jobs/{job_id}")
    async def get_job(job_id: str, owner: str = Depends(authenticate)):
        job = await asyncio.to_thread(store.get_for_owner, job_id, owner)
        if job is None:
            raise HTTPException(status_code=404, detail="job_not_found")
        return _public(job)

    @app.delete("/jobs/{job_id}")
    async def cancel_job(job_id: str, response: Response,
                         owner: str = Depends(authenticate)):
        job = await asyncio.to_thread(store.request_cancel, job_id, owner)
        if job is None:
            raise HTTPException(status_code=404, detail="job_not_found")
        task = active.get(job_id)
        if task is not None and job.state == "running":
            task.cancel()
        response.status_code = status.HTTP_202_ACCEPTED
        return _public(job)

    return app


def _input_for_job(store: JobStore, job_id: str) -> str:
    """Fetch private input only at execution time; never include in API/logs."""
    with closing(store._connect()) as connection:
        row = connection.execute("SELECT input_text FROM jobs WHERE job_id=?",
                                 (job_id,)).fetchone()
    if row is None:
        raise KeyError(job_id)
    return row[0]
