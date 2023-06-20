from aiogram.dispatcher.filters.state import State, StatesGroup


class SurveyState(StatesGroup):
    survey = State()
