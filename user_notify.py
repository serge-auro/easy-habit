import sqlite3
import schedule
import time
from main import user_notify


def notify_all_active_users():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()

    cur.execute("SELECT id FROM user WHERE active = 1")
    active_users = cur.fetchall()

    for user in active_users:
        user_id = user[0]
        notify_user_habits(user_id)

    conn.close()


def notify_user_habits(user_id):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()

    cur.execute("SELECT hh.name as habit_name, frequency_name, frequency_count "
                "  FROM user_habit as uh"
                "  JOIN habit as hh ON hh.id = uh.habit_id"
                " WHERE uh.user_id = ? AND uh.active = 1",
                (user_id,))
    user_habits = cur.fetchall()

    message = ''
    for habit in user_habits:
        habit_name, frequency_name, frequency_count = habit
        message += (f'Привычка: {habit_name} частота: {frequency_name} кол-во: {frequency_count}')

    user_notify(user_id, message)

    conn.close()


def scheduled_job():
    user_id = 314175772
    message = 'Это ваше сообщение от бота каждый час!'
    user_notify(user_id, message)


# Расписание крон задачи
# schedule.every().minute.do(scheduled_job) # test message
schedule.every().hour.do(notify_all_active_users)

# Запуск крон задачи
while True:
    schedule.run_pending()
    time.sleep(1)
