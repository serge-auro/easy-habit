import sqlite3
import schedule
import time


def create_table():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_notify (
            user_id INTEGER,
            habit_id INTEGER,
            time TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()
def add_reminder(user_id, habit_id, time, message):
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('INSERT INTO user_notify (user_id, habit_id, time, message) VALUES (?, ?, ?, ?)',
              (user_id, habit_id, time, message))
    conn.commit()
    conn.close()

def send_reminders():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('SELECT user_id, message FROM user_notify WHERE time=?', (time.strftime('%H:%M'),))
    reminders = c.fetchall()
    for reminder in reminders:
        chat_id, message = reminder
        bot.send_message(chat_id=chat_id, text=message)
    conn.close()

schedule.every().minute.at(":00").do(send_reminders)

while True:
    schedule.run_pending()
    time.sleep(1)

# Пример добавления напоминания
add_reminder(123456, 1, '09:00', 'Не забудьте выполнить вашу утреннюю зарядку!')
