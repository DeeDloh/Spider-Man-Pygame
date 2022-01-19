import pygame

from buttons import SpiderButtonImage
from terminate import terminate
from load_image import load_image
from player import Player
from domination import domination
from troichka import troichka

PEREVOD_PR = {'Domination': lambda n, m: domination(n, m),
              'Троечка': lambda n, m: troichka(n, m)}


class Pole:
    def __init__(self, screen, players, pravila_igr, pravila_splav='Амереканская версия',
                 size_cards=(126, 190), WIDTH=1280, HEIGHT=720):
        """players -> list | [(list_id, nickname)]
        pravila_igr -> str
        pravila_splav -> str"""
        self.k = 0
        self.screen = screen
        self.players = [Player(*i) for i in players]
        self.st_card = pygame.transform.scale(load_image('./data/kartinki cards/0.jpg'), size_cards)
        self.size_cards = size_cards
        self.pravila_igr = pravila_igr
        self.layout_concepts = [self.creat_layout_concept(i) for i in range(1, 7)]
        self.now_player = self.players[0]
        kol_kart = len(self.now_player.cards_list)
        self.now_button = self.layout_concepts[kol_kart - 1]
        self.move_plug_but = pygame.USEREVENT + 1
        pygame.time.set_timer(self.move_plug_but, 1)
        self.prod = False
        self.button_image = False
        #False - now players chooses card, True - players chose card and stand plug
        self.image_0 = load_image('./data/kartinki cards/0.jpg',
                                                scale=self.size_cards)
        self.coords_card_table = [[(577, 310)], [(511, 310), (643, 310)],
                                  [(445, 310), (577, 310), (709, 310)],
                                  [(379, 310), (511, 310), (643, 310), (775, 310)]]
        self.card_table = []
        for i in range(kol_kart):
            self.now_button[i].change_image(
                f'./data/kartinki cards/{self.now_player.cards_list[i]}.jpg', self.size_cards)
            self.now_button[i].show()

    def creat_layout_concept(self, n):
        buttons = []
        if n % 2 == 1:
            for i in range(n):
                button = SpiderButtonImage(self.screen, (577 - (132 * (n // 2)) + 132 * i, 525),
                                           './data/kartinki cards/0.jpg', self.size_cards)
                button.hide()
                buttons.append(button)
        else:
            for i in range(n):
                button = SpiderButtonImage(self.screen, (511 + i * 132 - (132 * (n // 2 - 1)), 525),
                                           './data/kartinki cards/0.jpg', self.size_cards)
                button.hide()
                buttons.append(button)
        return buttons

    def change_players(self, id):
        for i in self.now_button:
            i.hide()
        self.card_table.append(id)
        self.now_player.del_card(id)
        # сделать функци при вызове, которой делатся
        # заглушки с картами текущего игрока и анимация переворота карт
        # после переворота карт

    def update(self, events):
        for event in events:
            for i in self.now_button:
                if i.handleEvent(event):
                    self.change_players(int(i.name_image().split('.')[0]))
                    self.button_image = True
                    k = len(self.now_player.cards_list)
                    if k > 0:
                        self.coords_plug_but = []
                        for i in self.layout_concepts[k - 1]:
                            self.coords_plug_but.append([*i.getLoc(), (577 - i.getLoc()[0])])


            if event.type == self.move_plug_but and self.button_image:
                for cr in range(len(self.coords_plug_but)):
                    print(self.coords_plug_but[cr][0])
                    self.screen.blit(self.image_0, (int(self.coords_plug_but[cr][0]),
                                                                         self.coords_plug_but[cr][1]))
                    self.coords_plug_but[cr][0] += self.coords_plug_but[cr][2] / 1000
                if all(round(x[0]) == round(self.coords_plug_but[0][0]) for x in self.coords_plug_but):
                    self.button_image = False

        for i in self.now_button:
            i.draw()
        if len(self.card_table) != 0:
            coord_now = self.coords_card_table[len(self.card_table) - 1]
            for i in range(len(coord_now)):
                self.screen.blit(load_image(f'./data/kartinki cards/{self.card_table[i]}.jpg',
                                            scale=self.size_cards), coord_now[i])

        plug_players = []
        if len(self.players) == 2:
            plug_players = [(self.st_card, (577, 5))]
        elif len(self.players) == 3:
            plug_players = [(self.st_card, (100, 80)), (self.st_card, (1054, 80))]
        elif len(self.players) == 4:
            plug_players = [(self.st_card, (12, 265)), (self.st_card, (577, 5)), (self.st_card, (1142, 265))]
        for cr in plug_players:
            screen.blit(*cr)




'''
def screen_pole(screen, players, pravila_igr, pravila_splav='Амереканская версия',  WIDTH=1280, HEIGHT=720):
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    buttons = set_place_cards(screen, players[0])
    plug_players = []
    card = pygame.transform.scale(load_image('./data/kartinki cards/0.jpg'), size_cards)
    if len(players) == 2:
        plug_players.append((card, (577, 5)))
    elif len(players) == 3:
        plug_players.extend([(card, (100, 80)), (card, (1054, 80))])
    elif len(players) == 4:
        plug_players.extend([(card, (12, 265)), (card, (577, 5)), (card, (1149, 265))])
    zagl = pygame.transform.scale(load_image('./data/kartinki cards/0.jpg'), size_cards)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        pygame.draw.rect(screen, (0, 128, 0), (0, 0, WIDTH, HEIGHT),)

        for cr in plug_players:
            screen.blit(*cr)
        screen.blit(zagl, (577, 310))
        pygame.draw.ellipse(screen, (0, 0, 0), (150, 200, 980, 320), width=5)
        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(FPS)


def set_place_cards(screen, player):
    buttons = []
    if len(player.cards_list) % 2 == 1:
        for i in range(len(player.cards_list)):
            button = Button(screen, 577 - (132 * (len(player.cards_list) // 2)) + 132 * i, 525, *size_cards,
                            image=pygame.transform.scale(
                                load_image(f'./data/kartinki cards/{player.cards_list[i]}.jpg'),
                                size_cards))
            buttons.append(button)
    else:
        for i in range(len(player.cards_list)):
            button = Button(screen, 511 + i * 132 - (132 * (len(player.cards_list) // 2 - 1)), 525, *size_cards,
                            image=pygame.transform.scale(
                                load_image(f'./data/kartinki cards/{player.cards_list[i]}.jpg'),
                                size_cards))
            buttons.append(button)
    return buttons
'''


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    players = [([45, 53, 47, 53, 53, 53], 'DeeDloh'), ([78, 2, 6], 'ладно'), ([95, 36, 59], '123'), ([34, 39, 29], '456')]
    pole = Pole(screen, players, 'Domination')
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        pygame.draw.rect(screen, (0, 128, 0), (0, 0, 1280, 720))
        pygame.draw.ellipse(screen, (0, 0, 0), (150, 200, 980, 320), width=5)
        pole.update(events)
        pygame.display.flip()
        clock.tick(FPS)
