import asyncio
from forgeagent.llm_app import controlled_call


async def call(provider,request,attempts=3,deadline=2.0,base_delay=.01,sleep=asyncio.sleep):
    return await controlled_call(provider,request,attempts=attempts,deadline=deadline,base_delay=base_delay,sleep=sleep)
