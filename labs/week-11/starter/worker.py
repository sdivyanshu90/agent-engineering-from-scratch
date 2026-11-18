"""D62 starter: a small async worker pool with bounded active handlers."""
import asyncio


async def run_many(jobs, handler, concurrency):
    """Return handler results in input order; allow at most concurrency active."""
    raise NotImplementedError
