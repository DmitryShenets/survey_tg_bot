from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

from core.config import CONFIG


async def main() -> None:
    logger.info('Starting bot')

    storage = MemoryStorage()
    bot = Bot(token=CONFIG.TOKEN)
    dp = Dispatcher(bot, storage=storage)

    await dp.skip_updates()
    await dp.start_polling()

    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.warning('Storage connection close')
    logger.warning('Bot polling stop')

    return
