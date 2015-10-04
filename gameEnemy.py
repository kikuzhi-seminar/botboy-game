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

    def makeModel(self):
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def move(self):
        pass

class EasyEnemy(Enemy):
    def move(self):
        self.rect.x -= 3

class Boss(Enemy):
    def __init__(self, x_pos, y_pos, hp, img):
        self.hp = hp
        self.img = img
        super().__init__(x_pos, y_pos)

    def makeModel(self):
        self.left_image = pygame.image.load("data/" + self.img + ".png")
        self.left_image.set_colorkey(-1, pygame.RLEACCEL)
        self.right_image = pygame.transform.flip(self.left_image, True, False)
        self.image = self.left_image
        self.rect = self.image.get_rect()

    def update(self):
        pass
