import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.filters import Command, CommandStart, Text, or_f
from config.config import Config, load_config
from filters.is_digit import IsDigit
from filters.message_type import IsPoll
from handlers.currency_handler import process_start_currency, process_second_currency, process_end_currency, \
    process_amount_of_currency, process_another_currency, process_any_message, process_not_num, process_cancel_command
from handlers.cute_handler import process_cute
from handlers.poll_handler import process_end_poll, process_save_poll, process_enter_poll, \
    process_get_list_poll, process_main_menu_poll, process_echo_poll, process_send_poll
from handlers.user_handler import process_start, process_echo
from handlers.weather_handler import process_start_weather, process_end_weather
from states.currency_states import CurrencyStates
from states.poll_states import PollStates
from states.weather_states import WeatherStates

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Запуск бота.

    Загрузка всех токенов для всех API.
    """
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s'
                               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Обработка команды "/start".
    dp.message.register(process_start, CommandStart())

    # Реакция на нажатие кнопки "Опрос".
    dp.message.register(process_main_menu_poll, Text(text='Опрос 📋'))
    # Выход из меню Опрос.
    dp.message.register(process_end_poll, PollStates.menu, Text(text='Выйти'))
    # Реакция на нажатие кнопки "Список опросов" в меню "Опрос".
    dp.message.register(process_get_list_poll, PollStates.menu, Text(text='Список опросов'))
    # Реакция на кнопку в групповом чате "Отправить опрос".
    dp.message.register(process_enter_poll, Text(text='Отправить опрос'))
    # Срабатывает после выбора опроса для отправки в групповой чат.
    dp.callback_query.register(process_send_poll, PollStates.send_poll)
    # Реакция на определенное сообщение типа "Опрос". Если это опрос, сохраняет его.
    dp.message.register(process_save_poll, PollStates.menu, IsPoll())
    # Реакция на любые сообщения в меню "Опрос".
    dp.message.register(process_echo_poll, PollStates.menu)

    # Реакция на нажатие кнопки "Что-то милое" в главном меню.
    dp.message.register(process_cute, Text(text='Что-то милое 🥹'))

    # Реакция на нажатие кнопки "Конвертер валют" в главном меню.
    dp.message.register(process_start_currency, Text(text='Конвертер валют 💱'))
    # Реакция на команду "/cancel" в меню конвертации валют.
    dp.message.register(process_cancel_command, Command(commands='cancel'))
    # Реакция на нажатие в Inline клавиатуре кнопки "Другая валюта".
    dp.callback_query.register(process_another_currency,
                               or_f(CurrencyStates.main_currency, CurrencyStates.secondary_currency),
                               Text(text='another_currency'))
    # Срабатывает при выборе первой валюты.
    dp.callback_query.register(process_second_currency, CurrencyStates.main_currency)
    # Срабатывает при выборе второй валюты.
    dp.callback_query.register(process_amount_of_currency, CurrencyStates.secondary_currency)
    # Реакция на ввод числа для конвертации и проверка сообщения является ли оно числом.
    dp.message.register(process_end_currency, CurrencyStates.amount_of_currency, IsDigit())
    # Реакция на сообщения от пользователя во время выбора валют.
    dp.message.register(process_any_message, or_f(CurrencyStates.main_currency, CurrencyStates.secondary_currency))
    # Реакция если пользователь ввел не число, после выбора валют.
    dp.message.register(process_not_num, CurrencyStates.amount_of_currency)

    # Реакция на нажатие кнопки "Погода" в главном меню.
    dp.message.register(process_start_weather, Text(text='Погода 🌤'))
    # Срабатывает после ввода города
    dp.message.register(process_end_weather, WeatherStates.geo_position)
    # Реакция на любые сообщения в меню "Погода".
    dp.message.register(process_echo)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
