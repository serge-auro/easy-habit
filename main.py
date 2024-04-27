import telebot
from telebot import types
from config import BOT_TOKEN
from actions import *
from db import *
from report import report

init_db()

bot = telebot.TeleBot(BOT_TOKEN)

start_message = 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.'
help_message = 'Здесь будет список доступных команд и описание их функций.'
# Словарь кнопок
buttons_dict = {
    'menu': 'На главную',
    'status': 'Статус',
    'report': 'Отчеты',
    'edit_habit': 'Редактировать',
    'new_habit': 'Добавить',
    'del_habit': 'Удалить',
    'mark_habit': 'Отметить V',
    'habits': 'Привычки'
}

# Функция для создания inline клавиатуры
def create_inline_keyboard(button_keys):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=buttons_dict[key], callback_data=key) for key in button_keys if key in buttons_dict]
    keyboard.add(*buttons)
    return keyboard

# Обработчик для возврата в главное меню
@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_menu(call):
    keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
    bot.send_message(call.message.chat.id, 'На главную', reply_markup=keyboard)

# Обработчик для вывода статуса текущих привычек
@bot.callback_query_handler(func=lambda call: call.data == 'status')
def handle_status(call):
    habits_info = habit_status(call.from_user.id)
    keyboard = create_inline_keyboard(['edit_habit', 'mark_habit', 'menu'])

    if not habits_info:
        bot.send_message(call.message.chat.id, 'У вас пока нет активных привычек или произошла ошибка.',
                         reply_markup=keyboard)
        return

    # Создание одной строки с описанием всех привычек
    respond_message = "\n".join([f"{habit} - {description}" for habit, description in habits_info.items()])
    bot.send_message(call.message.chat.id, respond_message, reply_markup=keyboard)


# Обработчик для вывода отчета
@bot.callback_query_handler(func=lambda call: call.data == 'report')
def handle_report(call):
    # Запрос списка привычек пользователя для выбора
    user_habits = habit_status(
        call.from_user.id)  # Предполагается, что функция возвращает словарь {habit_id: habit_name}
    if not user_habits:
        bot.send_message(call.message.chat.id, 'У вас нет активных привычек для создания отчета.')
        return

    keyboard = types.InlineKeyboardMarkup()
    for habit_id, habit_name in user_habits.items():
        keyboard.add(types.InlineKeyboardButton(text=habit_name, callback_data=f'report_select_{habit_id}'))
    bot.send_message(call.message.chat.id, 'Выберите привычку для создания отчета:', reply_markup=keyboard)


# Обработчик для выбора привычки и запроса периода
@bot.callback_query_handler(func=lambda call: call.data.startswith('report_select_'))
def select_habit_for_report(call):
    habit_id = call.data.split('_')[2]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Неделя', callback_data=f'report_week_{habit_id}'))
    keyboard.add(types.InlineKeyboardButton(text='Месяц', callback_data=f'report_month_{habit_id}'))
    bot.send_message(call.message.chat.id, 'Выберите период для отчета:', reply_markup=keyboard)


# Обработчик для генерации отчета
@bot.callback_query_handler(
    func=lambda call: call.data.startswith('report_week_') or call.data.startswith('report_month_'))
def generate_report(call):
    habit_id = call.data.split('_')[2]
    period = 'week' if 'week' in call.data else 'month'
    user_id = call.from_user.id
    report_result = report(user_id, habit_id, period)

    # Обработка ответа от функции report
    if isinstance(report_result, str):
        bot.send_message(call.message.chat.id, report_result)
    else:
        report_message = f"Привычка: {report_result['Habit Name']}\n" \
                         f"Период: с {report_result['Period Start']} по {report_result['Period End']}\n" \
                         f"Количество выполнений: {report_result['Completion Count']}"
        bot.send_message(call.message.chat.id, report_message)


# Обработчик для выбора редактирования привычки
@bot.callback_query_handler(func=lambda call: call.data == 'edit_habit')
def handle_edit_habit(call):
    respond_message = habit_status(call.from_user.id)
    if not respond_message:
        keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
        bot.send_message(call.message.chat.id, 'У вас пока нет активных привычек или произошла ошибка.', reply_markup=keyboard)
        return

    keyboard = types.InlineKeyboardMarkup()
    for habit, description in respond_message.items():
        button_text = f"{habit} - {description}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data='edit_' + habit))
    bot.send_message(call.message.chat.id, 'Выберите привычку для редактирования:', reply_markup=keyboard)

