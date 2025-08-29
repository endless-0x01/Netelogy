import requests  # Для HTTP-запросов
import time  # Для функции sleep
from pprint import pprint

# Список популярных городов Великобритании
# Заполните список городами Великобритании

# Ключ доступа к API
API_KEY = "hiddet for git"


def find_uk_city(coordinates: list) -> str:
    """Ваш код здесь"""
    city_british = [
        "Leeds",
        "London",
        "Liverpool",
        "Manchester",
        "Oxford",
        "Edinburgh",
        "Norwich",
        "York",
    ]
    POPULAR_UK_CITIES = []

    api_url = "https://geocode.maps.co/reverse"

    for latitude, longitude in coordinates:
        params = {
            "lat": latitude,
            "lon": longitude,
            "api_key": API_KEY,
        }
        responce = requests.get(api_url, params=params)
        if responce.status_code != 200:
            print("Ошибка")
            continue
        else:
            answer = responce.json()

        if answer["address"]["city"] in city_british:
            # POPULAR_UK_CITIES.append(answer['address']['city'])
            return answer["address"]["city"]

    return "\n".join(POPULAR_UK_CITIES)


if __name__ == "__main__":
    _coordinates = [
        ("55.7514952", "37.618153095505875"),  # Москва
        ("52.3727598", "4.8936041"),  # Амстердам
        ("53.4071991", "-2.99168"),  # Ливерпуль
    ]

    print(find_uk_city(_coordinates))
