from aiogram import types
from keyboards.main_keyboard import main_keyboard
from lexicon.lexicon_ru import LEXICON_RU


async def process_start(message: types.Message) -> None:
    """
    Основное меню.

    Отправляем приветственное сообщение пользователю и отправляем клавиатуру с меню бота.
    """
    await message.answer(text=f'{message.chat.first_name}, {LEXICON_RU["start_message"]}',
                         reply_markup=main_keyboard())


async def process_echo(message: types.Message) -> None:
    """
    Отвечает сообщением на любые действия пользователя в основном меню, которые не отлавливает хендлер.
    """
    await message.answer(text=LEXICON_RU['all_message_answer'],
                         reply_markup=main_keyboard())

