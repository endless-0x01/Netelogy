cook_book = dict()

with open("cook_book\\recipes.txt", encoding="utf-8") as file:
    data = file.readlines()



for line in data:
    
    if not line.strip():
        continue

    if line.strip().isdigit():
        # cook_book[key].extend([dict() for _ in range(3)])
        pass
    elif '|' in line.strip():
        name, quantity, measure = [part.strip() for part in line.split('|')]
        cook_book[key].append({'name' : name, 'quantity' : quantity, 'measure' : measure})
    else:
        cook_book.setdefault(line.strip(), [])
        key = line.strip()

for dish, ingredients in cook_book.items():
    print(f'Блюдо {dish}')
    for dict_ing in ingredients:
        print(f'\tname: {dict_ing['name']} | quantity: {dict_ing['quantity']} | measure: {dict_ing['measure']}')

    print('\n')