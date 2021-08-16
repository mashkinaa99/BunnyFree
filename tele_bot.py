import telebot
from data_for_bot import DataForBot
import os

token = os.getenv("token")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     text='Привет! Напиши название косметической или парфюмерной компании и проверь, тестирует ли она свою продукцию на животных.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    data = DataForBot(message.text).correct_name()
    bot.send_message(message.chat.id, text=f'{data}', parse_mode='HTML')


bot.polling()
