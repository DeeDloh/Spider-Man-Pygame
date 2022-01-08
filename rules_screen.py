import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

from load_image import load_image
from terminate import terminate

import os


class RuleViewer:
    def __init__(self, screen, x, y, splav=0):
        bord_x, bord_y = x+1, y+1
        ins_x, ins_y = x+3, y+3
        w, h = 399, 599

        pygame.draw.rect(screen, 'black', (bord_x, bord_y, w, h), 3)
        screen.fill('white', (ins_x, ins_y, w-4, h-4))

        self.rule_txt_disp = TextBox(screen, ins_x+10, ins_y+10, w-24, h-94)
        back_btn = Button(screen, ins_x+10, ins_y+self.rule_txt_disp.getHeight()+15, 65, 65, borderThickness=3)
        self.rule_name_disp = TextBox(screen, back_btn.getX()+70, back_btn.getY(), 235, 65, borderThickness=3)
        forw_btn = Button(screen, self.rule_name_disp.getX()+240, back_btn.getY(), 65, 65, borderThickness=3)

        back_btn.setImage(load_image('data/back.png', scale=(65, 65)))
        forw_btn.setImage(load_image('data/forward.png', scale=(65, 65)))

    # подключаем правила, которые будут отображться (для сплава или обычные)
        self.rule_name, self.rule_txt = [], []
        fold = 'pravila' if not splav else 'dla_splav'
        rule_files_names = os.listdir(fold)
        for name in rule_files_names:
            with open(f'{fold}/{name}', encoding='utf-8') as txt:
                self.rule_name.append(name.split('.')[0])
                self.rule_txt.append(txt.readlines())

        self.disp_id = 0
        self.disp_len = len(self.rule_name)
        back_btn.onClick(self.change_rules())
        forw_btn.onClick(self.change_rules(1))

    def change_rules(self, direction=0): # переключение правил стрелками
        self.disp_id = self.disp_id + 1 if direction else self.disp_id - 1
        if self.disp_id < 0:
            self.disp_id = self.disp_len
        elif self.disp_id > self.disp_len:
            self.disp_id = 0
        print(self.disp_id)

        self.rule_name_disp.setText(self.rule_name[self.disp_id])
        self.rule_txt_disp.setText(self.rule_txt[self.disp_id])


def rules_screen(screen, WIDTH=1280, HEIGHT=720):
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        pygame.display.flip()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, -1))
        r = RuleViewer(screen, 10, 110)
        pygame_widgets.update(events)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('хуядно')
    clock = pygame.time.Clock()
    rules_screen(screen)