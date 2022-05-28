import random
import sqlite3
from telebot import types


class Base:

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id


    def display(self):
        pass

    def call_back(self, message):
        pass

    def process_answer_message(self):
        pass


class Main(Base):

    @staticmethod
    def gen_main_markup():
        keyboard = [[types.InlineKeyboardButton('Задачі', callback_data='nextstate:Task')],
                    [types.InlineKeyboardButton('Таблиця множення', callback_data='nextstate:Multiplacation')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        return markup

    def display(self):
        self.bot.send_message(self.chat_id, "<b>Привіт, друже! Давай трохи позаймаємось математикою</b> 😉",
                              reply_markup=self.gen_main_markup(), parse_mode='HTML')

    def call_back(self, message):
        if message.data and message.data == 'nextstate:Task':
            return Task
        elif message.data and message.data == 'nextstate:Multiplacation':
            return Multiplacation
        return Main


class Task(Base):

    def process_answer_message(self):
        with sqlite3.connect('database.db') as db:
            curs = db.cursor()
            curs.execute('SELECT * FROM math_tasks  ORDER BY RANDOM() LIMIT 1')
            data = curs.fetchall()

            for d in data:
                question = d[0]
                answer = d[1]
            keyboard = [[types.InlineKeyboardButton(answer, callback_data='nextstate:Correct')],
                        [types.InlineKeyboardButton(answer + random.randint(3, 5), callback_data='nextstate:Wrong')],
                        [types.InlineKeyboardButton(answer - random.randint(1, 2), callback_data='nextstate:Wrong')]]
            random.shuffle(keyboard)
            for sublist in keyboard:
                random.shuffle(sublist)
            markup = types.InlineKeyboardMarkup(keyboard)
            self.bot.send_message(self.chat_id, '<b>' + question + '</b>', reply_markup=markup, parse_mode='HTML')

    def call_back(self, message):
        if message.data and message.data == 'nextstate:Correct':
            return ReplyCorrect
        elif message.data and message.data == 'nextstate:Wrong':
            return ReplyWrong
        return Main


class Multiplacation(Base):

    def process_answer_message(self):
        with sqlite3.connect('database.db') as db:
            curs = db.cursor()
            curs.execute('SELECT * FROM multiplication  ORDER BY RANDOM() LIMIT 1')
            data = curs.fetchall()

            for d in data:
                question = d[0]
                answer = d[1]
            keyboard = [[types.InlineKeyboardButton(answer, callback_data='nextstate:Correct')],
                        [types.InlineKeyboardButton(answer + random.randint(1, 5), callback_data='nextstate:Wrong')],
                        [types.InlineKeyboardButton(answer - random.randint(1, 5), callback_data='nextstate:Wrong')]]
            random.shuffle(keyboard)
            for sublist in keyboard:
                random.shuffle(sublist)
            markup = types.InlineKeyboardMarkup(keyboard)
            self.bot.send_message(self.chat_id, '<b>' + question + '</b>', reply_markup=markup, parse_mode='HTML')

    def call_back(self, message):
        if message.data and message.data == 'nextstate:Correct':

            return ReplyCorrect
        elif message.data and message.data == 'nextstate:Wrong':
            return ReplyWrong
        return Main


class ReplyCorrect(Base):

    @staticmethod
    def gen_main_markup():
        keyboard = [[types.InlineKeyboardButton('Задачі', callback_data='nextstate:Task')],
                    [types.InlineKeyboardButton('Таблиця множення', callback_data='nextstate:Multiplacation')],
                    [types.InlineKeyboardButton('На сьогодні все', callback_data='nextstate:Finish')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        return markup

    def process_answer_message(self):
        self.bot.send_message(self.chat_id, '✅ <b>Ти молодець! Продовжимо?</b>', reply_markup=self.gen_main_markup(),
                              parse_mode='HTML')


    def call_back(self, message):
        if message.data and message.data == 'nextstate:Task':
            return Task
        elif message.data and message.data == 'nextstate:Multiplacation':
            return Multiplacation
        elif message.data and message.data == 'nextstate:Finish':
            return Finish
        return Main


class ReplyWrong(Base):

    @staticmethod
    def gen_main_markup():
        keyboard = [[types.InlineKeyboardButton('Задачі', callback_data='nextstate:Task')],
                    [types.InlineKeyboardButton('Таблиця множення', callback_data='nextstate:Multiplacation')],
                    [types.InlineKeyboardButton('На сьогодні все', callback_data='nextstate:Finish')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        return markup

    def process_answer_message(self):
        self.bot.send_message(self.chat_id, '❌ <b>На жаль, ти помилився. Спробуєш інше питання?</b>',
                              reply_markup=self.gen_main_markup(), parse_mode='HTML')

    def call_back(self, message):
        if message.data and message.data == 'nextstate:Task':
            return Task
        elif message.data and message.data == 'nextstate:Multiplacation':
            return Multiplacation
        elif message.data and message.data == 'nextstate:Finish':
            return Finish
        return Main


class Finish(Base):

    def process_answer_message(self):
        self.bot.send_message(self.chat_id, '<b>До скорої зустрічі!</b>👋', parse_mode='HTML')
