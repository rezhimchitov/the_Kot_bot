import telebot
import configparser
import requests
import random
import threading
import datetime
import time

def resfreshPics():
    return requests.get(f'https://pixabay.com/api/?key={pixabay}&q={tags}&image_type=photo&pretty=true&per_page={amount}').json()

config = configparser.ConfigParser()
config.read('token.ini')
kotoken = config.get('token', 'kot_token')
pixabay = config.get('token', 'pixabay_token')
amount = 200
tags = 'cute+cat'

pic_json = resfreshPics()

bot = telebot.TeleBot(kotoken)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Бля, держи кота')
    bot.send_photo(message.from_user.id,pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
    print(f'Sent message to {message.chat.id}: {message.text}')

def get_photo(bot, pic_json):
    IDs = [247725614, 836465463]
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if hour == 8 and minute >= 55 or hour == 9 and minute <= 5:
        for item in IDs:
            bot.send_message(item, 'Вставай, сонный котенок!')
            bot.send_photo(item, pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
    elif hour == 23 and minute >= 55 or hour == 23 and minute <= 5:
         for item in IDs:
            bot.send_message(item, 'Сладких снов, китя)')
            bot.send_photo(item, pic_json.get('hits')[random.randint(0, 199)]['largeImageURL'] )
    else: return(0)
    tt = threading.Timer(6000.0, get_photo, args=[bot, pic_json])
    tt.start()

t = threading.Timer(6000.0, get_photo, args=[bot, pic_json])
t.start()  

get_photo(bot, pic_json)              

bot.polling(none_stop=True)