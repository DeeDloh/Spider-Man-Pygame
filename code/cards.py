import pygame
import pygame_widgets
from pygame_widgets.slider import Slider

from code.functions.load_image import load_image
from classes.buttons import SpiderButton


class Cards_Screen:
    def __init__(self, screen):
        self.screen = screen

        self.do_cards()
        self.click_back = False

        # Создаем слайдер и скрываем его до момента пока не нужно будет поле с картами
        self.slider = Slider(screen, 150, 680, 1100, 20, min=0, max=14560, step=1, handleRadius=20,
                             colour=(142, 68, 173), handleColour=(91, 44, 111))
        self.slider.setValue(0)
        self.slider._hidden = True

        # Кнопка назад
        self.button_1 = SpiderButton(screen, (10, 670), '<-', width=100, height=40, upColor=(187, 143, 206),
                                     overColor=(165, 105, 189), downColor=(125, 60, 152),
                                     fontName="../data/UpheavalPro.ttf", fontSize=40)
        self.button_1.hide()

    def clicked_back(self):
        # Если нажали назад, то меняем флаг
        self.click_back = True

    def disabled_button(self):
        # Скрываем кнопку и слайдер
        self.slider._hidden = True
        self.button_1.hide()

    def enabled_button(self):
        # Показываем кнопку и слайдер
        self.slider._hidden = False
        self.button_1.show()

    def do_cards(self):
        # Функция которая устанавливает на координаты картинки с картами
        self.cards = []
        for i in range(1, 143):
            card = pygame.transform.scale(load_image(f'../data/kartinki cards/{i}.jpg'), (213, 320))
            self.cards.append(card)

    def update(self, events):
        self.enabled_button()
        if self.click_back:
            # Выходим из экрана с картаи если нажали назад
            self.click_back = False
            self.disabled_button()
            return 1
        sl = self.slider.getValue()
        for cd in range(len(self.cards)):
            # Меняем координаты в зависимости от позиции слайдера
            if cd < 71:
                self.screen.blit(self.cards[cd], (10 + 223 * cd - sl, 10))
            else:
                self.screen.blit(self.cards[cd], (10 + 223 * (cd - 71) - sl, 340))

        for event in events:

            if self.button_1.handleEvent(event):
                self.clicked_back()
                # Проверяет нажатие и наведение на кнопку
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Прокручивание слайдера колесиком мыши
                if event.button == 5:
                    if sl <= 14337:
                        self.slider.setValue(sl + 223)
                    else:
                        self.slider.setValue(14560)
                elif event.button == 4:
                    if sl >= 223:
                        self.slider.setValue(sl - 223)
                    else:
                        self.slider.setValue(0)
        self.button_1.draw()
        self.slider.draw()


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    size = WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ладно')
    clock = pygame.time.Clock()
