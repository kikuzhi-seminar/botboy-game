import pygame
import pygame.locals
import pygame.font
import sys
from util import *
from gamePlayer import *
from gameMob import *
from gameStage import *


class BotboyGame:
    def __init__(self, loadData = False):

        # ゲームキャラクター
        self.choseChar()

        # ステージ作成
        self.current_stage = Stage(self, self.player, ["01"])
        self.stageDict = {"01":self.current_stage}

        # クラス内のオブジェクトをリンクさせている。
        self.active_sprite_list = pygame.sprite.Group()
        self.player.stage = self.current_stage
        self.player.rect.x = 340
        self.player.rect.y = SCREEN_HEIGHT - self.player.rect.height
        self.active_sprite_list.add(self.player)

        # ゲームの基本定数
        if loadData == False:
            self.score = 0
            self.currentSavePoint = ["01", 0, 120, 530]
            self.currentDeathPoint = None
        else:
            with open("data/saveData", "r") as saveFile:
                self.score = eval(saveFile.readline().rstrip("\n"))
                saveData = eval(saveFile.readline().rstrip("\n"))
                if saveData[0] in self.stageDict:
                    self.current_stage = self.stageDict[saveData[0]]
                else:
                    self.current_stage = Stage(self, self, [saveData[0],[saveData[3],saveData[1]]])
                    self.stageDict[saveData[0]] = self.current_stage
                self.player.stage = self.current_stage
                try: # プレーヤーのy変更
                    self.player.rect.y = saveData[3]
                except: pass
                try: # world_shiftの変更
                    self.current_stage.shift_world(saveData[1])
                except: pass
                self.currentSavePoint = eval(saveFile.readline().rstrip("\n"))
                self.currentDeathPoint = eval(saveFile.readline().rstrip("\n"))

        # ゲームの用意
        self.done = False
        self.died = False
        self.gameover = False
        self.life = 5
        self.clock = pygame.time.Clock()
        self.timeL = 10000
        self.time0 = pygame.time.get_ticks()
        self.timeover = False

    # メインループ
    def main(self):
        while not self.done:
            self.k_up = False
            if not self.gameover:
                if not self.died:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                self.player.go_left()
                            if event.key == pygame.K_RIGHT:
                                self.player.go_right()
                            if event.key == pygame.K_UP:
                                self.k_up = True
                                self.player.jump()
                            if event.key == pygame.K_s: #セーブ
                                self.save()
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LEFT and self.player.change_x < 0:
                                self.player.stop()
                            if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                                self.player.stop()
                    self.update()
                    self.drow()
                else:
                    screen.fill(BLACK)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                             return True
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                             self.life -= 1
                             self.time0 = pygame.time.get_ticks()
                             self.timeover = False
                             self.died = False
                             self.load()
                    if self.timeover == True:
                         self.text = font.render("TIME OVER", True, RED)
                         self.text_rect = self.text.get_rect()
                         self.text_x = screen.get_width() / 2 - self.text_rect.width / 2
                         self.text_y = screen.get_height() / 2 - self.text_rect.height / 2
                         screen.blit(self.text, [self.text_x, self.text_y])
                    else:
                         self.text = font.render("YOU DIED", True, RED)
                         self.text_rect = self.text.get_rect()
                         self.text_x = screen.get_width() / 2 - self.text_rect.width / 2
                         self.text_y = screen.get_height() / 2 - self.text_rect.height / 2
                         screen.blit(self.text, [self.text_x, self.text_y])
                    self.text = font.render("Press Enter to Continue!", True, WHITE)
                    self.text_rect = self.text.get_rect()
                    self.text_x = screen.get_width() / 2 - self.text_rect.width / 2
                    self.text_y = screen.get_height() / 2 - self.text_rect.height / 2 + 50
                    screen.blit(self.text, [self.text_x, self.text_y])

            else:
                 screen.fill(BLACK)
                 for event in pygame.event.get():
                     if event.type ==pygame.QUIT:
                         return True
                     elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                         self.life=5
                         self.gameover = False
                         self.done=True

                 self.text = font.render("GAME OVER", True, RED)
                 self.text_rect = self.text.get_rect()
                 self.text_x = screen.get_width() / 2 - self.text_rect.width / 2
                 self.text_y = screen.get_height() / 2 - self.text_rect.height / 2
                 screen.blit(self.text, [self.text_x, self.text_y])
                 self.text = font.render("Press Enter to Continue!", True, WHITE)
                 self.text_rect = self.text.get_rect()
                 self.text_x = screen.get_width() / 2 - self.text_rect.width / 2
                 self.text_y = screen.get_height() / 2 - self.text_rect.height / 2 + 50
                 screen.blit(self.text, [self.text_x, self.text_y])
            self.clock.tick(60)
            pygame.display.flip()

    # キャラ選択
    def choseChar(self):
        self.player = Botboy(self)

    def timer(self):
        self.time = pygame.time.get_ticks()

    def update(self):
        self.active_sprite_list.update()
        self.current_stage.update()
        self.time = pygame.time.get_ticks()
        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.current_stage.shift_world(-diff)
        if self.player.rect.left <= 120:
            diff = 120 - self.player.rect.left
            self.player.rect.left = 120
            self.current_stage.shift_world(diff)
        if self.player.rect.y >= SCREEN_HEIGHT + self.player.rect.height and self.player.change_y >= 0:
            self.died=True
            self.death()
        if self.timeL - (self.time - self.time0) <= 0:
            self.timeover = True
            self.died=True
            self.death()
        if self.life == 0:
            self.gameover = True

    def death(self):
        stage = self.current_stage
        playerY = self.player.rect.y
        playerX = self.player.rect.x
        self.currentDeathPoint = [stage.stageId,stage.world_shift, playerX, playerY]

    def drow(self):
        self.current_stage.draw(screen)
        self.active_sprite_list.draw(screen)
        self.text = font.render("Total Life     :        " + str(self.life), True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_x = screen.get_width() - self.text_rect.width * 1.2
        self.text_y = 20
        screen.blit(self.text, [self.text_x, self.text_y])

        self.text =font.render("Total Credit :        " + str(self.score), True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_x = screen.get_width() - self.text_rect.width * 1.2
        self.text_y = 50
        screen.blit(self.text, [self.text_x, self.text_y])

        renderText(screen,font,"Time Limit    :",210,-210,BLACK)
        renderText(screen,font,str(self.timeL - (self.time - self.time0)),330,-210,BLACK)


    def save(self):
        stage = self.current_stage
        playerY = self.player.rect.y
        playerX = self.player.rect.x
        savePoint = [stage.stageId,stage.world_shift, playerX, playerY]
        with open("data/saveData","w") as saveFile:
            saveFile.write(str(self.score))
            saveFile.write("\n")
            saveFile.write(str(savePoint))
            saveFile.write("\n")
            saveFile.write(str(self.currentSavePoint))
            saveFile.write("\n")
            saveFile.write(str(self.currentDeathPoint))
            saveFile.write("\n")

    def gameOver(self):
        self.gameover = True

    def Died(self):
        self.died = True
        self.player.stop()


    def load(self):
        data = self.currentSavePoint
        if data is not None:
            self.current_stage = self.stageDict[data[0]]
            self.current_stage.shift_world( -1 * self.currentDeathPoint[1] )
            self.current_stage.world_shift = 0
            self.current_stage.shift_world(data[1])
            self.player.rect.x = data[2]
            self.player.rect.y = data[3]
        else: # sevePointを通過しなかったとき
            pass

def opening():
    done = False
    screen.fill(BLACK)
    renderText(screen,bigFont,"Bot-Boy",0, -50,WHITE)
    renderText(screen,font,"Load game > LEFT KEY ",0,70,WHITE)
    renderText(screen,font,"New game > RIGHT KEY",0,40,WHITE)

    pygame.display.flip()

    while not done:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                done = True
             elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                return True
             elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                return False

         pygame.display.flip()

# pygameの初期設定
pygame.init()
pygame.display.set_caption("BotBoy")
font = pygame.font.Font(None, 36)
bigFont = pygame.font.Font(None, 100)
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
done = False

while not done:
    load = opening()
    game = BotboyGame(load)
    done = game.main()
pygame.quit()