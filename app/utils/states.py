from aiogram.fsm.state import StatesGroup, State

class Sticker(StatesGroup):
    start = State()
    name = State()
    photo = State()
    end = State()