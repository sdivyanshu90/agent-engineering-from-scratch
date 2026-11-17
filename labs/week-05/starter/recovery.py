import asyncio


async def call(provider,request,attempts=3,deadline=2.0,base_delay=.01,sleep=asyncio.sleep):
    return await provider.complete(request)
