import sqlite3
def add_info():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
                (1234567890, '2024-04-22'))

    cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                ('Пить воду','Необходимо пить воду'))

    cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                "VALUES (?,?, ?, ?, ?)", (1234567890, 1, 1, 'ежедневно', 3))

    cur.execute("INSERT INTO user_habit_history "
                "(user_id, habit_id, mark_date, mark_count)"
                "VALUES (?, ?, ?, ?)", (1234567890, 1, '2024-04-22', 1))

    conn.commit()
    conn.close()

add_info()