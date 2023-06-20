import json

from core.redis.redis_cache import add_cache
from core.redis.redis_constants import ONE_DAY


class LoadFixturesController:
    @staticmethod
    async def load_data() -> bool:
        with open('app/fixtures/polls.json', 'r') as data:
            await add_cache(key='polls', data=json.load(data), expire=ONE_DAY)
        with open('app/fixtures/logic.json', 'r') as data:
            await add_cache(key='logic', data=json.load(data), expire=ONE_DAY)
        return True
