import pygame 
import sys
import random
pygame.init()
width = 1270
heigth = 720
screen = pygame.display.set_mode((width,heigth))
clock = pygame.time.Clock()
fps = 60
background = pygame.image.load("images/background.png").convert_alpha()
android_robot = pygame.image.load("images/android_robot.png").convert_alpha()
candy = pygame.image.load("images/candy.png").convert_alpha()
rotatedcandy = pygame.image.load("images/rotated_candy.png").convert_alpha()
point = pygame.mixer.Sound("sounds/sfx_point.wav")
hit = pygame.mixer.Sound("sounds/sfx_hit.wav")
pygame.display.set_caption("Lolipop")  
class Game:
    def __init__(self):
        self.gameOn = True
        self.android_robotX = 100
        self.android_robotY = 100
        self.candysX = [width, width+200, width+400, width+600, width+800, width+1000, width+1200]
        self.lowercandyY = [self.randomcandy(),self.randomcandy(),self.randomcandy(),self.randomcandy(),
            self.randomcandy(),self.randomcandy(),self.randomcandy()]
        self.uppercandyY = [self.randomRotatedcandy(),self.randomRotatedcandy(),self.randomRotatedcandy(),self.randomRotatedcandy(),
            self.randomRotatedcandy(),self.randomRotatedcandy(),self.randomRotatedcandy()]
        self.gravity = 0
        self.candyVel = 0
        self.flap = 0
        self.score = 0
        self.rotateAngle = 0
        self.isGameOver = False
        self.playSound = True

    def movingcandy(self):
        for i in range(0,7):
            self.candysX[i] += -self.candyVel
        
        for i in range(0,7):
            if(self.candysX[i] < -50):
                self.candysX[i] = width + 100
                self.lowercandyY[i] = self.randomcandy()
                self.uppercandyY[i] = self.randomRotatedcandy()

    def randomcandy(self):
        return random.randrange(int(heigth/2)+50, heigth-200)
    
    def randomRotatedcandy(self):
        return random.randrange(-int(heigth/2)+100, -100)

    def flapping(self):
        self.android_robotY += self.gravity
        if(self.isGameOver == False):
            self.flap -= 1
            self.android_robotY -= self.flap
    
    def isCollide(self):
        for i in range(0,7):
            if(self.android_robotX >= self.candysX[i] and self.android_robotX <= (self.candysX[i]+candy.get_width())
                and ((self.android_robotY+android_robot.get_height()-15) >= self.lowercandyY[i] or 
                (self.android_robotY) <= self.uppercandyY[i]+rotatedcandy.get_height()-15)):
                    return True
                
            elif(self.android_robotX == self.candysX[i] and (self.android_robotY <= self.lowercandyY[i] and self.android_robotY >= self.uppercandyY[i])):
                if(self.isGameOver == False):
                    self.score += 1
                    pygame.mixer.Sound.play(point)
        
        if(self.android_robotY <= 0):
            return True
        
        elif(self.android_robotY+android_robot.get_height() >= heigth):
            self.gravity = 0
            return True
 
        return False

    def gameOver(self):
        if(self.isCollide()):
            self.isGameOver = True
            self.screenText("Game Over!", (255,255,255), 450, 300, 84, "Fixedsys", bold=True)
            self.screenText("Press Enter To Play Again", (255,255,255), 400,  350, 48, "Fixedsys", bold=True)
            self.candyVel = 0
            self.flap = 0
            self.rotateAngle = -90
            if(self.playSound):
                pygame.mixer.Sound.play(hit)
                self.playSound =False

    def screenText(self, text, color, x,y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x,y))
    
    def mainGame(self):
        while self.gameOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if(self.isGameOver == False):
                            self.candyVel = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotateAngle = 15
                    
                    if event.key == pygame.K_RETURN:
                        newGame = Game()
                        newGame.mainGame()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.rotateAngle = 0

            screen.blit(background, (0,0))

            for i in range(0,7):
              
                screen.blit(candy, (self.candysX[i], self.lowercandyY[i]))
                screen.blit(rotatedcandy, (self.candysX[i], self.uppercandyY[i]))

            screen.blit(pygame.transform.rotozoom(android_robot, self.rotateAngle, 1), (self.android_robotX, self.android_robotY))

            self.movingcandy()
            self.flapping()
            self.gameOver()
            self.screenText(str(self.score), (255,255,255), 600, 50, 68, "Fixedsys", bold=True)
            pygame.display.update()
            clock.tick(fps)

Lolipop = Game()
Lolipop.mainGame()


