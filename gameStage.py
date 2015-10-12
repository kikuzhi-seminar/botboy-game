import pygame
from util import *
from gameStageObject import *
from gameEnemy import *

class Stage():
    def __init__(self, game, player, stageOpt):
        self.game = game
        self.world_shift = 0
        self.stage_block_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.door_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.player = player
        self.break_points = None
        self.BLOCKSIZE = 30
        self.stageId = stageOpt[0]
        self.startTime = pygame.time.get_ticks()
        self.stageBuilder(self.game, self.player, stageOpt)

    def update(self):
        self.stage_block_list.update()
        self.enemy_list.update()
        self.item_list.update()
        self.door_list.update()
        self.bullet_list.update()


    def draw(self, screen):
        screen.fill(LBLUE)
        self.stage_block_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)
        self.door_list.draw(screen)
        self.bullet_list.draw(screen)

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

    def stageBuilder(self, game, player, stageOpt):
        optNun = 0
        opt = []
        with open("data/stage_" + stageOpt[0] + ".pyopt", "r") as file:
            self.timeL = eval(file.readline().rstrip())
            for line in file:
                line = line.rstrip()
                opt.append(line.split(","))
        opt.reverse()
        map = []
        with open("data/stage_" + stageOpt[0] + ".pymap", "r") as file:
            for line in file:
                line = line.rstrip()
                map.append(list(line))
                self.row = len(map)
        map.reverse()
        self.row = len(map)
        self.col = len(map[0])
        self.width = self.col * self.BLOCKSIZE
        self.height = self.row * self.BLOCKSIZE
        for i in range(self.row):
            for j in range(self.col):
                if map[i][j] == 'B':
                    block = Block( j * self.BLOCKSIZE, SCREEN_HEIGHT - i * self.BLOCKSIZE )
                    # block.player = player
                    self.stage_block_list.add( block )
                elif map[i][j] == 'c':
                    coin = Coin( j * self.BLOCKSIZE, SCREEN_HEIGHT - i * self.BLOCKSIZE, self.game)
                    self.item_list.add( coin )
                elif map[i][j] == 's':
                    savePoint = SavePoint( j * self.BLOCKSIZE, SCREEN_HEIGHT - i * self.BLOCKSIZE, self.game)
                    self.item_list.add( savePoint )
                elif map[i][j] == 'm':
                    enemy = Enemy( j * self.BLOCKSIZE, SCREEN_HEIGHT - i * self.BLOCKSIZE)
                    self.enemy_list.add( enemy )
                elif map[i][j] == 'D':
                    door = Door( j * self.BLOCKSIZE, SCREEN_HEIGHT - i * self.BLOCKSIZE, self.game, opt[ optNun ] )
                    self.door_list.add( door )
                    optNun += 1
                elif map[i][j] == 'b':
                    boss = Boss(game, eval(opt[optNun][ 0 ]), eval(opt[optNun][ 1 ]), eval(opt[optNun][ 2 ]), opt[optNun][ 3 ])
                    self.enemy_list.add( boss )
                    optNun += 1
