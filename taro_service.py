import random
import logging
from card import GenericCard

class TaroService:
    def fill_Cards(self):
        self.cards = list()
        self.cards.append(GenericCard('Король Чаш', 'Получение мудрого совета, утешения и поддержки', 'D:\dev\Pictures\king_of_bowls.jpg'))
        self.cards.append(GenericCard('Дама чаш', 'Присутствие достаточно яркой эмоциональной реакции, переживания', 'D:\dev\Pictures\queen_of_bowls.jpg'))
        self.cards.append(GenericCard('Рыцарь чаш', 'Послание истинной любви, взаимной', 'D:\dev\Pictures\prince_of_bowls.jpg'))

    def create_logger(self):
        self.logger = logging.getLogger("taro_service")
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler("taro_service.log")
        self.logger.addHandler(self.fh)

    def __init__(self):
        self.create_logger()
        self.fill_Cards()
        self.logger.info("Successfully created taro service")

    def get_taro_cards(self):
        try:
            return(random.sample(self.cards, 3))
        except Exception as ex:
            self.logger.error(str(ex))
            self.logger.error('Unable to send cards!')
