import pygame
import pygame.locals
import pygame.font
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


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
        enemy_hit_list = pygame.sprite.spritecollide(self, self.stage.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.rect.y >= self.game.player.rect.y + self.game.player.rect.height - self.game.player.change_y:
                enemy.kill()
            else:
                self.game.gameover = True
        door_hit_list = pygame.sprite.spritecollide(self, self.stage.door_list, False)
        if len(door_hit_list) > 0:
            print("hit!")
            self.rect.x = 120
            if self.game.current_stage_no < len(self.game.stage_list) - 1:
                self.game.current_stage_no += 1
                self.game.current_stage = self.game.stage_list[self.game.current_stage_no]
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
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
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
        # self.rect.x -= 3
        pass

    def move(self):
        pass

class Easy_mob(Mob):
    def __init__(self,width,height):
        super().__init__(width,height)
    def move(self):
        self.rect.x -= 3


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
    def __init__(self,x_pos,y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, (0,0,30,30), 0)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
    def check(self):
        return True

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


class BotboyGame:
    def __init__(self):
        # pygameの初期設定
        pygame.init()
        pygame.display.set_caption("BotBoy")
        self.font = pygame.font.Font(None, 36)
        self.size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(self.size)

        # ゲームキャラクター
        self.choseChar()

        # ステージ作成
        self.stage_list = []
        self.stage_list.append(Stage_01(self.player))
        self.stage_list.append(Stage_02(self.player))
        self.stage_list.append(Stage_03(self.player))
        self.stage_list.append(Stage_04(self.player))
        self.current_stage_no = 0
        self.current_stage = self.stage_list[self.current_stage_no]

        # クラス内のオブジェクトをリンクさせている。
        self.active_sprite_list = pygame.sprite.Group()
        self.player.stage = self.current_stage
        self.player.rect.x = 340
        self.player.rect.y = SCREEN_HEIGHT - self.player.rect.height
        self.active_sprite_list.add(self.player)

        # ゲームの用意
        self.done = False
        self.gameover = False
        self.clock = pygame.time.Clock()

    # メインループ
    def main(self):
        while not self.done:
            if not self.gameover:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.player.go_left()
                        if event.key == pygame.K_RIGHT:
                            self.player.go_right()
                        if event.key == pygame.K_UP:
                            self.player.jump()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT and self.player.change_x < 0:
                            self.player.stop()
                        if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                            self.player.stop()
                self.update()
                self.drow()
            else:
                 self.screen.fill(BLACK)
                 for event in pygame.event.get():
                     if event.type == pygame.QUIT:
                         self.done = True
                     elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                         self.gameover = False
                         self.player.rect.y = 0

                 self.text = self.font.render("Game Over", True, WHITE)
                 self.text_rect = self.text.get_rect()
                 self.text_x = self.screen.get_width() / 2 - self.text_rect.width / 2
                 self.text_y = self.screen.get_height() / 2 - self.text_rect.height / 2
                 self.screen.blit(self.text, [self.text_x, self.text_y])
                 self.text = self.font.render("Press Enter to Continue!", True, WHITE)
                 self.text_rect = self.text.get_rect()
                 self.text_x = self.screen.get_width() / 2 - self.text_rect.width / 2
                 self.text_y = self.screen.get_height() / 2 - self.text_rect.height / 2 + 50
                 self.screen.blit(self.text, [self.text_x, self.text_y])
            self.clock.tick(60)
            pygame.display.flip()

    # キャラ選択
    def choseChar(self):
        self.player = Botboy(self)

    def update(self):
        self.active_sprite_list.update()
        self.current_stage.update()
        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.current_stage.shift_world(-diff)
        if self.player.rect.left <= 120:
            diff = 120 - self.player.rect.left
            self.player.rect.left = 120
            self.current_stage.shift_world(diff)
        self.current_position = self.player.rect.x + self.current_stage.world_shift
        # if self.current_stage.check():
        #     pass
        # 削除予定コード
        # print("currentPos" + str(self.current_position) ,end="\r")
        # if self.current_position < self.current_stage.level_limit:
        #     self.player.rect.x = 120
        #     if self.current_stage_no < len(self.stage_list) - 1:
        #         self.current_stage_no += 1
        #         self.current_stage = self.stage_list[self.current_stage_no]
        #         self.player.stage = self.current_stage
        if self.player.rect.y >= SCREEN_HEIGHT + self.player.rect.height and self.player.change_y >= 0:
            self.gameover=True
            self.player.stop()

    def drow(self):
        self.current_stage.draw(self.screen)
        self.active_sprite_list.draw(self.screen)
        self.text = self.font.render("Total Credit: " + str(self.player.score), True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_x = self.screen.get_width() - self.text_rect.width * 1.2
        self.text_y = 20
        self.screen.blit(self.text, [self.text_x, self.text_y])


game = BotboyGame()
game.main()
pygame.quit()
