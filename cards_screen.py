import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

from load_image import load_image
from terminate import terminate


def cards_screen(screen, WIDTH=1280, HEIGHT=720):
    cards = []

    for i in range(1, 40):
        card = pygame.transform.scale(load_image(f'./data/kartinki cards/{i}.jpg'), (213, 320))
        cards.append(card)
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    slider = Slider(screen, 100, 100, 800, 40, min=0, max=99, step=1)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, -1))
        for cd in range(len(cards)):
            if cd < 30:
                screen.blit(cards[cd], (10 + 223 * cd, 10))
            else:
                screen.blit(cards[cd], (10 + 223 * (cd - 30), 340))
        pygame_widgets.update(events)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    cards_screen(screen)