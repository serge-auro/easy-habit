import telebot

from config import BOT_TOKEN
from action import * # импортируем функции из actions.py


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я помощник, который поможет вам отслеживать и поддерживать свои ежедневные привычки.')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Здесь будет список доступных команд.')


bot.polling(none_stop=True)