import pygame
from util import *

class Mob(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.stage = None
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        pass

    def move(self):
        pass

class Easy_mob(Mob):
    def __init__(self,width,height):
        super().__init__(width,height)
    def move(self):
        self.rect.x -= 3
