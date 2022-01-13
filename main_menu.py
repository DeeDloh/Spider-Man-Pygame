import pygame
import pygame_widgets
from pygame_widgets.button import Button

from terminate import terminate
from load_image import load_image
from cards import Cards_screen
import rules_screen


class Menu:
    def __init__(self, screen, WIDTH=1280, HEIGHT=720):
        self.screen = screen
        self.fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
        text_but = ['Играть', 'Таблица лидеров', 'Карты', 'Выйти']
        func = [1, 2, 3, 4]
        font_all = pygame.font.Font("./data/UpheavalPro.ttf", 30)
        self.buttons = []
        self.cards = Cards_screen(screen)

        for i in range(4):
            button = Button(screen, 490, 300 + i * 100, 300, 75, text=text_but[i], margin=20, font=font_all,
                            inactiveColour=(220, 20, 60), hoverColour=(65, 105, 225), pressedColour=(75, 0, 130),
                            onClick=(lambda n=func[i]: self.clicked_func(n))
                            )
            self.buttons.append(button)

        self.color = [(0, 0, 0), (75, 0, 130), (128, 0, 128)]
        self.cords_1 = [(317, 102), (316, 101), (315, 100)]
        self.cords_2 = [(362, 202), (361, 201), (360, 200)]
        self.f1 = pygame.font.Font("./data/UpheavalPro.ttf", 70)

    def clicked_func(self, n):
        self.disabled_button()
        if n == 4:
            terminate()
        elif n == 3:
            self.cards.enabled_button()
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        terminate()
                self.screen.blit(self.fon, (0, 0))
                if self.cards.update(events) == 1:
                    return
                pygame.display.flip()
        elif n == 1:
            rules_screen.rules_screen(self.screen)

    def disabled_button(self):
        for i in self.buttons:
            i._hidden = True

    def enabled_button(self):
        for i in self.buttons:
            i._hidden = False

    def update(self, events):
        self.enabled_button()
        for i in range(3):
            text1 = self.f1.render('Spider-man cards', True, self.color[i])
            self.screen.blit(text1, self.cords_1[i])
            text2 = self.f1.render('Pygame edition', True, self.color[i])
            self.screen.blit(text2, self.cords_2[i])
        pygame_widgets.update(events)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))

    menu = Menu(screen)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        menu.update(events)
        pygame.display.flip()
