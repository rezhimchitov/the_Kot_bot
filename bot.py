import telebot
from telebot import types
from threading import Thread
import asyncio
import logging
import schedule
import time
from datetime import datetime, timezone
from services.pics_service import PicsService
from services.taro_service import TaroService
from services.holidays_service import HolidaysService
from services.db_service import DataBaseService

logging.basicConfig(filename="main_logger.log", level=logging.INFO)
main_service = PicsService()
taro_service = TaroService()
holidays_service = HolidaysService()
db_service = DataBaseService()
bot = telebot.TeleBot(main_service.kotoken)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        bot.send_message(message.from_user.id, f"Приветствуем в нашем кошачьем царстве!\n \nМогу прислать котика, сделать таро-расклад и рассказать, какие сегодня праздники :)\n \nПосмотри список моих команд и поехали, муррр :3")
        bot.send_photo(message.from_user.id, main_service.get_random_photo())
        user_id = message.chat.id
        user_list = []
        db_service.db_user_list(user_list)
        if user_id not in user_list:
            user_name = message.chat.username
            dt = datetime.now(timezone.utc)
            db_service.db_add_user(user_id, user_name, dt)
    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to send start message!')
        try:
            bot.send_message(message.from_user.id, 'У нас технические шоколадки(')
        except Exception as ex:
            logging.error(str(ex))

