import pygame
from util import *

class StageObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.makeModel()

    def makeModel(self):
        self.image = pygame.Surface([30, 30])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

class Coin(StageObject):
    def __init__(self, x_pos ,y_pos, game):
        # pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos
        super().__init__()


    def makeModel(self):
        self.image = pygame.Surface([20,20])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, CBROWN, (10, 10), 10, 0)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 9, 0)
        pygame.draw.rect(self.image, GRAY, (9,4,2,12), 0)
        self.image.set_colorkey(self.image.get_at((0,0)), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos + 15, self.y_pos +15)

    def action(self):
        self.game.score += 1

class SavePoint(Coin):
    def makeModel(self):
        super().makeModel()
        pygame.draw.circle(self.image, BLUE, (10, 10), 10, 0)

    def action(self):
        stage = self.game.stage
        playerY = self.game.player.rect.y
        playerX = self.game.player.rect.x
        self.game.currentSavePoint = [stage.stageId,stage.world_shift, playerX, playerY]

class Block(StageObject):
    def __init__(self, x_pos ,y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        super().__init__()

    def makeModel(self):
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, DBROWN, (0,0,30,30), 0)
        pygame.draw.rect(self.image, BROWN, (1,1,28,28), 0)
        pygame.draw.circle(self.image, DBROWN, (5, 5), 8, 0)
        pygame.draw.circle(self.image, DBROWN, (8, 15), 4, 0)
        pygame.draw.circle(self.image, DBROWN, (25, 12), 5, 0)
        pygame.draw.circle(self.image, DBROWN, (20, 22), 6, 0)
        pygame.draw.circle(self.image, DBROWN, (8, 25), 5, 0)
        pygame.draw.rect(self.image, GREEN, (0,0,30,5), 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

class Door(StageObject):
    # opt (stageId, condition = "on",pos[playerY,world_shift] )
    def __init__(self, x_pos, y_pos, game, opt):
        self.game = game
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.opt = opt
        super().__init__()

    def makeModel(self):
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, CBROWN, (0,0,30,30), 0)
        pygame.draw.rect(self.image, WBROWN, (3,3,10,24), 0)
        pygame.draw.rect(self.image, WBROWN, (17,3,10,24), 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.stageId = self.opt[0]
        try:
            self.condition = self.opt[1]
        except:
            self.condition = "on"
        try:
            self.pos = [int(x) for x in self.opt[2].split("/")]
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

class Bullet(StageObject):
    def __init__(self,whose, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.whose = whose
        super().__init__()

    def makeModel(self):
        self.image = pygame.Surface([20,20])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, BLACK, (10, 10), 10, 0)
        pygame.draw.circle(self.image, GRAY, (10, 10), 9, 0)
        pygame.draw.rect(self.image, GRAY, (9,4,2,12), 0)
        self.image.set_colorkey(self.image.get_at((0,0)), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos + 15, self.y_pos +15)

    def action(self):
        self.rect.x -= 2
