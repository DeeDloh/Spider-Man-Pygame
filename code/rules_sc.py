import os
import sqlite3

import pygame
import pygame_widgets
import random
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygwidgets import DisplayText, InputText, CustomCheckBox, PygWidgetsButton

from classes.buttons import SpiderButton, SpiderButtonImage
from code.functions.load_image import load_image
from code.functions.terminate import terminate
from pole import Pole


# файл с экраном подготовки к игре
class RuleViewer:  # класс карусели с выбором правил (вынесен отдельно, потому что таких карусели две)
    def __init__(self, screen, x, y, rule_folder):
        self.screen = screen
        font = "../data/UpheavalPro.ttf"
        bord_x, bord_y = x + 1, y + 1
        ins_x, ins_y = x + 3, y + 3
        w, h = 399, 599
        self.coords_stroke = (bord_x, bord_y, w, h)

        self.dis_text = []
        self.dis_but = []
        self.text_rect = (ins_x, ins_y, w - 4, h - 4)
        # поле для вывода текста правил
        self.rule_txt_disp = DisplayText(screen, (ins_x + 10, ins_y + 10), width=w - 24, height=h - 94,
                                         fontName=font, fontSize=16)
        self.rule_txt_disp.hide()
        self.dis_text.append(self.rule_txt_disp)

        # кнопка для переключения на прошлое правило
        back_btn = Button(screen, ins_x + 10, ins_y + self.rule_txt_disp.getRect()[3] + 15, 65, 65, borderThickness=3,
                          onClick=(lambda n=0: self.change_rules(screen, n)))
        back_btn._hidden = True
        self.dis_but.append(back_btn)

        # поле для отображения названия правила
        self.rule_name_disp = DisplayText(screen, (back_btn.getX() + 70, back_btn.getY()+25), width=235, height=65,
                                          fontName=font, fontSize=30, justified='center')
        self.rule_name_disp.hide()
        self.dis_text.append(self.rule_name_disp)

        self.r_n_d_loc = self.rule_name_disp.getX(), self.rule_name_disp.getY()
        # кнопка для переключения на предыдущее правило
        forw_btn = Button(screen, back_btn.getX() + 70 + 240, back_btn.getY(), 65, 65, borderThickness=3,
                          onClick=(lambda n=1: self.change_rules(screen, n)))
        forw_btn._hidden = True
        self.dis_but.append(forw_btn)

        back_btn.setImage(load_image('../data/images/back.png', scale=(65, 65)))
        forw_btn.setImage(load_image('../data/images/forward.png', scale=(65, 65)))

        # загружаем файлы и их названия из той директории, название которой было передано в кач-ве аргумента при
        # инициализации класса (проще говоря выбираем, будут в этой карусели отобр. правила игры или правила для сплава)
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

    def change_rules(self, screen, direction):  # переключение правил в карусели
        self.disp_id = self.disp_id + 1 if direction else self.disp_id - 1
        if self.disp_id < 0:
            self.disp_id = self.disp_len
        elif self.disp_id > self.disp_len:
            self.disp_id = 0

        screen.fill('white', self.text_rect)

        self.rule_name_disp.setLoc(self.r_n_d_loc)  # название правила немного сдвигается вниз, если занимает больше
        if '\n' in self.rule_name[self.disp_id]:    # одной строки
            self.rule_name_disp.moveY(-18)
        self.rule_name_disp.setValue(self.rule_name[self.disp_id])
        self.rule_txt_disp.setValue(self.rule_txt[self.disp_id])

    def disabled(self):  # скрытие всей карусели
        for i in self.dis_text:
            i.hide()
        for i in self.dis_but:
            i._hidden = True

    def enabled(self):  # отображение всей карусели
        for i in self.dis_text:
            i.show()
        for i in self.dis_but:
            i._hidden = False

    def update(self):  # обновление всей карусели (вызывается в методе обновления всего окна)
        pygame.draw.rect(self.screen, 'black', self.coords_stroke, 3)
        pygame.draw.rect(self.screen, 'white', self.text_rect)
        self.rule_name_disp.draw()
        self.rule_txt_disp.draw()


