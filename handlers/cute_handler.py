from aiogram import types
from aiogram.methods import SendPhoto
from keyboards.main_keyboard import main_keyboard
from services.get_cute_pic import get_cute_pic


async def process_cute(message: types.Message):
    """
    Запускается процесс после нажатия кнопки "Что-то милое", в основном меню.

    Отправляет пользователю фото с милым животным.
    """
    await SendPhoto(chat_id=message.chat.id,
                    photo=get_cute_pic(),
                    reply_markup=main_keyboard())
