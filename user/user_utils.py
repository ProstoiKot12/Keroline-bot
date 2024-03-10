from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    name_get = State()
    hair_length = State()
    hair_coloring = State()
    hair_photo = State()
    phone_number = State()
    free_dates = State()
    free_times = State()