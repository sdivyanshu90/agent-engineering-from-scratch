import asyncio


class TransientError(Exception):
    pass


async def retry(operation, *, attempts=3, timeout=1.0, base_delay=0.05, sleep=asyncio.sleep):
    return await operation()
