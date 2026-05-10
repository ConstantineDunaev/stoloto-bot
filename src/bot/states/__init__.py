from aiogram.fsm.state import StatesGroup, State


class OperationState(StatesGroup):
    TopInProcess = State()
    BmInProcess = State()
