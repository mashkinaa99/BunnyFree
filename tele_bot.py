import telebot
from data_for_bot import DataForBot
from parser import SearchNames
import os
from flask import Flask, request
import logging

token = os.getenv("token")
bot = telebot.TeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

server = Flask(__name__)


@server.route("/" + token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     text='Привет! Напиши название косметической или парфюмерной компании и проверь, тестирует ли она свою продукцию на животных.')


@bot.message_handler(commands=['upd'])
def upd_base(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.chat.id == 652981201:
        SearchNames().start()
        bot.send_message(message.chat.id, text='База данных обновлена')
    else:
        bot.send_message(message.chat.id,
                         text='У вас нет доступа к этой команде бота, но, не переживайте, базы данных обновляются каждые 3 месяца.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    data = DataForBot(message.text).correct_name()
    bot.send_message(message.chat.id, text=f'{data}', parse_mode='HTML')
    bot.send_message(652981201,
                     text=f'Chat_id: {message.chat.id}\nFirst_name: {message.chat.first_name}\nUsername: {message.chat.username}\nText: {message.text}')

