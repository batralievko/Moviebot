import telebot
from telebot.types import ReplyKeyboardMarkup

import config
import random
import parsing
from bs4 import BeautifulSoup
import dbworker
import re
import requests
import pandas as pd
from tabulate import tabulate
from random import randint

# our bot:
bot = telebot.TeleBot(config.token)

# здесь будет функция - результат парсинга

# будем срашивать жанр (в таблице будет связка
# настроение человека - жанры фильмов, под данное настроение)
# будем спрашивать год (связка вопроса "Хотите понастольгировать? и год фильма)
# переменные, которые использует бот

genre, year = None, None

pict = "https://www.tebya.net/wp-content/uploads/2020/01/Кадр-Однажды...-Тарантино-2019-Русский-трейлер-00-00-41.jpg"
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Yes!', 'No,thanks!')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Nostalgia', 'Something new')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Comedy', 'Drama', 'Thriller')
keyboard4 = telebot.types.ReplyKeyboardMarkup(True)
keyboard4.row('Hi!')
keyboard5 = telebot.types.ReplyKeyboardMarkup(True)
keyboard5.row('Okay!')


# приветствие
@bot.message_handler(commands=['start'])
def cmd_start(message):
    # add code for fix current status before code down
    bot.send_message(message.chat.id, 'Hi, I am moviebot!')
    bot.send_message(message.chat.id, 'I can help you choose a movie')
    bot.send_message(message.chat.id, 'Want some help?', reply_markup=keyboard1)
    bot.send_photo(message.chat.id, pict)
    # add code for fix current status and after code above


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Yes!":
        bot.send_message(message.from_user.id, 'Cool!')
        bot.send_message(message.from_user.id, 'I want to know what you want first...', reply_markup=keyboard5)
        bot.send_message(message.chat.id, 'Do you want nostalgia or something new?', reply_markup=keyboard2)
    elif message.text == "Nostalgia":
        # year = random.randint(2000, 2018)
        bot.send_message(message.from_user.id, 'Okay')
        bot.send_message(message.from_user.id, text='What about the genre?', reply_markup=keyboard)
    elif message.text == 'No,thanks!':
        bot.send_message(message.from_user.id, 'So, yeah, I wll be in here if you need something.')
    elif message.text == 'Something new':
        # year = random.randint(2019, 2020)
        bot.send_sticker(message.from_user.id, 'Okay')
        bot.send_message(message.from_user.id, text='What about the genre?', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Im not smart enough to understand you yet')


# todo сделать все таки кнопки, потому непрерывно как выше не работает
# todo вот ссылка: https://thecode.media/python-bot/


# Готовим кнопки
keyboard = telebot.types.InlineKeyboardMarkup()

# По очереди готовим текст и обработчик для каждого жанра

key_comedy = telebot.types.InlineKeyboardButton(text='Comedy', callback_data='Comedy')

# И добавляем кнопку на экран

keyboard.add(key_comedy)

key_drama = telebot.types.InlineKeyboardButton(text='Drama', callback_data='Drama')

keyboard.add(key_drama)

key_thriller = telebot.types.InlineKeyboardButton(text='Thriller', callback_data='Thriller')

keyboard.add(key_thriller)

key_action = telebot.types.InlineKeyboardButton(text='Action', callback_data='Action')

keyboard.add(key_action)

key_adventure = telebot.types.InlineKeyboardButton(text='Adventure', callback_data='Adventure')

keyboard.add(key_adventure)

key_horror = telebot.types.InlineKeyboardButton(text='Horror', callback_data='Horror')

keyboard.add(key_horror)

#
# @bot.message_handler(content_types=['text'])
# def get_text_messages_2(message):
#     bot.send_message(message.from_user.id, text='What about the genre?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 6 кнопок — выводим фильм
    data_table = parsing.refs(year, call.data)
    bot.send_message(call.message.chat.id, 'Hm, just let me think for a minute')
    bot.send_message(call.message.chat.id, data_table.Name[0] + ', ' + data_table.Date_release[0])
    bot.send_message(call.message.chat.id, 'Run time: ' + data_table.Run_time[0])
    bot.send_message(call.message.chat.id, 'IMDb Rating: ' + data_table.Imdb_rating[0])
    bot.send_photo(call.message.chat.id, data_table.Ref_for_image[0])



# Показываем все кнопки сразу и пишем сообщение о выборе

# def get_year(message):
#     if message.text.lower.strip() == "yes!":

#
# # @bot.message_handler(commands=['start'])
# def cmd_questions(message):
#     if keyboard1 == 'Yes!':
#         # add code for fix current status before code down
#         bot.send_message(message.chat.id, 'I want to know what you want first...')
#         bot.send_message(message.chat.id, 'Do you want nostalgia or something new?', reply_markup=keyboard2)
#         # todo добавить ответ в виде стикера вместо "Okey"
#         bot.send_message(message.chat.id, 'Okay')
#         bot.send_message(message.chat.id, 'What about the genre?', reply_markup=keyboard3)
#         bot.send_photo(message.chat.id, pict)
#         # add code for fix current status and after code above
#     else:
#         bot.send_message(message.chat.id, 'So, yeah, I wll be in here if you need something.')


# @bot.message_handler(content_types=['text'])
# def cmd_start(message):
#     # add code for fix current status before code down
#
#     # add code for fix current status and after code above


if __name__ == "__main__":
    bot.infinity_polling()
