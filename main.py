import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')  # Инициализация бота / Initialize the bot
start_message = 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.'
help_message = 'Здесь будет список доступных команд.'


# Создание универсальной клавиатуры / Create a universal keyboard
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Создание объекта клавиатуры / Create keyboard object
    button_add = types.KeyboardButton('Добавить')  # Кнопка добавления / Add button
    button_del = types.KeyboardButton('Удалить')  # Кнопка удаления / Delete button
    button_list = types.KeyboardButton('Список')  # Кнопка списка / List button
    button_stats = types.KeyboardButton('Статистика')  # Кнопка статистики / Statistics button
    keyboard.add(button_add, button_del, button_list, button_stats)  # Добавление кнопок на клавиатуру / Add buttons to the keyboard
    return keyboard

# Обработчик команды "start" / Handler for "start" command
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = create_keyboard()  # Получение клавиатуры / Get the keyboard
    # Отправка приветственного сообщения с клавиатурой / Send a welcome message with the keyboard
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)

# Обработчик команды "help" / Handler for "help" command
@bot.message_handler(commands=['help'])
def help(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)

bot.polling(none_stop=True)  # Запуск бота / Start the bot
