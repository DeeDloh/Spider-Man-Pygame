from classes.AnimatedSprite import AnimatedSprite

from code.functions.load_image import load_image
from code.functions.terminate import terminate
from main_menu import Menu


import pygame


def start_screen(all_sprites):
    # Приветственное окно с зайчиком
    FPS = 14
    intro_text = ["Привет игрок!",
                  "Это улучшенная версия игры",
                  "Spider-man PyQt на Pygame",
                  "Приятной игры!",
                  "",
                  "Авторы:",
                  "Венков Кирилл и Егор Захаров", ""
                  "ладно"
                  ]

    fon = pygame.transform.scale(load_image('../data/images/start.jpg'), (WIDTH, HEIGHT))
    font = pygame.font.Font("../data/UpheavalPro.ttf", 30)
    # Создаем класс с зайчиком
    chel = AnimatedSprite(load_image("../data/images/animated_rabbit.png"), 7, 2, 800, -100, all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fon = 1
                    return

        screen.fill(pygame.Color("black"))
        screen.blit(fon, (0, -1))
        all_sprites.draw(screen)
        # Меняем кадр зайчика на следидуйщий
        all_sprites.update()
        text1 = font.render('Нажми Enter чтобы продолжить', True, (255, 255, 255))
        screen.blit(text1, (375, 200))
        text_coord = 470
        # Текст с пояснением что это за программа
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
    fon = pygame.transform.scale(load_image('../data/images/fon_main.jpg'), (WIDTH, HEIGHT))

    screen.fill((0, 0, 0))
    player = None
    all_sprites = pygame.sprite.Group()
    start_screen(all_sprites)
    all_sprites = pygame.sprite.Group()

    menu = Menu(screen)
    menu.enabled_button()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        menu.update(events)
        pygame.display.flip()