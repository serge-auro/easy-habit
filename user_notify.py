import sqlite3


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

    cur.execute("SELECT habit_id, frequency_name, frequency_count FROM user_habit WHERE user_id = ? AND active = 1",
                (user_id,))
    user_habits = cur.fetchall()

    for habit in user_habits:
        habit_id, frequency_name, frequency_count = habit
        # При том, что функция user_notify уже определена в main.py
        user_notify(user_id, habit_id, frequency_name, frequency_count)

    conn.close()
