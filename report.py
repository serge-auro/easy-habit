import sqlite3

def create_tables():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_habit (
            user_id INTEGER,
            habit_id INTEGER,
            habit_name TEXT,
            habit_description TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            user_id INTEGER,
            habit_id INTEGER,
            date_completed DATE
        )
    ''')
    conn.commit()
    conn.close()

create_tables()


def report(user_id, habit_id, period):
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()

    # Определение даты начала периода
    if period == 'Прошедшая неделя':
        c.execute("Введите числа ('now', '-7 day')")
    elif period == 'Прошедшиц месяц':
        c.execute("Введите число ('now', '-1 month')")
    start_date = c.fetchone()[0]

    # Получение данных из таблиц
    query = '''
        SELECT uh.habit_name, h.date_completed
        FROM user_habit uh
        JOIN history h ON uh.user_id = h.user_id AND uh.habit_id = h.habit_id
        WHERE uh.user_id = ? AND uh.habit_id = ? AND h.date_completed >= ?
        ORDER BY h.date_completed
    '''
    c.execute(query, (user_id, habit_id, start_date))
    results = c.fetchall()
    conn.close()

    if not results:
        print("Не найдено записей.")
    else:
        for result in results:
            print(f"Привычка: {result[0]}, Дата: {result[1]}")


# Пример использования функции
report(123456, 1, 'last week')
