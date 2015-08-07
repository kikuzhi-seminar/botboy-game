import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.stage.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.stage.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.stage.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0


class StageObject(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()


class Stage():
    platform_list = None
    enemy_list = None
    world_shift = 0

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(BLUE)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Stage_01(Stage):
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
            self.platform_list.add(block)


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
            self.platform_list.add(block)


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
            self.platform_list.add(block)


class Stage_04(Stage):
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
            self.platform_list.add(block)


pygame.init()
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Side-scrolling Platformer")
player = Player()
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
clock = pygame.time.Clock()
while not done:
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
    current_stage.draw(screen)
    active_sprite_list.draw(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
