import telebot

bot = telebot.TeleBot('')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Ну типа котик')

bot.polling(none_stop=True)