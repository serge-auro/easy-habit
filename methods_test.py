import sqlite3
from datetime import datetime
from datetime import timedelta


#Метод создания нового юзера.  У нового юзера из ТГ достается его telegram id,
# и записывается в таблицу users как users.id
# (где users - название таблицы, id - название столбца)
#также, функция datetime.now().strftime('%Y-%m-%d') записывает дату создания записи
# о пользователе в таблицу users в столбец creation_date
#по умолчанию статус active = 1 (столбец users.active)
def init_user(user_id): #где user_id = message.chat.id
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, creation_date) VALUES (?, ?)",
                (user_id, datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

#Добавление привычки в таблицу, вводим вручную 5 предопределенных привычек
#надо продумать, как грамматически описывать новые привычки в зависимости от способа вывода в ТГ
#например name = "Пить воду", description = "Необходимо пить воду для поддержания водного баланса в организме"
#тогда ав ТГ выводим "Вы выбрали привычку: {habit.name}. Она важна, потому что {habit.description}"
def init_habit(name, description):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO habit ( name, description) VALUES (?, ?)",
                (name, description))
    conn.commit()
    conn.close()


#Метод присваивания привычки юзеру.

#????????????????Вопрос для FE: в логике программы будет получен habit.id
# или нужно написать функцию для его получения по какому-то параметру (имени, например)???????????????

#В таблицу user_habit записывается user_id юзера -
#id юзера из ТГ user_id = message.chat.id,
#habit_id - habit.id привычки из таблицы habit,
# Значения frequency_name (ежедневно, еженедельно, ежемесячно) и
# frequency_count (количество повторений привычки за период)
# должны быть заданы юзером в ТГ

def assign_habit(user_id, habit_id, frequency_name, frequency_count):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO user_habit (user_id, habit_id, frequency_name, frequency_count) VALUES (?, ?, ?, ?)",
                (user_id, habit_id,frequency_name, frequency_count))

                 # Значение user_id = message.chat.id, habit_id = id заданной привычки из таблицы habit
    cur.execute("SELECT name FROM habit WHERE id = ?", (habit_id,))
    print( f"Вы добавили себе привычку {cur.fetchone()[0]}, которую хотите выполнять {frequency_name}, {frequency_count} раз за период")
    conn.commit()
    conn.close()

# Метод вызова списка всех доступных для выбора привычек
# (пока что у нас их 5). Входной параметр id юзера из ТГ: user_id = message.chat.id

def list_habits(user_id):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("SELECT  id, name, description FROM habit")
    habits = cur.fetchall()
    print("Это результат работы функции list_habits: Cписок привычек:")
    for habit in habits:
        print(f"{habit[0]}. {habit[1]}: {habit[2]}")
    # возвращает список с именами и описаниями привычек
    # 1 строка = 1 привычка
    # надо посмотреть, как это выводится в ТГ
    conn.close()

# Запрос для получения названия и описания всех активных привычек пользователя
#Входной параметр id юзера из ТГ: user_id = message.chat.id
# сначала метод достает все активные привычки пользователя
# (столбцы habit.name и habit.description) из таблицы user_habit,
# и записывает данные в список habits,
# затем проверяется, если список пуст, то выводим сообщение об этом:
# "У Вас нет подключенных привычек"
# если список не пуст, то циклом выводим сообщением ТГ привычки, каждая с новой строки

