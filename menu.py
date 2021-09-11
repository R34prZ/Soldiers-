import pygame
import utilities


class Menu:
    def __init__(self, main: object) -> None:
        self.main = main

        self.midscreenX, self.midscreenY = self.main.width // 2, self.main.height // 2

        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self) -> None:
        utilities.blit_text(self.main.display, '*',
                            self.cursor_rect.x, self.cursor_rect.y)


class MainMenu(Menu):
    def __init__(self, main: object) -> None:
        super().__init__(main)

        self.state = 'Start'

        self.startx, self.starty = self.midscreenX, self.midscreenY
        self.optionsx, self.optionsy = self.midscreenX, self.midscreenY + 30
        self.controlsx, self.controlsy = self.midscreenX, self.midscreenY + 60
        self.exitx, self.exity = self.midscreenX, self.midscreenY + 90

        self.cursor_rect.center = (self.startx + self.offset, self.starty)

    def render_buttons(self) -> None:
        utilities.text_button(self.main.display, 'Start Game',
                              self.startx, self.starty)

        utilities.text_button(self.main.display, 'Options',
                              self.optionsx, self.optionsy)

        utilities.text_button(self.main.display, 'Controls',
                              self.controlsx, self.controlsy)

        utilities.text_button(self.main.display, 'Exit',
                              self.exitx, self.exity)

    def move_cursor(self) -> None:
        if self.main.keys['down_key']:
            if self.state == 'Start':
                self.cursor_rect.center = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.center = (
                    self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
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
            elif self.state == 'Controls':
                self.cursor_rect.center = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.center = (
                    self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'

        elif self.main.keys['enter_key']:
            if self.state == 'Start':
                self.main.on_menu = False
                self.main.playing = True
            elif self.state == 'Options':
                self.main.on_menu = False
                self.main.on_optionsmenu = True
            elif self.state == 'Controls':
                self.main.on_menu = False
                self.main.on_controlsmenu = True
            elif self.state == 'Exit':
                self.main.game_running = False

    def update(self) -> None:
        self.render_buttons()
        self.draw_cursor()
        self.move_cursor()


class OptionsMenu(Menu):
    def __init__(self, main: object) -> None:
        super().__init__(main)

        self.state = 'Back'

        self.backx, self.backy = self.midscreenX, self.midscreenY + 60

        self.cursor_rect.center = (self.backx + self.offset, self.backy)

    def render_buttons(self) -> None:
        utilities.text_button(self.main.display, 'Back',
                              self.backx, self.backy)

    def draw_menu(self) -> None:
        utilities.blit_text(self.main.display, 'Yet to be implemented!',
                            0, 0, self.main.width, self.main.height, center_x=1, center_y=1)

    def move_cursor(self) -> None:
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

    def update(self) -> None:
        self.render_buttons()
        self.draw_menu()
        self.draw_cursor()
        self.move_cursor()


class ControlsMenu(Menu):
    def __init__(self, main: object) -> None:
        super().__init__(main)

        self.state = 'Back'

        self.backx, self.backy = self.midscreenX, self.midscreenY + 60

        self.cursor_rect.center = (self.backx + self.offset, self.backy)

        # images
        self.main_keys_frame = pygame.image.load(
            './img/menus/main_keys_frame.png').convert()
        self.main_keys_frame.set_colorkey(utilities.BLACK)
        self.main_keys_frame_rect = self.main_keys_frame.get_rect()

        self.secondary_keys_frame = pygame.image.load(
            './img/menus/secondary_keys_frame.png').convert()
        self.secondary_keys_frame.set_colorkey(utilities.BLACK)
        self.secondary_keys_frame_rect = self.secondary_keys_frame.get_rect()

        self.spacebar_key_frame = pygame.image.load(
            './img/menus/key_frame_spacebar.png').convert()
        self.spacebar_key_frame.set_colorkey(utilities.BLACK)
        self.spacebar_key_frame_rect = self.spacebar_key_frame.get_rect()

    def render_buttons(self) -> None:
        utilities.text_button(self.main.display, 'Back',
                              self.backx, self.backy)

    def draw_menu(self) -> None:
        self.main.display.blit(self.main_keys_frame,
                               ((self.midscreenX - self.main_keys_frame_rect.width // 2) - 32, self.midscreenY - 40))

        self.main.display.blit(self.secondary_keys_frame,
                               ((self.midscreenX - self.secondary_keys_frame_rect.width // 2) + 32, self.midscreenY - 40))

        self.main.display.blit(self.spacebar_key_frame,
                               (self.midscreenX - self.spacebar_key_frame_rect.width // 2, self.midscreenY - 40))

        utilities.blit_text(self.main.display, 'Move and Shoot:', 0,
                            self.midscreenY - 65, self.main.width, center_x=1)

    def move_cursor(self) -> None:
        if self.main.keys['down_key']:
            if self.state == 'Back':
                pass
        elif self.main.keys['up_key']:
            if self.state == 'Back':
                pass
        elif self.main.keys['enter_key']:
            if self.state == 'Back':
                self.main.on_menu = True
                self.main.on_controlsmenu = False

    def update(self) -> None:
        self.render_buttons()
        self.draw_menu()
        self.draw_cursor()
        self.move_cursor()


class GameOverMenu(Menu):
    def __init__(self, main: object) -> None:
        super().__init__(main)

        self.state = 'Restart'

        self.restartx, self.restarty = self.midscreenX, self.midscreenY
        self.mainmenux, self.mainmenuy = self.midscreenX, self.midscreenY + 30

        # images
        self.dead_soldier_sprite = pygame.image.load(
            './img/menus/deadsoldier.png').convert()
        self.dead_soldier_sprite.set_colorkey(utilities.BLACK)
        self.dead_soldier_sprite_rect = self.dead_soldier_sprite.get_rect()

        self.cursor_rect.center = (self.restartx + self.offset, self.restarty)

    def render_buttons(self):
        utilities.text_button(self.main.display, 'Restart',
                              self.restartx, self.restarty)

        utilities.text_button(self.main.display, 'Main Menu',
                              self.mainmenux, self.mainmenuy)

    def draw_menu(self) -> None:
        self.main.display.blit(self.dead_soldier_sprite, (self.midscreenX -
                                                          self.dead_soldier_sprite_rect.width // 2, self.midscreenY - 180))

        utilities.blit_text(
            self.main.display, 'You died soldier.', 0, self.midscreenY - 100, self.main.width, center_x=1)

        utilities.blit_text(
            self.main.display, 'Try Again!', 0, self.midscreenY - 80, self.main.width, center_x=1)

        utilities.blit_text(self.main.display,
                            f'SCORE: {self.main.main_game.player.score}', 0, self.midscreenY + 100, self.main.width, center_x=1, font_size=18)

    def move_cursor(self) -> None:
        if self.main.keys['down_key']:
            if self.state == 'Restart':
                self.cursor_rect.center = (
                    self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Mainmenu'
            elif self.state == 'Mainmenu':
                self.cursor_rect.center = (
                    self.restartx + self.offset, self.restarty)
                self.state = 'Restart'
        elif self.main.keys['up_key']:
            if self.state == 'Restart':
                self.cursor_rect.center = (
                    self.mainmenux + self.offset, self.mainmenuy)
                self.state = 'Mainmenu'
            elif self.state == 'Mainmenu':
                self.cursor_rect.center = (
                    self.restartx + self.offset, self.restarty)
                self.state = 'Restart'
        elif self.main.keys['enter_key']:
            if self.state == 'Restart':
                self.main.on_gameover = False
                self.main.playing = True
                self.main.restart_game()
            elif self.state == 'Mainmenu':
                self.main.on_gameover = False
                self.main.on_menu = True
                self.main.restart_game()

    def update(self) -> None:

        self.render_buttons()
        self.draw_menu()
        self.draw_cursor()
        self.move_cursor()