# Обработчик для выбора периодичности привычки
@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_') and not call.data.count('_') > 2)
def edit_selected_habit_frequency(call):
    selected_habit = call.data.split('_')[1]
    keyboard = types.InlineKeyboardMarkup()
    periods = ["daily", "weekly", "monthly"]
    for period in periods:
        keyboard.add(types.InlineKeyboardButton(text=f"Ежедневно" if period == "daily" else "Еженедельно" if period == "weekly" else "Ежемесячно",
                                                callback_data=f'edit_{selected_habit}_{period}_setcount'))
    bot.send_message(call.message.chat.id, 'Выберите периодичность привычки:', reply_markup=keyboard)

# Обработчик для запроса ввода количества повторений
@bot.callback_query_handler(func=lambda call: call.data.endswith('setcount'))
def request_habit_repetition_input(call):
    _, selected_habit, frequency = call.data.split('_')[1:4]
    message_text = f"Введите количество повторений для '{selected_habit}' (от 1 до 30)."
    bot.send_message(call.message.chat.id, message_text, reply_markup=types.ForceReply(selective=True))
    # Сохранение или обновление сессии
    session_data = {'habit': selected_habit, 'frequency': frequency}
    update_session(call.message.chat.id, 'awaiting_repetition_count', json.dumps(session_data))


# Обработчик для текстовых ответов на запрос количества повторений
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.text.startswith("Введите количество повторений"))
def handle_repetition_count_input(message):
    session_data = get_session(message.chat.id)
    if session_data:
        data = json.loads(session_data['data'])
        try:
            repetition_count = int(message.text)
            if 1 <= repetition_count <= 30:
                edit_habit(message.chat.id, data['habit'], data['frequency'], repetition_count)
                bot.send_message(message.chat.id, f"Установлено {repetition_count} повторений в день для '{data['habit']}'.")
                # Обновление или завершение сессии
                update_session(message.chat.id, 'completed', '{}')
            else:
                bot.send_message(message.chat.id, "Введите число от 1 до 30.")
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
    else:
        bot.send_message(message.chat.id, "Истекло время ожидания ввода, пожалуйста начните процесс заново.")


# Обработчик для выбора добавления новой привычки
@bot.callback_query_handler(func=lambda call: call.data == 'new_habit')
def handle_new_habit(call):
    respond_message = list_habits(call.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    for line in respond_message.split('\n')[1:]:  # Пропускаем первую строку (заголовок)
        if line.strip():
            habit_id, habit_info = line.split('.', 1)
            keyboard.add(types.InlineKeyboardButton(text=habit_info.strip(), callback_data='add_select_' + habit_id.strip()))
    bot.send_message(call.message.chat.id, "Выберите привычку для добавления:", reply_markup=keyboard)

# Обработчик для выбора периодичности добавляемой привычки
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_select_'))
def select_habit(call):
    selected_habit_id = call.data.split('_')[2]
    keyboard = types.InlineKeyboardMarkup()
    periods = ["daily", "weekly", "monthly"]
    for period in periods:
        keyboard.add(types.InlineKeyboardButton(text=f"Ежедневно" if period == "daily" else "Еженедельно" if period == "weekly" else "Ежемесячно",
                                                callback_data=f'add_{selected_habit_id}_{period}_setcount'))
    bot.send_message(call.message.chat.id, 'Выберите периодичность привычки:', reply_markup=keyboard)

# Обработчик для запроса ввода количества повторений
@bot.callback_query_handler(func=lambda call: call.data.endswith('setcount'))
def request_habit_repetition_input(call):
    _, selected_habit_id, frequency = call.data.split('_')[1:4]
    message_text = f"Введите количество повторений для привычки с ID {selected_habit_id} (от 1 до 30)."
    bot.send_message(call.message.chat.id, message_text, reply_markup=types.ForceReply(selective=True))
    # Сохранение или обновление сессии
    session_data = {'habit_id': selected_habit_id, 'frequency': frequency}
    update_session(call.message.chat.id, 'Введите количество повторений', json.dumps(session_data))


# Обработчик для текстовых ответов на запрос количества повторений
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.text.startswith("Введите количество повторений"))
def handle_repetition_count_input(message):
    session_data = get_session(message.chat.id)
    if session_data:
        data = json.loads(session_data['data'])
        try:
            repetition_count = int(message.text)
            if 1 <= repetition_count <= 30:
                # Добавляем новую привычку, используя информацию из сессии
                response_message = assign_habit(message.chat.id, data['habit_id'], data['frequency'], repetition_count)
                bot.send_message(message.chat.id, response_message)
                # Обновление или завершение сессии
                update_session(message.chat.id, 'completed', '{}')
            else:
                bot.send_message(message.chat.id, "Введите число от 1 до 30.")
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
    else:
        bot.send_message(message.chat.id, "Истекло время ожидания ввода, пожалуйста начните процесс заново.")


