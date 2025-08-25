import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from configure import TOKEN_TG
from database import operations
from UserStates import UserStateManager

bot = telebot.TeleBot(TOKEN_TG)

user_states_manager = UserStateManager()


class Command:
    start_test = "🎯 Начать тест"
    add_word = "➕ Добавить слово"
    delete_word = "🔙 Удалить слово"
    show_stats = "📊 Статистика"

    def get_buttons():
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("🎯 Начать тест", callback_data="start_test"),
            InlineKeyboardButton("➕ Добавить слово", callback_data="add_word"),
            InlineKeyboardButton("🔙 Удалить слово", callback_data="delete_word"),
            InlineKeyboardButton("📊 Статистика", callback_data="show_stats"),
        )
        return keyboard


def start_test_mode(chat_id, user_id):

    user = operations.check_user_in_db(user_id)

    if not user:
        bot.send_message(chat_id, "Пользователь не найден в базе данных!")
        return

    data = operations.get_words_for_user(user.id)
    correct_answer = data["correct_answer"]

    if not data:
        bot.send_message(chat_id, "У вас нет слов для изучения")
        return

    keyboard = InlineKeyboardMarkup(row_width=2)

    for i in range(0, len(data["options"]), 2):
        if i + 1 < len(data["options"]):
            keyboard.add(
                InlineKeyboardButton(
                    data["options"][i],
                    callback_data=f"answer_{data['word_id']}_{correct_answer}_{data['options'][i]}",
                ),
                InlineKeyboardButton(
                    data["options"][i + 1],
                    callback_data=f"answer_{data['word_id']}_{correct_answer}_{data['options'][i+1]}",
                ),
            )
        else:
            keyboard.add(
                InlineKeyboardButton(
                    data["options"][i],
                    callback_data=f"answer_{data['word_id']}_{correct_answer}_{data['options'][i]}",
                )
            )

    keyboard.add(
        InlineKeyboardButton("➕ Добавить слово", callback_data="add_word_mode")
    )
    keyboard.add(
        InlineKeyboardButton("🔙 Удалить слово", callback_data="delete_word_mode")
    )

    question_text = f"Передите следующие слово: <b>{data['question_word']}</b>"
    bot.send_message(chat_id, question_text, reply_markup=keyboard, parse_mode="HTML")


def check_answer(call):
    parts = call.data.split("_")
    word_id = int(parts[1])
    correct_answer = parts[2]
    selected_answer = parts[3]
    bot.send_message(call.message.chat.id, f"Ваш ответ: {selected_answer}")

    if selected_answer == correct_answer:
        result_message = "Вы ответили правильно! ✅"
        is_correct = True

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("⏩ Следующее слово", callback_data="start_test")
        )
        keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        bot.send_message(call.message.chat.id, result_message)
        bot.send_message(
            call.message.chat.id, "Что делаем дальше?", reply_markup=keyboard
        )
    else:
        result_message = f"❌ Неправильно! Правильный ответ: {correct_answer}"
        is_correct = False

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("🔄 Попробовать снова", callback_data="start_test")
        )
        keyboard.add(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        bot.send_message(call.message.chat.id, result_message)
        bot.send_message(
            call.message.chat.id,
            "Попробуйте еще раз или вернитесь в меню:",
            reply_markup=keyboard,
        )

    user_id = operations.check_user_in_db(call.from_user.id)
    operations.record_result_user(user_id.id, word_id, is_correct)


@bot.message_handler(func=lambda message: not message.text.startswith("/"))
def handle_text_input(message):

    user_id = operations.check_user_in_db(message.from_user.id).id

    current_state = user_states_manager.get_state(user_id)

    if current_state:
        if current_state == "waiting_russian_word":

            user_states_manager.set_data(user_id, "russian_word", message.text)

            bot.send_message(message.chat.id, f"Русское слово: {message.text}")
            bot.send_message(message.chat.id, "Теперь введите английское слово")

            user_states_manager.set_state(user_id, "waiting_english_word")
            current_state = "waiting_english_word"

        elif current_state == "waiting_english_word":

            user_states_manager.set_data(user_id, "english_word", message.text)

            bot.send_message(message.chat.id, f"Английское слово: {message.text}")
            bot.send_message(message.chat.id, "Теперь введите категорию")

            user_states_manager.set_state(user_id, "waiting_category")
            current_state = "waiting_category"

        elif current_state == "waiting_category":
    

            user_states_manager.set_data(user_id, "category", message.text)
            bot.send_message(message.chat.id, f"Категория: {message.text}")

            result = operations.add_word_for_user(
                user_id,
                user_states_manager.get_data(user_id, "russian_word"),
                user_states_manager.get_data(user_id, "english_word"),
                user_states_manager.get_data(user_id, "category"),
            )
            if result:
                bot.send_message(message.chat.id, "Слово добавлено!")
            else:
                bot.send_message(message.chat.id, "Такое слово уже есть в вашем словаре")

            user_states_manager.clear_user(user_id)

            bot.send_message(
                message.chat.id, "Главное меню", reply_markup=Command.get_buttons()
            )

        elif current_state == 'waiting_word_search':
            found_words = operations.find_word_by_name(user_id, message.text)
            keyboard = InlineKeyboardMarkup(row_width=2)
            if found_words:
                for user_word, word in found_words:
                    keyboard.add(InlineKeyboardButton(word.russian_word, callback_data=f'delete_word_{user_word.user_id}_{word.id}'))
                
                bot.send_message(message.chat.id, 'Выберите слово для удаления', reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, 'Слово не найдено!')
                keyboard.add(InlineKeyboardButton('Главное меню 🏠', callback_data=f'main_menu'))
                bot.send_message(message.chat.id, 'Вернуться в главнео меню 🏠', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f"Вы ввели слово: {message.text}")


def add_word_mode(chat_id, user_id):
    user_id_ = operations.check_user_in_db(user_id).id
    user_states_manager.set_state(user_id_, "waiting_russian_word")

    bot.send_message(chat_id, "Введите слово на русском языке: ")
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("❌ Отмена", callback_data="main_menu"))
    bot.send_message(chat_id, "Или нажмите отмена", reply_markup=keyboard)

