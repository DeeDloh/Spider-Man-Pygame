import pygame
import random

from buttons import SpiderButtonImage
from terminate import terminate
from load_image import load_image
from player import Player
from domination import domination
from troichka import troichka
from AnimatedSprite import AnimatedSprite

PEREVOD_PR = {'Domination': lambda n, m: domination(n, m),
              'Троечка': lambda n, m: troichka(n, m)}


class Pole:
    def __init__(self, screen, players, pravila_igr, pravila_splav='Амереканская версия',
                 size_cards=(126, 190), WIDTH=1280, HEIGHT=720):
        """players -> list | [(list_id, nickname)]
        pravila_igr -> str
        pravila_splav -> str"""
        self.screen = screen
        self.players = [Player(*i) for i in players]
        self.st_card = pygame.transform.scale(load_image('./data/kartinki cards/0.jpg'), size_cards)
        self.size_cards = size_cards
        self.pravila_igr = pravila_igr
        self.layout_concepts = [self.creat_layout_concept(i) for i in range(1, 7)]
        self.now_player = self.players[0]
        kol_kart = len(self.now_player.cards_list)
        self.now_button = self.layout_concepts[kol_kart - 1]
        self.prod = False
        self.button_image = False
        self.flag_change_players = False
        # False - now players chooses card, True - players chose card and stand plug

        self.four_group = pygame.sprite.Group()
        self.three_group = pygame.sprite.Group()
        self.two_group = pygame.sprite.Group()
        self.perehod_2 = AnimatedSprite(load_image("./data/final2.png"), 9, 5, 0, 0, self.two_group)
        self.perehod_3 = AnimatedSprite(load_image("./data/final3.png"), 11, 3, 0, 0, self.three_group)
        self.perehod_4 = AnimatedSprite(load_image("./data/final.png"), 5, 5, 0, 0, self.four_group)
        self.kol_frames = 0
        self.image_0 = load_image('./data/kartinki cards/0.jpg',
                                  scale=self.size_cards)
        self.coords_card_table = [[(577, 310)], [(511, 310), (643, 310)],
                                  [(445, 310), (577, 310), (709, 310)],
                                  [(379, 310), (511, 310), (643, 310), (775, 310)]]
        self.card_table = []
        self.cords_animeted = [[[577, 525], [577, 5]], [[577, 525], [100, 80], [1054, 80]],
                               [[577, 525], [12, 265], [577, 5], [1142, 265]]]
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
        # сделать функци при вызове, которой делатся
        # заглушки с картами текущего игрока и анимация переворота карт
        # после переворота карт

    def animated_change_players(self):
        if len(self.players) == 4:
            self.four_group.draw(self.screen)
            self.four_group.update()
            clock.tick(FPS)
            self.kol_frames += 1
            if self.kol_frames == 25:
                self.kol_frames = 0
                self.flag_change_players = False
        elif len(self.players) == 3:
            self.three_group.draw(self.screen)
            self.three_group.update()
            clock.tick(FPS)
            self.kol_frames += 1
            if self.kol_frames == 33:
                self.kol_frames = 0
                self.flag_change_players = False
        elif len(self.players) == 2:
            self.two_group.draw(self.screen)
            self.two_group.update()
            clock.tick(FPS)
            self.kol_frames += 1
            if self.kol_frames == 45:
                self.kol_frames = 0
                self.flag_change_players = False

    def update(self, events):
        for event in events:
            for i in self.now_button:
                if i.handleEvent(event):
                    self.change_players(int(i.name_image().split('.')[0]))
                    self.button_image = True
                    k = len(self.now_player.cards_list) - 1 if len(self.now_player.cards_list) != 1 else len(self.now_player.cards_list)
                    if k > 0:
                        self.coords_plug_but = []
                        for i in self.layout_concepts[k - 1]:
                            self.coords_plug_but.append([*i.getLoc(), (577 - i.getLoc()[0])])
            if event.type == pygame.QUIT:
                terminate()

        if self.button_image:
            for cr in range(len(self.coords_plug_but)):
                self.screen.blit(self.image_0, (int(self.coords_plug_but[cr][0]),
                                                self.coords_plug_but[cr][1]))
                self.coords_plug_but[cr][0] += self.coords_plug_but[cr][2] / 100
            if all(round(x[0]) == round(self.coords_plug_but[0][0]) for x in self.coords_plug_but):
                self.button_image = False
                self.flag_change_players = True

        for i in self.now_button:
            i.draw()
        if len(self.card_table) != 0 and self.card_table != 5:
            coord_now = self.coords_card_table[len(self.card_table) - 1]
            for i in range(len(coord_now)):
                self.screen.blit(load_image(f'./data/kartinki cards/{self.card_table[i]}.jpg',
                                            scale=self.size_cards), coord_now[i])
        if not self.flag_change_players:
            plug_players = []
            if len(self.players) == 2:
                plug_players = [(self.st_card, (577, 5))]
            elif len(self.players) == 3:
                plug_players = [(self.st_card, (100, 80)), (self.st_card, (1054, 80))]
            elif len(self.players) == 4:
                plug_players = [(self.st_card, (12, 265)), (self.st_card, (577, 5)), (self.st_card, (1142, 265))]
            for cr in plug_players:
                screen.blit(*cr)
            self.cords_animeted = [[[577, 310], [577, 5]], [[577, 310], [100, 80], [1054, 80]],
                                   [[577, 310], [12, 265], [577, 5], [1142, 265]]]
        else:
            self.animated_change_players()


if __name__ == '__main__':
    pygame.init()
    FPS = 65
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    players = [([45], 'DeeDloh'), ([78, 2, 6], 'ладно'),
               ([95, 36, 59], '123')]
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
