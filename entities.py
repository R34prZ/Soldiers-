# Things related to game entities

import pygame
from random import randrange
from utilities import animate, WHITE, BLACK


class Shoot:
    def __init__(self, playerx, playery, playerlen: tuple, width, height, speed):

        # basic information
        self.width = width
        self.height = height
        self.bullet_speed = speed

        self.bullet_rect = pygame.Rect(
            playerx - (self.width - playerlen[0] // 2) - 4, playery, self.width, self.height)

    def update(self, up=True, down=False):

        if up:
            self.bullet_rect.y -= self.bullet_speed
        elif down:
            self.bullet_rect.y += self.bullet_speed


class Player:
    def __init__(self, x, y, length: tuple):

        # position and basic stuff
        self.x = x
        self.y = y
        self.length = length
        self.player_vel = 5
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

        # life bar
        self.life_bar_frame = pygame.image.load('./img/lifebarframe.png')
        self.life_bar_full = pygame.image.load('./img/lifebar_full.png')

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

    def move(self):

        self.keyboard = pygame.key.get_pressed()
        if self.keyboard[pygame.K_a] or self.keyboard[pygame.K_LEFT]:
            self.movements['left'] = True
        if self.keyboard[pygame.K_d] or self.keyboard[pygame.K_RIGHT]:
            self.movements['right'] = True
        if self.keyboard[pygame.K_SPACE]:
            if self.ammo > 0:
                self.movements['shooting'] = True

        print(self.movements)

        if self.movements['left']:
            self.x -= self.player_vel
            self.state = 'left'
            self.frame += 0.1

        elif self.movements['right']:
            self.x += self.player_vel
            self.state = 'right'
            self.frame += 0.2

        else:
            self.state = 'idle'

    def reset_keys(self):
        self.movements = {
            'left': False,
            'right': False,
            'shooting': False
        }

    def create_bullet(self):
        self.ammo -= 1
        return Shoot(self.x + 8, self.y, self.length, 6, 15, 25)

    def update(self, display, width):

        # player life bar
        lifebar_bg = pygame.Surface((64, 5))
        lifebar_bg.set_alpha(80)
        lifebar = pygame.Rect(self.x, self.y + 80, self.lives * 6.4, 5)

        lifebar_bg.fill(BLACK)
        display.blit(lifebar_bg, lifebar)
        pygame.draw.rect(display, WHITE, lifebar)

        # shot related
        self.move()

        if self.score % 10 == 0 and self.score > 0:  # makes the player earn 10 ammo and 1 score point every 10 score
            self.ammo += 10
            self.score += 1

        if self.movements['shooting']:

            self.shoot_timer += 1

            if self.shoot_timer > self.shoot_delay:
                self.shoot_timer = 0

            if self.shoot_timer == self.shoot_delay:
                self.bullet_list.append(self.create_bullet())

        for bullet in self.bullet_list:
            pygame.draw.rect(display, (20, 50, 85), bullet.bullet_rect)
            bullet.update()

            if bullet.bullet_rect.y <= 0:
                self.bullet_list.remove(bullet)

        # animation related
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

        actual_animation = self.animations[self.state][int(self.frame)]
        self.player_rect = pygame.Rect(
            self.x, self.y, self.length[0], self.length[1])
        display.blit(pygame.transform.scale(
            actual_animation, (64, 64)), self.player_rect)

        # player movement
        if self.x >= width - self.player_rect.width:
            self.x = width - self.player_rect.width
        elif self.x <= 0:
            self.x = 0

        self.reset_keys()


class Enemy:
    def __init__(self, x, y):

        # position and basic stuff
        self.x = x
        self.y = y
        self.vel = 1
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

    def spawn_enemy(quantity, screen_width) -> list:

        enemy_list = []

        for i in range(quantity):
            xpos = randrange(10, screen_width, 50)
            ypos = randrange(-50, 10, 50)

            enemy_list.append(Enemy(xpos, ypos))

        return enemy_list

    def create_bullet(self):
        return Shoot(self.x, self.y + self.len[1], self.len, 5, 15, 25)

    def move(self):
        self.y += self.vel
        self.frame += 0.1

    def update(self, display, height):

        # shot related
        self.shoot_timer += 1

        if self.shoot_timer > self.shoot_delay:
            self.shoot_timer = 0

        if self.shoot_timer == self.shoot_delay:
            self.bullet_list.append(self.create_bullet())

        for bullet in self.bullet_list:
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

        # enemy movement
        self.move()


class Packs:
    def spawn_packs(Type, amount, displaywidth, displayheight):
        pack_list = []

        for i in range(amount):
            x = randrange(20, displaywidth - 20)
            y = randrange(20, displayheight - 200)

            pack_list.append(Type(x, y, 64, 64))

        return pack_list


class Medipack:
    def __init__(self, x, y, width, height):

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

    def update(self, display):

        self.frames += 0.1

        if self.frames >= len(self.animations[self.state]):
            self.state = 'idle'
            self.frames = 0

        actual_animation = self.animations[self.state][int(self.frames)]

        display.blit(pygame.transform.scale(
            actual_animation, (64, 64)), (self.x, self.y))


class Ammobag:
    def __init__(self, x, y, width, height):

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

    def update(self, display):

        self.frames += 0.1

        if self.frames >= len(self.animations[self.state]):
            self.state = 'idle'
            self.frames = 0

        actual_animation = self.animations[self.state][int(self.frames)]

        display.blit(pygame.transform.scale(
            actual_animation, (64, 64)), (self.x, self.y))
