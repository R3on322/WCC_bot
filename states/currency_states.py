from aiogram.fsm.state import State, StatesGroup


class CurrencyStates(StatesGroup):
    """
    Состояния для валюты.
    """
    main_currency = State()
    secondary_currency = State()
    amount_of_currency = State()
    another_amount = State()
