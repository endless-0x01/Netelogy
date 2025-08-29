from contextlib import contextmanager
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

DSN = "postgresql://postgres:1234@localhost:5432/learningenglish_db"
engine = sq.create_engine(DSN)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        print(f"Ошибка - {e}, откат изменений")
        session.rollback()
        raise e
    finally:
        session.close()
        print("Сессия закрыта")
