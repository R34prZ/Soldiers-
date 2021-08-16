import pygame
import utilities


class Menu:
    def __init__(self, main):
        self.main = main

        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -50

    def draw_cursor(self):
        utilities.blit_text(self.main.display, '*',
                            self.cursor_rect.x, self.cursor_rect.y, font_size=32)


class MainMenu(Menu):
    def __init__(self, main):
        super().__init__(main)
        self.main = main

        self.state = 'Start'

        self.midscreenX, self.midscreenY = self.main.width // 2, self.main.height // 2
        self.startx, self.starty = self.midscreenX, self.midscreenY
        self.exitx, self.exity = self.midscreenX, self.midscreenY + 30

        self.cursor_rect.center = (self.startx + self.offset, self.starty)

    def buttons(self):
        utilities.text_button(self.main.display, 'Start Game',
                              self.startx, self.starty)

        utilities.text_button(self.main.display, 'Exit',
                              self.exitx, self.exity)

    def move_cursor(self):
        if self.main.keys['down_key']:
            if self.state == 'Start':
                self.cursor_rect.center = (
                    self.exitx + self.offset, self.exity)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.center = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.main.keys['up_key']:
            if self.state == 'Start':
                self.cursor_rect.center = (
                    self.exitx + self.offset, self.exity)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.center = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.main.keys['enter_key']:
            if self.state == 'Start':
                self.main.on_menu = False
                self.main.game_running = True

    def update(self):
        self.buttons()
        self.draw_cursor()
        self.move_cursor()
