from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from loguru import logger

from app.buttons import btn_main


async def process_start_command(message: types.Message) -> None:
    logger.info(f'Command start from: {message.from_user.id} {message.from_user.username}.')
    await message.answer(f"Hi, {message.from_user.username}!", reply_markup=btn_main)
    return


async def back_to_main(message: types.Message) -> None:
    await message.answer('Select action.', reply_markup=btn_main)
    return


def register_main_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(back_to_main, Text(equals='Back To Main'))
