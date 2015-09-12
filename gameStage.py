import pygame
from util import *
from gameStageObject import *

class Stage():
    stage_block_list = None
    enemy_list = None
    door_list = None
    world_shift = 0

    def __init__(self, player):
        self.stage_block_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.player = player
        self.break_points = None
        self.BLOCKSIZE = 30

    def update(self):
        self.stage_block_list.update()
        self.enemy_list.update()
        self.item_list.update()
        self.door_list.update()


    def draw(self, screen):
        screen.fill(WHITE)
        self.stage_block_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)
        self.door_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for stage in self.stage_block_list:
            stage.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for item in self.item_list:
            item.rect.x += shift_x
        for door in self.door_list:
            door.rect.x += shift_x

    def stageBuilder(self,filename,player):
        map = []
        with open(filename, "r") as file:
            for line in file:
                line = line.rstrip()
                map.append(list(line))
                self.row = len(map)
        map.reverse()
        self.row = len(map)
        self.col = len(map[0])
        self.level_limit = SCREEN_HEIGHT + ( -1 * (self.col -1) * self.BLOCKSIZE)
        print(-1 * (self.col -1) * self.BLOCKSIZE)
        self.width = self.col * self.BLOCKSIZE
        self.height = self.row * self.BLOCKSIZE
        for i in range(self.row):
            for j in range(self.col):
                if map[i][j] == 'B':
                    block = Block(j*self.BLOCKSIZE,SCREEN_HEIGHT - i*self.BLOCKSIZE)
                    block.player = player
                    self.stage_block_list.add(block)
                elif map[i][j] == 'c':
                    coin = Coin(j*self.BLOCKSIZE,SCREEN_HEIGHT- i*self.BLOCKSIZE)
                    self.item_list.add(coin)
                elif map[i][j] == 'm':
                    mob = Mob(j*self.BLOCKSIZE,SCREEN_HEIGHT - i*self.BLOCKSIZE ,30 ,30)
                    self.enemy_list.add(mob)
                elif map[i][j] == 'd':
                    door = Door(j*self.BLOCKSIZE,SCREEN_HEIGHT - i*self.BLOCKSIZE)
                    self.door_list.add(door)


    def loadStage(self):
        pass

class Stage_01(Stage):
    def __init__(self, player):
        super().__init__(self)
        self.stageBuilder("data/stage_01.pymap",self.player)

class Stage_02(Stage):
    def __init__(self, player):
        Stage.__init__(self, player)
        self.level_limit = -1000
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]
        for platform in level:
            block = StageObject(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.stage_block_list.add(block)


class Stage_03(Stage):
    def __init__(self, player):
        Stage.__init__(self, player)
        self.level_limit = -1000
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
        for platform in level:
            block = StageObject(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.stage_block_list.add(block)


class Stage_04(Stage):
    def __init__(self, player):
        Stage.__init__(self, player)
        self.stage_limit = -1000
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]
        for platform in level:
            block = StageObject(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.stage_block_list.add(block)
