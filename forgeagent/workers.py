"""Async worker lifecycle and bounded process-local admission primitives.

Durable claim/retry state lives in :mod:`forgeagent.service`; this module owns
the in-process worker task group and token bucket used by the API boundary.
"""
from __future__ import annotations

import asyncio
import math
import time


class TokenBucket:
    """Per-process request bucket with finite burst and serialized updates."""

    def __init__(self, rate_per_minute: int, burst: int | None = None):
        if type(rate_per_minute) is not int or rate_per_minute < 1:
            raise ValueError("rate_per_minute must be a positive integer")
        capacity = burst if burst is not None else rate_per_minute
        if type(capacity) is not int or capacity < 1:
            raise ValueError("burst must be a positive integer")
        self.rate = rate_per_minute / 60.0
        self.capacity = float(capacity)
        self._tokens: dict[str, tuple[float, float]] = {}
        self._lock = asyncio.Lock()

    async def take(self, owner: str) -> bool:
        async with self._lock:
            now = time.monotonic()
            tokens, previous = self._tokens.get(owner, (self.capacity, now))
            tokens = min(self.capacity, tokens + max(0.0, now - previous) * self.rate)
            if tokens < 1:
                self._tokens[owner] = (tokens, now)
                return False
            self._tokens[owner] = (tokens - 1, now)
            return True


class WorkerGroup:
    """Start and stop a fixed number of worker coroutines as one lifecycle.

    Each worker owns its claim loop. Shutdown cancels those loops and awaits
    their cleanup; durable running leases are left to expire and be reclaimed.
    """

    def __init__(self, worker, count: int):
        if not callable(worker) or type(count) is not int or count < 1:
            raise ValueError("worker callable and positive count required")
        self.worker = worker
        self.count = count
        self.tasks: list[asyncio.Task] = []

    def start(self) -> list[asyncio.Task]:
        if self.tasks:
            raise RuntimeError("worker group already started")
        self.tasks = [asyncio.create_task(self.worker(index),
                                         name=f"forgeagent-worker-{index}")
                      for index in range(self.count)]
        return list(self.tasks)

    async def stop(self) -> None:
        tasks, self.tasks = self.tasks, []
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
