import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider

from load_image import load_image
from terminate import terminate

class Cards_Screen:
    def __init__(self, screen):
        self.screen = screen
        self.do_cards()
        self.click_back = False

        self.dis = []
        slider = Slider(screen, 150, 680, 1100, 20, min=0, max=14560, step=1, handleRadius=20,
                        colour=(142, 68, 173), handleColour=(91, 44, 111))
        slider.setValue(0)
        slider._hidden = True
        self.dis.append(slider)

        button = Button(screen, 10, 670, 100, 40, inactiveColour=(187, 143, 206), hoverColour=(165, 105, 189),
                        pressedColour=(125, 60, 152), text=' <-', font=pygame.font.Font("./data/UpheavalPro.ttf", 40),
                        onClick=lambda: self.disabled_button())
        button._hidden = True
        self.dis.append(button)

    def disabled_button(self):
        for i in self.dis:
            i._hidden = True
        self.click_back = True

    def enabled_button(self):
        for i in self.dis:
            i._hidden = False


    def do_cards(self):
        self.cards = []
        for i in range(1, 143):
            card = pygame.transform.scale(load_image(f'./data/kartinki cards/{i}.jpg'), (213, 320))
            self.cards.append(card)

    def update(self, events):
        self.enabled_button()
        sl = self.dis[0].getValue()
        for cd in range(len(self.cards)):
            if cd < 71:
                self.screen.blit(self.cards[cd], (10 + 223 * cd - sl, 10))
            else:
                self.screen.blit(self.cards[cd], (10 + 223 * (cd - 71) - sl, 340))
        pygame_widgets.update(events)
        if self.click_back:
            self.click_back = False
            return 1


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()

