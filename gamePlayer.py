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

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.stage.stage_block_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.stage.stage_block_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
        item_hit_list = pygame.sprite.spritecollide(self, self.stage.item_list,True)
        for item in item_hit_list:
            self.score += 1
            print(self.score)
        # 敵との判定の実装
        enemy_hit_list = pygame.sprite.spritecollide(self, self.stage.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.rect.y >= self.game.player.rect.y + self.game.player.rect.height - self.game.player.change_y:
                enemy.kill()
            else:
                self.game.gameover = True
        # Doorオブジェクトのワープの実装
        door_hit_list = pygame.sprite.spritecollide(self, self.stage.door_list, False)
        if len(door_hit_list) > 0 and door_hit_list[0].check():
            self.rect.x = 120
            self.game.current_stage = Stage(self, door_hit_list[0].nextStage())
            self.stage.stage_block_list.empty()
            self.stage = self.game.current_stage

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= SCREEN_HEIGHT + self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT + self.rect.height*2

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


class Botboy(Player):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.left_botboy_image = pygame.image.load("data/python.png")
        self.left_botboy_image.set_colorkey(-1,pygame.RLEACCEL)
        self.right_botboy_image = pygame.transform.flip(self.left_botboy_image,True,False)
        self.image = self.right_botboy_image
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.stage = None
        self.score = 0

    def go_left(self):
        super().go_left()
        self.image = self.left_botboy_image

    def go_right(self):
        super().go_right()
        self.image = self.right_botboy_image
