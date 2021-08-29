import pygame
import entities
from utilities import *


class Game:

    def __init__(self, main):

        self.main = main

        # entities
        self.player = entities.Player(self.main.width // 2 - 32,
                                      self.main.height - 130, (64, 64))

        self.enemies = entities.Enemy.spawn_enemy(10, self.main.width)

        self.medipacks = entities.Packs.spawn_packs(
            entities.Medipack, 2, self.main.width, self.main.height)

        self.ammobags = entities.Packs.spawn_packs(
            entities.Ammobag, 1, self.main.width, self.main.height)

        # images
        self.background = pygame.image.load('./img/background.png')
        self.weapon_frame = pygame.image.load(
            './img/weaponframe_assaultrifle.png')
        self.bullet_frame = pygame.image.load('./img/bulletframe.png')

    def handle_events(self):
        '''Handle game events.'''

        if len(self.enemies) <= 0:
            self.enemies = entities.Enemy.spawn_enemy(10, self.main.width)

        if self.player.score % 200 == 0 and len(self.medipacks) == 0:
            self.medipacks = entities.Packs.spawn_packs(
                entities.Medipack, 2, self.main.width, self.main.height)

        if self.player.score % 50 == 0 and len(self.ammobags) == 0:
            self.ammobags = entities.Packs.spawn_packs(
                entities.Ammobag, 1, self.main.width, self.main.height)

        if self.player.lives == 0:
            self.main.on_gameover = True
            self.main.playing = False

    def draw(self):
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

    def update_game(self):
        '''updates the game state.'''
        self.player.update(self.main.display, self.main.width)

        for enemy in self.enemies:  # updates enemies and handle interactions with them
            enemy.update(self.main.display, self.main.height)

            if enemy.y >= self.main.height:
                self.player.lives -= 1
                self.enemies.remove(enemy)

            for bullet in self.player.bullet_list:  # player shots
                if bullet.bullet_rect.colliderect(enemy.enemyrect):
                    self.enemies.remove(enemy)
                    self.player.bullet_list.remove(bullet)
                    self.player.score += 1

            for bullet in enemy.bullet_list:    # enemy shots
                if bullet.bullet_rect.colliderect(self.player.player_rect):
                    enemy.bullet_list.remove(bullet)
                    self.player.lives -= 1

        for medipack in self.medipacks:  # updates medipacks and handle interactions with them
            medipack.update(self.main.display)

            for bullet in self.player.bullet_list:  # player shots
                if bullet.bullet_rect.colliderect(medipack.medipack_rect):
                    self.medipacks.remove(medipack)
                    self.player.bullet_list.remove(bullet)

                    if self.player.lives < 10:
                        self.player.lives += 1

        for ammobag in self.ammobags:   # updates ammobags and handle interactions with them
            ammobag.update(self.main.display)

            for bullet in self.player.bullet_list:  # player shots
                if bullet.bullet_rect.colliderect(ammobag.ammobag_rect):
                    self.ammobags.remove(ammobag)
                    self.player.bullet_list.remove(bullet)

                    self.player.ammo += 10

    def update(self) -> None:
        ''' Main loop of the game. Handles events, updates the game and render to the main display.'''

        self.handle_events()

        self.draw()

        self.update_game()
