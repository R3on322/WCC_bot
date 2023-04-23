import requests
from lexicon.lexicon_ru import WEATHER_ICONS, FEEL_ICONS
from config.config import Config, load_config


config: Config = load_config()


def get_weather(longitude: float = None, latitude: float = None, city: str = None) -> dict | None:
    """
    Запрашиваем погоду у стороннего API.

    Проверяем данные которые нам пришли:
    - если долгота и широта, то отправляем запрос по ним
    - если город, отправляем запрос по городу

    Если запрос прошел успешно, вернулся код 200, возвращаем словарь с данными о погоде

    Если возникла ошибка при запросе, ничего не возвращаем.
    """
    url = 'https://api.openweathermap.org/data/2.5/weather'
    if city:
        params = {'q': city,
                  'lang': 'ru',
                  'units': 'metric',
                  'appid': config.tg_bot.weather_token}
    else:
        params = {'lat': latitude,
                  'lon': longitude,
                  'lang': 'ru',
                  'units': 'metric',
                  'appid': config.tg_bot.weather_token}
    request = requests.get(url=url, params=params).json()
    if request['cod'] == 200:
        feel_icon = _get_feel_icon(request)
        weather_info = {
            'city_name': request.get('name'),
            'description': request.get('weather')[0].get('description'),
            'temperature': request.get('main').get('temp'),
            'feels_like': request.get('main').get('feels_like'),
            'wind_speed': request.get('wind').get('speed'),
            'icon': WEATHER_ICONS.get(request.get('weather')[0].get('icon'), "⛅"),
            'feel_icon': FEEL_ICONS.get(feel_icon)}
        return weather_info
    else:
        return None


def _get_feel_icon(request) -> str:
    """
    Сравнивает температуру на улице и выдает смайлик в зависимости от температуры.

    Смайлик отправляется пользователю вместе с ответом на общий запрос погоды.
    """
    temp = request.get('main').get('feels_like')
    if temp < 10:
        return 'cold'
    elif temp < 30:
        return 'normal'
    else:
        return 'hot'

