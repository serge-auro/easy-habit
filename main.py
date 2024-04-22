import telebot

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Здесь будет список доступных команд.')


bot.polling(none_stop=True)

import sqlite3

# Создание соединения с базой данных (или её создание, если она не существует)
conn = sqlite3.connect('mydatabase.db')

# Создание курсора
c = conn.cursor()

# SQL запрос на создание таблицы Users
c.execute('''
CREATE TABLE IF NOT EXISTS Users (
   user_id INTEGER PRIMARY KEY,
   created_at DATETIME
)
''')

# SQL запрос на создание таблицы Habits
c.execute('''
CREATE TABLE IF NOT EXISTS Habits (
   habit_id INTEGER PRIMARY KEY,
   habit_name VARCHAR(50),
   habit_description VARCHAR,
   habit_target VARCHAR
)
''')

# SQL запрос на создание таблицы Habit_frequencies
c.execute('''
CREATE TABLE IF NOT EXISTS Habit_frequencies (
   frequency_id INTEGER PRIMARY KEY,
   frequency VARCHAR(50),
   time_per_period INT
)
''')

# SQL запрос на создание таблицы User_habits
c.execute('''
CREATE TABLE IF NOT EXISTS User_habits (
   user_habits_id INTEGER PRIMARY KEY,
   user_id INT,
   habit_id INT,
   frequency_id INT,
   start_date DATE,
   active BOOLEAN
)
''')

# Фиксирование изменений и закрытие соединения с базой данных
conn.commit()
conn.close()