from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(70))
    first_name = Column(String(70))
    last_name = Column(String(70))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    words_count = Column(Integer, default=0)


class Words(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    russian_word = Column(String(80), nullable=False)
    english_word = Column(String(100), nullable=False)
    is_common = Column(Boolean, nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class User_Words(Base):
    __tablename__ = "user_words"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    is_learned = Column(Boolean, nullable=False)
    correct_answers = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    last_practiced = Column(
        DateTime,
        default=lambda: datetime.now(
            timezone.utc))

    word = relationship("Words", backref="user_words")
    user = relationship("Users", backref="word_users")
