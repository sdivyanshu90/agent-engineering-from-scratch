import asyncio


async def collect(operations):
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(operation()) for operation in operations]
    return [task.result() for task in tasks]
