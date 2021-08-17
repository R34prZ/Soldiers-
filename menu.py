import pygame
import utilities


class Menu:
    def __init__(self, main):
        self.main = main

        self.midscreenX, self.midscreenY = self.main.width // 2, self.main.height // 2

        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -50

    def draw_cursor(self):
        utilities.blit_text(self.main.display, '*',
                            self.cursor_rect.x, self.cursor_rect.y, font_size=32)


class MainMenu(Menu):
    def __init__(self, main):
        super().__init__(main)

        self.state = 'Start'

        self.startx, self.starty = self.midscreenX, self.midscreenY
        self.optionsx, self.optionsy = self.midscreenX, self.midscreenY + 30
        self.exitx, self.exity = self.midscreenX, self.midscreenY + 60

        self.cursor_rect.center = (self.startx + self.offset, self.starty)

    def buttons(self):
        utilities.text_button(self.main.display, 'Start Game',
                              self.startx, self.starty)

        utilities.text_button(self.main.display, 'Options',
                              self.optionsx, self.optionsy)

        utilities.text_button(self.main.display, 'Exit',
                              self.exitx, self.exity)

    def move_cursor(self):
        if self.main.keys['down_key']:
            if self.state == 'Start':
                self.cursor_rect.center = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.center = (
                    self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.center = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.main.keys['up_key']:
            if self.state == 'Start':
                self.cursor_rect.center = (
                    self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Options':
                self.cursor_rect.center = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Exit':
                self.cursor_rect.center = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

        elif self.main.keys['enter_key']:
            if self.state == 'Start':
                self.main.on_menu = False
                self.main.playing = True
            elif self.state == 'Options':
                self.main.on_optionsmenu = True
                self.main.on_menu = False
            elif self.state == 'Exit':
                self.main.game_running = False

    def update(self):
        self.buttons()
        self.draw_cursor()
        self.move_cursor()


class OptionsMenu(Menu):
    def __init__(self, main):
        super().__init__(main)

        self.state = 'Back'

        self.backx, self.backy = self.midscreenX, self.midscreenY + 60

        self.cursor_rect.center = (self.backx + self.offset, self.backy)

    def buttons(self):
        utilities.text_button(self.main.display, 'Back',
                              self.backx, self.backy)
        utilities.blit_text(self.main.display, 'Yet to be implemented!',
                            0, 0, self.main.width, self.main.height, center_x=1, center_y=1)

    def move_cursor(self):
        if self.main.keys['down_key']:
            if self.state == 'Back':
                pass
        elif self.main.keys['up_key']:
            if self.state == 'Back':
                pass
        elif self.main.keys['enter_key']:
            if self.state == 'Back':
                self.main.on_menu = True
                self.main.on_optionsmenu = False

    def update(self):
        self.buttons()
        self.draw_cursor()
        self.move_cursor()
