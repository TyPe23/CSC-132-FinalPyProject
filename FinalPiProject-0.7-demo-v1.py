import pygame, time, random, math
from pygame.locals import *
pygame.init()


#class that creates a button 
class Button(pygame.sprite.Sprite):

    def __init__(self, points, width, height, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.points = points
            self.screen = screen
            self.width = width
            self.height = height
            self.x = x 
            self.y = y
            self.image = pygame.Surface((width, height))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def update(self):
        self.clicked()

    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (self.rect.collidepoint(mouse_pos) and click[0] == 1):
            return True

        else:
            return False


class StartButton(Button):
    def __init__(self, sprite):
        Button.__init__(self, points = None, width = 248, height = 192, x = WIDTH / 4, y = HEIGHT / 3)
        self.sprite = sprite

    def update(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        if (self.rect.collidepoint(mouse_pos)):
            screen.blit(selectedStartButtonImg, self.rect)

        else:
            screen.blit(self.sprite, self.rect)

class ToggleButton(Button):
    def __init__(self, sprite):
        Button.__init__(self, points = None, width = 56, height = 44, x = toggleX, y = toggleY)
        self.sprite = sprite

    def update(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        if (Player.straightShot == True):
            if (self.rect.collidepoint(mouse_pos)):
                screen.blit(toggleStraight[1], self.rect)

            else:
                screen.blit(toggleStraight[0], self.rect)

        if (Player.vShot == True):
            if (self.rect.collidepoint(mouse_pos)):
                screen.blit(toggleWide[1], self.rect)

            else:
                screen.blit(toggleWide[0], self.rect)

#class that will create the player (must include a sprite)
class Player(pygame.sprite.Sprite):

    straightShot = True
    vShot = False

    def __init__(self, sprite, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image =  pygame.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, screen):
        global right
        global left
        global rightImg
        global leftImg
        global upImg
        global downImg
        global toggleImg

        if (self.rect.bottom > HEIGHT - 30):
            self.rect.y -= 6

        #creating all the buttons 
        downButton = Button([(stickX - 20, stickY + 30), (stickX, stickY + 70), (stickX + 20, stickY + 30)], 80, 0, stickX - 10, stickY + 20)
        rightButton = Button([(stickX + 70, stickY), (stickX + 30, stickY - 20), (stickX + 30, stickY + 20)], 0, 80, stickX + 25, stickY - 10)
        upButton = Button([(stickX - 20, stickY - 30), (stickX, stickY - 70), (stickX + 20, stickY - 30)], 80, 0, stickX - 10, stickY - 20)
        leftButton = Button([(stickX - 70, stickY), (stickX - 30, stickY - 20), (stickX - 30, stickY + 20)], 0, 80, stickX - 20, stickY - 10)

        if (Player.straightShot == True):
            toggleImg = pygame.image.load("sprites/DownArrow.png")

        else:
            toggleImg = pygame.image.load("sprites/UpArrow.png")

        if (not pygame.sprite.collide_rect(joystick, rightButton)):
            rightImg = pygame.image.load("sprites/RightArrow2.png")
                        
        else:
            rightImg = pygame.image.load("sprites/RightArrow.png")

        if (not pygame.sprite.collide_rect(leftButton, joystick)):
            leftImg = pygame.image.load("sprites/LeftArrow2.png")

        else:
            leftImg = pygame.image.load("sprites/LeftArrow.png")
                        
        if (not pygame.sprite.collide_rect(upButton, joystick)):
            upImg = pygame.image.load("sprites/UpArrow2.png") 

        else:
            upImg = pygame.image.load("sprites/UpArrow.png")
                        
        if (not pygame.sprite.collide_rect(downButton, joystick)):
            downImg = pygame.image.load("sprites/DownArrow2.png")

        else:
            downImg = pygame.image.load("sprites/DownArrow.png")

        if (pygame.sprite.collide_rect(upButton, joystick) and self.rect.y > 15):
            self.rect.y -= 6

        if (pygame.sprite.collide_rect(rightButton, joystick) and left == False and self.rect.x < WIDTH - self.rect.width - 45):
            self.rect.x += 6
            right = True

        if (pygame.sprite.collide_rect(downButton, joystick) and self.rect.y < HEIGHT - self.rect.height - 45):
            self.rect.y += 6                       

        if (pygame.sprite.collide_rect(leftButton, joystick) and right == False and self.rect.x > 5):
            self.rect.x -= 6
            left = True

        right = False
        left = False

    #function that creates a bullet object 
    def shoot(self):
        if (self.rect.bottom <= HEIGHT - 30) and (Player.straightShot == True):
            bullet1 = Bullet(self.rect.centerx + 45, self.rect.top, 12, 14, 0, -11)
            bullet2 = Bullet(self.rect.centerx, self.rect.top, 12, 14, 0, -11)
            bullets.add(bullet1, bullet2)
        
        elif (self.rect.bottom <= HEIGHT - 30) and (Player.vShot == True):
            bullet1 = Bullet(self.rect.centerx + 45, self.rect.top, 12, 14, 3, -11)
            bullet2 = Bullet(self.rect.centerx, self.rect.top, 12, 14, -3, -11)
            bullets.add(bullet1, bullet2)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Bullets.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = vx
        self.y_speed = vy

    def update(self, screen, bulletImg):

        #blit the given sprite to the bullet rect
        screen.blit(bulletImg, self.rect)

        #if it goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()
                
        #make it shoot upwards
        self.rect.x +=  self.x_speed
        self.rect.y += self.y_speed


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Enemy_Bullets.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = vx
        self.y_speed = vy

    def update(self, screen, enemyBulletImg):

        #blit the given sprite to the bullet rect
        screen.blit(enemyBulletImg, self.rect)

        self.offScreen()
                
        #make it shoot upwards
        self.rect.x +=  self.x_speed
        self.rect.y += self.y_speed

    def offScreen(self):

        #if bullet goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()

        elif (self.rect.top > HEIGHT):
            self.kill()

        elif (self.rect.left + self.rect.width > WIDTH):
            self.kill()

        elif (self.rect.right - self.rect.width < 0):
            self.kill()


#bullet that will have the ability to shoot in a circular pattern
class EnemyCircularBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Enemy_Bullets.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.x_speed = 5 * math.cos(math.radians(self.angle)) 
        self.y_speed = -5 * math.sin(math.radians(self.angle))
        self.posx = self.rect.centerx
        self.posy = self.rect.centery

    def update(self, screen, enemyBulletImg):

        #blit the given sprite to the bullet rect
        screen.blit(enemyBulletImg, self.rect)

        #check if the bullet is off the screen
        self.offScreen()

        self.posx += self.x_speed
        self.posy += self.y_speed
        self.rect.center = (self.posx, self.posy)

    def offScreen(self):

        #if bullet goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()

        elif (self.rect.top > HEIGHT):
            self.kill()

        elif (self.rect.left + self.rect.width > WIDTH):
            self.kill()

        elif (self.rect.right - self.rect.width < 0):
            self.kill()


class EnemyRotatingBullet(pygame.sprite.Sprite):
    def __init__(self, sprite, width, height, pos, direction, dt):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image = pygame.image.load('sprites/Enemy_Bullets.png')
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.dt = dt

    def update(self, screen, enemyBulletImg):

        screen.blit(enemyBulletImg, self.rect)
        
        self.offScreen()

        self.pos += self.direction * (self.dt / 3)
        self.rect.center = self.pos

    def offScreen(self):

        #if bullet goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()

        elif (self.rect.top > HEIGHT):
            self.kill()

        elif (self.rect.left + self.rect.width > WIDTH):
            self.kill()

        elif (self.rect.right - self.rect.width < 0):
            self.kill()


#class that creates the circle inside the d-pad
class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (x, y)
        self.image = pygame.image.load("sprites/Joystick.png")
        self.rect = self.image.get_rect(center = self.pos)
        self.x_boundary = (x - radius, x + radius)
        self.y_boundary = (y - radius, y + radius)
        self.color = color
        self.radius = radius

    #function that will redraw the circle as it is being moved
    def recalc_boundary(self):
        self.x_boundary = (self.pos[0] - self.radius, self.pos[0] + self.radius)
        self.y_boundary = (self.pos[1] - self.radius, self.pos[1] + self.radius)


class Enemy(pygame.sprite.Sprite):

    evadingEnemyAlive = False

    def __init__(self, sprite, hp, x_speed, y_speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image = image
        self.image.fill((255, 255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0 + self.rect.width, WIDTH - self.rect.width)
        self.rect.bottom = -150

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.hp = hp

    def update(self, screen):
        pass

    def checkCollision(self):
        for bullet in bullets:
            if (pygame.sprite.collide_rect(self, bullet)):
                if (self.hp > 0):
                    self.hp -= 1
                else:
                    self.kill()
                bullet.kill()

    def alive(self):
        if (self.hp > 0):
            return True
        else:
            return False

    def updateMove(self):
        pass

    def shoot(self):
        pass


class NormalEnemy(Enemy):
    def __init__(self, sprite, hp, x_speed, y_speed):
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((40, 41)).convert_alpha())
        self.sprite = sprite
        self.hp = hp
        self.x_speed = x_speed if (x_speed > 2 or x_speed < -2) else 3
        self.y_speed = y_speed if (x_speed > 2 or x_speed < -2) else 3
        self.xdirection = 1
        self.ydirection = 1

    def update(self, screen):

        screen.blit(normal[count // 6], self.rect)

        if Enemy.evadingEnemyAlive == False:
            self.checkCollision()

        if (self.rect.top < 0):
            self.rect.y += 6

        else:
            self.shoot()

            self.rect.x += self.x_speed * self.xdirection
            self.rect.y += self.y_speed * self.ydirection

            if ((self.rect.left <= 0) or (self.rect.left + self.rect.width >= WIDTH)):
                self.xdirection *= -1
                self.y_speed = random.uniform(3, 6)

            if ((self.rect.bottom > 450) or (self.rect.top <= 0)): 
                self.ydirection *= -1
                self.x_speed = random.uniform(3, 6)
                
    def shoot(self):
        if (random.randrange(20) == 0):
            enemyBullet = EnemyBullet(self.rect.centerx, self.rect.top + self.rect.height, 10, 20, 0, 6)
            enemyBullets.add(enemyBullet)


class SplashEnemy(Enemy):
    def __init__(self, sprite, hp, x_speed, y_speed):
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((72, 60)).convert_alpha())
        self.sprite = sprite
        self.hp = hp
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self, screen):

        screen.blit(spray[count // 6], self.rect)

        if (Enemy.evadingEnemyAlive == False):
            self.checkCollision()

        if (self.rect.bottom < 400):
            self.rect.y += self.y_speed

        else:
            self.rect.y += 0
            self.shoot()

    def shoot(self):
        enemyBullet1 = EnemyBullet(self.rect.centerx + 23, self.rect.top + self.rect.height, 10, 20, random.randint(0, 2), random.uniform(3.5, 7.5))
        enemyBullet2 = EnemyBullet(self.rect.centerx - 35, self.rect.top + self.rect.height, 10, 20, random.randint(-2, -0), random.uniform(3.5, 7.5))
        enemyBullets.add(enemyBullet1, enemyBullet2)


class EvadingEnemy(Enemy):

    edge = False
    leftMove = False
    rightMove = False

    def __init__(self, sprite, hp, x_speed, y_speed, player):       
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((72, 80)).convert_alpha())
        self.sprite = sprite
        self.hp = 10
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.player = player

    def update(self, screen):

        Enemy.evadingEnemyAlive = True

        if self.alive() == False:
            Enemy.evadingEnemyAlive = False

        global xDist
        xDist = (self.rect.centerx - self.player.rect.centerx)

        self.checkCollision()

        self.offScreen()

        if (self.rect.top >= 300):
            screen.blit(healer[count // 6], self.rect)

        else:
            screen.blit(healer2[count // 6], self.rect)

        if xDist < 0:
            xDist *= -1

        if self.rect.top < 300:
            self.rect.y += 12

        else:
            if (EvadingEnemy.edge == False) and (EvadingEnemy.leftMove == False) and (EvadingEnemy.rightMove == False):

                if (self.rect.x < self.player.rect.x) and (xDist < 185):
                    self.rect.x -= self.x_speed
            
                elif (self.rect.x > self.player.rect.x) and (xDist < 150):
                    self.rect.x += self.x_speed

            elif EvadingEnemy.edge == True and self.offScreen() == 1:
                EvadingEnemy.leftMove = True

            elif EvadingEnemy.edge == True and self.offScreen() == 2:
                EvadingEnemy.rightMove = True
    
            if EvadingEnemy.leftMove == True:
                if ((self.rect.left + self.rect.width) < self.player.rect.left):
                    self.rect.x += 0

                else:
                    self.leftScreenCollison()

            elif EvadingEnemy.rightMove == True:
                if ((self.player.rect.left + self.player.rect.width) < self.rect.left):
                    self.rect.x += 0
                
                else:
                    self.rightScreenCollison()

    def offScreen(self):
        if (self.rect.left <= 0):
            EvadingEnemy.edge = True
            return 1

        if(self.rect.left + self.rect.width >= WIDTH):
            EvadingEnemy.edge = True
            return 2

    def leftScreenCollison(self):
        if (self.rect.x <= self.rect.width):
            self.rect.x += self.x_speed

        else:
            EvadingEnemy.leftMove = False
            EvadingEnemy.edge = False

    def rightScreenCollison(self):
        if self.rect.x >= (WIDTH - (self.rect.width * 2)):
            self.rect.x -= self.x_speed

        else:
            EvadingEnemy.rightMove = False
            EvadingEnemy.edge = False


class KamikazeEnemy(Enemy):
    def __init__(self, sprite, hp, x_speed, y_speed, player):       
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((40, 41)).convert_alpha())
        self.sprite = sprite
        self.hp = 10
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.player = player

    def update(self, screen):

        screen.blit(kamikaze[count // 6], self.rect)

        self.checkCollision()

        if (self.rect.top < 0):
            self.rect.y += 6

        else:
            if (self.rect.x < self.player.rect.x):
                self.rect.x += self.x_speed
            
            elif (self.rect.x > self.player.rect.x):
                self.rect.x -= self.x_speed
                                
            if (self.rect.y < self.player.rect.y):
                self.rect.y += self.y_speed
            
            elif (self.rect.y > self.player.rect.y):
                self.rect.y -= self.y_speed


class Boss(pygame.sprite.Sprite):

    def __init__(self, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/Boss_Base.png")
        #self.image.fill((0, 0, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = -150
        self.hp = hp

        #creating left cannon
        self.leftCannon = pygame.image.load('sprites/Boss_Gun.png')
        #self.leftCannon.fill((0, 0, 255))
        self.leftCannonRect = self.leftCannon.get_rect()
        self.leftCannonRect.x = self.rect.width - 389
        self.leftCannonRect.y = self.rect.height
        self.leftCannonAngleSpeed = 1
        self.leftCannonCopy = self.leftCannon

        #creating right cannon
        self.rightCannon = pygame.image.load("sprites/Boss_Gun.png")
        #self.rightCannon.fill((0, 0, 255))
        self.rightCannonRect = self.rightCannon.get_rect()
        self.rightCannonRect.x = self.rect.width - 88
        self.rightCannonRect.y = self.rect.height 
        self.rightCannonAngleSpeed = -1
        self.rightCannonCopy = self.rightCannon


        #time to wait between each attack
        self.wait = 0

        #time before splash attack starts
        self.splashWait = 0

        #duration of splash attack
        self.splash = 0

        #timer that will handle delay between each spray shoot (bullets would
        #shoot continuously otherwise)
        self.sprayShootDelay = 0

        #duration of left spray attack
        self.leftSpray = 0

        #duration of right spray attack
        self.rightSpray = 0

        #duration of circular attack
        self.leftCircular = 0
        self.rightCircular = 0

        #timer that will handle delay between each circular shot (bullets would
        #shoot continuously otherwise)
        self.circularDelay = 0

        #will determine which attack is executed
        self.attack = 0

        #angle that the cannon will be rotating by during rotating attack
        self.angle = 0

        self.rotatingDelay = 0

        #variable to keep track of how many times surface has rotated 90 degrees
        self.rotateCount = 0

        self.untouchableCannonDelay = 0

    def update(self, screen):

        screen.blit(self.leftCannon, self.leftCannonRect)
        screen.blit(self.rightCannon, self.rightCannonRect)
        
        if self.rect.top <= 0:
            self.rect.y += 6
            self.leftCannonRect.y = self.rect.y + 45
            self.rightCannonRect.y = self.rect.y + 45

        else:  
            self.wait += 1

            #self.untouchableCannonDelay += 1

            if self.wait == 100:
                attack = 4

                if attack == 1:
                    self.attack = 1

                elif attack == 2:
                    self.attack = 2

                elif attack == 3:
                    self.attack = 3

                elif attack == 4:
                    self.attack = 4

            if self.attack == 1:
                self.splashAttack()

            elif self.attack == 2:
                self.sprayAttack()
            
            elif self.attack == 3:
                self.circularAttack()

            elif self.attack == 4:
                self.rotatingAttack(screen)
        
            #having the untouchable cannons shoot after a certain amount of time
            if self.untouchableCannonDelay % 50 == 343343:
                enemyBullet1 = EnemyCircularBullet(153, 60, 10, 20, -90)
                enemyBullet2 = EnemyCircularBullet(153, 60, 10, 20, -110)
                enemyBullet3 = EnemyCircularBullet(153, 60, 10, 20, -70)
                enemyBullet4 = EnemyCircularBullet(318, 60, 10, 20, -90)
                enemyBullet5 = EnemyCircularBullet(318, 60, 10, 20, -110)
                enemyBullet6 = EnemyCircularBullet(318, 60, 10, 20, -70)
                enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4, enemyBullet5, enemyBullet6)
                self.untouchableCannonDelay = 0 

    def splashAttack(self):

            self.splashWait += 1
            
            if self.splashWait >= 149:

                if self.splash < 99:
                    enemyBullet1 = EnemyBullet(self.leftCannonRect.centerx - 4, self.leftCannonRect.top + self.leftCannonRect.height - 10, 10, 20, random.randint(0, 2), random.uniform(3.5, 7.5))
                    enemyBullet2 = EnemyBullet(self.leftCannonRect.centerx - 4, self.leftCannonRect.top + self.leftCannonRect.height - 10, 10, 20, random.randint(-2, 0), random.uniform(3.5, 7.5))
                    enemyBullet3 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 10, 10, 20, random.randint(0, 2), random.uniform(3.5, 7.5))
                    enemyBullet4 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 10, 10, 20, random.randint(-2, 0), random.uniform(3.5, 7.5))        
                    enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4)
                    self.splash += 1

                else:
                    self.splash = 0
                    self.splashWait = 0
                    self.wait = -150
                    self.attack = 0

    def sprayAttack(self):

        self.sprayShootDelay += 1

        if self.leftSpray < 99:

            if self.sprayShootDelay % 10 == 0:
                enemyBullet1 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 0, 5)
                enemyBullet2 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 1, 5)    
                enemyBullet3 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 2, 5)    
                enemyBullet4 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 3, 5)    
                enemyBullet5 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 4, 5)    
                enemyBullet6 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 5, 5)
                enemyBullet7 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 6, 5)            
                enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4, enemyBullet5, enemyBullet6, enemyBullet7)
            self.leftSpray += 1

        elif self.leftSpray >= 99 and self.rightSpray < 99:

            #delay time between left cannon shooting and right cannon shooting
            if self.sprayShootDelay > 200:

                if self.sprayShootDelay % 10 == 0:
                    enemyBullet1 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, 0, 5)
                    enemyBullet2 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -1, 5)    
                    enemyBullet3 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -2, 5)    
                    enemyBullet4 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -3, 5)    
                    enemyBullet5 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -4, 5)    
                    enemyBullet6 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -5, 5)
                    enemyBullet7 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -6, 5)            
                    enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4, enemyBullet5, enemyBullet6, enemyBullet7)
                self.rightSpray += 1

        else:
            self.leftSpray = 0
            self.rightSpray = 0
            self.sprayShootDelay = 0
            self.wait = -100
            self.attack = 0

    def circularAttack(self):

        angle = 20

        self.circularDelay += 1

        if self.rightCircular < 99:

            if self.circularDelay % 10 == 0:

                for x in range (12):
                    enemyBullet = EnemyCircularBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.centery + (self.rightCannonRect.height / 2) - 10, 10, 20, angle)
                    enemyBullets.add(enemyBullet)
                    angle -= 20 if angle <= 140 else 140

            self.rightCircular += 1

        elif self.rightCircular >= 99 and self.leftCircular < 99: 
            angle = 20

            if self.circularDelay % 10 == 0:

                for x in range (12):
                    enemyBullet = EnemyCircularBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.centery + (self.leftCannonRect.height / 2) - 8, 10, 20, angle)
                    enemyBullets.add(enemyBullet)
                    angle -= 20 if angle <= 140 else 140
            
            self.leftCircular += 1

        else:
            self.circularDelay = 0
            self.rightCircular = 0
            self.leftCircular = 0 
            self.wait = -200
            angle = 0

    def rotatingAttack(self, screen):

        self.rotatingDelay += 5

        #the direction of the cannon
        global direction
        direction = pygame.Vector2(0, 1)

        #making the original images invisible
        self.leftCannon = transparent
        self.rightCannon = transparent

        #pivot point for cannon rotation
        leftPivot = self.leftCannonRect.x + (self.leftCannonRect.width / 2), self.leftCannonRect.y + 10
        rightPivot = self.rightCannonRect.x + (self.rightCannonRect.width / 2), self.rightCannonRect.y + 10

        #the offset that the rectangle will rotate by
        offset = pygame.math.Vector2(0, 50)

        #increasing the angle for rotation
        self.angle += self.leftCannonAngleSpeed

        #rotating the images
        leftRotatedImage, leftRect, direction = rotate(self.leftCannonCopy, self.angle, leftPivot, offset)

        rightRotatedImage, rightRect, direction = rotate(self.rightCannonCopy, self.angle, rightPivot, offset)

        leftPivotCopy = leftRect.centerx + 1, leftRect.centery - 20
        leftRotatedImageCopy, leftRectCopy, direction = rotate(self.leftCannonCopy, self.angle, leftPivotCopy, offset)
        leftRectCopy.bottom += 20
        leftPos = pygame.Vector2(leftRectCopy.center)

        rightPivotCopy = rightRect.centerx + 1, rightRect.centery - 20
        rightRotatedImageCopy, rightRectCopy, direction = rotate(self.rightCannonCopy, self.angle, rightPivotCopy, offset)
        rightRectCopy.bottom += 20
        rightPos = pygame.Vector2(rightRectCopy.center)

        #the delay between each shot
        if self.rotatingDelay % 40 == 0:
            enemyBullet1 = EnemyRotatingBullet(bulletImg, 10, 20, leftPos, direction.normalize(), dt)
            enemyBullet2 = EnemyRotatingBullet(bulletImg, 10, 20, rightPos, direction.normalize(), dt) 
            enemyBullets.add(enemyBullet1, enemyBullet2)

         #blitting the rotated images to its rectangle
        screen.blit(leftRotatedImage, leftRect)
        screen.blit(rightRotatedImage, rightRect)

        #preventing the cannon from rotating over 90 degrees
        if self.angle >= 90:
            self.leftCannonAngleSpeed *= -1
            self.rightCannonAngleSpeed *= -1
            self.rotateCount += 1

        elif self.angle <= -90:
            self.leftCannonAngleSpeed *= -1
            self.rightCannonAngleSpeed *= -1
            self.rotateCount += 1

        if (self.rotateCount == 2) and (self.angle >= 0):
            self.leftCannon = self.leftCannonCopy
            self.rightCannon = self.rightCannonCopy
            self.rotateCount = 0
            self.rotatingDelay = 0
            self.attack = 0
            self.wait = 0


