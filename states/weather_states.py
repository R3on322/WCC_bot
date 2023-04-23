from aiogram.fsm.state import State, StatesGroup


class WeatherStates(StatesGroup):
    """
    Состояния для погоды.
    """
    geo_position = State()
