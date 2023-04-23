from aiogram.fsm.state import State, StatesGroup


class PollStates(StatesGroup):
    """
    Состояния для опроса.
    """
    menu = State()
    send_poll = State()
