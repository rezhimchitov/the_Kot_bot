import telebot
from threading import Thread
import asyncio
import json
import sys
import logging
import schedule
import time
from pics_service import PicsService
from taro_service import TaroService
from holidays_service import HolidaysService

logging.basicConfig(filename="main_logger.log", level=logging.INFO)
main_service = PicsService()
taro_service = TaroService()
holidays_service = HolidaysService()
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

@bot.message_handler(commands=['taro'])
def taro_text(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        bot.send_message(message.from_user.id, f"Еще я умею делать расклады Таро:)\n \nМогу рассказать о твоем прошлом, настоящем и будущем!\n \nЕсли ты согласен - пиши 'расклад' :3")
        bot.send_photo(message.from_user.id, main_service.get_random_photo())
    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to send taro message!')
        try:
            bot.send_message(message.from_user.id, 'У нас технические шоколадки(')
        except Exception as ex:
            logging.error(str(ex))

@bot.message_handler(commands=['holidays'])
def taro_text(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        bot.send_message(message.from_user.id, f"А ты любишь праздники?\n \nКаждый день особенный, прямо как ты ^-^ \n \nЕсли хочешь узнать, какие сегодня праздники - пиши 'праздники' :3")
        bot.send_photo(message.from_user.id, main_service.get_random_photo())
    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to send holidays message!')
        try:
            bot.send_message(message.from_user.id, 'У нас технические шоколадки(')
        except Exception as ex:
            logging.error(str(ex))
    
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
        elif lowered_text == "расклад":
            bot.send_message(message.from_user.id, 'Генерирую тебе расклад!')
            time.sleep(3)
            list_of_phrases = ['Твое прошлое :3', 'Твое настоящее, муррр', 'Твое будущее, котя']
            list_of_cards = taro_service.get_taro_cards()
            for i in range(len(list_of_phrases)):
                bot.send_message(message.from_user.id, list_of_phrases[i])
                time.sleep(1)
                taro_name = list_of_cards[i].name
                taro_pic = list_of_cards[i].picture
                taro_text = list_of_cards[i].description
                bot.send_message(message.from_user.id, taro_name)
                bot.send_photo(message.from_user.id, open(taro_pic, 'rb'))
                bot.send_message(message.from_user.id, taro_text)
                time.sleep(2)
        elif lowered_text == "праздники":
            list_of_holidays = holidays_service.send_holidays()
            for holiday_message in list_of_holidays:
                bot.send_message(message.from_user.id, holiday_message)
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