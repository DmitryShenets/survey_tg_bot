import json
from contextlib import asynccontextmanager
import typing as t

from loguru import logger

from core.redis.redis import init_redis_pool

redis_pool_context = asynccontextmanager(init_redis_pool)


async def delete_cache(keys: list[str]) -> None:
    async with redis_pool_context() as redis:
        logger.info(f"Deleting cache by keys {keys}")
        await redis.delete(*keys)


async def get_cache(key: str) -> json:
    async with redis_pool_context() as redis:
        logger.info(f"Checking cache by key: {key}")
        get_key = await redis.get(key)
        if get_key:
            logger.info(f"Found Cache by key {key}")
            return get_key
        logger.info(f"Cache by key {key} not found")
        return None


async def add_cache(key: str, data: t.Union[list, dict], expire: int) -> None:
    async with redis_pool_context() as redis:
        logger.info(f"Trying to set cache by key {key}")
        await redis.set(key, json.dumps(data), ex=expire)
        logger.info(f"Successfully set cache by key {key}")
