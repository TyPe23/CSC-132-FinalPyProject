import pygame
pygame.init

winWidth = 500
winHeight = 500
x = winWidth - winWidth / 2
y = winHeight - winHeight / 4
playerWidth = 128
playerHeight = 128
vel = 10
left = False
right = False
walkCount = 0
idleCount = 0

win = pygame.display.set_mode((winWidth, winHeight))

pygame.display.set_caption("Final Py Project")

bg = pygame.image.load("sprites/City_Background.png")
char = [pygame.image.load("sprites/Player_Ship.png"), pygame.image.load("sprites/Player_Ship2.png")]

clock = pygame.time.Clock()

def drawWin():
    global walkCount
    global idleCount

    win.blit(bg, (0,0))

    if (walkCount + 1 >= 6):
        walkCount = 0

    if (idleCount + 1 >= 6):
        idleCount = 0

    win.blit(char[idleCount // 3], (x, y))
    idleCount += 1

    pygame.display.update()

# main loop
run = True

while (run):
    clock.tick(27)

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
    



        
