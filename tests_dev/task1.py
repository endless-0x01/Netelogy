def check_age(age: int):
    if not isinstance(age, int):
        raise TypeError(f'Возраст должен быть целым число, был передан тип {type(age).__name__}')
    if age >= 18: # Введите условие для проверки возраста
        result = 'Доступ разрешён'
    else:
        result = 'Доступ запрещён'

    return result
    


