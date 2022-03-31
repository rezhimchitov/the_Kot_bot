import logging
import requests
import configparser
import sys
import datetime
import json
import random
from PIL import Image

class PicsService:
    def create_logger(self):
        self.logger = logging.getLogger("pics_service")
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler("pics_service.log")
        self.logger.addHandler(self.fh)

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read('token.ini')
            self.kotoken = config.get('token', 'kot_token')
            self.pixabay = config.get('token', 'pixabay_token')
            self.admin_id = config.get('token', 'admin_id')
        except Exception as ex:
            self.logger.error(str(ex))
            sys.exit()

        self.amount = 200
        self.tags = 'cute+cat'
        self.pic_send = 0

    def load_base(self):
        try:
            with open('IDs_json.json') as f:
                content = f.read()
                self.IDs = json.loads(content)
                self.logger.info('Base exists, loaded')
        except Exception as ex:
            self.IDs = [836465463, 247725614]
            self.logger.error(str(ex))
            self.logger.error('File not found, rollbacked to defaults')

    def refresh_pics(self):
        try:
            self.pic_json = requests.get(f'https://pixabay.com/api/?key={self.pixabay}&q={self.tags}&image_type=photo&pretty=true&per_page={self.amount}').json()
        except Exception as ex:
            self.logger.error(str(ex))
            self.logger.error('Unable to refresh pics!')

    def __init__(self):
        logging.info('Creating service entity...')
        logging.info('Creating service logger...')
        self.create_logger()
        logging.info('Reading service config...')
        self.read_config()
        logging.info('Loading user base...')
        self.load_base()
        logging.info('Refreshing JSON...')
        self.refresh_pics()

    def sheduled_check(self):
        now = datetime.datetime.now()
        if now.hour < 10:
            return 'Вставай, сонный котенок!', self.pic_json.get('hits')[random.randint(0, 199)]['largeImageURL']
        else: return 'Сладких снов, китя', self.pic_json.get('hits')[random.randint(0, 199)]['largeImageURL']

    def get_random_photo(self):
        try:
            return self.pic_json.get('hits')[random.randint(0, 199)]['largeImageURL']
        except Exception as ex:
            self.logger.error(str(ex))
            self.logger.error('Unable to get photo!')