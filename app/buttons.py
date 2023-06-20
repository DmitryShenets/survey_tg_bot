from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

take_survey = KeyboardButton('Take a Survey')
show_results = KeyboardButton('Show Results')

select_poll = KeyboardButton('Select Poll')
select_question = KeyboardButton('Select Question')

client_answer_yes = KeyboardButton('Yes')
client_answer_no = KeyboardButton('No')

next_question = KeyboardButton('Next question')
btn_done = KeyboardButton('Done')
back = KeyboardButton('Back To Main')

btn_main = ReplyKeyboardMarkup(resize_keyboard=True).add(take_survey).insert(show_results)
btn_select_poll = ReplyKeyboardMarkup(resize_keyboard=True).add(select_poll).add(back)
btn_select_question = ReplyKeyboardMarkup(resize_keyboard=True).add(select_question).add(back)


btn_yes_no = ReplyKeyboardMarkup(resize_keyboard=True).add(client_answer_yes, client_answer_no)
btn_back = ReplyKeyboardMarkup(resize_keyboard=True).add(back)


async def answer_button_generation(answers: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for answer in answers.values():
        btn = KeyboardButton(f'Answer: {answer}')
        button.add(btn)
    return button


async def poll_button_generation(polls: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for poll in polls['polls'].values():
        btn = KeyboardButton(f'Choose {poll.get("name")}')
        button.add(btn)
    button.add(back)
    return button


async def answer_multiple_generation(answers: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in answers.values():
        btn = KeyboardButton(f'Multiple answer: {answer}')
        button.add(btn)
    button.add(next_question)
    return button


async def user_polls_button(polls: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for poll in polls.keys():
        btn = KeyboardButton(f'Result for {poll.replace("_", " ").capitalize()}')
        button.add(btn)
    button.add(back)
    return button


async def change_answers_button(user_question: dict, poll_data: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for question in user_question.keys():
        btn = KeyboardButton(f'Change question {poll_data[question]["question"]}')
        button.add(btn)
    button.add(back)
    return button


async def update_simple_answer(answers: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in answers.values():
        btn = KeyboardButton(f'Update answer to {answer}')
        button.add(btn)
    button.add(back)
    return button


async def update_multiple_answer(answers: dict) -> ReplyKeyboardMarkup:
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in answers.values():
        btn = KeyboardButton(f'Update multiple answer to {answer}')
        button.add(btn)
    button.add(btn_done).add(back)
    return button
