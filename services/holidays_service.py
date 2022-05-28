from datetime import datetime
import requests
import logging
from bs4 import BeautifulSoup

class HolidaysService:
    def create_logger(self):
        self.logger = logging.getLogger("holidays_service")
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler("holidays_service.log")
        self.logger.addHandler(self.fh)

    def __init__(self):
        self.month_base = ['yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avgust', 'sentyabr', 'oktyabr', 'noyabr', 'dekabr']
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.create_logger()
        self.logger.info("Successfully created holidays service")

    def send_holidays(self):
        current_datetime = datetime.now()
        self.day = current_datetime.day
        self.month_number = current_datetime.month
        
        self.month = self.month_base[self.month_number - 1]

        holidays_link = f'http://kakoysegodnyaprazdnik.ru/baza/{self.month}/{self.day}'
        self.response = requests.get(holidays_link, headers=self.headers)

        soup = BeautifulSoup(self.response.content, 'lxml')
        holidays = soup.find_all('span', itemprop="text")
        try:
            return(holidays)
        except Exception as ex:
            self.logger.error(str(ex))
            self.logger.error('Unable to send holidays!')
