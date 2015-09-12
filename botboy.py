import pygame
import pygame.locals
import pygame.font
import sys
from util import *
from gamePlayer import *
from gameMob import *
from gameStage import *

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
