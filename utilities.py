# Utilities module, supposed to contain functions, variables, and other things that can come handy
import json
from os.path import join as path_join

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


def blit_text(surface: pygame.Surface, text: str, x: int, y: int,
              displaywidth: int = None, displayheight: int = None,
              font: str = './font/Early GameBoy.ttf', font_size: int = 16,
              color: tuple = (255, 255, 255),
              center_x: bool = False, center_y: bool = False) -> None:
    """ Automatically blit text on the screen. """

    screen_font = pygame.font.Font(font, font_size)
    text_surface = screen_font.render(text, True, color)

    if center_x:
        x = (displaywidth // 2 - text_surface.get_width()/2)
    if center_y:
        y = (displayheight // 2 - text_surface.get_height()/2)

    surface.blit(text_surface, (x, y))


def text_button(surface: pygame.Surface, text: str, x: int, y: int,
                font: str = './font/Early GameBoy.ttf', font_size: int = 16,
                color: tuple = (255, 255, 255)) -> None:
    """ Blits a text button to the screen """

    button_font = pygame.font.Font(font, font_size)
    text_surface = button_font.render(text, True, color)
    button_rect = text_surface.get_rect(center=(x, y))

    surface.blit(text_surface, button_rect)


def animate(path: str, name: str, frames: int):
    '''Loads sprites for animation. Must be stores on a Animation Dictionary to be loaded based on state.'''

    animation_database = []

    for n in range(frames):
        image_name = f'{name}{n+1}.png'
        image_path = path_join(path, image_name)
        image = pygame.image.load(image_path).convert_alpha()
        image.set_colorkey((255, 255, 255))
        animation_database.append(image)

    return animation_database


def save_game(save_file: str, data: dict) -> None:
    with open(save_file, 'w') as save:
        json.dump(data, save, indent=4, sort_keys=True)


def load_game(save_file: str) -> dict:
    with open(save_file, 'r') as save:
        data = json.load(save)

    return data
