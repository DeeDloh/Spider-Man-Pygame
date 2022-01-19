class Player:
    def __init__(self, cards_l, nickname):
        self.cards_list = cards_l
        self.nickname = nickname

    def del_card(self, id):
        del self.cards_list[self.cards_list.index(id)]
