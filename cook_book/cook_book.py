def parse_cook_book():

    with open("cook_book\\recipes.txt", encoding="utf-8") as file:
        data = file.readlines()

    cook_book = dict()
    for line in data:

        if not line.strip():
            continue
        if line.strip().isdigit():
            continue
        elif "|" in line.strip():
            name, quantity, measure = [part.strip() for part in line.split("|")]
            cook_book[key].append(
                {"ingredient_name": name, "quantity": quantity, "measure": measure}
            )
        else:
            cook_book.setdefault(line.strip(), [])
            key = line.strip()

    return cook_book


def show(cook_book):
    for dish, ingredients in cook_book.items():
        print(f"Блюдо {dish}")
        for dict_ing in ingredients:
            print(
                f"\tНазвание ингредиента: {dict_ing['ingredient_name']:<15} | Количество : {dict_ing['quantity']:<10} | Единица измерения: {dict_ing['measure']:<5}"
            )

        print("\n")


def get_shop_list_by_dishes(dishes, count_person):
    cook_book = parse_cook_book()


    ingredients_for_dishes = dict()

    for dish in dishes:
        if dish not in cook_book:
            print(f'Блюда "{dish}" нет в кулинарной книге.')
            continue

        for ingredient in cook_book[dish]:
            name = ingredient["ingredient_name"]
            measure = ingredient["measure"]
            quantity = int(ingredient["quantity"]) * count_person

            if name in ingredients_for_dishes:
                ingredients_for_dishes[name]["quantity"] += quantity
            else:
                ingredients_for_dishes[name] = {
                    "measure": measure,
                    "quantity": quantity,
                }

    return ingredients_for_dishes





def main():
    result = get_shop_list_by_dishes(["Запеченный картофель", "Омлет"], 2)

    for key, value in result.items():
        print(f"{key:<10}: {value}")


if __name__ == "__main__":
    main()