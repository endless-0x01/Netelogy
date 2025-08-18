import sqlalchemy as sq
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Book, Publisher, Base, Shop, Sale, Stock


if __name__ == "__main__":
    DSN = "postgresql://postgres:1234@localhost:5432/netology_db"
    engine = sq.create_engine(DSN)

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = SessionLocal()

    # pub1 = Publisher(name="Эксмо")
    # book1 = Book(title="Книжный вор", id_publisher=1)
    # book2 = Book(
    #     title="Русский шлейф Шанель. Неизвестная история знаменитой француженки",
    #     id_publisher=1,
    # )
    # book3 = Book(title="Моя причуда", id_publisher=1)

    # pub2 = Publisher(name="Триумф")
    # book4 = Book(title="Гарри Поттер", id_publisher=2)
    # book5 = Book(title="Крепкий орешек", id_publisher=2)
    # book6 = Book(title="Скорость", id_publisher=2)

    # books = [pub1, pub2, book1, book2, book3, book4, book5, book6]

    # session.add_all(books)
    # session.commit()

    # shops = [
    #     Shop(name="Буквоед"),
    #     Shop(name="Академия"),
    #     Shop(name="Все свободны"),
    # ]

    # session.add_all(shops)
    # session.commit()

    # stocks = [
    #     Stock(id_book=1, id_shop=1, count=32),
    #     Stock(id_book=1, id_shop=2, count=25),
    #     Stock(id_book=1, id_shop=3, count=111),
    #     Stock(id_book=2, id_shop=1, count=213),
    #     Stock(id_book=2, id_shop=2, count=234),
    #     Stock(id_book=2, id_shop=3, count=43),
    #     Stock(id_book=3, id_shop=1, count=213),
    #     Stock(id_book=3, id_shop=2, count=234),
    #     Stock(id_book=3, id_shop=3, count=43),
    #     Stock(id_book=4, id_shop=1, count=213),
    #     Stock(id_book=4, id_shop=2, count=234),
    #     Stock(id_book=4, id_shop=3, count=43),
    #     Stock(id_book=5, id_shop=1, count=213),
    #     Stock(id_book=5, id_shop=2, count=234),
    #     Stock(id_book=5, id_shop=3, count=43),
    #     Stock(id_book=6, id_shop=1, count=213),
    #     Stock(id_book=6, id_shop=2, count=234),
    #     Stock(id_book=6, id_shop=3, count=43),
    # ]

    # session.add_all(stocks)
    # session.commit()

    # sales = [
    #     Sale(price=2054, date_sale="2024-01-15 14:30:00", id_stock=1, count=26),
    #     Sale(price=424, date_sale="2024-01-15 16:33:10", id_stock=2, count=23),
    #     Sale(price=3500, date_sale="2025-01-15 14:53:00", id_stock=3, count=26),
    #     Sale(price=99.84, date_sale="2025-02-15 11:22:40", id_stock=5, count=33),
    #     Sale(price=237, date_sale="2025-07-15 07:55:10", id_stock=4, count=7),
    # ]

    # session.add_all(sales)
    # session.commit()

    stocks_ids = [
        s.id for s in session.query(Stock.id).join(Book).filter(Book.id_publisher == 2)
    ]

    if stocks_ids:
        has_sales = session.query(Sale.id).filter(Sale.id_stock.in_(stocks_ids)).first()
        if has_sales is None:
            sales_for_pub2 = []
            base_prices = [990, 850, 765, 1230, 560]
            base_counts = [3, 1, 2, 4, 1]
            for idx, stock_id in enumerate(stocks_ids[:5]):
                sales_for_pub2.append(
                    Sale(
                        price=base_prices[idx],
                        date_sale=datetime(2025, 3, 1 + idx, 12, 0, 0),
                        id_stock=stock_id,
                        count=base_counts[idx],
                    )
                )
            session.add_all(sales_for_pub2)
            session.commit()

    user_input = input("Введите имя или id издателя: ").strip()
    publisher_filter = None
    if user_input.isdigit():
        publisher_filter = Publisher.id == int(user_input)
    else:
        publisher_filter = Publisher.name == user_input

    rows = (
        session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
        .join(Stock, Stock.id_book == Book.id)
        .join(Sale, Sale.id_stock == Stock.id)
        .join(Publisher, Publisher.id == Book.id_publisher)
        .join(Shop, Shop.id == Stock.id_shop)
        .filter(publisher_filter)
        .order_by(Sale.date_sale.desc())
        .all()
    )

    for title, shop_name, price, date_sale in rows:
        print(
            f"{title} | {shop_name:<12} | {int(price) if float(price).is_integer() else price} | {date_sale.strftime('%d-%m-%Y')}"
        )
