from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    weather_token: str          # Токен для доступа к API погоды


@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    env: Env = Env()
    env.read_env()

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               weather_token=env('API_KEY_WEATHER')))