#function that rotates a surface given a surface, angle, pivot, and offset
#returns the rotated surface, its rectangle, and the rectangles direction
def rotate(surface, angle, pivot, offset):
    direction = pygame.Vector2(0, 1).rotate(angle)    
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
    rotated_image = rotated_image.convert_alpha()
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center = pivot + rotated_offset)
    return rotated_image, rect, direction


WIDTH = 480
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps = 60

BLUE = ((0,0,100))
LIGHTBLUE = ((0,0,255))
BLACK = ((0, 0, 0))
TRANSPARENT = (0, 0, 0, 0)
WHITE = ((255, 255, 255))
MAROON = ((115, 0, 0))
bgCount = 0
bgCount2 = -1235
count = 0
right = False
left = False
evadingEnemyAlive = False

#loading in bullet images
bulletImg = pygame.image.load('sprites/Bullets.png')
enemyBulletImg = pygame.image.load('sprites/Enemy_Bullets.png')

#transparent image
transparent = pygame.image.load('sprites/transparent.png')

#loading in enemy images  
kamikaze = [pygame.image.load("sprites/Kamikaze.png"), pygame.image.load("sprites/Kamikaze2.png")]
normal = [pygame.image.load("sprites/Normal.png"),  pygame.image.load("sprites/Normal2.png")]
spray = [pygame.image.load("sprites/Spray.png"), pygame.image.load("sprites/Spray2.png")]
healer2 = [pygame.image.load("sprites/Healer.png"), pygame.image.load("sprites/Healer2.png")]
healer = [pygame.image.load("sprites/Healer3.png"), pygame.image.load("sprites/Healer4.png")]

