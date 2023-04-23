from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.get_currency import get_rates


def currency_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с основными валютами и кнопкой "Другая валюта".
    """
    USD_BUTTON = InlineKeyboardButton(text='USD', callback_data='USD')
    EUR_BUTTON = InlineKeyboardButton(text='EUR', callback_data='EUR')
    RUB_BUTTON = InlineKeyboardButton(text='RUB', callback_data='RUB')
    ANOTHER_BUTTON = InlineKeyboardButton(text='Другая валюта', callback_data='another_currency')
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[USD_BUTTON, EUR_BUTTON, RUB_BUTTON], [ANOTHER_BUTTON]]
    )

    return keyboard


def all_currency_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура со всем валютами.
    """
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    currency_pairs = get_rates()
    for currency_name in currency_pairs:
        keyboard_builder.add(InlineKeyboardButton(text=currency_name,
                                                  callback_data=currency_name))
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()

