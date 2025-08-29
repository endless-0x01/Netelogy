from database import engine, get_session
from models import Words, Base


def create_tables():
    """Создание всех таблиц в БД"""
    try:
        print("Создаю таблицы...")
        Base.metadata.create_all(engine)
        print("Таблицы созданы")
    except Exception as e:
        raise Exception(f"Ошибка при создание таблица {e}")


def check_tables():
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Кол-во созданных таблиц {len(tables)}")
    print("\nСозданные таблицы: ")
    for table in tables:
        print(f" - {table}")


def add_initial_words():
    with get_session() as session:

        basic_words = [
            {"russian": "красный", "english": "red", "category": "цвета"},
            {"russian": "синий", "english": "blue", "category": "цвета"},
            {"russian": "зеленый", "english": "green", "category": "цвета"},
            {"russian": "один", "english": "one", "category": "числа"},
            {"russian": "два", "english": "two", "category": "числа"},
            {"russian": "три", "english": "three", "category": "числа"},
            {"russian": "кот", "english": "cat", "category": "животные"},
            {"russian": "собака", "english": "dog", "category": "животные"},
            {"russian": "я", "english": "I", "category": "местоимения"},
            {"russian": "ты", "english": "you", "category": "местоимения"},
        ]

        for word_data in basic_words:
            new_word = Words(
                russian_word=word_data["russian"],
                english_word=word_data["english"],
                category=word_data["category"],
                is_common=True,
            )

            session.add(new_word)
        session.commit()
        print("Слова добавлены")


def check_words():
    with get_session() as session:
        words = session.query(Words).all()
        print(f"Кол-во слов {len(words)}")

        print("\nList words: ")
        for word in words:
            print(
                f" {
                    word.russian_word} = {
                    word.english_word} | Категория: {
                    word.category} | Общее для всех: {
                    word.is_common}"
            )


if __name__ == "__main__":
    create_tables()
    check_tables()
    add_initial_words()
    check_words()
