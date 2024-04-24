import sqlite3
def add_info():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
                (1234567890, '2024-04-22'))
    cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
                (1234567891, '2024-04-25'))
    cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
                (1234567892, '2024-04-26'))
    cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
                (1234567893, '2024-04-27'))
    cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
                (1234567894, '2024-04-28'))

    cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                ('Пить воду','Необходимо пить воду'))
    cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                ('Спорт','Необходимо ходить на тренировку'))
    cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                ('Отношения','Необходимо встречаться с друзьями'))
    cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                ('Память','Выучить стих'))
    cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                ('Вокал','Обучение пению'))


    cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                "VALUES (?,?, ?, ?, ?)", (1234567890, 1, 1, 'ежедневно', 3))
    cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                "VALUES (?,?, ?, ?, ?)", (1234567891, 2, 1, 'ежедневно', 1))
    cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                "VALUES (?,?, ?, ?, ?)", (1234567892, 3, 1, 'еженедельно', 1))
    cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                "VALUES (?,?, ?, ?, ?)", (1234567893, 4, 1, 'ежедневно', 1))
    cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                "VALUES (?,?, ?, ?, ?)", (1234567894, 5, 1, 'ежемесячно', 1))

    cur.execute("INSERT INTO user_habit_history "
                "(user_id, habit_id, mark_date, mark_count)"
                "VALUES (?, ?, ?, ?)", (1234567890, 1, '2024-04-29', 1))
    cur.execute("INSERT INTO user_habit_history "
                "(user_id, habit_id, mark_date, mark_count)"
                "VALUES (?, ?, ?, ?)", (1234567892, 2, '2024-04-29', 1))
    cur.execute("INSERT INTO user_habit_history "
                "(user_id, habit_id, mark_date, mark_count)"
                "VALUES (?, ?, ?, ?)", (1234567893, 3, '2024-04-29', 1))
    cur.execute("INSERT INTO user_habit_history "
                "(user_id, habit_id, mark_date, mark_count)"
                "VALUES (?, ?, ?, ?)", (1234567894, 4, '2024-04-29', 1))
    cur.execute("INSERT INTO user_habit_history "
                "(user_id, habit_id, mark_date, mark_count)"
                "VALUES (?, ?, ?, ?)", (1234567895, 5, '2024-04-29', 1))


    conn.commit()
    conn.close()

add_info()