import requests
from pprint import pprint

url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

def translate_word(word):
    params = {
        'key': 'hidden',
        'lang': 'ru-en',
        'text': word,
    }

    responce = requests.get(url, params=params).json()
    
    return responce['def'][0]['tr'][0]['text']

def main():
    print(translate_word('машина'))

if __name__ == "__main__":
    main()