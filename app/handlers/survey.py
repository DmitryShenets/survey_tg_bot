from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from loguru import logger

from app.buttons import (answer_button_generation, answer_multiple_generation,
                         btn_back, btn_main, btn_select_poll,
                         poll_button_generation)
from app.contollers.polls_controllers import PollsController
from app.utils import replace_key_value
from core.redis.redis_cache import add_cache
from core.redis.redis_constants import ONE_HOUR


async def take_survey(message: types.Message) -> None:
    logger.info(f'Command start from: {message.from_user.id} {message.from_user.username}')
    await message.answer("Select poll:", reply_markup=btn_select_poll)
    return


async def show_polls(message: types.Message) -> None:
    get_polls = await PollsController.get_polls()
    if get_polls:
        await message.answer("Select poll:", reply_markup=await poll_button_generation(polls=get_polls))
        return
    await message.answer("There are currently no polls", reply_markup=btn_back)
    return


async def start_survey(message: types.Message) -> None:
    client_message = message.text.split(' ')
    poll = f'{client_message[1]}_{client_message[2]}'.lower()
    get_polls = await PollsController.get_polls()
    poll_for_survey = get_polls['polls'].get(poll)

    if poll_for_survey.get('questions'):
        key_questions = sorted([key for key in poll_for_survey.get('questions').keys()])
        survey_data = {
            'name': poll,
            'key_question': key_questions[0],
        }
        await add_cache(key=f'survey_{message.from_user.id}', data=survey_data, expire=ONE_HOUR)

        await message.answer("Poll starts")
        first_question = poll_for_survey['questions'][key_questions[0]]

        await message.answer(
            f"{first_question['question']}",
            reply_markup=await answer_button_generation(answers=first_question['answers']),
        )
        return
    await message.answer("Sorry, the poll hasn't been created yet", reply_markup=btn_main)
    return


async def got_answer(message: types.Message) -> None:
    data_survey = await PollsController.get_survey_data(key=f'survey_{message.from_user.id}')
    answer_key = message.text.split('Answer: ')[1]

    get_polls, poll_data, question_data, logic_current_survey =\
        await PollsController.return_poll_data(
            name_poll=data_survey['name'],
            key_question=data_survey['key_question'],
        )

    change_key_value_place = await replace_key_value(data=question_data['answers'])
    current_key_question = data_survey['key_question']
    next_question = str(logic_current_survey.get(current_key_question),
                        ) if logic_current_survey.get(current_key_question) else None

    if question_data.get('branching'):
        answer_id = change_key_value_place[answer_key]
        next_question = str(logic_current_survey.get(current_key_question).get(answer_id),
                            ) if logic_current_survey.get(current_key_question) else None

    if data_survey.get('answers'):
        data_survey['answers'] = \
            {**data_survey['answers'], **{current_key_question: change_key_value_place[answer_key]}}
    else:
        data_survey['answers'] = {current_key_question: change_key_value_place[answer_key]}

    data_survey['key_question'] = next_question

    await add_cache(key=f'survey_{message.from_user.id}', data=data_survey, expire=ONE_HOUR)
    next_multiple = None
    if next_question:
        next_multiple = get_polls['polls'][data_survey['name']]['questions'][next_question]['multiple']

    if next_multiple:
        await message.answer(
            f"{poll_data[next_question]['question']}",
            reply_markup=await answer_multiple_generation(answers=poll_data[next_question]['answers']),
        )
        return
    if next_question:
        await message.answer(
            f"{poll_data[next_question]['question']}",
            reply_markup=await answer_button_generation(answers=poll_data[next_question]['answers']),
        )

        return

    await PollsController.record_user_data(client_id=str(message.from_user.id), data={data_survey['name']: data_survey})
    result = await PollsController.get_user_result(client_id=message.from_user.id)
    await message.answer(f"{result}")
    await message.answer("Survey ended", reply_markup=btn_main)
    return


async def got_multiple_answer(message: types.Message) -> None:
    data_survey = await PollsController.get_survey_data(key=f'survey_{message.from_user.id}')
    if message.text.startswith('Next question'):
        get_polls, poll_data, question_data, logic_current_survey =\
            await PollsController.return_poll_data(
                name_poll=data_survey['name'],
                key_question=data_survey['key_question'],
            )
        current_key_question = data_survey['key_question']

        next_question = \
            str(logic_current_survey.get(current_key_question)) if logic_current_survey\
            .get(current_key_question) else None

        get_polls = await PollsController.get_polls()
        poll_data = get_polls['polls'][data_survey['name']]['questions']

        data_survey['key_question'] = next_question
        if data_survey['answers'].get(current_key_question):
            data_survey['answers'][current_key_question] = list(set(data_survey['answers'][current_key_question]))
        else:
            await message.answer("You didn't give any answer")
            await message.answer(
                f"{poll_data[current_key_question]['question']}",
                reply_markup=await answer_multiple_generation(answers=poll_data[current_key_question]['answers']),
            )
            return

        await add_cache(key=f'survey_{message.from_user.id}', data=data_survey, expire=ONE_HOUR)

        next_miltiple = get_polls['polls'][data_survey['name']]['questions'][next_question]['multiple']

        if next_miltiple:
            await message.answer(
                f"{poll_data[next_question]['question']}",
                reply_markup=await answer_multiple_generation(answers=poll_data[next_question]['answers']),
            )
            return
        if next_question:
            await message.answer(
                f"{poll_data[next_question]['question']}",
                reply_markup=await answer_button_generation(answers=poll_data[next_question]['answers']),
            )

            return
        await PollsController.record_user_data(
            client_id=str(message.from_user.id),
            data={data_survey['name']: data_survey},
        )
        await message.answer(f"{data_survey}")
        await message.answer("Survey ended", reply_markup=btn_main)
        return

    get_polls, poll_data, question_data, logic_current_survey =\
        await PollsController.return_poll_data(
            name_poll=data_survey['name'],
            key_question=data_survey['key_question'],
        )

    current_key_question = data_survey['key_question']
    change_key_value_place = await replace_key_value(data=question_data['answers'])
    answer_id = message.text.split('Multiple answer: ')[1]

    if data_survey.get('answers'):
        if data_survey['answers'].get(current_key_question):
            data_answer = data_survey['answers'][current_key_question]
            data_answer.append(change_key_value_place[answer_id])
            data_survey['answers'][current_key_question] = data_answer
        else:
            data_survey['answers'][current_key_question] = [change_key_value_place[answer_id]]

    await add_cache(key=f'survey_{message.from_user.id}', data=data_survey, expire=ONE_HOUR)
    await message.answer(
        "You can give more answers",
        reply_markup=await answer_multiple_generation(answers=poll_data[current_key_question]['answers']),
    )
    return


def register_take_survey(dp: Dispatcher) -> None:
    dp.register_message_handler(show_polls, Text(equals='Take a Survey'))
    dp.register_message_handler(start_survey, lambda message: 'Choose' in message.text)
    dp.register_message_handler(got_answer, lambda message: 'Answer: ' in message.text)
    dp.register_message_handler(got_multiple_answer, Text(startswith='Next question'))
    dp.register_message_handler(got_multiple_answer, Text(startswith='Multiple answer: '))
