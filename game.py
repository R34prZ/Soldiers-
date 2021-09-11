from time import time

import entities
import pygame
from utilities import *


class Game:

    def __init__(self, main: object) -> None:

        self.main = main

        self.enemy_quantity = 10

        # entities
        self.player = entities.Player(self.main.width // 2 - 32,
                                      self.main.height - 130, (64, 64))

        self.enemies = entities.Enemy.spawn_enemy(
            self.enemy_quantity, self.main.width)

        self.medipacks = entities.Packs.spawn_packs(
            entities.Medipack, 2, self.main.width, self.main.height)

        self.ammobags = entities.Packs.spawn_packs(
            entities.Ammobag, 1, self.main.width, self.main.height)

        # images
        self.background = pygame.image.load(
            './img/background.png').convert()
        self.weapon_frame = pygame.image.load(
            './img/weaponframe_assaultrifle.png').convert()
        self.bullet_frame = pygame.image.load(
            './img/bulletframe.png').convert()

        # delta time
        self.dt = 0
        self.first_time = time()

    def handle_events(self) -> None:
        '''Handle game events.'''

        if len(self.enemies) <= 0:
            self.enemies = entities.Enemy.spawn_enemy(
                self.enemy_quantity, self.main.width)

        if self.player.score % 200 == 0 and len(self.medipacks) == 0:
            self.medipacks = entities.Packs.spawn_packs(
                entities.Medipack, 2, self.main.width, self.main.height)

        if self.player.score % 50 == 0 and len(self.ammobags) == 0:
            self.ammobags = entities.Packs.spawn_packs(
                entities.Ammobag, 1, self.main.width, self.main.height)

        if (
            self.player.score % 10 == 0
            and self.player.score > 0
            and self.enemy_quantity < 20
        ):
            self.enemy_quantity += 1

        if self.player.lives == 0:
            self.main.on_gameover = True
            self.main.playing = False

    def draw(self) -> None:
        '''Render to the screen.'''
        self.main.display.blit(self.background, (0, 0))
        self.main.display.blit(self.weapon_frame, (10, self.main.height - 64))
        self.main.display.blit(pygame.transform.scale(self.bullet_frame, (56, 56)),
                               (self.main.width - 45, self.main.height - 60))

        blit_text(self.main.display, str(self.player.score), 0, 20,
                  self.main.width, self.main.height, font_size=32, color=(0, 0, 0), center_x=True)

        blit_text(
            self.main.display, f'FPS: {self.main.clock.get_fps(): .2f}', 20, 20, color=(0, 0, 0), font_size=12)

        blit_text(self.main.display, 'Ammo', self.main.width - 85,
                  self.main.height - 55, color=(0, 0, 0))

        pygame.draw.line(self.main.display, (0, 0, 0), (self.main.width - 90,
                                                        self.main.height - 35), (self.main.width - 30, self.main.height - 35), 1)

        blit_text(self.main.display, str(self.player.ammo), self.main.width -
                  75, self.main.height - 35, color=(0, 0, 0))

    def update_game(self) -> None:
        '''updates the game state.'''

        self.second_time = time()
        self.dt = self.second_time - self.first_time
        self.first_time = self.second_time

        self.player.update(self.main.display, self.main.width, self.dt)

        # updates medipacks and handle interactions with them
        for i, medipack in sorted(enumerate(self.medipacks), reverse=True):
            medipack.update(self.main.display)

            # player shots
            for z, bullet in sorted(enumerate(self.player.bullet_list), reverse=True):
                if bullet.bullet_rect.colliderect(medipack.medipack_rect):
                    self.medipacks.pop(i)
                    self.player.bullet_list.pop(z)

                    if self.player.lives < 10:
                        self.player.lives += 1

        # updates ammobags and handle interactions with them
        for i, ammobag in sorted(enumerate(self.ammobags), reverse=True):
            ammobag.update(self.main.display)

            # player shots
            for z, bullet in sorted(enumerate(self.player.bullet_list), reverse=True):
                if bullet.bullet_rect.colliderect(ammobag.ammobag_rect):
                    self.ammobags.pop(z)
                    self.player.bullet_list.pop(i)

                    self.player.ammo += 10

        # updates enemies and handle interactions with them
        for i, enemy in sorted(enumerate(self.enemies), reverse=True):
            enemy.update(self.main.display, self.main.height, self.dt)

            if enemy.y >= self.main.height:
                self.player.lives -= 1
                self.enemies.pop(i)

            # player shots
            for z, bullet in sorted(enumerate(self.player.bullet_list), reverse=True):
                if bullet.bullet_rect.colliderect(enemy.enemyrect):
                    self.enemies.pop(i)
                    self.player.bullet_list.pop(z)
                    self.player.score += 1

            # enemy shots
            for z, bullet in sorted(enumerate(enemy.bullet_list), reverse=True):
                if bullet.bullet_rect.colliderect(self.player.player_rect):
                    enemy.bullet_list.pop(z)
                    self.player.lives -= 1

    def update(self) -> None:
        ''' Main loop of the game. Handles events, updates the game and render to the main display.'''

        self.handle_events()

        self.draw()

        self.update_game()
