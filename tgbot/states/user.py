from aiogram.fsm.state import State, StatesGroup


class UserMainMenu(StatesGroup):
    menu = State()
    input_address = State()