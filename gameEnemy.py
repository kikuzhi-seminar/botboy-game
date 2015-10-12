import pygame
from util import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.makeModel()

        self.change_x = 0
        self.change_y = 0
        self.stage = None
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.isEnemy = True

    def makeModel(self):
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def getBullet(self):
        self.kill()

    def update(self):
        pass

    def move(self):
        pass

class EasyEnemy(Enemy):
    def move(self):
        self.rect.x -= 3

class Boss(Enemy):
    def __init__(self, game, x_pos, y_pos, hp, img):
        self.game = game
        self.hp = hp
        self.img = img
        self.change_y = -10
        self.change_x = 0
        super().__init__(x_pos, y_pos)

    def makeModel(self):
        self.left_image = pygame.image.load("data/" + self.img )
        self.left_image.set_colorkey(-1, pygame.RLEACCEL)
        self.right_image = pygame.transform.flip(self.left_image, True, False)
        self.image = self.left_image
        self.rect = self.image.get_rect()

    def getBullet(self):
        self.hp -= 1

    def update(self):
        self.jump()

        if self.hp <= 0:
            self.kill()
            self.game.finish = True
            self.game.player.died()

    def jump(self):
        platform_hit_list = pygame.sprite.spritecollide(self, self.game.stage.stage_block_list, False)
        if len(platform_hit_list) > 0:
            self.change_y = -5
        else:
            self.change_y += .35

        self.rect.y += self.change_y