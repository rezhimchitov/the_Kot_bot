
import telebot
import configparser
import requests
import random

config = configparser.ConfigParser()
config.read('token.ini')
kotoken = config.get('token', 'kot_token')
pixabay = config.get('token', 'pixabay_token')
amount = 200
tags = 'cute+cat'

##############################################
r = requests.get(f'https://pixabay.com/api/?key={pixabay}&q={tags}&image_type=photo&pretty=true&per_page={amount}')
j = r.json()
##############################################

bot = telebot.TeleBot(kotoken)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Бля, держи котика')
    bot.send_photo(message.from_user.id,j.get('hits')[random.randint(0, 199)]['largeImageURL'] )
    print(f'Sent message to {message.chat.id}: {message.text}')
    
bot.polling(none_stop=True)  