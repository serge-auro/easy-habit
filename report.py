import sqlite3
from datetime import datetime

def report(user_id, habit_id, period):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')  # Текущая дата в формате YYYY-MM-DD

    # Определяем начало периода для отчета
    if period == 'week':
        start_date = datetime.now().strftime('%Y-%m-%d')  # Сегодняшний день как начало периода
    elif period == 'month':
        start_date = datetime.now().strftime('%Y-%m-%d')  # Также сегодняшний день

    # Выборка данных из базы данных для отчета
    query = '''
        SELECT h.name, COUNT(*) as completion_count
        FROM user_habit_history uhh
        JOIN user_habit uh ON uh.id = uhh.user_habit_id
        JOIN habit h ON h.id = uh.habit_id
        WHERE uhh.mark_date >= ? AND uh.user_id = ? AND uh.habit_id = ?
        GROUP BY uh.habit_id
    '''
    cur.execute(query, (start_date, user_id, habit_id))
    result = cur.fetchone()
    conn.close()

    # Формируем и возвращаем отчет
    if not result:
        return f"No records found for habit ID {habit_id} starting from {start_date}"
    else:
        habit_name, completion_count = result
        return {
            "Habit Name": habit_name,
            "Start Date": start_date,
            "Completion Count": completion_count
        }

# Пример вызова функции
print(report(1, 2, 'week'))
print(report(1, 2, 'month'))
