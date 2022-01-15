import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
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

        self.rule_name_disp.setLoc(self.r_n_d_loc)
        if '\n' in self.rule_name[self.disp_id]:
            self.rule_name_disp.moveY(-18)
        self.rule_name_disp.setValue(self.rule_name[self.disp_id])
        self.rule_txt_disp.setValue(self.rule_txt[self.disp_id])
        # screen.blit(screen, (0, 0))  нахуя я его тут написал?? я закомментил, ничего не поменялось о_0

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
            # ------------------------------------------------------------------------------------------------
            choose_players_label = DisplayText(screen, (70 - 1 * i + 420, 22 - 1 * i),
                                               fontName="./data/UpheavalPro.ttf", fontSize=40,
                                               value='Введите\nимена игроков:',
                                               justified='center', textColor=color[i])
            self.text.append(choose_players_label)
            choose_players_label.hide()
            # ------------------------------------------------------------------------------------------------
            choose_splav_label = DisplayText(screen, (90 - 1 * i + 865, 22 - 1 * i),
                                             fontName="./data/UpheavalPro.ttf", fontSize=40,
                                             value='Выберите\nправила\nдля сплава:',
                                             justified='center', textColor=color[i])
            self.text.append(choose_splav_label)
            choose_splav_label.hide()
            # ------------------------------------------------------------------------------------------------
            choose_cards_amount_label = DisplayText(screen, (70 - 1 * i + 368, 400 - 1 * i),
                                                fontName="./data/UpheavalPro.ttf", fontSize=40,
                                                value='Выберите,\nпо сколько карт\nраздавать игрокам:',
                                                justified='center', textColor=color[i])
            self.text.append(choose_cards_amount_label)
            choose_cards_amount_label.hide()

        self.game_rules = RuleViewer(screen, 15, 105, 'pravila')
        self.splav_rules = RuleViewer(screen, 865, 105, 'dla_splav')
        self.game_rules.disabled()
        self.splav_rules.disabled()
        self.color_rect = ['red', 'yellow', (17, 113, 209), (23, 163, 5)]

        self.player_names = []
        self.checks = []
        for i in range(4):
            name_inp = InputText(screen, (490, 121 + 65 * i), value=f'Игрок {i + 1}', width=300,
                                 fontName="./data/UpheavalPro.ttf", fontSize=40, focusColor=(255, 255, 255),
                                 backgroundColor=(255, 255, 255), textColor='gray')
            name_inp.disable()
            check = CustomCheckBox(screen, (797, 108 + 65 * i), nickname=f'{i}',
                                   callBack=lambda n=i: self.change_status_player(n),
                                   on='data/checked.png', off='data/unchecked.png',
                                   onDisabled='data/checked_disabled.png')
            self.checks.append(check)
            check.hide()
            self.player_names.append(name_inp)
            name_inp.hide()
        for i in range(2):  # здесь жлезобетонно включаются первые два (чек строку 165)
            self.checks[i].setValue(1)
            self.checks[i].disable()
            self.player_names[i].textColor = 'black'
            self.player_names[i].clearText()
            self.player_names[i].enable()

        self.card_amount_disp = DisplayText(screen, (618, 500), fontName="./data/UpheavalPro.ttf", fontSize=80)
        self.card_amount_slider = Slider(screen, 537, 570, 200, 20, colour=(197, 163, 207), handleColour=(128, 0, 128),
                                         min=1, max=6, initial=1)

        self.back = Button(screen, 505, 646, 125, 60, inactiveColour=(187, 143, 206), hoverColour=(165, 105, 189),
                        pressedColour=(125, 60, 152), text='назад', font=pygame.font.Font("./data/UpheavalPro.ttf", 30),
                        onClick=lambda: self.disabled(), borderThickness=3, inactiveBorderColour=(163, 60, 207),
                           hoverBorderColour=(163, 60, 207), pressedBorderColour=(163, 60, 207))
        self.play = Button(screen, 650, 646, 125, 60, inactiveColour=(206, 143, 143), hoverColour=(189, 105, 105),
                           pressedColour=(152, 60, 60), text='играть', font=pygame.font.Font("./data/UpheavalPro.ttf", 30),
                           onClick=lambda: self.start(), borderThickness=3, inactiveBorderColour=(207, 60, 60),
                           hoverBorderColour=(207, 60, 60), pressedBorderColour=(207, 60, 60))
        self.back._hidden = True
        self.cl_back = False

    def change_status_player(self, n):  # а это остается по сути только для вторых двух
        n = int(n)
        if self.checks[n].getValue():
            self.player_names[n].disable()
            self.player_names[n].textColor = 'grey'
            self.player_names[n].setValue(f'Игрок {n + 1}')

        else:
            self.player_names[n].enable()
            self.player_names[n].textColor = 'black'
            self.player_names[n].setValue('')
            self.player_names[n].giveFocus()

    def start(self):
        pass

    def disabled(self):
        for i in self.text:
            i.hide()
        self.game_rules.disabled()
        self.splav_rules.disabled()
        for i in range(4):
            self.player_names[i].hide()
            self.checks[i].hide()
        self.cl_back = True
        self.back._hidden = True

    def enabled(self):
        for i in self.text:
            i.show()
        self.game_rules.enabled()
        self.splav_rules.enabled()
        for i in range(4):
            self.player_names[i].show()
            self.checks[i].show()
        self.cl_back = False
        self.back._hidden = False

    def update(self, events):
        self.enabled()
        for event in events:
            for i in range(4):
                self.checks[i].handleEvent(event)
                self.player_names[i].handleEvent(event)
        for i in range(4):
            self.screen.fill('white', (435, 106 + 65 * i, 410, 50))
            self.screen.fill(self.color_rect[i], (435, 106 + 65 * i, 50, 50))
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 410, 50), width=3)
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 361, 50), width=3)
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 50, 50), width=3)

        for i in self.text:
            i.draw()
        for i in range(4):
            self.player_names[i].draw()
            self.checks[i].draw()

        self.screen.fill('white', (613, 495, 54, 50))
        pygame.draw.rect(self.screen, 'black', (613, 495, 54, 50), width=3)
        self.screen.blit(font.render('1', 1, 'black'), (507, 573))
        self.screen.blit(font.render('6', 1, 'black'), (756, 573))

        c_a = self.card_amount_slider.getValue()
        if c_a == 1:
            self.card_amount_disp.moveX(14)

        self.card_amount_disp.setValue(self.card_amount_slider.getValue())
        self.card_amount_disp.draw()
        self.card_amount_slider.draw()
        self.card_amount_disp.setLoc((618, 500))

        self.game_rules.upgrade()
        self.splav_rules.upgrade()
        pygame_widgets.update(events)

        if self.cl_back:
            self.cl_back = False
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
