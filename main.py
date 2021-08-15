import pygame
import sys
import entities
from pygame.locals import *
from utilities import *

# Game made by R34prZ#6633
# https://github.com/R34prZ

pygame.init()


class Menu:
    NAME = 'Allied vs Axis'
    VERSION = '0.3'

    def __init__(self, width, height):

        # display settings
        self.width = width
        self.height = height

        pygame.display.set_caption(
            '{} | version {}'.format(Menu.NAME, Menu.VERSION))

        self.SCREEN_SIZE = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        self.clock = pygame.time.Clock()
        self.FPS = 60


class Main(Menu):

    def __init__(self):

        # entities
        self.player = entities.Player(self.width // 2 - 32,
                                      self.height - 130, (64, 64))

        self.enemies = entities.Enemy.spawn_enemy(10, self.width)

        self.medipacks = entities.Packs.spawn_packs(
            entities.Medipack, 2, self.width, self.height)

        self.ammobags = entities.Packs.spawn_packs(
            entities.Ammobag, 1, self.width, self.height)

        # images
        self.background = pygame.image.load('./img/background.png')
        self.weapon_frame = pygame.image.load(
            './img/weaponframe_assaultrifle.png')
        self.bullet_frame = pygame.image.load('./img/bulletframe.png')

    def update(self) -> None:
        ''' Main loop of the game. Handles events, updates the game and render to the screen.'''

        # render
        self.screen.fill(WHITE)

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.weapon_frame, (10, self.height - 64))
        self.screen.blit(pygame.transform.scale(self.bullet_frame, (56, 56)),
                         (self.width - 45, self.height - 60))

        blit_text(self.screen, str(self.player.score), 0, 20,
                  self.width, self.height, font_size=48, color=(0, 0, 0), center_x=True)

        blit_text(
            self.screen, f'FPS: {self.clock.get_fps(): .2f}', 20, 20, color=(0, 0, 0), font_size=12)

        blit_text(self.screen, 'Ammo', self.width - 80,
                  self.height - 55, color=(0, 0, 0), font_size=18)

        pygame.draw.line(self.screen, (0, 0, 0), (self.width - 90,
                                                  self.height - 35), (self.width - 30, self.height - 35), 1)

        blit_text(self.screen, str(self.player.ammo), self.width -
                  75, self.height - 35, color=(0, 0, 0), font_size=24)

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_a or event.key == K_LEFT:
                    self.player.movements['left'] = True
                elif event.key == K_d or event.key == K_RIGHT:
                    self.player.movements['right'] = True
                if self.player.ammo > 0:
                    if event.key == K_SPACE:
                        self.player.movements['shooting'] = True

            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_LEFT:
                    self.player.movements['left'] = False
                elif event.key == K_d or event.key == K_RIGHT:
                    self.player.movements['right'] = False
                elif event.key == K_SPACE:
                    self.player.movements['shooting'] = False

        if len(self.enemies) <= 0:
            self.enemies = entities.Enemy.spawn_enemy(10, self.width)

        if self.player.score % 200 == 0 and len(self.medipacks) == 0:
            self.medipacks = entities.Packs.spawn_packs(
                entities.Medipack, 2, self.width, self.height)

        if self.player.score % 50 == 0 and len(self.ammobags) == 0:
            self.ammobags = entities.Packs.spawn_packs(
                entities.Ammobag, 1, self.width, self.height)

        # update game state
        self.player.update(self.screen, self.width)

        for medipack in self.medipacks:
            medipack.update(self.screen)

            for bullet in self.player.bullet_list:
                if bullet.bullet_rect.colliderect(medipack.medipack_rect):
                    self.medipacks.remove(medipack)
                    self.player.bullet_list.remove(bullet)

                    if self.player.lives < 10:
                        self.player.lives += 1

        for ammobag in self.ammobags:
            ammobag.update(self.screen)

            for bullet in self.player.bullet_list:
                if bullet.bullet_rect.colliderect(ammobag.ammobag_rect):
                    self.ammobags.remove(ammobag)
                    self.player.bullet_list.remove(bullet)

                    self.player.ammo += 10

        for enemy in self.enemies:
            enemy.update(self.screen, self.height)

            if enemy.y >= self.height:
                self.player.lives -= 1
                self.enemies.remove(enemy)

            for bullet in self.player.bullet_list:
                if bullet.bullet_rect.colliderect(enemy.enemyrect):
                    self.enemies.remove(enemy)
                    self.player.bullet_list.remove(bullet)
                    self.player.score += 1

            for bullet in enemy.bullet_list:
                if bullet.bullet_rect.colliderect(self.player.player_rect):
                    enemy.bullet_list.remove(bullet)
                    self.player.lives -= 1

        self.clock.tick(self.FPS)
        pygame.display.flip()


if __name__ == '__main__':
    game = Main(400, 600)

    while True:
        game.update()
