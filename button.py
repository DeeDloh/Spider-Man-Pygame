import pygame
from pygwidgets import TextButton, PygWidgetsButton
from pygwidgets import PygwidgetsFontManager

_PYGWIDGETS_FONT_MANAGER = PygwidgetsFontManager()


class SpiderButton(PygWidgetsButton):
    MINIMUM_WIDTH = 100

    def __init__(self, window, loc, text, width=None, height=40, textColor=(0, 0, 0),
                 upColor=(170, 170, 170), overColor=(210, 210, 210), downColor=(140, 140, 140),
                 fontName=None, fontSize=20, soundOnClick=None,
                 enterToActivate=False, callBack=None, nickname=None):

        # Create the button's Surface objects.
        if nickname is None:
            nickname = text  # use the text as the internal name
        text = ' ' + text + ' '  # add padding for drawn text
        self.textColor = textColor
        self.upColor = upColor
        self.overColor = overColor
        self.downColor = downColor

        self.font = _PYGWIDGETS_FONT_MANAGER.loadFont(fontName, fontSize)

        # create the text surface for up state of button (to get the size)
        textSurfaceUp = self.font.render(text, True, self.textColor, self.upColor)
        textRect = textSurfaceUp.get_rect()
        if width is None:
            # See if the text will fit inside the minimum width
            if textRect.width < TextButton.MINIMUM_WIDTH:
                width = TextButton.MINIMUM_WIDTH
            else:  # Make the width wide enough to handle all the text
                width = textRect.width

        buttonRect = pygame.Rect(loc[0], loc[1], width, height)
        w = buttonRect.width  # syntactic sugar
        h = buttonRect.height  # syntactic sugar
        size = buttonRect.size

        textRect.center = (int(w / 2), int(h / 2))

        # draw the up button
        surfaceUp = pygame.Surface(size)
        surfaceUp.fill(self.upColor)
        surfaceUp.blit(textSurfaceUp, textRect)

        # draw the down button
        surfaceDown = pygame.Surface(size)
        surfaceDown.fill(self.downColor)
        textSurfaceDown = self.font.render(text, True, self.textColor, self.downColor)
        textOffsetByOneRect = pygame.Rect(textRect.left + 1, textRect.top + 1, textRect.width,
                                          textRect.height)
        surfaceDown.blit(textSurfaceDown, textOffsetByOneRect)

        # draw the over button
        surfaceOver = pygame.Surface(size)
        surfaceOver.fill(self.overColor)
        textSurfaceOver = self.font.render(text, True, self.textColor, self.overColor)
        surfaceOver.blit(textSurfaceOver, textRect)

        # draw the disabled button
        surfaceDisabled = pygame.Surface(size)
        surfaceDisabled.fill((220, 220, 220))
        textSurfaceDisabled = self.font.render(text, True, (128, 128, 128), (220, 220, 220))
        surfaceDisabled.blit(textSurfaceDisabled, textRect)

        # call the PygWidgetsButton superclass to finish initialization

        super().__init__(window, loc, surfaceUp, surfaceOver, surfaceDown, surfaceDisabled,
                         buttonRect, soundOnClick, nickname, enterToActivate, callBack)
