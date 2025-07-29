from aiogram.fsm.state import State, StatesGroup


class FileStates(StatesGroup):
    file = State()

class ResponseFromDocumentStates(StatesGroup):
    responses = State()
