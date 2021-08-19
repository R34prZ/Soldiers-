# Utilities module, supposed to contain functions, variables, and other things that can come handy

import pygame
import json

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


def blit_text(surface, text, x, y, displaywidth=None, displayheight=None, font='./font/Early GameBoy.ttf', font_size=16, color=(255, 255, 255), center_x=False, center_y=False) -> None:
    """ Automatically blit text on the screen. """

    screen_font = pygame.font.Font(font, font_size)
    text_surface = screen_font.render(text, True, color)

    if center_x:
        x = (displaywidth // 2 - text_surface.get_width()/2)
    if center_y:
        y = (displayheight // 2 - text_surface.get_height()/2)

    surface.blit(text_surface, (x, y))


def text_button(surface, text, x, y, font='./font/Early GameBoy.ttf', font_size=16, color=(255, 255, 255)):
    """ Blits a text button to the screen """

    button_font = pygame.font.Font(font, font_size)
    text_surface = button_font.render(text, True, color)
    button_rect = text_surface.get_rect(center=(x, y))

    surface.blit(text_surface, button_rect)


def animate(path, name, frames):
    '''Loads sprites for animation. Must be stores on a Animation Dictionary to be loaded based on state.'''

    animation_database = []

    n = 1
    for i in range(frames):
        image_id = name + str(n)
        image_path = path + image_id + '.png'
        image = pygame.image.load(image_path).convert_alpha()
        image.set_colorkey((255, 255, 255))
        animation_database.append(image)

        n += 1

    return animation_database


def save_game(save_file, data):
    with open(save_file, 'w') as save:
        json.dump(data, save)


def load_game(save_file):
    with open(save_file, 'r') as save:
        data = json.load(save)

    return data
