from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsDigit(BaseFilter):
    """
    Фильтр проверяет сообщение, является оно числом или нет
    """
    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit():
            return True
        else:
            return False
