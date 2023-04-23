from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPoll(BaseFilter):
    """
    Фильтр проверяет сообщение, есть ли в нем опрос или нет
    """
    async def __call__(self, message: Message) -> bool:
        if message.poll:
            return True
        else:
            return False
