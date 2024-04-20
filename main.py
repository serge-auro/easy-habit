import telebot


bot = telebot.TeleBot('7174356124:AAHBmXI1GinX8hQ2amvIZLapqYo36c20bKo')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Здесь будет список доступных команд.')


bot.polling(none_stop=True)