def habit_status(user_id):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT habit.name, habit.description
        FROM habit 
        INNER JOIN user_habit ON user_habit.habit_id = habit.id
        WHERE user_habit.user_id = ? AND user_habit.active = 1
    ''', (user_id,))
    i=1 #чтобы пронумеровать активные привычки
    habits = cur.fetchall()
    if habits: # если список активных привычек не пуст
        print("Это результат работы функции habit_status: Список Ваших подключенных привычек:")
        for habit in habits:
            print( f"{i}. {habit[0]}: {habit[1]}")
            i += 1
    else: # если список активных привычек пуст
        print( "У Вас нет подключенных привычек")
    conn.close()

#Метод редактирования привычки - возможность изменения периодичночти frequency_name
#и количества повторений привычки за период frequency_count.
# Входные параметры id юзера из ТГ: user_id = message.chat.id,
# habit_id = id привычки из таблицы habit
# frequency_name (ежедневно, еженедельно, ежемесячно) вводит пользователь в ТГ
# frequency_count (количество повторений привычки за период) вводит пользователь в ТГ

def edit_habit(user_id, habit_id, frequency_name, frequency_count):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("UPDATE user_habit SET frequency_name = ?, frequency_count = ? WHERE user_id = ? AND habit_id = ?",
                (frequency_name, frequency_count, user_id, habit_id))
    cur.execute("SELECT name FROM habit WHERE id = ?", (habit_id,))
    print(f"Вы изменили параметры привычки {cur.fetchone()[0]} на {frequency_name}, {frequency_count} раз за период")
    conn.commit()
    conn.close()

#Метод удаления привычки - меняет столбец user_habit.active на 0
#и количества повторений привычки за период frequency_count.
# Входные параметры id юзера из ТГ: user_id = message.chat.id,
# habit_id = id привычки из таблицы habit

def delete_habit(user_id, habit_id):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM user_habit WHERE user_id = ? AND habit_id = ?",
                (user_id, habit_id))
    cur.execute("SELECT name FROM habit WHERE id = ?",(habit_id,))
    print( f"Вы удалили привычку {cur.fetchone()[0]}")
    conn.commit()
    conn.close()



# Функция для отметки привычки

#????????????????????????? Вопрос для FE - по умолчанию mark_count увеличивается на 1, то есть человек,
# который уже попил воду 2 раза из 3 нужных должен два раза зайти и отметить
# выполненной привычку. Это неудобно, если он вспомнил об отметке позже.
# Для этого мы можем задать количество отмечаний count,
# чтобы отметить сразу несколько выполнений, но тогда нужен соответствующий функционал в FE???????????????????????????

# Принцип работы функции: из таблицы user_habit_history достаем user_habit_history.id
# (просто порядковый номер записи о выполнении привычки) и
# переменную count - то, сколько раз привычка уже была отмечена
# и записываем эти данные в переменную result.
# если нет записи в таблице user_habit_history, мы ее создаем, по умолчанию параметр count = 1
# (но его можно изменить, если просто прописать ему значение).
# Если запись есть, то мы увеличиваем count на frequency_count на величину count (по умолчанию count = 1)
# Также, входные параметры id юзера из ТГ: user_id = message.chat.id,
# # habit_id = id привычки из таблицы habit.

#Замечание: если привычка была отмечена достаточно раз, то при повторном вызове функции
# будет выведено сообщение об этом: "Вы уже выполняли эту привычку достаточно раз",
# но если она выполнена недостаточно раз: 2 раза из 3,
# то теоретически пользователь может добавить еще 2 выполнения.
# Сейчас он получает об этом сообщение и не может добавить еще 2 выполнения.
# Стоит ли ограничивать перевыполнение нормы?



def mark_habit(user_id, habit_id, mark_date, count=1):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    try:
        # получаем название привычки
        cur.execute("SELECT name FROM habit WHERE id = ?", (habit_id,))
        habit_name = cur.fetchone()[0]
        #используем конструкцию try-finally, чтобы точно закрыть подключение к БД, если функция завершиться раньше
        # Сначала проверяем, существует ли уже запись для данного пользователя, привычки и даты
        # и сохраняем id записи, число выполнений и дату выполнения в
        # переменные user_habit_history_id, current_count, current_date
        cur.execute('''
            SELECT id, mark_count
            FROM user_habit_history
            WHERE user_id = ? AND habit_id = ? AND mark_date = ?
        ''', (user_id, habit_id, mark_date))
        result = cur.fetchone()
        if result:
            user_habit_history_id, current_count = result
        else:
            user_habit_history_id, current_count = None, 0


        # Проверяем, какую периодичность и частоту выполнения привычки за период пользователь установил
        # в целях и сохраняем это в переменные set_frequency_name, set_frequency_count
        cur.execute('''
                    SELECT frequency_name, frequency_count
                    FROM user_habit
                    WHERE user_id = ? AND habit_id = ?
                ''', (user_id, habit_id))
        set_frequency = cur.fetchone()
        if set_frequency:
            set_frequency_name, set_frequency_count = set_frequency
        else:
            set_frequency_name, set_frequency_count = None, None

        # Если запись существует, увеличиваем mark_count на count, по умолчанию count = 1,
        # в зависимости от периода для привычек: Ежедневно, Еженедельно, Ежемесячно
        if result:

            mark_date_obj = datetime.strptime(mark_date, '%Y-%m-%d')
            # Преобразование даты в объект datetime - вроде она в БД уже записана в формате %Y-%m-%d,
            # но я не уверена, как они взаимодействуют, поэтому на всякий случай преобразуем дату
            if set_frequency_name == 'ежедневно':
                period_start = mark_date_obj
            elif set_frequency_name == 'еженедельно':
                period_start = mark_date_obj - timedelta(days=mark_date_obj.weekday())
                # Понедельник текущей недели - вычитаем количество дней, соответствующее текущему дню недели
            elif set_frequency_name == 'ежемесячно':
                period_start = mark_date_obj.replace(day=1)  # День месяца изменяется на первый

            period_start_str = period_start.strftime('%Y-%m-%d')# Преобразование даты в строку в формате %Y-%m-%d

            cur.execute('''
                        SELECT SUM(mark_count)
                        FROM user_habit_history
                        WHERE user_id = ? AND habit_id = ? AND mark_date >= ?
                    ''', (user_id, habit_id, period_start_str))
            current_period_count = cur.fetchone()[0] or 0
            # Считаем количество выполнений в заданный период. Если current_period_count = None, то возвращаем 0

            if current_period_count >= set_frequency_count:
                print(f"Привычка {habit_name} уже выполнена необходимое количество раз ({set_frequency_count}) "
                    f"за период '{set_frequency_name}' с {period_start_str} по {mark_date}.")
                return

            new_count = current_period_count + count
            if new_count > set_frequency_count:
                print(
                    f"Вы не можете отметить привычку {habit_name} более {set_frequency_count} раз за период. Текущее количество: {current_period_count}.")
                return

            # Выполнение запроса на получение последней даты выполнения привычки
            cur.execute('''
                SELECT MAX(mark_date)
                FROM user_habit_history
                WHERE user_id = ? AND habit_id = ?
            ''', (user_id, habit_id))
            completion = cur.fetchone()
            last_completion_date = completion[0]
            last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d')
            last_completion_date_print = result[0] if result[0] is not None else "Привычка {habit_name} еще не была выполнена."
            print(f"Последняя дата выполнения привычки {habit_name}: {last_completion_date}")# выводим для проверки в консоли

            if (set_frequency_name == 'еженедельно' or set_frequency_name == 'ежемесячно') and (mark_date != last_completion_date):
                cur.execute( '''
                            INSERT INTO user_habit_history (user_id, habit_id, mark_date, mark_count)
                            VALUES (?, ?, ?, ?)
                        ''', (user_id, habit_id, mark_date, count))
                print(f"Ваша привычка {habit_name} была выполнена {current_period_count+count} раз за период '{set_frequency_name}' с {period_start_str} по {mark_date}.")
                if current_period_count + count >= set_frequency_count:
                    print (f"Вы достигли цели по выполнению привычки {habit_name} за период. Поздравляем!")


            else:
                #то есть в случаях, когда set_frequency_name == 'ежедневно'
                # или ((set_frequency_name == 'еженедельно' or set_frequency_name == 'ежемесячно')
                # and (mark_date == last_completion_date))):
                cur.execute('''
                                     UPDATE user_habit_history
                                     SET mark_count = ?
                                     WHERE id = ?
                                 ''', (new_count, user_habit_history_id))
                print(
                    f"Ваша привычка {habit_name} была выполнена {current_period_count + count} раз за период '{set_frequency_name}' с {period_start_str} по {mark_date}.")
                if new_count >= set_frequency_count:
                    print (f"Вы достигли цели по выполнению привычки {habit_name} за период. Поздравляем!")
        else:
            # Если записи нет, создаем новую с mark_count = count, по умолчанию 1
            cur.execute('''
                INSERT INTO user_habit_history (user_id, habit_id, mark_date, mark_count)
                VALUES (?, ?, ?, ?)
            ''', (user_id, habit_id, mark_date, count))
            print(
                f"Ваша привычка {habit_name} была выполнена {count} раз за период '{set_frequency_name}'.")
            if count >= set_frequency_count:
                print(f"Вы достигли цели по выполнению привычки {habit_name} за период. Поздравляем!")
        conn.commit()
    finally:
        conn.close()


#функция для получения habit.id по названию привычки
def habit_id(habit_name):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    cur.execute("SELECT id FROM habit WHERE name = ? ",
                (habit_name,))
    result = cur.fetchone()
    print(f"Это результат работы функции habit_id: {result} и result[0] = {result[0]}")
    conn.commit()
    conn.close()
    return result[0]


#Тестовое выполнение функций
#init_user(1111111111)
#init_user(2222222222)
#init_user(3333333333)
#init_habit('Пить воду', 'Пить воду 2 раза в неделю важно для поддержания водного баланса')
#init_habit('Пробежка', 'Пробежка 2 раза в неделю важна для поддержания работы сердца')
#assign_habit(1111111111, habit_id('Пробежка'), 'ежедневно', 3)
#assign_habit(1111111111, habit_id('Пить воду'), 'ежедневно', 5)
#assign_habit(2222222222, habit_id('Пробежка'), 'ежедневно', 2)
#assign_habit(2222222222, habit_id('Пить воду'), 'ежедневно', 2)
#edit_habit(1111111111,habit_id('Пить воду') , 'ежедневно', 3)
#delete_habit(1111111111, habit_id('Пить воду'))
#mark_habit(1111111111, habit_id('Пробежка'), '2022-12-12', 1)
#edit_habit(1111111111,habit_id('Пробежка') , 'ежедневно', 8)
#mark_habit(1111111111, habit_id('Пробежка'), '2022-12-12', 1)
#list_habits(2222222222)
#mark_habit(1111111111, habit_id('Пить воду'), '2022-12-12', 5)
#habit_status(1111111111)
#habit_status(2222222222)



