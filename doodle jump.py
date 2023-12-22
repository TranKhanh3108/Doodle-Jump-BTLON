import pygame #import thư viện pygame
from pygame.locals import *
import sys
import random
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))  #Tạo khung màn hình
pygame.display.set_caption("Menu") #Tên nền
BG = pygame.image.load("assets/Background.png") #Ảnh nền

game_over = False

#font chữ - kích thước
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600)) # Tạo khung màn có kích thước
        self.green = pygame.image.load("assets/green.png").convert_alpha() #Load ảnh nền
        pygame.font.init()
        self.score = 0 #Biến điểm cá nhân
        self.font = pygame.font.SysFont("Arial", 25) #Font chữ
        self.blue = pygame.image.load("assets/blue.png").convert_alpha() #Load ảnh cho element
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        self.direction = 0 #Vị trí nhân vật
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0 #Camera của game
        self.jump = 10  #Độ cao nhảy của nhân vật
        self.gravity = 0 #Trọng lực của nhân vật
        self.xmovement = 0 #Vị trí mặc định khi di chuyển

#Hàm update player cập nhật nhân vật chỉnh

    def updatePlayer(self): #Cập nhật trạng thái nhân vật khi nhảy tại chỗ
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 15
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

#Cập nhật màn hình trạng thái game
    #Cập nhật mỗi khi nhân vật đi quá màn hình phía trên
    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15 #độ cao nhảy tại chỗ
                    self.gravity = 0.4
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1
#Vẽ thêm vật cản
    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 950 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))
#Vật hỗ trợ: lò xo
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(
                    pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(),
                                self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50

#Tự động tạo thêm vật cản xanh lá
    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

#Kẻ nền
    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (800, x * 12))

#Màn hình gameover
    def game_over(self, game_over=None):
        bg = pygame.image.load("assets/End.png")
        SCREEN.blit(bg,(0,0))
        while game_over==True:
            game_over_text = get_font(60).render("Game Over", True, "#b68f40")
            game_over_rect = game_over_text.get_rect(center=(400, 100))
            SCREEN.blit(game_over_text, game_over_rect)
            game_over_text = get_font(20).render("Spacebar to restart!", True, "#40b466")
            game_over_rect = game_over_text.get_rect(center=(400, 200))
            SCREEN.blit(game_over_text, game_over_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        game_over= False
        self.run()
#Reset game được thực thi
    def run(self):

        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.playery - self.cameray > 540:
                game_over = True
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
                if game_over == True:
                    self.game_over(game_over)

            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("DOODLE JUMP", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 200),
                             text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 320),
                             text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    DoodleJump().run()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
