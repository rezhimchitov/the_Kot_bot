
import telebot
import configparser

config = configparser.ConfigParser()
config.read('token.ini')
kotoken = config.get('token', 'kot_token')

bot = telebot.TeleBot(kotoken)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.infinity_polling()