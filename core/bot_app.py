from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from app.handlers.main_handlers import register_main_handlers
from app.handlers.poll_result import register_show_result
from app.handlers.survey import register_take_survey
from core.config import CONFIG


async def main() -> None:
    logger.info('Starting bot')

    storage = MemoryStorage()
    bot = Bot(token=CONFIG.TOKEN)
    dp = Dispatcher(bot, storage=storage)

    register_main_handlers(dp=dp)
    register_take_survey(dp=dp)
    register_show_result(dp=dp)

    await dp.skip_updates()
    await dp.start_polling(dp)

    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.warning('Storage connection close')
    logger.warning('Bot polling stop')

    return
