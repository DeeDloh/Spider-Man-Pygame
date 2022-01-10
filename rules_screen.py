import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygwidgets import DisplayText

from load_image import load_image
from terminate import terminate

disp_id = 0
first_draw = 0


class RuleViewer:
    def __init__(self, screen, x, y, rule_folder):
        bord_x, bord_y = x + 1, y + 1
        ins_x, ins_y = x + 3, y + 3
        w, h = 399, 599

        global first_draw
        if not first_draw:
            pygame.draw.rect(screen, 'black', (bord_x, bord_y, w, h), 3)
            pygame.draw.rect(screen, 'white', (ins_x, ins_y, w - 4, h - 4))
            first_draw = 1
        self.text_rect = (ins_x, ins_y, w - 4, h - 4)

        self.rule_txt_disp = DisplayText(rule_surf, (ins_x + 10, ins_y + 10), width=w - 24, height=h - 94,
                                         fontName="./data/UpheavalPro.ttf", fontSize=23)
        back_btn = Button(screen, ins_x + 10, ins_y + self.rule_txt_disp.getRect()[3] + 15, 65, 65, borderThickness=3,
                          onClick=(lambda n=0: self.change_rules(n)))
        self.rule_name_disp = DisplayText(rule_surf, (back_btn.getX() + 70, back_btn.getY()+25), width=235, height=65,
                                          fontName="./data/UpheavalPro.ttf", fontSize=30, justified='center')
        # print(self.rule_name_disp.getRect())
        forw_btn = Button(screen, self.rule_name_disp.getX() + 240, back_btn.getY(), 65, 65, borderThickness=3,
                          onClick=(lambda n=1: self.change_rules(n)))

        back_btn.setImage(load_image('data/back.png', scale=(65, 65)))
        forw_btn.setImage(load_image('data/forward.png', scale=(65, 65)))

        # подключаем правила, которые будут отображться (для сплава или обычные)
        self.rule_name, self.rule_txt = [], []
        rule_files_names = os.listdir(rule_folder)
        for name in rule_files_names:
            with open(f'{rule_folder}/{name}', encoding='utf-8') as txt:
                self.rule_name.append(name.split('.')[0])
                x = []
                for i in txt.readlines():
                    x.append(i.strip())
                    x.append('\n')
                self.rule_txt.append(x)

        self.disp_len = len(self.rule_name) - 1

    def change_rules(self, direction): # переключение правил стрелками
        global disp_id, font, fon
        disp_id = disp_id + 1 if direction else disp_id - 1
        if disp_id < 0:
            disp_id = self.disp_len
        elif disp_id > self.disp_len:
            disp_id = 0

        rule_surf.fill('white', self.text_rect)
        self.rule_name_disp.setValue(self.rule_name[disp_id])
        self.rule_txt_disp.setValue(self.rule_txt[disp_id])

        rule_surf.blit(rule_surf, (0, 0))
        self.rule_name_disp.draw()
        self.rule_txt_disp.draw()


def rules_screen(screen, WIDTH=1280, HEIGHT=720):
    global fon
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, -1))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        pygame.display.flip()
        game_rules = RuleViewer(screen, 15, 105, 'pravila')
        # splav_rules = RuleViewer(screen, 865, 105, 'dla_splav')
        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    rule_surf = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    pygame.display.set_caption('хуядно')
    clock = pygame.time.Clock()
    rules_screen(screen)