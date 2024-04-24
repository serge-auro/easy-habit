import sqlite3
from datetime import datetime, timedelta


def report(user_id, habit_id, period):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()

    # Определение периода для отчета
    today = datetime.now()
    if period == 'Текущая неделя':
        start_of_week = today - timedelta(days=today.weekday())  # начало текущей недели (понедельник)
        start_date = start_of_week.strftime('%Y-%m-%d')
    elif period == 'Прошедшая неделя':
        start_of_last_week = today - timedelta(days=today.weekday() + 7)  # начало прошлой недели
        end_of_last_week = start_of_last_week + timedelta(days=6)  # конец прошлой недели
        start_date = start_of_last_week.strftime('%Y-%m-%d')
        end_date = end_of_last_week.strftime('%Y-%m-%d')
    elif period == 'Текущий месяц':
        start_of_month = today.replace(day=1)  # начало текущего месяца
        start_date = start_of_month.strftime('%Y-%m-%d')
    elif period == 'Прошедший месяц':
        start_of_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)  # начало прошлого месяца
        end_of_last_month = (today.replace(day=1) - timedelta(days=1))  # конец прошлого месяца
        start_date = start_of_last_month.strftime('%Y-%m-%d')
        end_date = end_of_last_month.strftime('%Y-%m-%d')

    # Выборка данных из базы
    if period in ['Текущая неделя', 'Текущий месяц']:
        query = '''
            SELECT uh.habit_id, h.name, uh.user_id, COUNT(*) as completion_count
            FROM user_habit_history uhh
            JOIN user_habit uh ON uh.id = uhh.user_habit_id
            JOIN habit h ON h.id = uh.habit_id
            WHERE uhh.mark_date >= ? AND uh.user_id = ? AND uh.habit_id = ?
            GROUP BY uh.habit_id, uhh.mark_date
        '''
        cur.execute(query, (start_date, user_id, habit_id))
    else:
        query = '''
            SELECT uh.habit_id, h.name, uh.user_id, COUNT(*) as completion_count
            FROM user_habit_history uhh
            JOIN user_habit uh ON uh.id = uhh.user_habit_id
            JOIN habit h ON h.id = uh.habit_id
            WHERE uhh.mark_date BETWEEN ? AND ? AND uh.user_id = ? AND uh.habit_id = ?
            GROUP BY uh.habit_id, uhh.mark_date
        '''
        cur.execute(query, (start_date, end_date, user_id, habit_id))

    results = cur.fetchall()
    conn.close()

    if not results:
        return "На данный период записей не найдено"
    else:
        report_data = []
        for result in results:
            report_data.append({
                "Habit ID": result[0],
                "Habit Name": result[1],
                "User ID": result[2],
                "Completion Count": result[3]
            })
        return report_data


# Пример вызова функции
print(report(1, 2, 'Прошедшая неделя'))