#loading in the start images
startButtonImg = pygame.image.load('sprites/FinalPi2.png')
selectedStartButtonImg = pygame.image.load('sprites/FinalPi.png')
toggleStraight = [pygame.image.load('sprites/Toggle.png'), pygame.image.load('sprites/Toggle2.png')]
toggleWide = [pygame.image.load('sprites/Toggle3.png'), pygame.image.load('sprites/Toggle4.png')]

#list that will hold all sprite objects
all_sprites = pygame.sprite.Group()

#list that will hold all bullet objects
bullets = pygame.sprite.Group()

#list that will hold all enemy bullet objects 
enemyBullets = pygame.sprite.Group()

#loading in ship sprite and scaling it up
# sprites
Ship = pygame.image.load("sprites/Player_Ship.png")
Ship2 = pygame.image.load("sprites/Player_Ship2.png")
Left = pygame.image.load("sprites/Player_Ship_Left.png")
Left2 = pygame.image.load("sprites/Player_Ship_Left2.png")
Right = pygame.image.load("sprites/Player_Ship_Right.png")
Right2 = pygame.image.load("sprites/Player_Ship_Right2.png")
# scaling
Ship = pygame.transform.scale(Ship, (84, 48))
Ship2 = pygame.transform.scale(Ship2, (84, 48))
Left = pygame.transform.scale(Left, (84, 48))
Left2 = pygame.transform.scale(Left2, (84, 48))
Right = pygame.transform.scale(Right, (84, 48))
Right2 = pygame.transform.scale(Right2, (84, 48))
# sprite lists for animation
char = [Ship, Ship2]
charLeft = [Left, Left2]
charRight = [Right, Right2]

