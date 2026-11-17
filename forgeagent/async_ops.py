"""Bounded retries for explicitly transient failures; cancellation propagates."""
import asyncio
import math


class TransientError(Exception):
    """An adapter explicitly labels a failure as eligible for retry."""


async def retry(operation, *, attempts=3, timeout=1.0, base_delay=0.05, sleep=asyncio.sleep):
    if type(attempts) is not int or attempts < 1:
        raise ValueError("attempts must be a positive integer")
    if not math.isfinite(timeout) or timeout <= 0 or not math.isfinite(base_delay) or base_delay < 0:
        raise ValueError("timeout/delay must be finite with timeout>0, delay>=0")
    for attempt in range(attempts):
        try:
            async with asyncio.timeout(timeout):
                return await operation()
        except TransientError:
            if attempt + 1 == attempts:
                raise
            await sleep(base_delay * 2 ** attempt)
    raise RuntimeError("unreachable")
