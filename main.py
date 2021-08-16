import pygame
import sys
import menu
import game
from pygame.locals import *
from utilities import *

# Game made by R34prZ#6633
# https://github.com/R34prZ

pygame.init()


class Main:

    NAME = 'Allied vs Axis'
    VERSION = '0.5'

    def __init__(self, width, height):

        # screen information
        self.width = width
        self.height = height

        pygame.display.set_caption(
            '{} | version {}'.format(Main.NAME, Main.VERSION))

        self.SCREEN_SIZE = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.display = pygame.Surface(self.SCREEN_SIZE)

        # clock information
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # keys
        self.keys = {
            'up_key': False,
            'down_key': False,
            'enter_key': False,
            'return_key': False
        }

        # other
        self.main_menu = menu.MainMenu(self)
        self.main_game = game.Game(self)

        self.on_menu = True
        self.game_running = False

    def check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.keys['up_key'] = True
                elif event.key == K_DOWN:
                    self.keys['down_key'] = True
                elif event.key == K_RETURN:
                    self.keys['enter_key'] = True
                elif event.key == K_BACKSPACE or event.key == K_ESCAPE:
                    self.keys['return_key'] == True

    def reset_keys(self):
        self.keys = {
            'up_key': False,
            'down_key': False,
            'enter_key': False,
            'return_key': False
        }

    def update(self):

        self.display.fill(BLACK)

        self.check_event()

        if self.on_menu:
            self.main_menu.update()
        elif self.game_running:
            self.main_game.update()

        self.reset_keys()

        self.screen.blit(self.display, (0, 0))
        self.clock.tick(self.FPS)
        pygame.display.flip()


if __name__ == '__main__':
    game = Main(400, 600)

    while True:
        game.update()