#creating player object 
player = Player(char, WIDTH / 2, HEIGHT + 100, 56, 32)
all_sprites.add(player)

#creating sprite group for the enemies
enemies = pygame.sprite.Group()
enemySprites = [kamikaze, normal, spray, healer]

# background
bg = pygame.image.load("sprites/City_Background.png")

'''uncomment the line that contains the enemy you want to spawn'''
#enemies.add(KamikazeEnemy(enemySprites[0], 10, 3, 3, player))
#enemies.add(NormalEnemy(enemySprites[1], 15, random.randint(-6, 6), random.randint(-6, 6)))
#enemies.add(SplashEnemy(enemySprites[2], 30, 0, 6))
#enemies.add(EvadingEnemy(enemySprites[3], 10, 5, 5, player))
enemies.add(Boss(40))

clock = pygame.time.Clock()

pygame.display.set_caption("First Game")

#creating joystick object
stickX = (WIDTH - (WIDTH / 4))
stickY = (HEIGHT - (HEIGHT / 8))
joystick = Circle(stickX, stickY, TRANSPARENT, 15)
all_sprites.add(joystick)

toggleX = (WIDTH - (5 * WIDTH / 6))
toggleY = (HEIGHT - (HEIGHT / 8))

toggleButton = Button(None, 56, 44, toggleX, toggleY)

