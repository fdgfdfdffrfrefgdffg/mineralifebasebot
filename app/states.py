from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    name = State()
    phone = State()
    quantity = State()
    location = State()
