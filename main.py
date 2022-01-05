import os
import sys
import sqlite3
from AnimatedSprite import AnimatedSprite

import pygame
import pygame_widgets
from pygame_widgets.button import Button


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

    fon = pygame.transform.scale(load_image('start.jpg'), (WIDTH, HEIGHT))
    f1 = pygame.font.Font("./data/UpheavalPro.ttf", 30)

    font = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    chel = AnimatedSprite(load_image("animated_rabbit.png"), 7, 2, 800, -100, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    return  # начинаем игру
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


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def clicked_func(n):
    if n == 4:
        terminate()
    else:
        print(n)

def second_screen():
    fon = pygame.transform.scale(load_image('fon_main.jpg'), (WIDTH, HEIGHT))
    text_but = ['Играть', 'Таблица лидеров', 'Карты', 'Выйти']
    func = [1, 2, 3, 4]
    color = [(0, 0, 0), (75, 0, 130), (128, 0, 128)]
    cords_1 = [(317, 102), (316, 101), (315, 100)]
    cords_2 = [(362, 202), (361, 201), (360, 200)]
    font_all = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    f1 = pygame.font.Font("./data/UpheavalPro.ttf", 70)
    for i in range(4):
        button = Button(screen, 490, 300 + i * 100, 300, 75, text=text_but[i], margin=20, font=font_all,
        inactiveColour=(220, 20, 60), hoverColour=(65, 105, 225), pressedColour=(75, 0, 130),
        onClick=(lambda n=func[i]: clicked_func(n))
        )
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        screen.blit(fon, (0, -1))
        for i in range(3):
            text1 = f1.render('Spider-man cards', True, color[i])
            screen.blit(text1, cords_1[i])
            text2 = f1.render('Pygame edition', True, color[i])
            screen.blit(text2, cords_2[i])
        pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
        pygame.display.update()


def cards_screen():
    pass


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
    #start_screen()
    second_screen()

