from aiogram.fsm.state import StatesGroup, State


class CreateNew(StatesGroup):
    is_continue = State()

class CreateVideo(StatesGroup):
    image = State()
    audio = State()

class PublishVideo(StatesGroup):
    title = State()
    description = State()
    tags = State()
    confirm = State()

class Connect(StatesGroup):
    link = State()
    credentials = State()