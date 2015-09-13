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
    # doorOpt (stageId, condition = "on",pos[playerY,world_shift] )
    def __init__(self, x_pos, y_pos, game, doorOpt):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, (0,0,30,30), 0)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.stageId = doorOpt[0]
        try:
            self.condition = doorOpt[1]
        except:
            self.condition = "on"
        try:
            self.pos = [int(x) for x in doorOpt[2].split("/")]
        except:
            self.pos = []

    def check(self):
        if self.condition == "on":
            return True
        elif self.condition == "up":
            if self.game.k_up:
                self.game.player.change_y = 0
                return True
            else:
                return False
