"""Reference: semaphore bounds active work and gather preserves order."""
import asyncio


async def run_many(jobs, handler, concurrency):
    if type(concurrency) is not int or concurrency < 1:
        raise ValueError("concurrency must be a positive integer")
    semaphore = asyncio.Semaphore(concurrency)

    async def run(job):
        async with semaphore:
            return await handler(job)

    return await asyncio.gather(*(run(job) for job in jobs))
