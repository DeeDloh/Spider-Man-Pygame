class Player:
    def __init__(self, cards_l, nickname):
        self.cards_list = cards_l
        self.nickname = nickname
        self.but_cards = []

    def add_button(self, button):
        self.but_cards.append(button)
