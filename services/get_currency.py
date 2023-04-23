import requests


def get_currency(main_cur: str, second_cur: str, amount: float = None) -> float:
    """
    Запрос курса валют на сторонний API.

    Передаем основную валюту, вторую валюту и кол-во валюты для расчета.

    Возвращает, рассчитанный на стороне API, курс валюты.
    """
    url = 'https://api.exchangerate.host/latest'
    params = {
        'base': second_cur,
        'symbols': main_cur,
        'amount': amount,
        'places': 2
    }
    request = requests.get(url=url, params=params).json()
    return request.get('rates').get(main_cur)


def get_rates() -> set:
    """
    Возвращает множество(set), доступной для расчета на стороне API, валюты.
    """
    url = 'https://api.exchangerate.host/latest'
    request = requests.get(url=url).json()
    return set(request.get('rates').keys())
