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
    def __init__(self):
        super().__init__()
        width = 40
        height = 60
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
            global gameover
            print("enemy:"+ str(enemy.rect.y))
            print("playover:" + str(player.rect.y + player.rect.height))
            if enemy.rect.y >= player.rect.y + player.rect.height - player.change_y:
                enemy.kill()
            else:
                gameover = True



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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = right_botboy_image
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.stage = None
        self.score = 0
    def go_left(self):
        super().go_left()
        self.image = left_botboy_image

    def go_right(self):
        super().go_right()
        self.image = right_botboy_image

class Mob(pygame.sprite.Sprite):
    def __init__(self,x_pos, y_pos, width, height):
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
        self.rect.center = (x_pos,y_pos)

class Block(StageObject):
    def __init__(self,x_pos,y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, GREEN, (0,0,30,30), 0)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

class Stage():
    stage_block_list = None
    enemy_list = None
    world_shift = 0

    def __init__(self, player):
        self.stage_block_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.player = player
        self.break_points = None
        self.BLOCKSIZE = 30

    def update(self):
        self.stage_block_list.update()
        self.enemy_list.update()
        self.item_list.update()

    def draw(self, screen):
        screen.fill(WHITE)
        self.stage_block_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for stage in self.stage_block_list:
            stage.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for item in self.item_list:
            item.rect.x += shift_x

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


class Stage_01(Stage):
    def __init__(self, player):
        super().__init__(self)
        self.level_limit = -1000
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


pygame.init()
font = pygame.font.Font(None, 36)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BotBoy")
left_botboy_image = pygame.image.load("data/python.png")
left_botboy_image.set_colorkey(-1,pygame.RLEACCEL)
right_botboy_image = pygame.transform.flip(left_botboy_image,True,False)

try:
    if sys.argv[1] == "player":
        player = Player()
    else:
        player = Botboy()
except IndexError:
    player = Botboy()
stage_list = []
stage_list.append(Stage_01(player))
stage_list.append(Stage_02(player))
stage_list.append(Stage_03(player))
stage_list.append(Stage_04(player))
current_stage_no = 0
current_stage = stage_list[current_stage_no]
active_sprite_list = pygame.sprite.Group()
player.stage = current_stage
player.rect.x = 340
player.rect.y = SCREEN_HEIGHT - player.rect.height
active_sprite_list.add(player)
done = False
gameover = False
clock = pygame.time.Clock()
while not done:
    if not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        active_sprite_list.update()
        current_stage.update()
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_stage.shift_world(-diff)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_stage.shift_world(diff)
        current_position = player.rect.x + current_stage.world_shift
        if current_position < current_stage.level_limit:
            player.rect.x = 120
            if current_stage_no < len(stage_list) - 1:
                current_stage_no += 1
                current_stage = stage_list[current_stage_no]
                player.stage = current_stage
        if player.rect.y >= SCREEN_HEIGHT + player.rect.height and player.change_y >= 0:
            gameover=True
        current_stage.draw(screen)
        active_sprite_list.draw(screen)
        text = font.render("Total Credit: " + str(player.score), True, BLACK)
        text_rect = text.get_rect()
        text_x = screen.get_width() - text_rect.width * 1.2
        text_y = 20
        screen.blit(text, [text_x, text_y])
    else:
         screen.fill(BLACK)
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 done = True
             elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                 gameover = False
                 player.rect.y = 0

         text = font.render("Game Over", True, WHITE)
         text_rect = text.get_rect()
         text_x = screen.get_width() / 2 - text_rect.width / 2
         text_y = screen.get_height() / 2 - text_rect.height / 2
         screen.blit(text, [text_x, text_y])
         text = font.render("Press Enter to Continue!", True, WHITE)
         text_rect = text.get_rect()
         text_x = screen.get_width() / 2 - text_rect.width / 2
         text_y = screen.get_height() / 2 - text_rect.height / 2 + 50
         screen.blit(text, [text_x, text_y])
    clock.tick(60)
    pygame.display.flip()
pygame.quit()