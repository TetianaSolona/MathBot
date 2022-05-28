import os

import telebot
from dotenv import load_dotenv
from telebot import types

from states import Main

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))

kids: dict = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    my_bot = Main(bot, message.chat.id)
    my_bot.display()
    kids[message.chat.id] = Main

@bot.message_handler(commands=['help'])
def help_command(message):
   keyboard = [[types.InlineKeyboardButton('Написати робробнику', url='telegram.me/TaniaSolona')]]
   markup = types.InlineKeyboardMarkup(keyboard)
   bot.send_message(message.chat.id, '<b>Виникли проблеми...</b>', reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda message: True)
def process_call_back(message):
    current_state = kids[message.from_user.id]
    new_state = current_state(bot, message.from_user.id)
    new_class_state = new_state.call_back(message)
    new_example = new_class_state(bot, message.from_user.id)
    new_example.process_answer_message()
    kids[message.from_user.id] = new_class_state


@bot.callback_query_handler(func=lambda message: True)
def process_answer_back(message):
    current_state = kids[message.from_user.id]
    new_state = current_state(bot, message.from_user.id)
    new_class_state = new_state.process_answer_message()
    new_example = new_class_state(bot, message.from_user.id)
    new_example.call_back(message)
    kids[message.from_user.id] = new_class_state


if __name__ == '__main__':
    bot.infinity_polling()
