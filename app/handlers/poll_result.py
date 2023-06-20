from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from app.buttons import (btn_back, btn_main, change_answers_button,
                         update_multiple_answer, update_simple_answer,
                         user_polls_button)
from app.contollers.polls_controllers import PollsController
from app.contollers.result_controllers import ResultController
from app.utils import replace_key_value
from core.redis.redis_cache import add_cache
from core.redis.redis_constants import ONE_DAY, ONE_HOUR


async def select_poll_for_result(message: types.Message) -> None:
    client_id = message.from_user.id
    result = await PollsController.get_user_result(client_id=client_id)
    if not result:
        await message.answer(
            "You don't have any poll results.",
            reply_markup=btn_main)
        return
    await message.answer(
        "You can see the results for the following polls:",
        reply_markup=await user_polls_button(polls=result))
    return


async def show_result_for_poll(message: types.Message) -> None:
    client_id = message.from_user.id
    result = await PollsController.get_user_result(client_id=client_id)
    all_polls = await PollsController.get_polls()
    poll = message.text.split('Result for ')[1].replace(' ', '_').lower()
    all_polls = await PollsController.get_polls()
    poll_data_question_and_answer = all_polls['polls'][poll]['questions']
    client_poll_data = result[poll]['answers']
    client_answers_and_questions = await ResultController.return_answer_message_text(
        client_poll_data=client_poll_data,
        poll_data=poll_data_question_and_answer,
    )
    await message.answer(
        f"{client_answers_and_questions}",
        reply_markup=await change_answers_button(
            user_question=client_poll_data,
            poll_data=poll_data_question_and_answer,
        ))
    await add_cache(key=f'change_{client_id}', data=poll, expire=ONE_HOUR)
    return


async def select_question(message: types.Message) -> None:
    client_id = message.from_user.id
    question_client = message.text.split('Change question ')[1]
    poll_changing = await PollsController.get_change_poll(key=f'change_{client_id}')
    all_polls = await PollsController.get_polls()
    poll_data_question_and_answer = all_polls['polls'][poll_changing]['questions']

    multiple, data_for_cache, branching, data_answers = await ResultController.return_answer_data(
        poll_changing=poll_changing,
        question_client=question_client,
        data=poll_data_question_and_answer,
    )
    if branching:
        await message.answer(
            "You cannot change the answer in this question because it is branched.",
            reply_markup=btn_back)
        return
    await add_cache(key=f'change_{client_id}', data=data_for_cache, expire=ONE_HOUR)

    if multiple:
        await message.answer(
            "Select answer for update",
            reply_markup=await update_multiple_answer(answers=data_answers))
        return

    await message.answer(
        "Select answer for update",
        reply_markup=await update_simple_answer(answers=data_answers))
    return


async def change_answer(message: types.Message) -> None:
    selected_answer = message.text.split('Update answer to ')[1]
    client_id = message.from_user.id
    data_for_change = await PollsController.get_change_poll(key=f'change_{client_id}')
    result = await PollsController.get_user_result(client_id=client_id)
    key_value_answer = await replace_key_value(data=data_for_change['data_answers'])
    updated_key_answer = key_value_answer[selected_answer]
    result[data_for_change['poll']]['answers'][data_for_change['key_question']] = updated_key_answer

    await add_cache(key=client_id, data=result, expire=ONE_DAY)

    await message.answer(
        f"{result}",
        reply_markup=btn_main)
    return


async def change_multiple_answer(message: types.Message) -> None:
    client_id = message.from_user.id
    data_for_change = await PollsController.get_change_poll(key=f'change_{client_id}')
    result = await PollsController.get_user_result(client_id=client_id)
    if message.text.startswith('Done'):
        if data_for_change.get('temporary_multiple'):
            result[data_for_change['poll']]['answers'][data_for_change['key_question']] = list(
                set(data_for_change['temporary_multiple']))
            await add_cache(key=client_id, data=result, expire=ONE_DAY)
            await message.answer(
                f"{result}",
                reply_markup=btn_main,
            )
            return
        await message.answer(
            f"{result}",
            reply_markup=btn_main,
        )
        return

    selected_answer = message.text.split('Update multiple answer to ')[1]
    key_value_answer = await replace_key_value(data=data_for_change['data_answers'])
    updated_key_answer = key_value_answer[selected_answer]

    if data_for_change.get('temporary_multiple'):
        data_answer = data_for_change.get('temporary_multiple')
        data_answer.append(updated_key_answer)
        data_for_change['temporary_multiple'] = data_answer
    else:
        data_for_change['temporary_multiple'] = [updated_key_answer]

    await add_cache(key=f'change_{client_id}', data=data_for_change, expire=ONE_HOUR)

    await message.answer(
        "Got it.",
        reply_markup=await update_multiple_answer(answers=data_for_change['data_answers']))
    return


def register_show_result(dp: Dispatcher) -> None:
    dp.register_message_handler(select_poll_for_result, Text(equals='Show Results'))
    dp.register_message_handler(show_result_for_poll, Text(startswith='Result for '))
    dp.register_message_handler(select_question, Text(startswith='Change question '))
    dp.register_message_handler(change_answer, Text(startswith='Update answer to '))
    dp.register_message_handler(change_multiple_answer, Text(startswith='Update multiple answer to '))
    dp.register_message_handler(change_multiple_answer, Text(startswith='Done'))
