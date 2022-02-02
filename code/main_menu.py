import pygame
import pygame_widgets
from pygame_widgets.button import Button

from code.functions.terminate import terminate
from code.functions.load_image import load_image
from cards import Cards_Screen
from rules_sc import Rules_Screen
from leaderboard import LeadTable


class Menu:
    def __init__(self, screen, WIDTH=1280, HEIGHT=720):
        self.screen = screen
        self.fon = pygame.transform.scale(load_image('../data/images/fon_main.jpg'), (WIDTH, HEIGHT))
        self.fon_leaderboard = pygame.transform.scale(load_image('../data/images/fon_leaderboard.jpg'), (WIDTH, HEIGHT))
        text_but = ['Играть', 'Таблица лидеров', 'Карты', 'Выйти']
        func = [1, 2, 3, 4]
        font_all = pygame.font.Font("../data/UpheavalPro.ttf", 30)
        self.buttons = []
        self.cards = Cards_Screen(screen)
        self.rules = Rules_Screen(screen)
        self.lb = LeadTable(screen, self.fon_leaderboard)

        for i in range(4):
            # Этот класс кнопок в далнейшем больше не использовался из-за того что программа лагала из-за неё
            # В этом окне этот класс лагов не вызывает
            button = Button(screen, 490, 300 + i * 100, 300, 75, text=text_but[i], margin=20, font=font_all,
                            inactiveColour=(220, 20, 60), hoverColour=(65, 105, 225), pressedColour=(75, 0, 130),
                            onClick=(lambda n=func[i]: self.clicked_func(n))
                            )
            self.buttons.append(button)

        # Цвета для кнопок и текста
        self.color = [(0, 0, 0), (128, 0, 128), (178, 0, 178)]
        self.cords_1 = [(317, 102), (316, 101), (315, 100)]
        self.cords_2 = [(362, 202), (361, 201), (360, 200)]
        self.f1 = pygame.font.Font("../data/UpheavalPro.ttf", 70)

    def clicked_func(self, n):
        # Функция нажатия на кнопку в зависимоти от n

        # Скрываем кнопки при нажатии на любую из них
        self.disabled_button()

        if n == 4:
            # Выходим если была нажата кнопка ВЫХОД
            terminate()
        elif n == 3:
            # Показываем лобби с картами если была нажата кнопка КАРТЫ
            self.cards.enabled_button()
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        terminate()
                self.screen.blit(self.fon, (0, 0))
                if self.cards.update(events) == 1:
                    break
                pygame.display.flip()
            # Показываем кнопки меню если в лобби с картами нажали назад
            self.enabled_button()
        elif n == 2:
            # Показываем таблицу очков игроков если была нажата кнопка ТАБЛИЦА ЛИДЕРОВ
            self.lb.enabled_button()
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        terminate()
                self.screen.blit(self.fon_leaderboard, (0, 0))
                if self.lb.update(events) == 1:
                    break
                pygame.display.flip()
            # Показываем кнопки меню если в Таблице с очками нажали назад
            self.enabled_button()
        elif n == 1:
            # Показываем таблицу лобби с правилами если была нажата кнопка ИГРАТЬ
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        terminate()
                self.screen.blit(self.fon, (0, 0))
                if self.rules.update(events) == 1:
                    break
                pygame.display.flip()

    def disabled_button(self):
        # Скрытие кнопок меню
        for i in self.buttons:
            i._hidden = True

    def enabled_button(self):
        # Показ кнопок меню
        for i in self.buttons:
            i._hidden = False

    def update(self, events):
        self.enabled_button()
        for i in range(3):
            text1 = self.f1.render('Spider-man cards', True, self.color[i])
            self.screen.blit(text1, self.cords_1[i])
            text2 = self.f1.render('Pygame edition', True, self.color[i])
            self.screen.blit(text2, self.cords_2[i])
        # Для кнопок
        pygame_widgets.update(events)


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('../data/images/fon_main.jpg'), (WIDTH, HEIGHT))

    menu = Menu(screen)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(fon, (0, 0))
        menu.update(events)
        pygame.display.flip()