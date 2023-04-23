import requests


def get_cute_pic() -> str:
    """
    Запрос на API с милыми котиками.
    """
    url = 'https://api.thecatapi.com/v1/images/search'
    request = requests.get(url).json()
    return request[0]['url']
