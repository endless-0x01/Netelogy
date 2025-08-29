import requests


def get_the_smartest_superhero() -> str:
    the_smartest_superhero = dict()

    url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
    responce = requests.get(url).json()
    checker_heroes = ["Hulk", "Captain America", "Thanos"]
    for heroe in responce:
        if heroe["name"] in checker_heroes:
            the_smartest_superhero[heroe["name"]] = heroe["powerstats"]["intelligence"]

    return max(the_smartest_superhero.items(), key=lambda x: x[1])[0]


def main():
    print(get_the_smartest_superhero())


if __name__ == "__main__":
    main()
