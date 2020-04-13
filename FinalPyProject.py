import pygame
pygame.init()

winWidth = 500
winHeight = 500
x = winWidth - winWidth / 2
y = winHeight - winHeight / 4
playerWidth = 128
playerHeight = 128
vel = 5
left = False
right = False
idleCount = 0
bgCount = 0
bgCount2 = -1235

win = pygame.display.set_mode((winWidth, winHeight))

pygame.display.set_caption("Final Py Project")

bullet = pygame.image.load("sprites/Bullets.png")
bg = pygame.image.load("sprites/City_Background.png")
char = [pygame.image.load("sprites/Player_Ship.png"), pygame.image.load("sprites/Player_Ship2.png")]
charLeft = [pygame.image.load("sprites/Player_Ship_Left.png"), pygame.image.load("sprites/Player_Ship_Left2.png")]
charRight = [pygame.image.load("sprites/Player_Ship_Right.png"), pygame.image.load("sprites/Player_Ship_Right2.png")]

clock = pygame.time.Clock()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        win.blit(bullet, (x, y - 50))

    def update(self, x, y):
        win.blit(bullet, (x, y -50))
        self.y -= 5

def shoot():
    bullet = Bullet(x, y)
    bullets.add(bullet)

bullets = pygame.sprite.Group()

def drawWin():
    global bgCount
    global bgCount2
    global idleCount

    win.blit(bg, (0, bgCount))
    win.blit(bg, (0, bgCount2))
    bgCount += 5
    bgCount2 += 5
    if (bgCount >= 500):
        bgCount = bgCount2 - 1235

    if (bgCount2 >= 500):
        bgCount2 = bgCount -1235

    if (idleCount + 1 >= 12):
        idleCount = 0

    if (left == True):
        win.blit(charLeft[idleCount // 6], (x, y))
    elif (right == True):
        win.blit(charRight[idleCount // 6], (x, y))
    else:
        win.blit(char[idleCount // 6], (x, y))
    idleCount += 1

    bullets.update(x, y)

    pygame.display.update()

# main loop
run = True

while (run):
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
        
    if (keys[pygame.K_LEFT] and x > vel and not right):
        x -= vel
        left = True
        right = False

    elif (keys[pygame.K_RIGHT] and x < winWidth - playerWidth - vel and not left):
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False

    drawWin()

pygame.quit()
    



        
