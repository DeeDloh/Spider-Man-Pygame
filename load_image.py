import pygame


def load_image(name, colorkey=None, scale=(0, 0)):
    fullname = name
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if scale != (0, 0):
        image = pygame.transform.scale(image, scale)
    return image