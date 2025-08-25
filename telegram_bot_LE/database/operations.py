from database.database import get_session
from database.models import Base, User_Words, Users, Words
from datetime import datetime, timezone
import random


def check_user_in_db(telegram_id):
    with get_session() as session:
        user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if user:
            return user
        else:
            return False


def create_user_db(data_user: dict):
    with get_session() as session:
        user = session.query(Users).filter(Users.telegram_id == data_user["id"]).first()
        if user:
            return user

        user = Users(
            telegram_id=data_user["id"],
            username=data_user["login"] if data_user["login"] else None,
            first_name=data_user["fname"] if data_user["fname"] else None,
            last_name=data_user["lname"] if data_user["lname"] else None,
            created_at=datetime.now(timezone.utc),
        )

        session.add(user)
        session.commit()

        for word in session.query(Words).all():
            user_words = User_Words(
                user_id=user.id,
                word_id=word.id,
                is_learned=False,
                last_practiced=datetime.now(timezone.utc),
            )
            session.add(user_words)
        session.commit()

        return user


def get_words_for_user(user_id: int):
    with get_session() as session:
        user_words = (
            session.query(User_Words).filter(User_Words.user_id == user_id).all()
        )
        if not user_words:
            return []
        random_user_word = random.choice(user_words)
        word = session.query(Words).filter(Words.id == random_user_word.word_id).first()

        correct_answer = word.english_word
        wrong_words = (
            session.query(Words)
            .filter(Words.english_word != correct_answer)
            .limit(3)
            .all()
        )

        options = [correct_answer]
        for wrong_word in wrong_words:
            options.append(wrong_word.english_word)

        random.shuffle(options)

    return {
        "question_word": word.russian_word,
        "correct_answer": correct_answer,
        "options": options,
        "word_id": word.id,
    }


def record_result_user(user_id: int, word_id: int, is_correct: bool):
    with get_session() as session:
        user_word = (
            session.query(User_Words)
            .filter(User_Words.user_id == user_id, User_Words.word_id == word_id)
            .first()
        )

        if not user_word:
            return False

        user_word.total_attempts += 1
        if is_correct:
            user_word.correct_answers += 1

        user_word.last_practiced = datetime.now(timezone.utc)

        session.commit()

    return True


def add_word_for_user(
    user_id_: int, russian_word_: str, english_word_: str, category_: str
):
    with get_session() as session:

        existing_word = (
            session.query(Words)
            .join(User_Words, Words.id == User_Words.word_id)
            .filter(
                Words.russian_word == russian_word_,
                Words.english_word == english_word_,
                User_Words.user_id == user_id_,
            )
            .first()
        )
        if existing_word:
            return False

        new_word = Words(
            russian_word=russian_word_,
            english_word=english_word_,
            is_common=False,
            category=category_,
            created_at=datetime.now(timezone.utc),
        )

        session.add(new_word)
        session.commit()

        user_word = User_Words(
            user_id=user_id_,
            word_id=new_word.id,
            is_learned=False,
            correct_answers=0,
            total_attempts=0,
            last_practiced=datetime.now(timezone.utc),
        )

        session.add(user_word)
        session.commit()

        user = session.query(Users).filter(Users.id == user_id_).first()
        user.words_count += 1
        session.commit()

        return True


def find_word_by_name(user_id: int, search_text: str):
    with get_session() as session:
        user_words = (
            session.query(User_Words, Words)
            .join(Words, User_Words.word_id == Words.id)
            .filter(
                User_Words.user_id == user_id,
                Words.russian_word.ilike(f"%{search_text}%"),
            )
            .all()
        )
    return user_words


def delete_word_for_user(user_id_: int, word_id_: int):
    with get_session() as session:
        user_words = (
            session.query(User_Words)
            .filter(
                User_Words.user_id == user_id_,
                User_Words.word_id == word_id_,
            )
            .first()
        )
        if user_words is None:
            return False

        word = session.query(Words).filter(Words.id == user_words.word_id).first()
        if word.is_common:
            session.delete(user_words)
        else:
            other_relations = (
                session.query(User_Words)
                .filter(
                    User_Words.word_id == word.id,
                    User_Words.user_id != user_id_,
                )
                .first()
            )
            if other_relations:
                session.delete(user_words)
            else:
                session.delete(user_words)
                session.delete(word)

        session.commit()
        return True


def get_user_stats(user_id: int):
    with get_session() as session:
        user_stats = (
            session.query(User_Words)
            .filter(
                User_Words.user_id == user_id,
            )
            .all()
        )

        if not user_stats:
            return False

        total_correct = sum(word.correct_answers for word in user_stats)
        total_attempts = sum(word.total_attempts for word in user_stats)

        if total_attempts > 0:
            percentage = (total_correct / total_attempts) * 100
        else:
            percentage = 0

        last_practice = (
            session.query(User_Words)
            .filter(User_Words.user_id == user_id)
            .order_by(User_Words.last_practiced.desc())
            .first()
        )

        return {
            "Общее количество слов": len(user_stats),
            "Количество изученных слов": len(
                session.query(User_Words)
                .filter(
                    User_Words.user_id == user_id,
                    User_Words.is_learned == True,
                )
                .all()
            ),
            "Процент правильных ответов": percentage,
            "Последнее время практики": (
                last_practice.last_practiced if last_practice else "Практика отсуствует"
            ),
        }
