# Things related to game entities

from random import randint

import pygame
from utilities import BLACK
from utilities import WHITE
from utilities import animate


class Shoot:
    def __init__(self, playerx: int, playery: int, playerlen: tuple,
                 width: int, height: int, speed: int) -> None:

        # basic information
        self.width = width
        self.height = height
        self.bullet_speed = speed

        self.bullet_rect = pygame.Rect(
            playerx - (self.width - playerlen[0] // 2) - 4, playery, self.width, self.height)

    def update(self, up: bool = True, down: bool = False) -> None:
        if up:
            self.bullet_rect.y -= self.bullet_speed
        elif down:
            self.bullet_rect.y += self.bullet_speed


class Player:
    def __init__(self, x: int, y: int, length: tuple) -> None:
        # position and basic stuff
        self.x = x
        self.y = y
        self.length = length
        self.player_vel = 300
        self.player_rect = pygame.Rect(
            self.x, self.y, self.length[0], self.length[1])

        # important information
        self.score = 0
        self.lives = 10
        self.ammo = 100

        self.movements = {
            'left': False,
            'right': False,
            'shooting': False
        }

        # shot related
        self.shoot_delay = 60 // 6
        self.shoot_timer = 0

        self.bullet_list = []

        # animation related
        self.player_img = pygame.image.load(
            './img/animations/player/idle.png')

        self.frame = 0

        self.animations = {}
        self.animations['left'] = animate(
            './img/animations/player/', 'move', 4)
        self.animations['right'] = [pygame.transform.flip(
            image, True, False) for image in self.animations['left']]
        self.animations['idle'] = [self.player_img]

        self.state = 'idle'

    def move(self, dt: float) -> None:
        self.keyboard = pygame.key.get_pressed()
        if self.keyboard[pygame.K_a] or self.keyboard[pygame.K_LEFT]:
            self.movements['left'] = True
        if self.keyboard[pygame.K_d] or self.keyboard[pygame.K_RIGHT]:
            self.movements['right'] = True
        if self.keyboard[pygame.K_SPACE] and self.ammo > 0:
            self.movements['shooting'] = True

        if self.movements['left']:
            self.x -= self.player_vel * dt
            self.state = 'left'
            self.frame += 0.1

        elif self.movements['right']:
            self.x += self.player_vel * dt
            self.state = 'right'
            self.frame += 0.2

        else:
            self.state = 'idle'

    def reset_keys(self) -> None:
        self.movements = {
            'left': False,
            'right': False,
            'shooting': False
        }

    def create_bullet(self) -> Shoot:
        self.ammo -= 1
        return Shoot(self.x + 8, self.y, self.length, 6, 15, 25)

    def update(self, display: pygame.Surface, width: int, dt: float):
        # player movement
        self.move(dt)

        if self.x >= width - self.player_rect.width:
            self.x = width - self.player_rect.width
        elif self.x <= 0:
            self.x = 0

        # shot related
        if self.score % 10 == 0 and self.score > 0:  # makes the player earn 5 ammo and 1 score point every 10 score
            self.ammo += 5
            self.score += 1

        if self.movements['shooting']:  # shoot logic

            self.shoot_timer += 1

            if self.shoot_timer > self.shoot_delay:
                self.shoot_timer = 0

            if self.shoot_timer == self.shoot_delay:
                self.bullet_list.append(self.create_bullet())

        for bullet in self.bullet_list:  # render and update bullets
            pygame.draw.rect(display, (20, 50, 85), bullet.bullet_rect)
            bullet.update()

            if bullet.bullet_rect.y <= 0:
                self.bullet_list.remove(bullet)

        # player life bar
        lifebar_bg = pygame.Surface((64, 5))
        lifebar_bg.set_alpha(80)
        lifebar = pygame.Rect(self.x, self.y + 80, self.lives * 6.4, 5)

        lifebar_bg.fill(BLACK)
        display.blit(lifebar_bg, lifebar)
        pygame.draw.rect(display, WHITE, lifebar)

        self.lives = max(self.lives, 0)
        # animation related
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        actual_animation = self.animations[self.state][int(self.frame)]
        self.player_rect = pygame.Rect(
            self.x, self.y, self.length[0], self.length[1])
        display.blit(pygame.transform.scale(
            actual_animation, (64, 64)), self.player_rect)

        self.reset_keys()


class Enemy:
    def __init__(self, x: int, y: int) -> None:

        # position and basic stuff
        self.x = x
        self.y = y
        self.vel = 50
        self.len = (64, 64)
        self.enemyrect = pygame.Rect(self.x, self.y, self.len[0], self.len[1])

        # shot related
        self.shoot_delay = 60 * 2
        self.shoot_timer = 0

        self.bullet_list = []

        # animation related
        self.animations = {}

        self.animations['move'] = animate(
            './img/animations/enemy/', 'move', 4)

        self.state = 'move'
        self.frame = 0

    @classmethod
    def spawn(cls, quantity: int, screen_width: int) -> list:

        enemy_list = {}

        for _ in range(quantity):
            xpos = randint(10, screen_width - 64)
            ypos = randint(-50, 10)
            key = (xpos, ypos)
            if key not in enemy_list:
                enemy_list[key] = (cls(*key))

        return list(enemy_list.values())

    def create_bullet(self) -> Shoot:
        return Shoot(self.x, self.y + self.len[1], self.len, 5, 15, 25)

    def move(self, dt: float) -> None:
        self.y += self.vel * dt
        self.frame += 0.1

    def update(self, display: pygame.Surface, height: int, dt: float) -> None:

        # enemy movement
        self.move(dt)

        # shot related
        self.shoot_timer += 1

        if self.shoot_timer > self.shoot_delay:
            self.shoot_timer = 0

        if self.shoot_timer == self.shoot_delay:
            self.bullet_list.append(self.create_bullet())

        for bullet in self.bullet_list:  # draws and updates bullets
            pygame.draw.rect(display, (255, 255, 0), bullet.bullet_rect)
            bullet.update(up=False, down=True)

            if bullet.bullet_rect.y >= height:
                self.bullet_list.remove(bullet)

        # animation related
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        actual_animation = self.animations[self.state][int(self.frame)]
        self.enemyrect = pygame.Rect(self.x, self.y, 64, 64)
        display.blit(pygame.transform.flip(pygame.transform.scale(
            actual_animation, (64, 64)), False, True), self.enemyrect)


class Pack:
    @classmethod
    def spawn(cls, amount: int, displaywidth: int, displayheight: int):
        pack_list = []

        for _ in range(amount):
            x = randint(20, displaywidth - 64)
            y = randint(20, displayheight - 200)

            pack_list.append(cls(x, y, 64, 64))

        return pack_list


class Medipack(Pack):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.medipack_rect = pygame.Rect(
            self.x, self.y, self.width, self.height)

        # animation
        self.animations = {}

        self.frames = 0
        self.state = 'entrance'

        self.medipack_image = pygame.image.load(
            './img/animations/packs/medipack.png')

        self.animations['idle'] = [self.medipack_image]

        self.animations['entrance'] = animate(
            './img/animations/packs/entrance_anim/', 'entrance', 16)

    def update(self, display: pygame.Surface) -> None:

        self.frames += 0.1

        if self.frames >= len(self.animations[self.state]):
            self.state = 'idle'
            self.frames = 0

        actual_animation = self.animations[self.state][int(self.frames)]

        display.blit(pygame.transform.scale(
            actual_animation, (64, 64)), (self.x, self.y))


class Ammobag(Pack):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.ammobag_rect = pygame.Rect(
            self.x, self.y, self.width, self.height)

        # animation
        self.animations = {}

        self.frames = 0
        self.state = 'entrance'

        self.medipack_image = pygame.image.load(
            './img/animations/packs/ammobag.png')

        self.animations['idle'] = [self.medipack_image]

        self.animations['entrance'] = animate(
            './img/animations/packs/entrance_anim/', 'entrance', 16)

    def update(self, display: pygame.Surface) -> None:

        self.frames += 0.1

        if self.frames >= len(self.animations[self.state]):
            self.state = 'idle'
            self.frames = 0

        actual_animation = self.animations[self.state][int(self.frames)]

        display.blit(pygame.transform.scale(
            actual_animation, (64, 64)), (self.x, self.y))