# Обработчик для добавления выбранной привычки
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def add_selected_habit(call):
    selected_habit = call.data.split('_')[1]
    assign_habit(call.from_user.id, selected_habit)
    bot.send_message(call.message.chat.id, f"Привычка '{selected_habit}' добавлена.")

# Обработчик для выбора удаления привычки
@bot.callback_query_handler(func=lambda call: call.data == 'del_habit')
def handle_del_habit(call):
    user_habit_status = habit_status(call.from_user.id)
    if not user_habit_status:
        keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
        bot.send_message(call.message.chat.id, 'У вас нет активных привычек или произошла ошибка.', reply_markup=keyboard)
        return

    keyboard = types.InlineKeyboardMarkup()
    for habit, description in user_habit_status.items():
        button_text = f"{habit} - {description}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data='del_' + habit))
    bot.send_message(call.message.chat.id, 'Выберите привычку для удаления:', reply_markup=keyboard)

# Обработчик для удаления выбранной привычки
@bot.callback_query_handler(func=lambda call: call.data.startswith('del_'))
def delete_selected_habit(call):
    selected_habit = call.data.split('_')[1]
    delete_habit(call.from_user.id, selected_habit)
    bot.send_message(call.message.chat.id, f"Привычка '{selected_habit}' была удалена.")

# Обработчик для выбора отметки привычки
@bot.callback_query_handler(func=lambda call: call.data == 'mark_habit')
def handle_mark_habit(call):
    user_habit_status = habit_status(call.from_user.id)
    if not user_habit_status:
        keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
        bot.send_message(call.message.chat.id, 'У вас пока нет активных привычек или произошла ошибка.', reply_markup=keyboard)
        return

    keyboard = types.InlineKeyboardMarkup()
    for habit, description in user_habit_status.items():
        button_text = f"{habit} - {description}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data='mark_' + habit))
    bot.send_message(call.message.chat.id, 'Выберите привычку для отметки:', reply_markup=keyboard)

# Обработчик для отметки выбранной привычки
@bot.callback_query_handler(func=lambda call: call.data.startswith('mark_'))
def mark_selected_habit(call):
    habit = call.data.split('mark_')[1]
    mark_habit(call.from_user.id, habit)
    bot.answer_callback_query(call.id, f"Привычка '{habit}' отмечена как выполненная.")
    bot.send_message(call.message.chat.id, f"Привычка '{habit}' успешно отмечена как выполненная!")


# Обработчики для вывода списка всех привычек (предустановленных)
@bot.callback_query_handler(func=lambda call: call.data == 'habits')
def handle_habits(call):
    respond_message = list_habits(call.from_user.id)
    keyboard = create_inline_keyboard(['new_habit', 'edit_habit', 'del_habit', 'menu'])
    bot.send_message(call.message.chat.id, respond_message, reply_markup=keyboard)


# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        init_user(message.chat.id)
    except Exception as e:
        print(e)
    finally:
        keyboard = create_inline_keyboard(['habits', 'status', 'new_habit'])
        bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


# Обработчик для команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    keyboard = create_inline_keyboard(['status', 'habits', 'mark_habit'])
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)


bot.polling(none_stop=True)