def delete_word_mode(chat_id, user_id):
    user_states_manager.set_state(operations.check_user_in_db(user_id).id, 'waiting_word_search')
    bot.send_message(chat_id, 'Введите названия слова для поиска:')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("❌ Отмена", callback_data="main_menu"))
    bot.send_message(chat_id, "Или нажмите отмена", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    bot.answer_callback_query(call.id)

    if call.data == "start_test":
        start_test_mode(call.message.chat.id, call.from_user.id)
    elif call.data == "add_word":
        add_word_mode(call.message.chat.id, call.from_user.id)
    elif call.data == "delete_word":
        delete_word_mode(call.message.chat.id, call.from_user.id)
    elif call.data == "show_stats":
        bot.send_message(call.message.chat.id, "📊 Показываем статистику!")
    elif call.data.startswith("answer_"):
        check_answer(call)
    elif call.data == "main_menu":
        bot.send_message(
            call.message.chat.id, "Главное меню", reply_markup=Command.get_buttons()
        )
    elif call.data == "add_word_mode":
        add_word_mode(call.message.chat.id, call.from_user.id)
    elif call.data == 'delete_word_mode':
        delete_word_mode(call.message.chat.id, call.from_user.id)
    elif call.data.startswith('delete_word_'):
        parts = call.data.split('_')
        user_word_id = int(parts[2])
        word_id = int(parts[3])
        result = operations.delete_word_for_user(user_word_id, word_id)

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Вернуться в главное меню 🏠', callback_data='main_menu'))

        if result:
            bot.send_message(call.message.chat.id, 'Слово успешно удалено!')
            bot.send_message(call.message.chat.id, 'Вернуться в главное меню 🏠', reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, 'Мы не смогли удалить данное слово')
            bot.send_message(call.message.chat.id, 'Вернуться в главное меню 🏠', reply_markup=keyboard)



@bot.message_handler(commands=["start"])
def send_welcome(message):
    if operations.check_user_in_db(message.from_user.id):
        bot.reply_to(message, f"Рады снова тебя видеть {message.from_user.username}!")
    else:
        data_user = {
            "id": message.from_user.id,
            "login": message.from_user.username,
            "fname": message.from_user.first_name,
            "lname": message.from_user.last_name,
        }

        welcome_text = """Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе.
У тебя есть возможность использовать тренажёр, как конструктор, и собирать свою собственную базу для обучения. 
Для этого воспрользуйся инструментами:

        добавить слово ➕,
        удалить слово  🔙.
        Ну что, начнём ⬇️
                    """
        operations.create_user_db(data_user)
        bot.reply_to(
            message, f"Привет {message.from_user.first_name} 👋, {welcome_text}"
        )

    bot.send_message(
        message.chat.id, "Чем займемся: ", reply_markup=Command.get_buttons()
    )


if __name__ == "__main__":
    print("Бот запущен")
    bot.polling()
