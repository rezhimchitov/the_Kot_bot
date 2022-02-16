import telebot
import configparser
import requests
import random
import threading
import datetime
import json
import sys

def resfreshPics():
    return requests.get(f'https://pixabay.com/api/?key={pixabay}&q={tags}&image_type=photo&pretty=true&per_page={amount}').json()

config = configparser.ConfigParser()
config.read('token.ini')
kotoken = config.get('token', 'kot_token')
pixabay = config.get('token', 'pixabay_token')
amount = 200
tags = 'cute+cat'
pic_send = 0
IDs = []

pic_json = resfreshPics()

bot = telebot.TeleBot(kotoken)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, f"Приветствуем в нашем кошачьем царстве!\n \nМогу прислать котика, а если напишешь мне 'подписка', то пополнишь нашу кошачью армию!\n \n'Отписка' сделает тебя дезертиром(\n \nТак что решайся, муррр :3")
    bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
    sys.stdout.write(str(f'Got message from {message.chat.id}: {message.text}') + '\n')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    sys.stdout.write(str(f'Got message from {message.chat.id}: {message.text}') + '\n')
    match str.lower(message.text):
        case "подписка":
            if message.chat.id not in IDs:
                IDs.append(message.chat.id)
                sys.stdout.write(str(f'User subscibed: {message.chat.id}') + '\n')
                bot.send_message(message.from_user.id, 'Теперь ты котик!')
                bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
            else:
                bot.send_message(message.from_user.id, 'Ты подписан, дурачок')
                bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
        case "отписка":
            if message.chat.id in IDs:
                IDs.remove(message.chat.id)
                sys.stdout.write(str(f'User left: {message.chat.id}') + '\n')
                bot.send_message(message.from_user.id, 'Прощай(')
                bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
            else:
                bot.send_message(message.from_user.id, 'Ты не подписан, дурачок')
                bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
        case _:
            bot.send_message(message.from_user.id, 'Бля, держи кота')
            bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
    
def get_photo(bot, pic_json):
    global pic_send
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if hour == 8 and minute >= 55 or hour == 9 and minute <= 5:
        if pic_send == 0:
            for item in IDs:
                bot.send_message(item, 'Вставай, сонный котенок!')
                bot.send_photo(item, pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
            pic_send = 1
    elif hour == 22 and minute >= 55 or hour == 23 and minute <= 5:
        if pic_send == 0:
            for item in IDs:
                bot.send_message(item, 'Сладких снов, китя)')
                bot.send_photo(item, pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
            pic_send = 1
    else: pic_send = 0
    tt = threading.Timer(300.0, get_photo, args=[bot, pic_json])
    tt.start()


get_photo(bot, pic_json)              

bot.polling(none_stop=True)