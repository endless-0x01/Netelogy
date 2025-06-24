import requests



def get_the_smartest_superhero(superheros) -> str:
    the_smartest_superhero = []

    url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
    responce = requests.get(url).json()
    for heroe in responce:
        if heroe['id'] in superheros:
            the_smartest_superhero.append({
                'id'    : heroe['id'],
                'name'  : heroe['name'],
                'power' : heroe['powerstats']['intelligence'],
            })

    smart_hero = max(the_smartest_superhero, key=lambda hero : hero['power'])
    return smart_hero['name']


def main():
    print(get_the_smartest_superhero([332, 149, 655]))


if __name__ == "__main__":
    main()
