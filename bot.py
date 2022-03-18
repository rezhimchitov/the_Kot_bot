import telebot
from threading import Thread
import asyncio
import json
import sys
import logging
import schedule
import time
from service import pics_service

logging.basicConfig(filename="main_logger.log", level=logging.INFO)
main_service = pics_service()
bot = telebot.TeleBot(main_service.kotoken)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        bot.send_message(message.from_user.id, f"Приветствуем в нашем кошачьем царстве!\n \nМогу прислать котика, а если напишешь мне 'подписка', то пополнишь нашу кошачью армию!\n \n'Отписка' сделает тебя дезертиром(\n \nТак что решайся, муррр :3")
        bot.send_photo(message.from_user.id, main_service.get_random_photo())
    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to send start message!')
        try:
            bot.send_message(message.from_user.id, 'У нас технические шоколадки(')
        except Exception as ex:
            logging.error(str(ex))

@bot.message_handler(commands=['refresh'])
def refresh_command(message):
    try:
        if str(message.chat.id) == main_service.admin_id:
            main_service.refresh_pics()
            bot.send_message(message.from_user.id, 'Картинки обновлены!')
        else: return()
    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to refresh pics command!')
        
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        lowered_text = str.lower(message.text)
        if lowered_text == "подписка":
            if message.chat.id not in main_service.IDs:
                main_service.IDs.append(message.chat.id)
                logging.info(f'User subscibed: {message.chat.id}\n')
                bot.send_message(message.from_user.id, 'Теперь ты котик!')
                bot.send_photo(message.from_user.id, main_service.get_random_photo())
                with open('IDs_json.json', 'w') as f:
                    f.write(json.dumps(main_service.IDs))
            else:
                bot.send_message(message.from_user.id, 'Ты подписан, дурачок')
                bot.send_photo(message.from_user.id, main_service.get_random_photo())
        elif lowered_text == "отписка":
            if message.chat.id in main_service.IDs:
                main_service.IDs.remove(message.chat.id)
                sys.stdout.write(str(f'User left: {message.chat.id}') + '\n')
                bot.send_message(message.from_user.id, 'Прощай(')
                bot.send_photo(message.from_user.id, main_service.get_random_photo())
                with open('IDs_json.json', 'w') as f:
                    f.write(json.dumps(main_service.IDs))
            else:
                bot.send_message(message.from_user.id, 'Ты не подписан, дурачок')
                bot.send_photo(message.from_user.id, main_service.get_random_photo())
        else:
            bot.send_message(message.from_user.id, 'Бля, держи кота')
            bot.send_photo(message.from_user.id, main_service.get_random_photo())

    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to send message!')
        try:
            bot.send_message(message.from_user.id, 'У нас технические шоколадки(')
        except Exception as ex:
            logging.error(str(ex))

def schedule_func():
    global main_service
    global bot
    logging.info('Scheduled work started')
    main_service.refresh_pics()
    text, photo = main_service.sheduled_check()
    for id in main_service.IDs:
        try:
            bot.send_message(id, text)
            bot.send_photo(id, photo)
        except Exception as ex:
            logging.error(str(ex))

schedule.every().day.at("09:00").do(schedule_func)
schedule.every().day.at("23:00").do(schedule_func)

def run_async():
    global bot
    asyncio.run(bot.polling())

thread = Thread(target = run_async, name = 'Bot Polling Thread')
thread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
    