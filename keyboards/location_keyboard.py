from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton
from lexicon.lexicon_ru import LEXICON_RU


def location_button() -> ReplyKeyboardMarkup:
    """
    Клавиатура с одной кнопкой "Отправить мое местоположение".
    """
    button = KeyboardButton(text=LEXICON_RU['my_location'],
                            request_location=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='⬇ Отправить местоположение ⬇')
    return keyboard
