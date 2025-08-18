from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "Publisher"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)

    books = relationship("Book", backref="publisher")


class Book(Base):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80), nullable=False)

    id_publisher = Column(Integer, ForeignKey("Publisher.id"), nullable=False)


class Stock(Base):
    __tablename__ = "Stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_book = Column(Integer, ForeignKey("Book.id"), nullable=False)
    id_shop = Column(Integer, ForeignKey("Shop.id"), nullable=False)
    count = Column(Integer)

    book = relationship("Book", backref="stocks")
    shop = relationship("Shop", backref="stocks")
    sales = relationship("Sale", backref="stock")


class Shop(Base):
    __tablename__ = "Shop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)


class Sale(Base):
    __tablename__ = "Sale"
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    date_sale = Column(DateTime, nullable=False)
    id_stock = Column(Integer, ForeignKey("Stock.id"), nullable=False)
    count = Column(Integer, nullable=False)
