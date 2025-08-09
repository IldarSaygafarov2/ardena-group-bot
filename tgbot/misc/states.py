from aiogram.fsm.state import State, StatesGroup


class MessageCounterState(StatesGroup):
    counter = State()


class AdminChemistryFilesState(StatesGroup):
    data = State()
