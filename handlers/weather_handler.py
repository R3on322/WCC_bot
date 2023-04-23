from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.location_keyboard import location_button
from keyboards.main_keyboard import main_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.get_weather import get_weather
from states.weather_states import WeatherStates


async def process_start_weather(message: types.Message, state: FSMContext) -> None:
    """
    Запускается процесс после нажатия кнопки "Погода", в основном меню.

    Проверяем откуда пришло сообщение:
    Если из группового чата, там делиться местоположением с ботом нельзя,
    поэтому просим ввести город для получения прогноза погоды вручную и не формируем кнопку "Отправить местоположение".

    Если из личного чата, просим ввести город вручную или отправить местоположение
    с помощью кнопки "Отправить местоположение".
    """
    if message.chat.type == 'group':
        await message.answer(text=LEXICON_RU['enter_city'])
    else:
        await message.answer(text=LEXICON_RU['enter_city'],
                             reply_markup=location_button())
    await state.set_state(WeatherStates.geo_position)


async def process_end_weather(message: types.Message, state: FSMContext) -> None:
    """
    Проверяем, какой вид данных отправил пользователь, местоположение или город.

    Если такой город есть, то отправляем данные о погоде.

    Если город не найден, отправляем сообщение, что такой город не найден.
    """
    await message.answer(text=LEXICON_RU['wait_weather'], reply_markup=main_keyboard())
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        weather_info = get_weather(longitude=lon, latitude=lat)
    else:
        weather_info = get_weather(city=message.text)
    await state.update_data(weather=weather_info)
    if weather_info:
        weather_data = await state.get_data()
        await state.clear()
        weather_data = weather_data['weather']
        await message.answer(text=f'📍 Погода в {weather_data.get("city_name")}:\r\n\n'
                                  f'🏡 На улице : {weather_data.get("icon")} {weather_data.get("description")} \r\n'
                                  f'🌡 Температура воздуха: {weather_data.get("temperature")}°С\r\n'
                                  f'{weather_data["feel_icon"]} Ощущается как: {weather_data.get("feels_like")}°С\r\n'
                                  f'💨 Скорость ветра: {weather_data.get("wind_speed")} м/с')
    else:
        await message.answer(text=f'{LEXICON_RU["no_city"]}{message.text}.')
