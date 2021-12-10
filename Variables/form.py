from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    username_tariff_category = State()
    mailing = State()