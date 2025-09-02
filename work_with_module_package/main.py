from application import salary
from application.db import people
from datetime import datetime, timezone
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from bs4 import BeautifulSoup
import os

def save_html(soup_object: BeautifulSoup, file_name='netology.html'):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(soup_object.prettify())
    return True

def get_html_netology():
    try:
        response = requests.get('https://netology.ru/')
        response.raise_for_status()
        response.encoding = 'utf-8'
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')
            if save_html(html):
                print('html сохранен')
            else:
                print('Ошибка сохранения файла')

    except ConnectionError:
        print('Ошибка соединения')
    except Timeout:
        print('Превышено время ожидания запроса')
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        


if __name__ == '__main__':
    salary.calculate_salary()
    people.get_employees()
    get_html_netology()
    print(f'Запуск программы выполнялся {datetime.now(timezone.utc)}')