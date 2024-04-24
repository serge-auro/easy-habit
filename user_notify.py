import sqlite3
import schedule
import time
from telegram import Bot

# Настройки Telegram бота
TOKEN = 'your_telegram_bot_token'
bot = Bot(token=TOKEN)

# Инициализация базы данных и таблиц
def init_db():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()

    # Включаем поддержку внешних ключей
    cur.execute("PRAGMA foreign_keys = ON")

    # Создание таблицы пользователей
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            active BOOLEAN NOT NULL DEFAULT 1,
            creation_date DATE
        )
    ''')

    # Создание таблицы привычек
    cur.execute('''
        CREATE TABLE IF NOT EXISTS habit (
            id INTEGER PRIMARY KEY autoincrement NOT NULL,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Создание таблицы связи пользователей и привычек
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_habit (
            id INTEGER PRIMARY KEY autoincrement NOT NULL,
            user_id INTEGER,
            habit_id INTEGER,
            active BOOLEAN NOT NULL DEFAULT 1,
            frequency_name TEXT CHECK(frequency_name IN ('ежедневно', 'еженедельно', 'ежемесячно')),
            frequency_count INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (habit_id) REFERENCES habit(id),
            CONSTRAINT unique_user_habit UNIQUE (user_id, habit_id)
        )
    ''')

    # Создание таблицы для хранения истории привычек
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_habit_history (
            id INTEGER PRIMARY KEY autoincrement NOT NULL,
            user_id INTEGER,
            habit_id INTEGER,
            mark_date DATE,
            mark_count INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (habit_id) REFERENCES habit(id),
            CONSTRAINT unique_user_habit UNIQUE (user_id, habit_id, mark_date)
        )
    ''')

    # Создание таблицы напоминаний
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY autoincrement NOT NULL,
            user_id INTEGER,
            habit_id INTEGER,
            reminder_time TIME,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (habit_id) REFERENCES habit(id)
        )
    ''')

    conn.commit()
    conn.close()

# Добавление напоминаний
def add_reminder(user_id, habit_id, reminder_time, message):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO reminders (user_id, habit_id, reminder_time, message)
        VALUES (?, ?, ?, ?)
    ''', (user_id, habit_id, reminder_time, message))
    conn.commit()
    conn.close()

# Функция отправки напоминаний
def send_reminders():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    current_time = time.strftime('%H:%M')
    cur.execute('SELECT user_id, message FROM reminders WHERE reminder_time=?', (current_time,))
    reminders = cur.fetchall()
    for reminder in reminders:
        user_id, message = reminder
        chat_id = get_telegram_chat_id(user_id)  # Заглушка для получения chat_id
        bot.send_message(chat_id=chat_id, text=message)
    conn.close()

# Планировщик для отправки напоминаний каждую минуту
schedule.every().minute.do(send_reminders)

# Инициализация БД и таблиц
init_db()

# Пример добавления напоминания
add_reminder(1, 2, '08:00', 'Время выполнить вашу привычку: Пить воду каждые 2 часа!')

# Запуск планировщика в бесконечном цикле
while True:
    schedule.run_pending()
    time.sleep(1)
