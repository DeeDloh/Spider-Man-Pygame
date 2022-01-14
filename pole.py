import pygame
import pygame_widgets

from pygame_widgets.button import Button

from terminate import terminate
from load_image import load_image
from player import Player
from domination import domination
from troichka import troichka

PEREVOD_PR = {'Domination': domination,
              'Троечка': troichka}

class Pole:
    def __init__(self, screen, players, pravila_igr, pravila_splav='Амереканская версия', WIDTH=1280, HEIGHT=720):
        self.screen = screen
        self.fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
        self.players = players

        self.layout_concepts = [self.creat_layout_concept(i) for i in range(1, 6)]



    def creat_layout_concept(self, n):
        buttons = []
        if n % 2 == 1:
            for i in range(n):
                button = Button(self.screen, 577 - (132 * n) + 132 * i, 525, *size_cards)
                buttons.append(button)
        else:
            for i in range(n):
                button = Button(self.screen, 511 + i * 132 - (132 * (n // 2 - 1)), 525, *size_cards)
                buttons.append(button)
        return buttons






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


    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        for cr in plug_players:
            screen.blit(*cr)

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



if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    size_cards = (126, 190)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    players = []
    Player_1 = Player([45, 53, 47], 'DeeDloh')
    Player_2 = Player([46, 12], 'ладно')
    Player_3 = Player([45, 53, 47], '123')
    players.extend([Player_1, Player_2, Player_3])
    screen_pole(screen, players, 'Троечка')
