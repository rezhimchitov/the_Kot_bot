class GenericCard:
    def __init__(self, card_name, card_description, card_picture):
        self.link_prefix = 'taro_pictures\\'
        self.name = card_name
        self.description = card_description
        self.picture = self.link_prefix + card_picture + '.jpg'
