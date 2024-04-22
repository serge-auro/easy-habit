import telebot
from telebot import types
from config import BOT_TOKEN
from actions import * # импортируем функции из actions.py

bot = telebot.TeleBot(BOT_TOKEN)


# Словарь кнопок
buttons_dict = {
    'menu': 'На главную',
    'status': 'Статус',
    'report': 'Отчеты',
    'edit_habit': 'Редактировать',
    'new_habit': 'Добавить',
    'del_habit': 'Удалить',
    'mark_habit': 'Отметить V',
    'habits': 'Привычки'
}


# Функция для создания inline клавиатуры
def create_inline_keyboard(button_keys):
  keyboard = types.InlineKeyboardMarkup(row_width=2)  # Устанавливаем ширину ряда равной 2
  buttons = []
  for key in button_keys:
      if key in buttons_dict:
          button_text = buttons_dict[key]
          callback_data = key  # используем ключ словаря как callback_data
          buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
  # Добавляем кнопки по две в ряд
  keyboard.add(*buttons)  # Распаковываем список кнопок
  return keyboard


# Обработчики inline-кнопок
@bot.callback_query_handler(func=lambda call: call.data == 'status')
def handle_status(call):
    # TODO: Добавьте здесь функционал для статуса
    keyboard = create_inline_keyboard(['new_habit', 'del_habit', 'menu'])
    bot.send_message(call.message.chat.id, 'Ваш текущий статус привычек', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'report')
def handle_report(call):
    # TODO: Добавьте здесь функционал для отчетов
    keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
    bot.send_message(call.message.chat.id, 'Отчет', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'edit_habit')
def handle_edit_habit(call):
    # TODO: Добавьте здесь функционал для редактирования привычки
    keyboard = create_inline_keyboard(['new_habit', 'del_habit', 'menu'])
    bot.send_message(call.message.chat.id, 'Редактировать', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'new_habit')
def handle_new_habit(call):
    # TODO: Добавьте здесь функционал для добавления новой привычки
    keyboard = create_inline_keyboard(['edit_habit', 'del_habit', 'menu'])
    bot.send_message(call.message.chat.id, 'Добавить', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'del_habit')
def handle_del_habit(call):
    # TODO: Добавьте здесь функционал для удаления привычки
    keyboard = create_inline_keyboard(['edit_habit', 'menu'])
    bot.send_message(call.message.chat.id, 'Удалить', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'mark_habit')
def handle_mark_habit(call):
    # TODO: Добавьте здесь функционал для отметки привычки
    keyboard = create_inline_keyboard(['status', 'edit_habit', 'menu'])
    bot.send_message(call.message.chat.id, 'Отметить V', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'habits')
def handle_habits(call):
    # TODO: Добавьте здесь функционал для просмотра всех привычек
    keyboard = create_inline_keyboard(['new_habit', 'edit_habit', 'del_habit', 'menu'])
    bot.send_message(call.message.chat.id, 'Привычки', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_menu(call):
    # кнопка для возврата в главное меню
    keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
    bot.send_message(call.message.chat.id, 'На главную', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = create_inline_keyboard(['status', 'edit_habit', 'mark_habit'])
    bot.send_message(message.chat.id, 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def handle_help(message):
    keyboard = create_inline_keyboard(['status', 'habits', 'mark_habit'])
    bot.send_message(message.chat.id, 'Здесь будет список доступных команд и описание их функций.', reply_markup=keyboard)

bot.polling(none_stop=True)
