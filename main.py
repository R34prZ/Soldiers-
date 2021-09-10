import pygame
import sys
import menu
#import game
from pygame.locals import *
from utilities import *
from game import Game

# Game made by R34prZ#6633
# https://github.com/R34prZ

# Font by: https://www.dafont.com/pt/early-gameboy.font

pygame.init()


class Main:

    NAME = 'Allied vs Axis'
    VERSION = '0.5.7'

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

        # game windows (based on states)
        self.main_menu = menu.MainMenu(self)
        self.options_menu = menu.OptionsMenu(self)
        self.controls_menu = menu.ControlsMenu(self)
        self.main_game = Game(self)
        self.gameover_menu = menu.GameOverMenu(self)

        # game states
        self.game_running = True
        self.on_menu = True
        self.on_optionsmenu = False
        self.on_controlsmenu = False
        self.playing = False
        self.on_gameover = False

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

    def restart_game(self):
        ''' Restarts the main game state to be able to run it again after dying. '''
        self.main_game = Game(self)

    def update(self):

        while self.game_running:

            self.display.fill(BLACK)

            self.check_event()

            if self.on_menu:
                self.main_menu.update()
            elif self.on_optionsmenu:
                self.options_menu.update()
            elif self.on_controlsmenu:
                self.controls_menu.update()
            elif self.playing:
                self.main_game.update()

                self.on_menu = False
                self.on_optionsmenu = False
                self.on_controlsmenu = False
            elif self.on_gameover:
                self.gameover_menu.update()

            self.reset_keys()

            self.screen.blit(self.display, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':

    # define main object
    game = Main(400, 600)
    # update the entire game
    game.update()
