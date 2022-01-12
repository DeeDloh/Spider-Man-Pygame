import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygwidgets import DisplayText

from load_image import load_image
from terminate import terminate


first_draw = 0


class RuleViewer:
    def __init__(self, screen, x, y, rule_folder):
        bord_x, bord_y = x + 1, y + 1
        ins_x, ins_y = x + 3, y + 3
        w, h = 399, 599

        pygame.draw.rect(screen, 'black', (bord_x, bord_y, w, h), 3)
        pygame.draw.rect(screen, 'white', (ins_x, ins_y, w - 4, h - 4))

        self.text_rect = (ins_x, ins_y, w - 4, h - 4)

        self.rule_txt_disp = DisplayText(screen, (ins_x + 10, ins_y + 10), width=w - 24, height=h - 94,
                                         fontName="./data/UpheavalPro.ttf", fontSize=16)
        back_btn = Button(screen, ins_x + 10, ins_y + self.rule_txt_disp.getRect()[3] + 15, 65, 65, borderThickness=3,
                          onClick=(lambda n=0: self.change_rules(screen, n)))
        self.rule_name_disp = DisplayText(screen, (back_btn.getX() + 70, back_btn.getY()+25), width=235, height=65,
                                          fontName="./data/UpheavalPro.ttf", fontSize=30, justified='center')
        self.r_n_d_loc = self.rule_name_disp.getX(), self.rule_name_disp.getY()
        forw_btn = Button(screen, back_btn.getX() + 70 + 240, back_btn.getY(), 65, 65, borderThickness=3,
                          onClick=(lambda n=1: self.change_rules(screen, n)))

        back_btn.setImage(load_image('data/back.png', scale=(65, 65)))
        forw_btn.setImage(load_image('data/forward.png', scale=(65, 65)))

        # подключаем правила, которые будут отображться (для сплава или обычные)
        self.rule_name, self.rule_txt = [], []
        rule_files_names = os.listdir(rule_folder)
        for name in rule_files_names:
            with open(f'{rule_folder}/{name}', encoding='utf-8') as txt:
                n = name.split('.')[0]
                if len(n) > 10:
                    n = n.split()
                    n.insert(1, '\n')
                    n.insert(3, '\n')
                    n = ''.join(n)
                self.rule_name.append(n)
                x = []
                for i in txt.readlines():
                    x.append(i.strip())
                    x.append('\n')
                self.rule_txt.append(x)

        self.disp_len = len(self.rule_name) - 1
        self.disp_id = -1
        self.change_rules(screen, 1)

    def change_rules(self, screen, direction):  # переключение правил стрелками
        self.disp_id = self.disp_id + 1 if direction else self.disp_id - 1
        if self.disp_id < 0:
            self.disp_id = self.disp_len
        elif self.disp_id > self.disp_len:
            self.disp_id = 0

        screen.fill('white', self.text_rect)

        if '\n' in self.rule_name[self.disp_id]:
            self.rule_name_disp.moveY(-18)
        self.rule_name_disp.setValue(self.rule_name[self.disp_id])
        self.rule_txt_disp.setValue(self.rule_txt[self.disp_id])
        screen.blit(screen, (0, 0))

        self.rule_name_disp.draw()
        self.rule_txt_disp.draw()
        self.rule_name_disp.setLoc(self.r_n_d_loc)


def rules_screen(screen, WIDTH=1280, HEIGHT=720):
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))


    color = [(0, 0, 0), (75, 0, 130), (128, 0, 128)]
    for i in range(3):
        choose_rules_label = DisplayText(screen, (55 - 1 * i, 22 - 1 * i),
                                         fontName="./data/UpheavalPro.ttf", fontSize=40,
                                         value='Выберите\nправила игры:',
                                         justified='center', textColor=color[i])

        choose_rules_label.draw()
        choose_rules_label = DisplayText(screen, (55 - 1 * i + 865, 22 - 1 * i),
                                         fontName="./data/UpheavalPro.ttf", fontSize=40,
                                         value='Выберите\nправила\nдля сплава',
                                         justified='center', textColor=color[i])

        choose_rules_label.draw()

    game_rules = RuleViewer(screen, 15, 105, 'pravila')
    splav_rules = RuleViewer(screen, 865, 105, 'dla_splav')
    text = [('Выберите', 'правила игры:'), ('123',)]
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()


        pygame.display.flip()
        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    rule_surf = pygame.display.set_mode(size)

    pygame.display.set_caption('хуядно')
    clock = pygame.time.Clock()
    rules_screen(screen)