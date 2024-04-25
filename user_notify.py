import schedule
import time
from telegram import Bot

# Инициализация Telegram бота
TOKEN = 'телеграм-бот токен '
bot = Bot(token=TOKEN)
import sqlite3

def init_reminders_table():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
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

init_reminders_table()

def add_reminder(user_id, habit_id, reminder_time, message):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO reminders (user_id, habit_id, reminder_time, message)
        VALUES (?, ?, ?, ?)
    ''', (user_id, habit_id, reminder_time, message))
    conn.commit()
    conn.close()

def send_reminders():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    current_time = time.strftime('%H:%M')
    cur.execute('SELECT user_id, message FROM reminders WHERE reminder_time=?', (current_time,))
    reminders = cur.fetchall()
    for reminder in reminders:
        user_id, message = reminder
        chat_id = get_telegram_chat_id(user_id)  # Предполагаем, что у вас есть функция для получения chat_id по user_id
        bot.send_message(chat_id=chat_id, text=message)
    conn.close()

schedule.every().minute.do(send_reminders)

while True:
    schedule.run_pending()
    time.sleep(1)

