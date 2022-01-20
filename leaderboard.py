import pygame
import pygame_widgets
import sqlite3
from pygame_widgets.slider import Slider

from load_image import load_image
from terminate import terminate
from buttons import SpiderButton


class LeadTable:
    def __init__(self, screen, fon):
        con = sqlite3.connect('data/leaderboard.db')
        cur = con.cursor()
        db_pull = cur.execute('SELECT * FROM name_score ORDER BY score DESC').fetchall()
        con.close()
        self.name_score = [[i[0] for i in db_pull], [str(i[1]) for i in db_pull]]
        self.lb_len = len(self.name_score[0])

        self.font = pygame.font.Font("./data/UpheavalPro.ttf", 40)
        self.fon = fon
        self.screen = screen

        self.slider = Slider(screen, 1224, 40, 20, 640, vertical=True, step=40, handleRadius=20,
                             colour=(142, 68, 173), handleColour=(91, 44, 111))
        self.no_slider_flag = False
        if self.lb_len < 17:
            self.slider.disable()
            self.slider._hidden = True
            self.no_slider_flag = True
        self.slider.max = 40 * (self.lb_len - 16)
        self.slider.setValue(self.slider.max)
        self.slider._hidden = True

        self.button_1 = SpiderButton(screen, (0, 0), '<-', width=150, height=60, upColor=(187, 143, 206),
                                     overColor=(165, 105, 189), downColor=(125, 60, 152),
                                     fontName="./data/UpheavalPro.ttf", fontSize=40)
        self.button_1.hide()

        self.click_back = False
        self.scroll(0)

    def clicked_back(self):
        self.click_back = True
        print(123)

    def disabled_button(self):
        self.slider._hidden = True
        self.button_1.hide()

    def enabled_button(self):
        if not self.no_slider_flag:
            self.slider._hidden = False
        self.button_1.show()

    def scroll(self, movement):
        x = 400
        for i in range(2):
            y = 40 + (movement - self.slider.max)
            for j in range(self.lb_len):
                y += 10
                if i == 0:
                    self.screen.blit(self.font.render(self.name_score[i][j], True, 'white'), (x, y))
                else:
                    p_len = self.font.render(self.name_score[i][j], True, 'white').get_size()[0]
                    self.screen.blit(self.font.render(self.name_score[i][j], True, 'white'), (x - p_len, y))
                y += 30
            x = 880

    def update(self, events):
        self.enabled_button()
        if self.click_back:
            self.click_back = False
            self.disabled_button()
            return 1
        sl = self.slider.getValue()
        sl_max = self.slider.max

        for event in events:
            if self.button_1.handleEvent(event):
                self.clicked_back()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.no_slider_flag:
                if event.button == 1:
                    print(event.pos)
                elif event.button == 4:
                    if sl <= sl_max - 40:
                        self.slider.setValue(sl + 40)
                    else:
                        self.slider.setValue(sl_max)
                elif event.button == 5:
                    if sl >= 40:
                        self.slider.setValue(sl - 40)
                    else:
                        self.slider.setValue(0)
        self.scroll(sl)
        self.screen.blit(self.fon, (350, 0), (350, 0, 580, 40))
        self.screen.blit(self.fon, (350, 680), (350, 680, 580, 40))
        self.button_1.draw()
        pygame_widgets.update(events)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('./data/fon_leaderboard.jpg'), (WIDTH, HEIGHT))
    a = LeadTable(screen, fon)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(fon, (0, 0))
        a.update(events)
        pygame.display.flip()