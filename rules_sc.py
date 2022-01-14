import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygwidgets import DisplayText, InputText, CustomCheckBox

from load_image import load_image
from terminate import terminate


class RuleViewer:
    def __init__(self, screen, x, y, rule_folder):
        self.screen = screen
        bord_x, bord_y = x + 1, y + 1
        ins_x, ins_y = x + 3, y + 3
        w, h = 399, 599
        self.coords_stroke = (bord_x, bord_y, w, h)

        self.dis_text = []
        self.dis_but = []
        self.text_rect = (ins_x, ins_y, w - 4, h - 4)
        self.rule_txt_disp = DisplayText(screen, (ins_x + 10, ins_y + 10), width=w - 24, height=h - 94,
                                         fontName="./data/UpheavalPro.ttf", fontSize=16)
        self.rule_txt_disp.hide()
        self.dis_text.append(self.rule_txt_disp)
        back_btn = Button(screen, ins_x + 10, ins_y + self.rule_txt_disp.getRect()[3] + 15, 65, 65, borderThickness=3,
                          onClick=(lambda n=0: self.change_rules(screen, n)))
        back_btn._hidden = True
        self.dis_but.append(back_btn)
        self.rule_name_disp = DisplayText(screen, (back_btn.getX() + 70, back_btn.getY()+25), width=235, height=65,
                                          fontName="./data/UpheavalPro.ttf", fontSize=30, justified='center')
        self.rule_name_disp.hide()
        self.dis_text.append(self.rule_name_disp)

        self.r_n_d_loc = self.rule_name_disp.getX(), self.rule_name_disp.getY()
        forw_btn = Button(screen, back_btn.getX() + 70 + 240, back_btn.getY(), 65, 65, borderThickness=3,
                          onClick=(lambda n=1: self.change_rules(screen, n)))
        forw_btn._hidden = True
        self.dis_but.append(forw_btn)

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
        self.rule_name_disp.setLoc(self.r_n_d_loc)

    def disabled(self):
        for i in self.dis_text:
            i.hide()
        for i in self.dis_but:
            i._hidden = True

    def enabled(self):
        for i in self.dis_text:
            i.show()
        for i in self.dis_but:
            i._hidden = False

    def upgrade(self):
        self.enabled()
        pygame.draw.rect(self.screen, 'black', self.coords_stroke, 3)
        pygame.draw.rect(self.screen, 'white', self.text_rect)
        self.rule_name_disp.draw()
        self.rule_txt_disp.draw()


class Rules_Screen:
    def __init__(self, screen):
        self.screen = screen
        color = [(0, 0, 0), (75, 0, 130), (128, 0, 128)]
        self.text = []
        for i in range(3):
            choose_rules_label = DisplayText(screen, (70 - 1 * i, 22 - 1 * i),
                                             fontName="./data/UpheavalPro.ttf", fontSize=40,
                                             value='Выберите\nправила игры:',
                                             justified='center', textColor=color[i])
            self.text.append(choose_rules_label)
            choose_rules_label.hide()
            choose_players_label = DisplayText(screen, (70 - 1 * i + 420, 22 - 1 * i),
                                               fontName="./data/UpheavalPro.ttf", fontSize=40,
                                               value='Введите\nимена игроков:',
                                               justified='center', textColor=color[i])
            self.text.append(choose_players_label)
            choose_players_label.hide()
            choose_rules_label = DisplayText(screen, (90 - 1 * i + 865, 22 - 1 * i),
                                             fontName="./data/UpheavalPro.ttf", fontSize=40,
                                             value='Выберите\nправила\nдля сплава:',
                                             justified='center', textColor=color[i])
            self.text.append(choose_rules_label)
            choose_rules_label.hide()
        self.game_rules = RuleViewer(screen, 15, 105, 'pravila')
        self.splav_rules = RuleViewer(screen, 865, 105, 'dla_splav')
        self.game_rules.disabled()
        self.splav_rules.disabled()
        self.color_rect = ['red', 'yellow', (17, 113, 209), (23, 163, 5)]

        self.player_names = []
        self.checks = []
        for i in range(4):
            if i < 2:
                name_inp = InputText(screen, (490, 121 + 65 * i), value='', width=300,
                                     fontName="./data/UpheavalPro.ttf", fontSize=40, focusColor=(255, 255, 255),
                                     backgroundColor=(255, 255, 255), textColor='black')
            else:
                name_inp = InputText(screen, (490, 121 + 65 * i), value=f'Игрок {i + 1}', width=300,
                                     fontName="./data/UpheavalPro.ttf", fontSize=40, focusColor=(255, 255, 255),
                                     backgroundColor=(255, 255, 255), textColor='gray')
                name_inp.disable()
                check = CustomCheckBox(screen, (797, 108 + 65 * i), on='data/checked.png', off='data/unchecked.png',
                                       nickname=f'{i}', callBack=lambda n=i: self.change_status_player(n))
                self.checks.append(check)
                check.hide()
            self.player_names.append(name_inp)
            name_inp.hide()

        self.back = Button(screen, 500, 670, 100, 40, inactiveColour=(187, 143, 206), hoverColour=(165, 105, 189),
                        pressedColour=(125, 60, 152), text=' <-', font=pygame.font.Font("./data/UpheavalPro.ttf", 40),
                        onClick=lambda: self.disabled())
        self.click_back = False

    def change_status_player(self, n):
        n = int(n)
        if self.checks[n - 2].getValue():
            self.player_names[n].disable()
            self.player_names[n].textColor = 'grey'
            self.player_names[n].setValue(f'Игрок {n + 1}')

        else:
            self.player_names[n].enable()
            self.player_names[n].textColor = 'black'
            self.player_names[n].setValue('')

    def disabled(self):
        for i in self.text:
            i.hide()
        self.game_rules.disabled()
        self.splav_rules.disabled()
        for i in range(4):
            self.player_names[i].hide()
            if i < 2:
                self.checks[i].hide()
        self.click_back = True
        self.back._hidden = True

    def enabled(self):
        for i in self.text:
            i.show()
        self.game_rules.enabled()
        self.splav_rules.enabled()
        for i in range(4):
            self.player_names[i].show()
            if i < 2:
                self.checks[i].show()
        self.back._hidden = False

    def update(self, events):
        self.enabled()
        for event in events:
            self.checks[0].handleEvent(event)
            self.checks[1].handleEvent(event)
            for i in self.player_names:
                i.handleEvent(event)
        for i in range(4):
            if i < 2:
                self.screen.fill('white', (435, 106 + 65 * i, 360, 50))
            else:
                self.screen.fill('white', (435, 106 + 65 * i, 410, 50))
            self.screen.fill(self.color_rect[i], (435, 106 + 65 * i, 50, 50))
            if i > 1:
                pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 410, 50), width=3)
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 361, 50), width=3)
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 50, 50), width=3)
        for i in self.text:
            i.draw()
        for j in range(4):
            self.player_names[j].draw()
            if j < 2:
                self.checks[j].draw()
        self.game_rules.upgrade()
        self.splav_rules.upgrade()
        pygame_widgets.update(events)

        if self.click_back:
            self.click_back = False
            return 1


if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font("./data/UpheavalPro.ttf", 30)
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    rl_sc = Rules_Screen(screen)
    fon = pygame.transform.scale(load_image('./data/fon_main.jpg'), (WIDTH, HEIGHT))
    pygame.display.set_caption('хуядно')
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(fon, (0, 0))
        rl_sc.update(events)
        pygame.display.flip()
