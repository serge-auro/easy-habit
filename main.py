import telebot
from telebot import types
from config import BOT_TOKEN
from actions import * # импортируем функции из actions.py

bot = telebot.TeleBot(BOT_TOKEN)
start_message = 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.'
help_message = 'Здесь будет список доступных команд и описание их функций.'

# Словарь кнопок
buttons_dict = {
    'menu': 'В главное Меню',
    'status': 'Статус',
    'report': 'Отчеты',
    'edit': 'Редактировать',
    'add': 'Добавить',
    'delete': 'Удалить',
    'done': 'Отметить V',
    'habits': 'Привычки'
}

# Функция для создания клавиатуры с выбранными кнопками
def create_keyboard(button_keys):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for key in button_keys:
        if key in buttons_dict:
            keyboard.add(types.KeyboardButton(buttons_dict[key]))
    return keyboard


# Обработчик команды "start" / Handler for "start" command (пока не реализовано)
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = create_keyboard(['status', 'edit', 'done'])
    bot.send_message(message.chat.id, 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.', reply_markup=keyboard)
    # функция init_user() для записи в базу данных информации о пользователе


# Обработчик команды 'status' / Handler for "status" command
@bot.message_handler('status')
def status(message):
    keyboard = create_keyboard(['done', 'menu'])
    bot.send_message(message.chat.id, 'Статус', reply_markup=keyboard)
    # функция get_habit_status() для получения статуса привычек пользователя


# Обработчик команды 'report' / Handler for "report" command
@bot.message_handler('report')
def report(message):
    keyboard = create_keyboard(['menu'])
    bot.send_message(message.chat.id, 'Отчеты', reply_markup=keyboard)
    # функция report() для получения отчета о выполненных привычках


# Обработчик команды 'edit' / Handler for "edit" command
@bot.message_handler('edit')
def edit(message):
    keyboard = create_keyboard(['add', 'delete', 'menu'])
    bot.send_message(message.chat.id, 'Редактировать', reply_markup=keyboard)
    bot.delete_message(message.chat.id, message.message_id)
    # просто отправка сообщения с клавиатурой


# Обработчик команды 'add' / Handler for "add" command
@bot.message_handler('add')
def add(message):
    keyboard = create_keyboard(['edit', 'delete', 'menu'])
    bot.send_message(message.chat.id, 'Добавить', reply_markup=keyboard)
    # функция edit_habit() для добавления привычки пользователя


# Обработчик команды 'delete' / Handler for "delete" command
@bot.message_handler('delete')
def delete(message):
    keyboard = create_keyboard(['edit', 'menu'])
    bot.send_message(message.chat.id, 'Удалить', reply_markup=keyboard)
    # функция edit_habit() для удаления привычки пользователя


# Обработчик команды 'done' / Handler for "done" command
@bot.message_handler('done')
def done(message):
    keyboard = create_keyboard(['status', 'edit', 'done', 'menu'])
    bot.send_message(message.chat.id, 'Отметить V', reply_markup=keyboard)
    # функция mark_habit() для отметки привычки пользователя как выполненной


# Обработчик команды 'habits' / Handler for "habits" command
@bot.message_handler('habits')
def habits(message):
    keyboard = create_keyboard(['add', 'edit', 'delete', 'menu'])
    bot.send_message(message.chat.id, 'Привычки', reply_markup=keyboard)
    bot.delete_message(message.chat.id, message.message_id)
    # просто отправка сообщения с клавиатурой


# Обработчик команды 'menu' / Handler for "menu" command
@bot.message_handler('menu')
def menu(message):
    keyboard = create_keyboard(['status', 'edit', 'done'])
    bot.send_message(message.chat.id, 'В главное Меню', reply_markup=keyboard)
    bot.delete_message(message.chat.id, message.message_id)
    # просто отправка сообщения с клавиатурой


# Обработчик команды "help" / Handler for "help" command
@bot.message_handler(commands=['help'])
def help(message):
    keyboard = create_keyboard(['status', 'habits', 'done'])
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)

bot.polling(none_stop=True)