@bot.message_handler(commands=['notifications'])
def notifications_text(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        markup_nots = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_nots = types.KeyboardButton("Да, хочу!")
        btn2_nots = types.KeyboardButton("Нет, я бука(")
        markup_nots.add(btn1_nots, btn2_nots)  
        bot.send_message(message.from_user.id, "Хочешь получать от меня милые сообщения утром и перед сном?".format(message.from_user), reply_markup=markup_nots)
    except Exception as ex:
        logging.error(str(ex))
        logging.error('Unable to send notifications message!')
        try:
            bot.send_message(message.from_user.id, 'У нас технические шоколадки(')
        except Exception as ex:
            logging.error(str(ex))

@bot.message_handler(commands=['taro'])
def taro_text(message):
    logging.info(f'Got message from {message.chat.id}: {message.text}\n')
    try:
        bot.send_message(message.from_user.id, f"Еще я умею делать расклады Таро:)\n \nМогу рассказать о твоем прошлом, настоящем и будущем :3")
        bot.send_photo(message.from_user.id, main_service.get_random_photo())
        time.sleep(1)
        markup_taro = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_taro = types.KeyboardButton("Усь!")
        btn2_taro = types.KeyboardButton("Ни(")
        markup_taro.add(btn1_taro, btn2_taro)  
        bot.send_message(message.from_user.id, "Тебе сделать рассклад таро?".format(message.from_user), reply_markup=markup_taro)
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
        bot.send_message(message.from_user.id, f"А ты любишь праздники?\n \nКаждый день особенный, прямо как ты ^-^")
        bot.send_photo(message.from_user.id, main_service.get_random_photo())
        time.sleep(1)
        markup_holidays = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_holidays = types.KeyboardButton("Да, конечно!")
        btn2_holidays = types.KeyboardButton("Неа...")
        markup_holidays.add(btn1_holidays, btn2_holidays) 
        bot.send_message(message.from_user.id, "Хочешь узнать, какие сегодня праздники?".format(message.from_user), reply_markup=markup_holidays)
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
    remove = telebot.types.ReplyKeyboardRemove()
    telegram_id = message.chat.id
    try:
        if(message.text == "Да, хочу!"):
            bot.send_message(message.chat.id, text="Я буду стараться ради тебя :)", reply_markup=remove)
            cat_sub = True
            db_service.db_sub_notifications(telegram_id, cat_sub)
            logging.info(f'User subscibed: {message.chat.id}\n')
            bot.send_photo(message.from_user.id, main_service.get_random_photo()) 
        elif(message.text == "Нет, я бука("):
            bot.send_message(message.chat.id, text="Ну ладно...(", reply_markup=remove)
            cat_sub = False
            db_service.db_sub_notifications(telegram_id, cat_sub)
            logging.info(f'User left: {message.chat.id}\n')
        elif(message.text == "Усь!"):
            bot.send_message(message.from_user.id, 'Генерирую тебе расклад!', reply_markup=remove)
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
        elif(message.text == "Ни("):
            bot.send_message(message.chat.id, text="Ну ладно...(", reply_markup=remove)
        elif(message.text == "Да, конечно!"):
            list_of_holidays = holidays_service.send_holidays()
            for holiday_message in list_of_holidays:
                bot.send_message(message.from_user.id, holiday_message)
            bot.send_photo(message.from_user.id, main_service.get_random_photo())
            time.sleep(3)
            markup_holidays_sub = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1_holidays_sub = types.KeyboardButton("Давай!")
            btn2_holidays_sub = types.KeyboardButton("Нит(")
            markup_holidays_sub.add(btn1_holidays_sub, btn2_holidays_sub) 
            bot.send_message(message.from_user.id, "А можешь ты хочешь получать утреннюю сводку праздников от меня?".format(message.from_user), reply_markup=markup_holidays_sub)
        elif(message.text == "Неа..."):
            bot.send_message(message.chat.id, text="Ну ладно...(", reply_markup=remove)
            time.sleep(2)
            markup_holidays_sub = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1_holidays_sub = types.KeyboardButton("Давай!")
            btn2_holidays_sub = types.KeyboardButton("Ни(")
            markup_holidays_sub.add(btn1_holidays_sub, btn2_holidays_sub) 
            bot.send_message(message.from_user.id, "А можешь ты хочешь получать утреннюю сводку праздников от меня?".format(message.from_user), reply_markup=markup_holidays_sub)
        elif(message.text == "Давай!"):
            markup_holidays_amount = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1_holidays_amount = types.KeyboardButton("5")
            btn2_holidays_amount = types.KeyboardButton("10")
            btn3_holidays_amount = types.KeyboardButton("25")
            btn4_holidays_amount = types.KeyboardButton("Все!")
            markup_holidays_amount.add(btn1_holidays_amount, btn2_holidays_amount, btn3_holidays_amount, btn4_holidays_amount)
            bot.send_message(message.from_user.id, "Сколько хочешь получать праздников?".format(message.from_user), reply_markup=markup_holidays_amount)
            holidays_sub = True
            db_service.db_sub_holidays(telegram_id, holidays_sub)
        elif(message.text == "Нит("):
            bot.send_message(message.chat.id, text="Ну ладно...(", reply_markup=remove)
            holidays_sub = False
            db_service.db_sub_holidays(telegram_id, holidays_sub)
        elif(message.text == "5"): #Начиная отсюда можно умнее, но проблема что кнопки... типа holidays_amount = message.from_user.id
            bot.send_message(message.chat.id, text="Я буду стараться ради тебя :)", reply_markup=remove)
            holidays_amount = 5
            db_service.db_amount_holidays(telegram_id, holidays_amount)
        elif(message.text == "10"):
            bot.send_message(message.chat.id, text="Я буду стараться ради тебя :)", reply_markup=remove)
            holidays_amount = 10
            db_service.db_amount_holidays(telegram_id, holidays_amount)
        elif(message.text == "25"):
            bot.send_message(message.chat.id, text="Я буду стараться ради тебя :)", reply_markup=remove)
            holidays_amount = 25
            db_service.db_amount_holidays(telegram_id, holidays_amount)
        elif(message.text == "Все!"):
            bot.send_message(message.chat.id, text="Я буду стараться ради тебя :)", reply_markup=remove)
            holidays_amount = 100
            db_service.db_amount_holidays(telegram_id, holidays_amount)
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
