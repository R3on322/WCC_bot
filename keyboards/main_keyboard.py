from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура главного меню пользователя
    """
    button1: KeyboardButton = KeyboardButton(text='Погода 🌤')
    button2: KeyboardButton = KeyboardButton(text='Конвертер валют 💱')
    button3: KeyboardButton = KeyboardButton(text='Что-то милое 🥹')
    button4: KeyboardButton = KeyboardButton(text='Опрос 📋')

    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1, button2, button3, button4]],
                                                        resize_keyboard=True, is_persistent=True)
    return keyboard
