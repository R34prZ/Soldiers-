# Utilities module, supposed to contain functions, variables, and other things that can come handy

import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)


def blit_text(surface, text, x, y, displaywidth=None, displayheight=None, font='Arial', font_size=24, color=(255, 255, 255), center_x=False, center_y=False) -> None:
    """ Automatically blit text on the screen. """
    screen_font = pygame.font.SysFont(font, font_size)
    text_surface = screen_font.render(text, True, color)
    if center_x:
        x = (displaywidth // 2 - text_surface.get_width()/2)
    if center_y:
        y = (displayheight // 2 - text_surface.get_height()/2)

    surface.blit(text_surface, (x, y))


def animate(path, name, frames):

    animation_database = []

    n = 1
    for i in range(frames):
        image_id = name + str(n)
        image_path = path + image_id + '.png'
        image = pygame.image.load(image_path)  # .convert()
        image.set_colorkey((255, 255, 255))
        animation_database.append(image)

        n += 1

    return animation_database
