import pygame
import pygame_widgets
from pygame_widgets.button import Button

from terminate import terminate
from load_image import load_image
import cards
import rules_screen



def menu(screen, WIDTH=1280, HEIGHT=720):
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    text_but = ['Играть', 'Таблица лидеров', 'Карты', 'Выйти']
    func = [1, 2, 3, 4]
    color = [(0, 0, 0), (75, 0, 130), (128, 0, 128)]
    cords_1 = [(317, 102), (316, 101), (315, 100)]
    cords_2 = [(362, 202), (361, 201), (360, 200)]
    font_all = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    f1 = pygame.font.Font("./data/UpheavalPro.ttf", 70)
    buttons = []
    for i in range(4):
        button = Button(screen, 490, 300 + i * 100, 300, 75, text=text_but[i], margin=20, font=font_all,
        inactiveColour=(220, 20, 60), hoverColour=(65, 105, 225), pressedColour=(75, 0, 130),
        onClick=(lambda n=func[i], k=buttons: clicked_func(n, screen, k))
        )
        buttons.append(button)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(fon, (0, -1))
        for i in range(3):
            text1 = f1.render('Spider-man cards', True, color[i])
            screen.blit(text1, cords_1[i])
            text2 = f1.render('Pygame edition', True, color[i])
            screen.blit(text2, cords_2[i])

        pygame_widgets.update(events)
        pygame.display.flip()


def clicked_func(n, screen, buttons):
    for i in buttons: # вынес скрытие кнопок сюда, т.к. по нажатию любой кнопки в гл. меню нам надо скрывать кнопки
        i._hidden = True
        i._disabled = True

    if n == 4:
        terminate()
    elif n == 3:
        cards.cards_screen(screen)
    elif n == 1:
        rules_screen.rules_screen(screen)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    menu(screen)