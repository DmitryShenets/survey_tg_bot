from typing import AsyncIterator

from aioredis import Redis, from_url

from core.config import CONFIG

REDIS_HOST = CONFIG.REDIS_HOST
REDIS_PORT = CONFIG.REDIS_PORT
REDIS_DB = CONFIG.REDIS_DB


REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'



async def init_redis_pool() -> AsyncIterator[Redis]:
    async with from_url(f"{REDIS_URL}", encoding="utf-8", decode_responses=True) as session:
        yield session
