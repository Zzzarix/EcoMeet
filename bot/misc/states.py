from aiogram.fsm.state import State, StatesGroup


class SignUpState(StatesGroup):
    phone = State()
    name = State()
    last_name = State()
    patronymic = State()
    birth_date = State()
    email = State()

class TaskState(StatesGroup):
    answer = State()