#function that will check if mouse is over the joystick
within = (lambda x, low, high: low <= x <= high)

paused = False

movetime = 0


def menu():

    global bgCount
    global bgCount2

    menu = True
        
    startButton = StartButton(startButtonImg)

    while (menu == True):

        try:
            screen.blit(bg, (0, bgCount))
            screen.blit(bg, (0, bgCount2))
            bgCount += 3
            bgCount2 += 3
            if (bgCount >= 720):
                bgCount = bgCount2 - 1235

            if (bgCount2 >= 720):
                bgCount2 = bgCount -1235


            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    menu = False

                if (startButton.clicked()):
                    menu = False
                    game()
                        
            startButton.update(screen)
                
            pygame.display.update()

        except pygame.error:
            return

    pygame.quit()


def game():

    global left
    global right
    global paused
    global count
    global bgCount
    global bgCount2
    global dt

    #will count the delay between each shot
    shootTime = 0

    #boolean that will check if the player is clicking on the joystick
    selected = False

    #boolean that will control the state of the game (running or not running)
    running = True

    #main game loop
    while (running == True):

        #Will add pause function later 
        if (paused == False):

                dt = clock.tick(fps)

                toggleButton = ToggleButton(toggleStraight[0])

                shootTime += 1

                if (shootTime == 10):
                    player.shoot()
                    shootTime = 0
    
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        running = False

                    if (event.type == pygame.KEYDOWN):
                        if (event.button == K_ESCAPE):
                            paused = True

                    if (event.type == pygame.MOUSEBUTTONDOWN):

                        #if the left mouse button has been clicked
                        if (event.button == 1):
                            pos = pygame.mouse.get_pos()

                            #if the mouse is within the joystick
                            if ((within(pos[0], *joystick.x_boundary)
                                and within(pos[1], *joystick.y_boundary))):
                                selected = True
                            
                            if toggleButton.clicked() and Player.straightShot == True:
                                Player.straightShot = False
                                Player.vShot = True

                            elif toggleButton.clicked() and Player.vShot == True:
                                Player.vShot = False 
                                Player.straightShot = True

                            #if the mouse button has been released
                    elif (event.type == pygame.MOUSEBUTTONUP):

                        #move the joystick back to the center of the d-pad
                        joystick.rect.centerx, joystick.rect.centery = stickX, stickY
                        selected = False

                        #if the mouse cursor is over the joystick and the mouse is being pressed
                if (selected):
                    joystick.pos = pygame.mouse.get_pos()
                    joystick.recalc_boundary()
                    joystick.rect.centerx, joystick.rect.centery = pygame.mouse.get_pos()

                    #range checking to make sure the joystick doesn't move beyond the d-pad
                    if (joystick.pos[0] <= (stickX - 20)):
                        pygame.mouse.set_pos((stickX - 19), joystick.pos[1])
                
                    elif (joystick.pos[0] >= (stickX + 20)):
                        pygame.mouse.set_pos((stickX + 19), joystick.pos[1])

                    if (joystick.pos[1] <= (stickY - 20)):
                        pygame.mouse.set_pos(joystick.pos[0], (stickY - 19))

                    elif (joystick.pos[1] >= (stickY + 20)):
                        pygame.mouse.set_pos(joystick.pos[0], (stickY + 19))

                #move the joystick back to the middle of the d-pad
                else:
                    joystick.pos = (stickX, stickY)
                    joystick.recalc_boundary()

                # redraw the window
                screen.blit(bg, (0, bgCount))
                screen.blit(bg, (0, bgCount2))
                bgCount += 5
                bgCount2 += 5
                if (bgCount >= 720):
                    bgCount = bgCount2 - 1235

                if (bgCount2 >= 720):
                    bgCount2 = bgCount -1235


                toggleButton.update(screen)
                        
                #drawing and refreshing the bullets list to check for any action in bullet object
                bullets.update(screen, bulletImg)
                bullets.draw(screen)

                #drawing and refreshing the enemies list to check for any action in enemy object
                enemies.draw(screen)
                enemies.update(screen)

                #drawing and refreshing enemy bullets list to check for any action in enemy bullet object
                enemyBullets.draw(screen)
                enemyBullets.update(screen, enemyBulletImg)

                #refreshing the player to check for any action
                player.update(screen)

                #all_sprites.draw(screen)
                screen.blit(joystick.image, joystick.rect)
                if (left == False and right == False):
                    screen.blit(char[count // 6], player.rect)

                if (left == True):
                    screen.blit(charLeft[count // 6], player.rect)

                if (right == True):
                    screen.blit(charRight[count // 6], player.rect)
                        
                if (count + 1 >= 12):
                    count = 0

                count += 1

                screen.blit(rightImg, (stickX + 20, stickY - 15))
                screen.blit(leftImg, (stickX - 55, stickY - 15))
                screen.blit(upImg, (stickX - 15, stickY - 55))
                screen.blit(downImg, (stickX - 15, stickY + 20))

                pygame.display.update()

        elif (paused == True):
            pause()

    pygame.quit()

menu()