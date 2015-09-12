import pygame
from util import *

class StageObject(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

class Coin(StageObject):
    def __init__(self, x_pos ,y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20,20])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10, 0)
        self.image.set_colorkey(self.image.get_at((0,0)), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos + 15,y_pos +15)

class Block(StageObject):
    def __init__(self,x_pos,y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, GREEN, (0,0,30,30), 0)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

class Door(StageObject):
    def __init__(self, x_pos, y_pos, doorOpt):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, (0,0,30,30), 0)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.stageId = doorOpt[0]

    def check(self):
        return True

    def nextStage(self):
        return self.stageId
