import os
import sys
import sqlite3


from AnimatedSprite import AnimatedSprite
from pygame_widgets.button import Button

from load_image import load_image
from cards_screen import cards_screen
from terminate import terminate
from main_menu import menu

import pygame
import pygame_widgets



def start_screen():
    FPS = 12
    intro_text = ["Привет игрок!",
                  "Это улучшенная версия игры",
                  "Spider-man PyQt на Pygame",
                  "Приятной игры!",
                  "",
                  "Авторы:",
                  "Венков Кирилл и Егор Захаров", ""
                  "ладно"
                  ]

    fon = pygame.transform.scale(load_image('./data/start.jpg'), (WIDTH, HEIGHT))
    f1 = pygame.font.Font("./data/UpheavalPro.ttf", 30)

    font = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    chel = AnimatedSprite(load_image("./data/animated_rabbit.png"), 7, 2, 800, -100, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill(pygame.Color("black"))
        screen.blit(fon, (0, -1))
        all_sprites.draw(screen)
        all_sprites.update()
        text1 = f1.render('Нажми Enter чтобы продолжить', True, (255, 255, 255))
        screen.blit(text1, (375, 200))
        text_coord = 470
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)




if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0))
    player = None
    all_sprites = pygame.sprite.Group()
    start_screen()
    menu(screen)

