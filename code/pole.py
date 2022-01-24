import pygame
import random
import sqlite3

from pygwidgets import DisplayText
from classes.buttons import SpiderButtonImage
from code.functions.terminate import terminate
from code.functions.load_image import load_image
from player import Player
from troichka import troichka
from troichka_plus import troichka_plus
from classes.AnimatedSprite import AnimatedSprite

PEREVOD_HAR = {'intellect': 'интеллект',
               'power': 'сила',
               'speed_and_agility': 'скорость и ловкость',
               'special_skills': 'особые умения',
               'fighting_skills': 'бойцовские навыки',
               }



class Pole:
    def __init__(self, screen, players, pravila_igr, pravila_splav='Амереканская версия',
                 size_cards=(126, 190), WIDTH=1280, HEIGHT=720):
        """players -> list | [(list_id, nickname)]
        pravila_igr -> str
        pravila_splav -> str"""

        self.screen = screen
        self.players = [Player(*i) for i in players]
        self.player_winner = ''
        self.clock = pygame.time.Clock()
        if pravila_splav == 'Амереканская версия':
            self.haract_splav = (132, 125, 140, 351, 110)

        if pravila_igr == 'Троечка':
            self.now_haract = ('скорость и ловкость', 'сила')
        if pravila_igr == 'Троечка+':
            self.now_haract = list(PEREVOD_HAR.keys())
            random.shuffle(self.now_haract)
            self.now_haract = self.now_haract[:2]
        self.font = pygame.font.Font("../data/UpheavalPro.ttf", 30)
        self.st_card = pygame.transform.scale(load_image('../data/kartinki cards/0.jpg'), size_cards)
        self.size_cards = size_cards
        self.pravila_igr = pravila_igr
        con = sqlite3.connect("../data/databases/Spider-man_cards_stats.sqlite")
        self.cur = con.cursor()
        self.haract_disp = DisplayText(screen, (776, 110), fontName="../data/UpheavalPro.ttf",
                                       fontSize=30, backgroundColor=(255, 255, 255),
                                       justified='center', width=195, height=390)
        self.layout_concepts = [self.creat_layout_concept(i) for i in range(1, 7)]
        self.now_player = self.players[0]
        kol_kart = len(self.now_player.cards_list)
        self.now_button = self.layout_concepts[kol_kart - 1]
        self.prod = False
        self.button_image = True
        self.flag_change_players = False
        # False - now players chooses card, True - players chose card and stand plug
        self.four_group = pygame.sprite.Group()
        self.three_group = pygame.sprite.Group()
        self.two_group = pygame.sprite.Group()
        self.perehod_2 = AnimatedSprite(load_image("../data/images/final2.png"), 9, 5, 0, 0, self.two_group)
        self.perehod_3 = AnimatedSprite(load_image("../data/images/final3.png"), 11, 3, 0, 0, self.three_group)
        self.perehod_4 = AnimatedSprite(load_image("../data/images/final.png"), 5, 5, 0, 0, self.four_group)
        self.kol_frames = 0
        self.coords_card_table = [[(577, 310)], [(511, 310), (643, 310)],
                                  [(445, 310), (577, 310), (709, 310)],
                                  [(379, 310), (511, 310), (643, 310), (775, 310)]]
        self.card_table = []
        self.cords_animeted = [[[577, 525], [577, 5]], [[577, 525], [100, 80], [1054, 80]],
                               [[577, 525], [12, 265], [577, 5], [1142, 265]]]
        for i in range(kol_kart):
            self.now_button[i].change_image(
                f'../data/kartinki cards/{self.now_player.cards_list[i]}.jpg', self.size_cards)
        self.FPS = 65

    def creat_layout_concept(self, n):
        buttons = []
        if n % 2 == 1:
            for i in range(n):
                button = SpiderButtonImage(self.screen, (577 - (132 * (n // 2)) + 132 * i, 525),
                                           '../data/kartinki cards/0.jpg', self.size_cards)
                button.hide()
                buttons.append(button)
        else:
            for i in range(n):
                button = SpiderButtonImage(self.screen, (511 + i * 132 - (132 * (n // 2 - 1)), 525),
                                           '../data/kartinki cards/0.jpg', self.size_cards)
                button.hide()
                buttons.append(button)
        return buttons

    def player_turn(self, id):
        for i in self.now_button:
            i.hide()
        self.card_table.append(id)

    def animated_change_players(self):
        if len(self.players) == 4:
            self.four_group.draw(self.screen)
            self.four_group.update()
            self.clock.tick(self.FPS)
            self.kol_frames += 1
            if self.kol_frames == 25:
                self.kol_frames = 0
                self.flag_change_players = False
                self.button_image = True
                self.show_change_player()

        elif len(self.players) == 3:
            self.three_group.draw(self.screen)
            self.three_group.update()
            self.clock.tick(self.FPS)
            self.kol_frames += 1
            if self.kol_frames == 33:
                self.kol_frames = 0
                self.flag_change_players = False
                self.button_image = True
                self.show_change_player()

        elif len(self.players) == 2:
            self.two_group.draw(self.screen)
            self.two_group.update()
            self.clock.tick(self.FPS)
            self.kol_frames += 1
            if self.kol_frames == 45:
                self.kol_frames = 0
                self.flag_change_players = False
                self.button_image = True
                self.show_change_player()

    def show_change_player(self):
        k = self.players.index(self.now_player) + 1 \
            if self.players.index(self.now_player) + 1 != len(self.players) else 0
        self.now_player = self.players[k]
        for i in self.players:
            if len(i.cards_list) == 0:
                del self.players[self.players.index(i)]

        kol_kart = len(self.now_player.cards_list)
        self.now_button = self.layout_concepts[kol_kart - 1]
        for i in range(kol_kart):
            self.now_button[i].change_image(
                f'../data/kartinki cards/{self.now_player.cards_list[i]}.jpg', self.size_cards)
            self.now_button[i].show()

    def opr_winnner_troichka(self):
        losser = troichka(*self.card_table, har_spla=self.haract_splav)

        if losser != None and self.card_table.index(losser) == 0:
            k = self.players.index(self.now_player)
            self.player_winner = self.players[k].nickname
            self.players[k - 1].del_card(self.card_table[0])
        elif losser != None and self.card_table.index(losser) == 1:
            k = self.players.index(self.now_player) - 1
            self.player_winner = self.players[k].nickname
            self.players[k + 1].del_card(self.card_table[1])
        else:
            self.player_winner = 'Ничья'
            k = self.players.index(self.now_player)
            self.players[k - 1].del_card(self.card_table[0])
            self.players[k].del_card(self.card_table[1])
        self.card_table = []

    def opr_winnner_troichka_plus(self):
        losser = troichka_plus(*self.card_table, self.now_haract)
        print(losser)
        print(self.card_table)

        if losser != None and self.card_table.index(losser) == 0:
            k = self.players.index(self.now_player)
            self.player_winner = self.players[k].nickname
            self.players[k - 1].del_card(self.card_table[0])
        elif losser != None and self.card_table.index(losser) == 1:
            k = self.players.index(self.now_player) - 1
            self.player_winner = self.players[k].nickname
            self.players[k + 1].del_card(self.card_table[1])
        else:
            self.player_winner = 'Ничья'
            k = self.players.index(self.now_player)
            self.players[k - 1].del_card(self.card_table[0])
            self.players[k].del_card(self.card_table[1])
        self.card_table = []
        self.now_haract = list(PEREVOD_HAR.keys())
        random.shuffle(self.now_haract)
        self.now_haract = self.now_haract[:2]

    def enabled(self):
        for i in self.now_button:
            i.show()

    def disabled(self):
        for i in self.now_button:
            i.hide()

    def update(self, events):

        for event in events:
            for i in self.now_button:
                if i.handleEvent(event):
                    self.player_turn(int(i.name_image().split('.')[0]))
                    self.button_image = False
                    k = len(self.now_player.cards_list) if len(self.now_player.cards_list) != 1 \
                        else len(self.now_player.cards_list)
                    if k > 1:
                        self.coords_plug_but = []
                        for i in self.layout_concepts[k - 1]:
                            self.coords_plug_but.append([*i.getLoc(), (577 - i.getLoc()[0])])
                    else:
                        self.coords_plug_but = []

            if event.type == pygame.QUIT:
                terminate()

        if len(self.card_table) != 0 and self.card_table != 5:
            coord_now = self.coords_card_table[len(self.card_table) - 1]
            for i in range(len(coord_now)):
                self.screen.blit(load_image(f'../data/kartinki cards/{self.card_table[i]}.jpg',
                                            scale=self.size_cards), coord_now[i])

            if self.pravila_igr == 'Троечка' and len(self.card_table) == 2:
                self.opr_winnner_troichka()
            elif self.pravila_igr == 'Троечка+' and len(self.card_table) == 2:
                self.opr_winnner_troichka_plus()


        if not self.flag_change_players:
            plug_players = []
            if len(self.players) == 2:
                plug_players = [(self.st_card, (577, 5))]
            elif len(self.players) == 3:
                plug_players = [(self.st_card, (100, 80)), (self.st_card, (1054, 80))]
            elif len(self.players) == 4:
                plug_players = [(self.st_card, (12, 265)), (self.st_card, (577, 5)), (self.st_card, (1142, 265))]
            for cr in plug_players:
                self.screen.blit(*cr)
            self.cords_animeted = [[[577, 310], [577, 5]], [[577, 310], [100, 80], [1054, 80]],
                                   [[577, 310], [12, 265], [577, 5], [1142, 265]]]
            co = self.now_button[-1].getLoc()
            text2 = self.font.render(self.now_player.nickname, True, (255, 255, 255))
            self.screen.blit(text2, (co[0] + 132, co[1] + 5))
        else:
            self.animated_change_players()
        if self.pravila_igr == 'Троечка':
            text1 = self.font.render(', '.join(self.now_haract), True, (255, 255, 255))
            self.screen.blit(text1, (380, 220))
        elif self.pravila_igr == 'Троечка+':
            text1 = self.font.render(', '.join([PEREVOD_HAR[i] for i in self.now_haract]), True, (255, 255, 255))
            self.screen.blit(text1, (380, 220))
        text3 = self.font.render('Выиграл: ' + self.player_winner, True, (255, 255, 255))
        self.screen.blit(text3, (380, 250))
        if len(self.players) == 1 or len(self.players) == 0:
            return self.players

        if not self.button_image:
            for cr in range(len(self.coords_plug_but)):
                self.screen.blit(self.st_card, (int(self.coords_plug_but[cr][0]),
                                                self.coords_plug_but[cr][1]))
                self.coords_plug_but[cr][0] += self.coords_plug_but[cr][2] / 50
            if all(round(x[0]) == round(self.coords_plug_but[0][0]) for x in self.coords_plug_but):
                self.button_image = True
                self.flag_change_players = True
        else:
            for i in self.now_button:
                i.draw()
                if not self.flag_change_players:
                    k = i.getLoc()
                    if pygame.mouse.get_pos()[0] in range(k[0], k[0] + 126) \
                            and pygame.mouse.get_pos()[1] in range(k[1], k[1] + 190):
                        if i.name_image().split('.')[0] != '142':
                            haract = self.cur.execute(f"""SELECT * from cadrs_hero_villain
                              WHERE id = {i.name_image().split('.')[0]}""").fetchall()[0]
                            vivod_1 = f'{haract[1]}\n\n\nинтеллект:\n{haract[3]}\n\nсила:\n{haract[4]}\n'
                            vivod_2 = f'\nскорость и\nловкость:\n{haract[5]}\n\nособые\nумения:\n{haract[6]}\n'
                            vivod_3 = f'\nбойцовские\n\nнавыки:\n{haract[7]}'
                        else:
                            vivod_1 = f'Сплав\n\n\nинтеллект:\n{self.haract_splav[0]}\n\nсила:\n{self.haract_splav[1]}\n'
                            vivod_2 = f'\nскорость и\nловкость:\n{self.haract_splav[2]}\n\nособые\nумения:\n{self.haract_splav[3]}\n'
                            vivod_3 = f'\nбойцовские\n\nнавыки:\n{self.haract_splav[4]}'
                        vivod = vivod_1 + vivod_2 + vivod_3
                        self.haract_disp.setValue(vivod)
                        card = load_image(f'../data/kartinki cards/{i.name_image()}', scale=(266, 400))
                        self.screen.blit(card, (507, 100))
                        pygame.draw.rect(self.screen, (255, 255, 255), (773, 100, 200, 400), width=0)
                        self.haract_disp.draw()
                        pygame.draw.rect(self.screen, (0, 0, 0), (773, 100, 200, 400), width=4)


if __name__ == '__main__':
    pygame.init()
    FPS = 65
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    players = [([142, 24], 'DeeDloh'), ([78, 2], 'ладно'),
               ([95, 36], '123')]
    pole = Pole(screen, players, 'Троечка+')
    pole.enabled()
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