class Rules_Screen:  # класс окна подготовки к игре
    def __init__(self, screen):
        self.screen = screen
        font = "../data/UpheavalPro.ttf"
        color = [(0, 0, 0), (128, 0, 128), (178, 0, 178)]
        self.text = []
        self.clock = pygame.time.Clock()
        self.st_card = pygame.transform.scale(load_image('../data/kartinki cards/0.jpg'), (126, 190))
        for i in range(3):  # создание надписей, предлагающих игроку настроить свою игру (выполняется три раза,
            # по скольку текст состоит из трёх слоёв)
            choose_rules_label = DisplayText(screen, (70 - 1 * i, 22 - 1 * i),
                                             fontName=font, fontSize=40, value='Выберите\nправила игры:',
                                             justified='center', textColor=color[i])
            self.text.append(choose_rules_label)
            choose_rules_label.hide()
            # ------------------------------------------------------------------------------------------------
            choose_players_label = DisplayText(screen, (70 - 1 * i + 420, 22 - 1 * i),
                                               fontName=font, fontSize=40, value='Введите\nимена игроков:',
                                               justified='center', textColor=color[i])
            self.text.append(choose_players_label)
            choose_players_label.hide()
            # ------------------------------------------------------------------------------------------------
            choose_splav_label = DisplayText(screen, (90 - 1 * i + 865, 22 - 1 * i),
                                             fontName=font, fontSize=40, value='Выберите\nправила\nдля сплава:',
                                             justified='center', textColor=color[i])
            self.text.append(choose_splav_label)
            choose_splav_label.hide()
            # ------------------------------------------------------------------------------------------------
            choose_cards_amount_label = DisplayText(screen, (70 - 1 * i + 368, 400 - 1 * i),
                                                    fontName=font, fontSize=40,
                                                    value='Выберите,\nпо сколько карт\nраздавать игрокам:',
                                                    justified='center', textColor=color[i])
            self.text.append(choose_cards_amount_label)
            choose_cards_amount_label.hide()

        self.game_rules = RuleViewer(screen, 15, 105, '../rules')  # создание каруселей с правилами
        self.splav_rules = RuleViewer(screen, 865, 105, '../splav_rules')
        self.game_rules.disabled()
        self.splav_rules.disabled()
        self.color_rect = ['red', 'yellow', (17, 113, 209), (23, 163, 5)]

        self.player_names = []
        self.checks = []
        for i in range(4):  # создание полей для ввода имён игроков
            name_inp = InputText(screen, (490, 121 + 65 * i), value=f'Игрок {i + 1}', width=300,
                                 fontName=font, fontSize=40, focusColor=(255, 255, 255),
                                 backgroundColor=(255, 255, 255), textColor='gray')
            name_inp.disable()
            check = CustomCheckBox(screen, (797, 108 + 65 * i), nickname=f'{i}',
                                   callBack=lambda n=i: self.change_status_player(n),
                                   on='../data/images/checked.png', off='../data/images/unchecked.png',
                                   onDisabled='../data/images/checked_disabled.png')
            self.checks.append(check)
            check.hide()
            self.player_names.append(name_inp)
            name_inp.hide()
        for i in range(2):              # включение двух полей для ввода имен игроков по умолчанию (не может быть меньше
            self.checks[i].setValue(1)  # двух игроков)
            self.checks[i].disable()
            self.player_names[i].textColor = 'black'
            self.player_names[i].clearText()
            self.player_names[i].enable()

        # создание интерфейса для выбора количества карт, которое будет раздаваться каждому игроку
        self.card_amount_disp = DisplayText(screen, (618, 500), fontName=font, fontSize=80)
        self.card_amount_slider = Slider(screen, 537, 570, 200, 20, colour=(197, 163, 207), handleColour=(128, 0, 128),
                                         min=1, max=6, initial=1)

        # создание кнопок назад, играть и информация
        self.back = SpiderButton(screen, (505, 646), 'назад', width=125, height=60, upColor=(187, 143, 206),
                                 overColor=(165, 105, 189), downColor=(125, 60, 152), fontName=font, fontSize=30,
                                 borderThickness=3, borderColour=(163, 60, 207))
        self.play = SpiderButton(screen, (650, 646), 'играть', width=125, height=60, upColor=(206, 143, 143),
                                 overColor=(189, 105, 105), downColor=(152, 60, 60), fontName=font, fontSize=30,
                                 borderThickness=3, borderColour=(207, 60, 60))
        self.info = SpiderButtonImage(screen, (1218, 30), '../data/images/info.png', (49, 49),
                                      over='../data/images/info_hover.png', down='../data/images/info_hover.png')
        with open('../data/history_splav.txt', encoding='utf-8') as hist_splav:
            hist_splav = hist_splav.readlines()
        self.info_field = DisplayText(screen, (818, 44), width=380, height=580, fontName=font, fontSize=16,
                                      backgroundColor=(197, 163, 207), value=hist_splav)
        self.font = pygame.font.Font("../data/UpheavalPro.ttf", 30)
        self.play.hide()
        self.card_amount_slider._hidden = True
        self.back.hide()
        self.info.hide()
        self.info_field.hide()
        self.cl_back = False

    def change_status_player(self, n):  # включение/отключения поля для ввода имени игркока при помощи чекбокса
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

    def start(self):  # начало игры с применением выбранных настроек
        id = list(range(1, 143))
        random.shuffle(id)
        names = []
        players = []
        k = self.card_amount_slider.getValue()
        for i in range(2):  # сохранение имен игроков (если поле игкрока включено, но имя оставлено пустым, то он
            if ''.join(self.player_names[i].getValue().split()) == '':  # сохраняется как "Игрок n")
                names.append(f'Игрок {i + 1}')
            else:
                names.append(self.player_names[i].getValue())
        for i in range(3, 5):
            if self.checks[i - 1].getValue() == 1:
                if ''.join(self.player_names[i - 1].getValue().split()) == '':
                    names.append(f'Игрок {i}')
                else:
                    names.append(self.player_names[i].getValue())
        for i in range(len(names)):
            players.append((id[(i * k):((i + 1) * k)], names[i]))

        # создание экземпляра класса Pole и старт игры
        pole = Pole(self.screen, players, self.game_rules.rule_name_disp.getValue())
        pole.enabled()
        fon = load_image('../data/images/fon_pole.jpg')
        table = pygame.Surface((980, 320), pygame.SRCALPHA)
        table.fill((0, 0, 0, 0))
        pygame.draw.ellipse(table, (0, 0, 0, 160), (0, 0, 980, 320))
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    terminate()

            self.screen.blit(fon, (0, 0))
            self.screen.blit(table, (150, 200))
            winner = pole.update(events)
            if type(winner) is list:
                break
            pygame.display.flip()
            self.clock.tick(65)

        # завершение игры (отображение побетиля и кнопок выйти и поиграть ещё)
        self.final = pygame.Surface((1280, 720), pygame.SRCALPHA)
        self.final.fill((34, 34, 34, 152))
        buttons = []
        button = SpiderButton(self.screen, (490, 255), 'Поиграть ещё', width=300, height=100, upColor=(187, 143, 206),
                              overColor=(165, 105, 189), downColor=(125, 60, 152), fontName="../data/UpheavalPro.ttf",
                              fontSize=30, borderThickness=3, borderColour=(163, 60, 207))
        buttons.append(button)
        button = SpiderButton(self.screen, (490, 365), 'выход', width=300, height=100, upColor=(187, 143, 206),
                              overColor=(165, 105, 189), downColor=(125, 60, 152), fontName="../data/UpheavalPro.ttf",
                              fontSize=30, borderThickness=3, borderColour=(163, 60, 207))
        buttons.append(button)
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    terminate()
                if buttons[0].handleEvent(event):
                    run = False
                if buttons[1].handleEvent(event):
                    terminate()
            self.screen.blit(fon, (0, 0))
            self.screen.blit(self.st_card, (577, 525))
            self.screen.blit(self.final, (0, 0))

            text = self.font.render(f'Выиграл: {winner[0].nickname}', True, 'white')
            self.screen.blit(text, (490, 230))
            for i in buttons:
                i.draw()
            pygame.display.flip()
            self.clock.tick(65)
        # запись/обновление победителя результата в таблице лидеров
        con = sqlite3.connect("../data/databases/leaderboard.db")
        cur = con.cursor()
        if winner != []:
            print(winner)
            name = ''.join(winner[0].nickname.split())
            if name != 'Игрок1' and name != 'Игрок2' and name != 'Игрок3' and name != 'Игрок4'\
                    and name != '':
                info = cur.execute('SELECT * FROM name_score WHERE name=?', (winner[0].nickname,))
                if info.fetchone() is None:
                    cur.execute(f'INSERT INTO name_score(name, score) VALUES("{winner[0].nickname}", 30)')
                    con.commit()
                else:
                    k = cur.execute('SELECT score FROM name_score WHERE name=?', (winner[0].nickname,)).fetchall()[0][0]
                    cur.execute(f"UPDATE name_score SET score = {k + 30} WHERE name = '{winner[0].nickname}'")
                    con.commit()
        # запись/обновление проигравшех результата в таблице лидеров
        for i in range(len(self.player_names)):
            if self.checks[i].getValue() == 1:
                name = ''.join(self.player_names[i].getValue().split())
                if name != 'Игрок1' and name != 'Игрок2' and name != 'Игрок3' and name != 'Игрок4'\
                        and name != '' and name != ''.join(winner[0].nickname.split()):
                    d = self.player_names[i].getValue()
                    info = cur.execute('SELECT * FROM name_score WHERE name=?', (d,))
                    if info.fetchone() is None:
                        cur.execute(f'INSERT INTO name_score(name, score) VALUES("{d}", 0)')
                        con.commit()
                    else:
                        k = cur.execute('SELECT score FROM name_score WHERE name=?', (d,)).fetchall()[0][0]
                        if k != 0:
                            cur.execute(f"UPDATE name_score SET score = {k - 15} WHERE name = '{d}'")
                            con.commit()

    def disabled(self):  # скрытие всего интерфейса окна подготовки к игре
        for i in self.text:
            i.hide()
        self.game_rules.disabled()
        self.splav_rules.disabled()
        for i in range(4):
            self.player_names[i].hide()
            self.checks[i].hide()
        self.play.hide()
        self.back.hide()
        self.info.hide()
        self.info_field.hide()
        self.card_amount_slider._hidden = True
        self.cl_back = True

    def enabled(self):  # отображение всего интерфейса окна подготовки к игре
        for i in self.text:
            i.show()
        self.game_rules.enabled()
        self.splav_rules.enabled()
        for i in range(4):
            self.player_names[i].show()
            self.checks[i].show()
        self.play.show()
        self.back.show()
        self.info.show()
        self.card_amount_slider._hidden = False
        self.cl_back = False

    def update(self, events):  # обновление окна подготовки к игре (вызывается в цикле событий в файле main_menu.py)
        if self.cl_back:
            self.cl_back = False
            return 1
        self.enabled()
        for event in events:
            self.info.handleEvent(event)
            if self.back.handleEvent(event):
                self.disabled()
            if self.play.handleEvent(event):
                self.start()
            for i in range(4):
                self.checks[i].handleEvent(event)
                self.player_names[i].handleEvent(event)
        for i in range(4):
            self.screen.fill('white', (435, 106 + 65 * i, 410, 50))
            self.screen.fill(self.color_rect[i], (435, 106 + 65 * i, 50, 50))
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 410, 50), width=3)
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 361, 50), width=3)
            pygame.draw.rect(self.screen, 'black', (435, 106 + 65 * i, 50, 50), width=3)

        # проверка введенных никнеймов на уникальность (нельзя начать игру, если ники игроков в одной игре совпадают)
        unique_check = list(filter(None, [i.getValue() for i in self.player_names]))
        if len(unique_check) != len(set(unique_check)):
            self.play.hide()
            self.play.disable()
        else:
            self.play.show()
            self.play.enable()
        for i in self.text:
            i.draw()
        for i in range(4):
            self.player_names[i].draw()
            self.checks[i].draw()

        self.back.draw()
        self.play.draw()
        self.info.draw()

        self.screen.fill('white', (613, 495, 54, 50))
        pygame.draw.rect(self.screen, 'black', (613, 495, 54, 50), width=3)
        self.screen.blit(pygame.font.Font("../data/UpheavalPro.ttf", 30).render('1', True, 'black'), (507, 573))
        self.screen.blit(pygame.font.Font("../data/UpheavalPro.ttf", 30).render('6', True, 'black'), (756, 573))

        c_a = self.card_amount_slider.getValue()
        if c_a == 1:
            self.card_amount_disp.moveX(14)

        self.card_amount_disp.setValue(self.card_amount_slider.getValue())
        self.card_amount_disp.draw()
        self.card_amount_slider.draw()
        self.card_amount_disp.setLoc((618, 500))

        self.game_rules.update()
        self.splav_rules.update()
        # отображение истории сплава при навеведении курсора на кнопку информации
        if self.info.state == PygWidgetsButton.STATE_OVER or self.info.state == PygWidgetsButton.STATE_ARMED:
            self.screen.fill((197, 163, 207), (808, 34, 400, 590))
            self.info_field.show()
            self.info_field.draw()
            pygame.draw.rect(self.screen, 'black', (808, 34, 400, 590), width=3)
        else:
            self.info_field.hide()
            self.info_field.draw()
        pygame_widgets.update(events)


if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font("../data/UpheavalPro.ttf", 30)
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    rl_sc = Rules_Screen(screen)
    fon = pygame.transform.scale(load_image('../data/images/fon_main.jpg'), (WIDTH, HEIGHT))
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(fon, (0, 0))
        rl_sc.update(events)
        pygame.display.flip()
