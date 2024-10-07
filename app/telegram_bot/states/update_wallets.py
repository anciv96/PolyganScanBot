from aiogram.fsm.state import StatesGroup, State


class UpdateWallets(StatesGroup):
    get_file = State()
