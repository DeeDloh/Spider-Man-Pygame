import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

import main_menu
from load_image import load_image
from terminate import terminate


def cards_screen(screen, WIDTH=1280, HEIGHT=720):
    cards = []

    for i in range(1, 143):
        card = pygame.transform.scale(load_image(f'./data/kartinki cards/{i}.jpg'), (213, 320))
        cards.append(card)

    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    dis = []
    slider = Slider(screen, 150, 680, 1100, 20, min=0, max=14560, step=1, handleRadius=20,
                    colour=(142, 68, 173), handleColour=(91, 44, 111))
    slider.setValue(0)
    dis.append(slider)

    button = Button(screen, 10, 670, 100, 40, inactiveColour=(187, 143, 206), hoverColour=(165, 105, 189),
                    pressedColour=(125, 60, 152), text=' <-', font=pygame.font.Font("./data/UpheavalPro.ttf", 40),
                    onClick=lambda k=dis, n=cards: clicked(screen, k, n))
    dis.append(button)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))

        sl = slider.getValue()
        for cd in range(len(cards)):
            if cd < 71:
                screen.blit(cards[cd], (10 + 223 * cd - sl, 10))
            else:
                screen.blit(cards[cd], (10 + 223 * (cd - 71) - sl, 340))

        pygame_widgets.update(events)
        pygame.display.flip()


def clicked(screen, dis, n):
    for i in dis:
        i._hidden = True
        i._disabled = True
    n.clear()
    main_menu.menu(screen)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    cards_screen(screen)
