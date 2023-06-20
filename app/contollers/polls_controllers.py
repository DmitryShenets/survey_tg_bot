import json
import typing as t

from core.redis.redis_cache import add_cache, get_cache
from core.redis.redis_constants import ONE_DAY


class PollsController:
    @classmethod
    async def get_polls(cls: object) -> t.Union[dict, None]:
        data = await get_cache(key='polls')
        if data:
            return json.loads(data)
        return None

    @classmethod
    async def get_logic(cls: object) -> t.Union[dict, None]:
        data = await get_cache(key='logic')
        if data:
            return json.loads(data)
        return None

    @staticmethod
    async def get_survey_data(key: str) -> t.Union[dict, None]:
        data = await get_cache(key=key)
        if data:
            return json.loads(data)
        return None

    @staticmethod
    async def get_change_poll(key: str) -> t.Union[dict, None]:
        data = await get_cache(key=key)
        if data:
            return json.loads(data)
        return None

    @classmethod
    async def return_poll_data(cls: object, name_poll: str, key_question: str) -> tuple[dict, dict, dict, dict]:
        get_polls = await cls.get_polls()
        logic = await cls.get_logic()
        poll_data = get_polls['polls'][name_poll]['questions']
        question_data = get_polls['polls'][name_poll]['questions'][key_question]
        logic_current_survey = logic['poll_logic'][name_poll]
        return get_polls, poll_data, question_data, logic_current_survey

    @staticmethod
    async def record_user_data(client_id: str, data: dict) -> bool:
        cache = await get_cache(key=client_id)
        if cache:
            cache_data = json.loads(cache)
            new_data = {**cache_data, **data}
        else:
            new_data = data
        await add_cache(key=client_id, data=new_data, expire=ONE_DAY)
        return True

    @staticmethod
    async def get_user_result(client_id: str) -> t.Union[dict, None]:
        data = await get_cache(key=client_id)
        if data:
            return json.loads(data)
        return None
