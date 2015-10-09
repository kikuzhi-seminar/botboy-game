import pygame
from util import *
from gameStage import *

class Player(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        width = 40
        height = 60
        self.game = game
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.stage = None
        self.score = 0
        self.isEnemy = False

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= SCREEN_HEIGHT + self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT + self.rect.height * 2

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.stage.stage_block_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

    def getBullet(self):
        self.died()

    def died(self):
        if self.game.finish == True:
            self.game.gameover = True
        else:
            self.game.died = True
            self.stop()
            stage = self.game.stage
            playerY = self.rect.y
            playerX = self.rect.x
            self.game.currentDeathPoint = [stage.stageId, stage.world_shift, playerX, playerY]
            stage.shift_world( -1 * self.game.currentDeathPoint[1] )
            stage.world_shift = 0

class Botboy(Player):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.left_botboy_image = pygame.image.load("data/botboy.png")
        self.left_botboy_image.set_colorkey(-1, pygame.RLEACCEL)
        self.right_botboy_image = pygame.transform.flip(self.left_botboy_image, True, False)
        self.image = self.right_botboy_image
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.stage = None
        self.isRight = True
        self.isEnemy = False

    def go_left(self):
        super().go_left()
        self.image = self.left_botboy_image
        self.isRight = False

    def go_right(self):
        super().go_right()
        self.image = self.right_botboy_image
        self.isRight = True
