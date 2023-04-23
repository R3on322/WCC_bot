from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def poll_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура для личного чата с ботом.

    Кнопки: "Создать опрос", "Список опросов", "Выйти".
    """
    create_button: KeyboardButton = KeyboardButton(text='Создать опрос',
                                                   request_poll=KeyboardButtonPollType(type='regular'))
    list_poll_button: KeyboardButton = KeyboardButton(text='Список опросов')
    cancel_button: KeyboardButton = KeyboardButton(text='Выйти')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[create_button], [list_poll_button], [cancel_button]],
        resize_keyboard=True)
    return keyboard


def list_poll_keyboard(saved_polls) -> InlineKeyboardMarkup:
    """
    Клавиатура принимает список сохраненных опросов.

    Возвращает Inline клавиатуру со списком опросов в виде клавиатуры.
    """
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for poll in saved_polls:
        keyboard_builder.add(InlineKeyboardButton(text=poll,
                                                  callback_data=poll))
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def group_chat_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура для группового чата с ботом.

    Кнопки: "Отправить опрос", "Выйти".
    """
    send_poll_button: KeyboardButton = KeyboardButton(text='Отправить опрос')
    cancel_button: KeyboardButton = KeyboardButton(text='Выйти')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[send_poll_button], [cancel_button]],
        resize_keyboard=True)
    return keyboard
