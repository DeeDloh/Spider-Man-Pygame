import pygame
import pygame_widgets
import sqlite3
from pygame_widgets.slider import Slider

from load_image import load_image
from terminate import terminate
from buttons import SpiderButton


class LeadTable:
    def __init__(self, screen):
        con = sqlite3.connect('data/leaderboard.db')
        cur = con.cursor()
        db_pull = cur.execute('SELECT * FROM name_score ORDER BY score DESC').fetchall()
        con.close()
        self.name_score = [[i[0] for i in db_pull], [str(i[1]) for i in db_pull]]

        self.font = pygame.font.Font("./data/UpheavalPro.ttf", 35)
        self.screen = screen

        self.slider = Slider(screen, 768, 115, 20, 400, vertical=True, max=700, step=1, handleRadius=20, initial=700,
                             colour=(142, 68, 173), handleColour=(91, 44, 111))
        self.slider._hidden = True

        self.button_1 = SpiderButton(screen, (0, 0), '<-', width=100, height=40, upColor=(187, 143, 206),
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
        self.slider._hidden = False
        self.button_1.show()

    def scroll(self, movement):
        x = 200
        for i in range(2):
            y = 75 + (movement - 700)
            for j in range(len(self.name_score[0])):
                if i == 0:
                    self.screen.blit(self.font.render(self.name_score[i][j], True, 'white'), (x, y))
                else:
                    p_len = self.font.render(self.name_score[i][j], True, 'white').get_size()[0]
                    self.screen.blit(self.font.render(self.name_score[i][j], True, 'white'), (x - p_len, y))
                y += 45
            x = x + 300

    def update(self, events):
        self.enabled_button()
        if self.click_back:
            self.click_back = False
            self.disabled_button()
            return 1
        sl = self.slider.getValue()

        for event in events:
            if self.button_1.handleEvent(event):
                self.clicked_back()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                elif event.button == 4:
                    if sl <= 665:
                        self.slider.setValue(sl + 35)
                    print(sl)
                elif event.button == 5:
                    if sl >= 35:
                        self.slider.setValue(sl - 35)
                    print(sl)
        self.scroll(sl)
        self.button_1.draw()
        pygame_widgets.update(events)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    a = LeadTable(screen)
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