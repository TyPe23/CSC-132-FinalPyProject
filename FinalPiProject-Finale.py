import pygame, time, random, math
from pygame.locals import *
pygame.init()


# class that creates a button 
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

    # checking for collision detection 
    def update(self):
        self.clicked()

    # function that checks if the button has been clicked 
    def clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (self.rect.collidepoint(mouse_pos) and click[0] == 1):
            return True

        else:
            return False


# class that creates start button for the menu (inherits from Button class)
class StartButton(Button):
    def __init__(self, sprite):
        Button.__init__(self, points = None, width = 248, height = 192, x = WIDTH / 4, y = HEIGHT / 3)
        self.sprite = sprite

    # updates collision detection
    def update(self, screen):

        mouse_pos = pygame.mouse.get_pos()

    # if the mouse is over the start button then shade it 
        if (self.rect.collidepoint(mouse_pos)):
            screen.blit(selectedStartButtonImg, self.rect)

    # else do not shade it 
        else:
            screen.blit(self.sprite, self.rect)

# class that creates toggle button for gameplay (inherits from Button class)
class ToggleButton(Button):
    def __init__(self, sprite):
        Button.__init__(self, points = None, width = 56, height = 44, x = toggleX, y = toggleY)
        self.sprite = sprite

    # updates collision detection
    def update(self, screen):

        mouse_pos = pygame.mouse.get_pos()

    # shading the straight shot toggle button based on mouse position
        if (Player.straightShot == True):

            # if the mouse is over the button, shade it
            if (self.rect.collidepoint(mouse_pos)):

                screen.blit(toggleStraight[1], self.rect)

            # if the mouse is not over the button, do not shade it
            else:         
                screen.blit(toggleStraight[0], self.rect)

    # shading the v shot toggle button based on mouse position
        if (Player.vShot == True):

            # if the mouse is over the button, shade it
            if (self.rect.collidepoint(mouse_pos)):        
                screen.blit(toggleWide[1], self.rect)

            # if the mouse is not over the button, do not shade it
            else:         
                screen.blit(toggleWide[0], self.rect)

# class that will create the player 
class Player(pygame.sprite.Sprite):

    straightShot = True
    vShot = False
    hit = False

    def __init__(self, sprite, x, y, width, height, hp):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image =  pygame.Surface((width, height)).convert_alpha()
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.hitDelay = 0
        self.spawn = False

    # updates the health, collision and position
    def update(self, screen):
        global right
        global left
        global rightImg
        global leftImg
        global upImg
        global downImg
        global toggleImg

        if (self.rect.bottom > HEIGHT - 150 and self.spawn == False):
            self.rect.y -= 6

        if (self.rect.bottom < HEIGHT - 150):
            self.spawn = True


    # if the player is not hit check for collision
        if (Player.hit == False):
            self.checkCollision()
            
    # else have a delay before checking collision again
        else:
            self.iFrame()

        if (self.alive() == False):
            Player.hit = False
            Player.straightShot = True
            Player.vShot = False

        #pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
        # creating all the buttons 
        downButton = Button([(stickX - 20, stickY + 30), (stickX, stickY + 70), (stickX + 20, stickY + 30)], 80, 0, stickX - 10, stickY + 20)
        rightButton = Button([(stickX + 70, stickY), (stickX + 30, stickY - 20), (stickX + 30, stickY + 20)], 0, 80, stickX + 25, stickY - 10)
        upButton = Button([(stickX - 20, stickY - 30), (stickX, stickY - 70), (stickX + 20, stickY - 30)], 80, 0, stickX - 10, stickY - 20)
        leftButton = Button([(stickX - 70, stickY), (stickX - 30, stickY - 20), (stickX - 30, stickY + 20)], 0, 80, stickX - 20, stickY - 10)

    # load the correct toggle image 
        if (Player.straightShot == True):
            toggleImg = pygame.image.load("sprites/Joystick/DownArrow.png")

        else:
            toggleImg = pygame.image.load("sprites/Joystick/UpArrow.png")

        if (not pygame.sprite.collide_rect(joystick, rightButton)):
            rightImg = pygame.image.load("sprites/Joystick/RightArrow2.png")
                        
        else:
            rightImg = pygame.image.load("sprites/Joystick/RightArrow.png")

        if (not pygame.sprite.collide_rect(leftButton, joystick)):
            leftImg = pygame.image.load("sprites/Joystick/LeftArrow2.png")

        else:
            leftImg = pygame.image.load("sprites/Joystick/LeftArrow.png")
                        
        if (not pygame.sprite.collide_rect(upButton, joystick)):
            upImg = pygame.image.load("sprites/Joystick/UpArrow2.png") 

        else:
            upImg = pygame.image.load("sprites/Joystick/UpArrow.png")
                        
        if (not pygame.sprite.collide_rect(downButton, joystick)):
            downImg = pygame.image.load("sprites/Joystick/DownArrow2.png")

        else:
            downImg = pygame.image.load("sprites/Joystick/DownArrow.png")

        if ((pygame.sprite.collide_rect(upButton, joystick) and self.rect.y > 15)):
            self.rect.y -= 6

        if ((pygame.sprite.collide_rect(rightButton, joystick) and left == False and self.rect.x < WIDTH - self.rect.width - 45)):
            self.rect.x += 6
            right = True

        if ((pygame.sprite.collide_rect(downButton, joystick) and self.rect.y < HEIGHT - self.rect.height - 45)):
            self.rect.y += 6                       

        if ((pygame.sprite.collide_rect(leftButton, joystick) and right == False and self.rect.x > 5)):
            self.rect.x -= 6
            left = True

    # function that creates a bullet object 
    def shoot(self):
        
    # shoot in a straight line if straightShot is true
        if ((self.rect.bottom <= HEIGHT - 30) and (Player.straightShot == True)):
            bullet1 = Bullet(self.rect.x + 30, self.rect.y - 7, 12, 14, 0, -11)
            bullet2 = Bullet(self.rect.x - 3, self.rect.y - 7, 12, 14, 0, -11)
            bullet3 = Bullet(self.rect.x + 37, self.rect.y - 7, 12, 14, 0, -11)
            bullet4 = Bullet(self.rect.x - 10, self.rect.y - 7, 12, 14, 0, -11)
            bullets.add(bullet1, bullet2, bullet3, bullet4)

    # else shoot in a v shape if vShot is true
        elif ((self.rect.bottom <= HEIGHT - 30) and (Player.vShot == True)):
            bullet1 = Bullet(self.rect.x + 30, self.rect.y - 7, 12, 14, 0, -11)
            bullet2 = Bullet(self.rect.x - 3, self.rect.y - 7, 12, 14, 0, -11)
            bullet3 = Bullet(self.rect.x + 30, self.rect.y - 7, 12, 14, 5, -11)
            bullet4 = Bullet(self.rect.x - 3, self.rect.y - 7, 12, 14, -5, -11)
            bullets.add(bullet1, bullet2, bullet3, bullet4)

    # function that checks for collision regarding the player 
    def checkCollision(self):

    # for every enemy bullet that is currently on the screen
        for bullet in enemyBullets:

        # if any of the bullets collide with the player 
            if (pygame.sprite.collide_rect(self, bullet)):

        # if the player is not dead
                if (self.hp > 0):

            # decrease player health by 1 
                    self.hp -= 1

            # kill the bullet that hit the player 
                    bullet.kill()

            # indicate that the player has been hit
                    Player.hit = True

    # if the player hp is zero
        if (self.hp <= 0):

        # kill the player 
            self.kill()

    # function to check if the player is alive 
    def alive(self):
        if (self.hp > 0):
            return True

        else:
            return False

    # function that creates a delay everytime the player is shot
    # the player will not take damage until the delay is over
    def iFrame(self):

    # incrementing the delay
        self.hitDelay += 1
        
    # once the delay reaches a certain value
        if (self.hitDelay >= 250):

        # allow the player to check for collision again
            Player.hit = False

        # reset the delay 
            self.hitDelay = 0

# class that creates a basic bullet 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Misc/Bullets.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = vx
        self.y_speed = vy

    # updates the collision and position
    def update(self, screen, bulletImg):

        # blit the given sprite to the bullet rect
        screen.blit(bulletImg, self.rect)

        # if it goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()
                
        # make it shoot upwards
        self.rect.x +=  self.x_speed
        self.rect.y += self.y_speed


# class that creates enemy bullets
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Misc/Enemy_Bullets.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = vx
        self.y_speed = vy

    # updates the collision and position
    def update(self, screen, enemyBulletImg):

        # blit the given sprite to the bullet rect
        screen.blit(enemyBulletImg, self.rect)

    # check if the bullet has gone offscreen
        self.offScreen()
                
        # make it shoot upwards
        self.rect.x +=  self.x_speed
        self.rect.y += self.y_speed

    # function that checks whether the bullet has gone off the screen
    def offScreen(self):

        # if bullet goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()

        elif (self.rect.top > HEIGHT):
            self.kill()

        elif (self.rect.left + self.rect.width > WIDTH):
            self.kill()

        elif (self.rect.right - self.rect.width < 0):
            self.kill()


# bullet that will have the ability to shoot in a circular pattern
class EnemyCircularBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Misc/Enemy_Bullets.png')
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

    # updates the collision and position
    def update(self, screen, enemyBulletImg):

        # blit the given sprite to the bullet rect
        screen.blit(enemyBulletImg, self.rect)

        # check if the bullet is off the screen
        self.offScreen()

    # change the bullet's position according to its speed
        self.posx += self.x_speed
        self.posy += self.y_speed

    # change the bullet's actual position with previously calculated values  
        self.rect.center = (self.posx, self.posy)

    # function that checks if the bullet has gone off the screen
    def offScreen(self):

        # if bullet goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()

        elif (self.rect.top > HEIGHT):
            self.kill()

        elif (self.rect.left + self.rect.width > WIDTH):
            self.kill()

        elif (self.rect.right - self.rect.width < 0):
            self.kill()


# bullet that will have the ability to shoot in a circular pattern for the unhittable cannons
class EnemyCircularBullet2(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Misc/Enemy_Bullets2.png')
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

    # updates the collision and position
    def update(self, screen, enemyBulletImg):

        # blit the given sprite to the bullet rect
        screen.blit(pygame.image.load('sprites/Misc/Enemy_Bullets2.png'), self.rect)

        # check if the bullet is off the screen
        self.offScreen()

    # change the bullet's position according to its speed
        self.posx += self.x_speed
        self.posy += self.y_speed

    # change the bullet's actual position with previously calculated values         
        self.rect.center = (self.posx, self.posy)

    # function that checks if the bullet has gone off the screen
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

# class that creates a bullet that can shoot while an object is rotating
class EnemyRotatingBullet(pygame.sprite.Sprite):
    def __init__(self, sprite, width, height, pos, direction, dt):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image = pygame.image.load('sprites/Misc/Enemy_Bullets.png')
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.dt = dt

    # updates the collision and position
    def update(self, screen, enemyBulletImg):

    # blit the bullet image to its rectangle
        screen.blit(enemyBulletImg, self.rect)
        
    # check if the bullet has gone off the screen
        self.offScreen()

    # change the bullet's position based of the given direction
        self.pos += self.direction * (self.dt / 3)

    # change the bullet's actual position based off the previously calculated values
        self.rect.center = self.pos

    # function that checks if the bullet has gone off the screen
    def offScreen(self):

        # if bullet goes off the screen then kill it
        if (self.rect.bottom < 0):
            self.kill()

        elif (self.rect.top > HEIGHT):
            self.kill()

        elif (self.rect.left + self.rect.width > WIDTH):
            self.kill()

        elif (self.rect.right - self.rect.width < 0):
            self.kill()


# class that creates the circle inside the d-pad
class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.pos = (x, y)
        self.image = pygame.image.load("sprites/Joystick/Joystick.png")
        self.rect = self.image.get_rect(center = self.pos)
        self.x_boundary = (x - radius, x + radius)
        self.y_boundary = (y - radius, y + radius)
        self.color = color
        self.radius = radius

    # function that will redraw the circle as it is being moved
    def recalc_boundary(self):
        self.x_boundary = (self.pos[0] - self.radius, self.pos[0] + self.radius)
        self.y_boundary = (self.pos[1] - self.radius, self.pos[1] + self.radius)


# class that provides basic skeleton for enemy creation
class Enemy(pygame.sprite.Sprite):

    evadingEnemyAlive = False
    move = False

    def __init__(self, sprite, hp, x_speed, y_speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image = image
        self.image.fill((255, 255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0 + self.rect.width, WIDTH - self.rect.width)
        self.rect.bottom = -150
        self.hit = False
        self.hitDelay = 50

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.hp = hp

    # function that checks for bullet collision with the enemy 
    def checkCollision(self):

    # for every bullet that is created by the player and is on the screen
        for bullet in bullets:

        # if any of the bullets collide with the enemy
            if (pygame.sprite.collide_rect(self, bullet)):

        # if the enemy is not dead 
                if (self.hp > 0):

            # decrease its health by one 
                    self.hp -= 1

            # indicate that it has been hit
                    self.hit = True

        # kill the bullet that hit it
                bullet.kill()

    # if the enemy is dead 
        if (self.hp <= 0):

        #start the decrementing the hit delay 
            self.hitDelay -= 1

        # while the hit delay is not below zero
            if (self.hitDelay >= 0):

        #show the explosion animations 
                screen.blit(explosion[count // 6], self.rect)

        # once the delay reaches below zero 
            else:

        #kill itself
                self.kill()

    # function that checks if the enemy is alive
    def alive(self):

        if (self.hp > 0):

            return True
        
        else:

            return False


# class that creates the normal enemies (inherits from Enemy class)
class NormalEnemy(Enemy):
    def __init__(self, sprite, hp, x_speed, y_speed):
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((40, 41)).convert_alpha())
        self.sprite = sprite
        self.hp = hp
        self.x_speed = x_speed if (x_speed > 2 or x_speed < -2) else 3
        self.y_speed = y_speed if (x_speed > 2 or x_speed < -2) else 3
        self.xdirection = 1
        self.ydirection = 1
        self.delay = random.randint(-400, -100)

    # updates the health, collision and position
    def update(self, screen):

    # if the evading enemy is alive, blit the invulnerable sprite to its rectangle 
        screen.blit(normalInvul[count // 6], self.rect)

    # if the evading enemy is dead 
        if (Enemy.evadingEnemyAlive == False):

        # blit the normal sprite to its rectangle 
            screen.blit(normal[count // 6], self.rect)

        # check for collision
            self.checkCollision()

    # increment the move delay
        if (self.delay <= 0):
            self.delay += 1
            
    # once the move delay reaches a certain value, allow it to move 
        elif ((self.rect.top < 0) and (self.delay >= 0)):

        # cannot be hit while it is not on the screen
            self.hit = False

            self.rect.y += 6
            
        else:

        # if it has been hit
            if (self.hit == True):

        # blit the hit sprite 
                screen.blit(normalHit[count // 6], self.rect)

        # if it is dead, do not allow it to move 
            if (self.alive() == False):
                self.x_speed = 0
                self.y_speed = 0

        # consistently shooting while it is on the screen and alive 
            self.shoot()

        # having it move based on its direction and speed 
            self.rect.x += self.x_speed * self.xdirection
            self.rect.y += self.y_speed * self.ydirection

        # if it hits the side of the screen
            if ((self.rect.left <= 0) or (self.rect.left + self.rect.width >= WIDTH)):

        # flip its x direction
                self.xdirection *= -1

        # pick a random y speed
                self.y_speed = random.uniform(3, 6)

        # if it hits the top of the screen or the bottom barrier 
            if ((self.rect.bottom > 450) or (self.rect.top <= 0)): 

        # flip its y direction
                self.ydirection *= -1

        # pick a random x speed 
                self.x_speed = random.uniform(3, 6)

    # always setting the default value of hit to be false
        self.hit = False

    # function that allows the normal enemy to shoot           
    def shoot(self):

    # if the random number generated is 0 and it is alive then shoot  
        if (random.randrange(20) == 0 and self.alive() == True):
            enemyBullet = EnemyBullet(self.rect.centerx, self.rect.top + self.rect.height, 10, 20, 0, 6)
            enemyBullets.add(enemyBullet)


# class that creates the splash enemies (inherits from Enemy class)
class SplashEnemy(Enemy):
    def __init__(self, sprite, hp, x_speed, y_speed):
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((72, 60)).convert_alpha())
        self.sprite = sprite
        self.hp = hp
        self.x_speed = x_speed
        self.y_speed = y_speed

    # updates the health, collision and position
    def update(self, screen):

    # blit its sprite to its rectangle
        screen.blit(spray[count // 6], self.rect)

        # checking for collision
        self.checkCollision()

    # if it has been hit
        if (self.hit == True):

        # blit the hit sprite to its rectangle 
            screen.blit(sprayHit[count // 6], self.rect)

    # if it is no longer alive, do not allow it to move 
        if (self.alive() == False):
                self.x_speed = 0
                self.y_speed = 0

    # if it has not reached its destination
        if (self.rect.bottom < 400):
            self.rect.y += self.y_speed

        else:

        # do not allow it to move 
            self.rect.y += 0

        # have it consistenly shoot while it is alive 
            self.shoot()

    # setting the default value of hit to be false 
        self.hit = False

    # function that allows the splash enemy to shoot 
    def shoot(self):

        # if it is alive then shoot 
        if (self.alive() == True) and count % 3 == 0:
            enemyBullet1 = EnemyBullet(self.rect.centerx + 23, self.rect.top + self.rect.height, 10, 20, random.randint(1, 2), random.uniform(3.5, 7.5))
            enemyBullet2 = EnemyBullet(self.rect.centerx - 35, self.rect.top + self.rect.height, 10, 20, random.randint(-2, -1), random.uniform(3.5, 7.5))
            enemyBullets.add(enemyBullet1, enemyBullet2)


# class that creates the evading, or the healer, enemies (inherits from Enemy class)
class EvadingEnemy(Enemy):

    edge = False
    leftMove = False
    rightMove = False

    def __init__(self, sprite, hp, x_speed, y_speed, player):       
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((72, 80)).convert_alpha())
        self.sprite = sprite
        self.hp = hp
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.player = player

    # updates the health, collision and position
    def update(self, screen):

    # upon its instantiation, indicate it is alive 
        Enemy.evadingEnemyAlive = True

    # when it dies indicate it has died and do not allow it to move 
        if (self.alive() == False):
            Enemy.evadingEnemyAlive = False
            self.x_speed = 0
            self.y_speed = 0

    # variable that calculates the x distance between the healer and the player 
        global xDist
        xDist = (self.rect.centerx - self.player.rect.centerx)

    # checking if the healer has hit the edge of the screen
        self.offScreen()

    # if it has reached its destination
        if (self.rect.top >= 300):

        #blit the default healer sprite
            screen.blit(healer[count // 6], self.rect)

    # until it reaches its destination
        else:

        # blit the moving healer sprite 
            screen.blit(healer2[count // 6], self.rect)

    # checking for collision
        self.checkCollision()

    # if the x distance between the healer and player is less than zero
        if (xDist < 0):

        # have the healer move in the opposite direction
            xDist *= -1

    # if it has not reached its destination
        if (self.rect.top < 300):

        #change its y position
            self.rect.y += 6

        # if it has been hit 
        if (self.hit == True):

            # if it has reached its destination
            if (self.rect.top >= 300):

        # blit the hit sprite for the default healer sprite 
                screen.blit(healerHit[count // 6], self.rect)

        # if it is still moving 
            else:

                # blit the hit sprite for the moving healer sprite 
                screen.blit(healerHit2[count // 6], self.rect)

        else:

        # if it has not hit the edge
            if ((EvadingEnemy.edge == False) and (EvadingEnemy.leftMove == False) and (EvadingEnemy.rightMove == False)):

        # if the player is to right of the healer and is a certain x distance from the player 
                if ((self.rect.x < self.player.rect.x) and (xDist < 185)):

            # move to the left 
                    self.rect.x -= self.x_speed
            
        # if the player is to left of the healer and is a certain x distance from the player 
                elif ((self.rect.x > self.player.rect.x) and (xDist < 150)):

            # move to the right 
                    self.rect.x += self.x_speed

        # indicate the left edge move needs to happen if the healer has hit the left side of the screen
            elif (EvadingEnemy.edge == True and self.offScreen() == 1):
                EvadingEnemy.leftMove = True

        # indicate the right edge move needs to happen if the healer has hit the right side of the screen
            elif (EvadingEnemy.edge == True and self.offScreen() == 2):
                EvadingEnemy.rightMove = True
    
        # if the left edge move has been triggered 
            if (EvadingEnemy.leftMove == True):

        # if the player is so far away from the healer then do not move 
                if ((self.rect.left + self.rect.width) < self.player.rect.left):
                    self.rect.x += 0

        # if the player is close enough move accordingly 
                else:
                    self.leftScreenCollison()

        # if the right edge move has been triggered 
            elif (EvadingEnemy.rightMove == True):

        # if the player is so far away from the healer then do not move 
                if ((self.player.rect.left + self.player.rect.width) < self.rect.left):
                    self.rect.x += 0
                
        # if the player is close enough move accordingly 
                else:
                    self.rightScreenCollison()

    # always setting the default value of hit to be false
        self.hit = False

    # function that checks whether the healer has hit the edge 
    def offScreen(self):

    # return a 1 if the healer hits the left side of the screen
        if (self.rect.left <= 0):
            EvadingEnemy.edge = True
            return 1

    # return a 2 if the healer has hit the right side of the screen
        if(self.rect.left + self.rect.width >= WIDTH):
            EvadingEnemy.edge = True
            return 2

    # function that handles the event of the healer hitting the left side of the screen
    def leftScreenCollison(self):

    # move a certain x distance away from the edge
        if (self.rect.x <= self.rect.width):
            self.rect.x += self.x_speed

    # indicate the healer is no longer on or near the edge 
        else:
            EvadingEnemy.leftMove = False
            EvadingEnemy.edge = False

    # function that handles the event of the healer hitting the right side of the screen
    def rightScreenCollison(self):

    # move a certain x distance away from the edge
        if (self.rect.x >= (WIDTH - (self.rect.width * 2))):
            self.rect.x -= self.x_speed

    # indicate the healer is no longer on or near the edge 
        else:
            EvadingEnemy.rightMove = False
            EvadingEnemy.edge = False

# class that creates the kamikaze enemies (inherits from Enemy class)
class KamikazeEnemy(Enemy):
    def __init__(self, sprite, hp, x_speed, y_speed, player):       
        Enemy.__init__(self, sprite, hp, x_speed, y_speed, pygame.Surface((40, 41)).convert_alpha())
        self.sprite = sprite
        self.hp = 10
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.player = player

    # updates the health, collision and position
    def update(self, screen):

    # blit the kamikaze sprite to its rectangle
        screen.blit(kamikaze[count // 6], self.rect)

    # if it is no longer alive, do not allow it to move 
        if (self.alive() == False):
                self.x_speed = 0
                self.y_speed = 0

    # checking for collision
        self.checkCollision()

    # if it is not on the screen change its y position
        if (self.rect.top < 0):
            self.rect.y += 6

    # if it has been hit
        if (self.hit == True):

        # blit the hit sprite to its rectangle 
            screen.blit(kamikazeHit[count // 6], self.rect)

        else:
        # following the player based on the player's x position
            if (self.rect.x < self.player.rect.x):
                self.rect.x += self.x_speed
            
            elif (self.rect.x > self.player.rect.x):
                self.rect.x -= self.x_speed
                                
        # following the player based on the player's y position
            if (self.rect.y < self.player.rect.y):
                self.rect.y += self.y_speed
            
            elif (self.rect.y > self.player.rect.y):
                self.rect.y -= self.y_speed

    # always setting the default value of hit to be false 
        self.hit = False

# class that creates the boss 
class Boss(pygame.sprite.Sprite):

    def __init__(self, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/Enemies/Boss_Base.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = -150
        self.hp = hp
        self.hitDelay = 50
        self.hitDelay2 = 50
        self.hitDelay3 = 200

        # creating left cannon
        self.leftCannon = pygame.image.load('sprites/Enemies/Boss_Gun.png')
        self.leftCannonRect = self.leftCannon.get_rect()
        self.leftCannonRect.x = self.rect.width - 389
        self.leftCannonRect.y = self.rect.height
        self.leftCannonAngleSpeed = 1
        self.leftCannonCopy = self.leftCannon
        self.leftCannonHP = self.hp

        # creating right cannon
        self.rightCannon = pygame.image.load("sprites/Enemies/Boss_Gun.png")
        self.rightCannonRect = self.rightCannon.get_rect()
        self.rightCannonRect.x = self.rect.width - 88
        self.rightCannonRect.y = self.rect.height 
        self.rightCannonAngleSpeed = -1
        self.rightCannonCopy = self.rightCannon
        self.rightCannonHP = self.hp

        # creating the final hit point once both cannons are dead
        self.finalHitpoint = pygame.Surface((138, 98))
        self.finalHitpointRect = self.finalHitpoint.get_rect()
        self.finalHitpointRect.left = 172
        self.finalHitpointRect.y = self.rect.y - 20
        self.finalHitpointHP = self.hp / 2

        # time to wait between each attack
        self.wait = 0

        # time before splash attack starts
        self.splashWait = 0

        # duration of splash attack
        self.splash = 0

        # timer that will handle delay between each spray shoot (bullets would
        # shoot continuously otherwise)
        self.sprayShootDelay = 0

        # duration of left spray attack
        self.leftSpray = 0

        # duration of right spray attack
        self.rightSpray = 0

        # duration of circular attack
        self.leftCircular = 0
        self.rightCircular = 0

        # timer that will handle delay between each circular shot (bullets would
        # shoot continuously otherwise)
        self.circularDelay = 0

        # will determine which attack is executed
        self.attack = 0

        # keeps track of the attack previously executed 
        self.oldAttack = 0 

        # angle that the cannon will be rotating by during rotating attack
        self.angle = 0

    # delay between each rotating attack shot 
        self.rotatingDelay = 0

        # variable to keep track of how many times surface has rotated 90 degrees
        self.rotateCount = 0

    # delay between the untouchable cannons' attacks
        self.untouchableCannonDelay = 0

    def update(self, screen):

        global rightCannonHit
        global leftCannonHit
        global finalHitPointHit

    # blit the left and right cannons to the screen
        screen.blit(self.leftCannon, self.leftCannonRect)
        screen.blit(self.rightCannon, self.rightCannonRect)
        
    # if the boss has not reached its destination
        if (self.rect.top <= 0):

        # move itself and every other cannon accordingly 
            self.rect.y += 6
            self.leftCannonRect.y = self.rect.y + 45
            self.rightCannonRect.y = self.rect.y + 45
            self.finalHitpointRect.y = self.rect.y + 20

        else:  

        # check for collisions with the left and right cannnons 
            self.cannonCollision(screen)

        # if the rotating attack is not happening and the left cannon has been hit 
            if ((self.attack != 4) and (leftCannonHit == True)):

            # blit the hit sprite to the left cannon's rectangle 
                    screen.blit(pygame.image.load('sprites/Enemies/Boss_GunHit.png'), self.leftCannonRect)

        # if the rotating attack is not happening and the right cannon has been hit 
            elif ((self.attack != 4) and (rightCannonHit == True)):

            # blit the hit sprite to the right cannon's rectangle
                    screen.blit(pygame.image.load('sprites/Enemies/Boss_GunHit.png'), self.rightCannonRect)

        # incrementing the wait time between each attack
            self.wait += 1

        # incrementing the delay between the untouchable cannon attack
            self.untouchableCannonDelay += 0.5

        # if the wait value has reached a hundred
            if (self.wait == 100):

        # choose one of the four attacks randomly 
                attack = random.randint(1, 4)
                
        # if the attack chosen is the same as the previous attack
                if (attack == self.oldAttack):
                    
            # if the attack is four, have it be one
                    if (attack == 4):
                        self.attack = 1

            # have the attack be whatever the previous attack was plus one 
                    else:
                        self.attack = self.oldAttack + 1

                elif (attack == 1):
                    self.attack = 1

                elif (attack == 2):
                    self.attack = 2

                elif (attack == 3):
                    self.attack = 3

                elif (attack == 4):
                    self.attack = 4
                
        # keeping track of the attack happening 
                self.oldAttack = self.attack

            if (self.attack == 1):
                self.splashAttack()

            elif (self.attack == 2):
                self.sprayAttack()
            
            elif (self.attack == 3):
                self.circularAttack()

            elif (self.attack == 4):
                self.rotatingAttack(screen)
        
            # having the untouchable cannons shoot after a certain amount of time
            if ((self.untouchableCannonDelay % 50 == 0) and ((self.rightCannonHP > 0) or (self.leftCannonHP > 0)) and self.attack != 1):
                enemyBullet1 = EnemyCircularBullet2(153, 60, 10, 20, -90)
                enemyBullet2 = EnemyCircularBullet2(153, 60, 10, 20, -110)
                enemyBullet3 = EnemyCircularBullet2(153, 60, 10, 20, -70)
                enemyBullet4 = EnemyCircularBullet2(318, 60, 10, 20, -90)
                enemyBullet5 = EnemyCircularBullet2(318, 60, 10, 20, -110)
                enemyBullet6 = EnemyCircularBullet2(318, 60, 10, 20, -70)
                enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4, enemyBullet5, enemyBullet6)
                self.untouchableCannonDelay = 0

        # having the untouchable cannons shoot five bullets if both cannons are dead 
            elif ((self.untouchableCannonDelay % 50 == 0) and (self.leftCannonHP <= 0) and (self.rightCannonHP <=  0) and (self.finalHitpointHP > 0)):
                enemyBullet1 = EnemyCircularBullet2(153, 60, 10, 20, -90)
                enemyBullet2 = EnemyCircularBullet2(153, 60, 10, 20, -110)
                enemyBullet3 = EnemyCircularBullet2(153, 60, 10, 20, -70)
                enemyBullet4 = EnemyCircularBullet2(153, 60, 10, 20, -50)
                enemyBullet5 = EnemyCircularBullet2(153, 60, 10, 20, -130)
                enemyBullet6 = EnemyCircularBullet2(318, 60, 10, 20, -90)
                enemyBullet7 = EnemyCircularBullet2(318, 60, 10, 20, -110)
                enemyBullet8 = EnemyCircularBullet2(318, 60, 10, 20, -70)
                enemyBullet9 = EnemyCircularBullet2(318, 60, 10, 20, -50)
                enemyBullet10 = EnemyCircularBullet2(318, 60, 10, 20, -130)
                enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4, enemyBullet5, enemyBullet6,enemyBullet7, enemyBullet8, enemyBullet9, enemyBullet10)
                self.untouchableCannonDelay = 0

    # always set the default values of hit to be false
        leftCannonHit = False
        rightCannonHit = False
        finalHitPointHit = False

    # function that handles collisions with the left and right cannon
    def cannonCollision(self, screen):

        global rightCannonHit
        global leftCannonHit
        
    # for every bullet created by the player that is on the screen
        for bullet in bullets:

        # if any bullet collides with the right cannon 
            if (self.rightCannonRect.colliderect(bullet)):

                # if the right cannon is not dead 
                if (self.rightCannonHP > 0):

            #decrease its health by one 
                    self.rightCannonHP -= 1

            #indicate it has been hit 
                    rightCannonHit = True

            #kill the bullet that hit it 
                    bullet.kill()

        # if any bullet collides with the left cannon
            if (self.leftCannonRect.colliderect(bullet)):

        # if the left cannon is not dead 
                if (self.leftCannonHP > 0):

            # decrease its health by one 
                    self.leftCannonHP -= 1

            # indicate it has been hit
                    leftCannonHit = True

            # kill the bullet that hit it 
                    bullet.kill()

    # if the left cannon is dead, play its death animation
        if (self.leftCannonHP <= 0):
            screen.blit(brokenGun[count // 6], self.leftCannonRect)
            if (self.hitDelay >= 0):
                self.hitDelay -= 1
                screen.blit(explosion[count // 6], \
                            (self.leftCannonRect.x - 20, self.leftCannonRect.y))
                
    # if the right cannon is dead, play its death animation
        if (self.rightCannonHP <= 0):
            screen.blit(brokenGun[count // 6], self.rightCannonRect)
            if (self.hitDelay2 >= 0):
                self.hitDelay2 -= 1
                screen.blit(explosion[count // 6], \
                            (self.rightCannonRect.x - 20, self.rightCannonRect.y))

    # if both of the cannons are dead, stop the attacks and spawn in the final hit point 
        if (self.leftCannonHP == 0 and self.rightCannonHP == 0):
            self.attack = 0
            self.wait = 0 
            self.finalHitPointCollision()

    # function that handles collisions with the final hit point 
    def finalHitPointCollision(self):
        global finalHitPointHit
        
    # for every bullet created by the player that is on the screen
        for bullet in bullets:

        # if the bullets collide with the hitpoint and the hitpoint's health is greater than zero
            if ((self.finalHitpointRect.colliderect(bullet)) and (self.finalHitpointHP > 0)):

        # blit the damaged skull sprite to its rectangle
                screen.blit(pygame.image.load('sprites/Enemies/Boss_SkullHit.png'), self.rect)

        # decrease the final hitpoint hp by one 
                self.finalHitpointHP -= 1

        # indicate that the final hit point has been hit 
                finalHitPointHit = True

        # kill the bullet that hit it 
                bullet.kill()
        
    # if the final hitpoint is dead, have the death animation play
        if (self.finalHitpointHP <= 0):
            screen.blit(brokenSkull[count // 6], self.rect)
            if (self.hitDelay3 >= 0):
                self.hitDelay3 -= 1
                screen.blit(explosion[count // 6], \
                            (self.leftCannonRect.x - 20, self.leftCannonRect.y))
                screen.blit(explosion[count // 6], \
                            (self.rightCannonRect.x - 20, self.rightCannonRect.y))
                screen.blit(explosion[count // 6], \
                            (random.randint(0, 400), random.randint(0, 100)))
            else:

        # then promplty kill it 
                self.kill()

    # function that executes a splash shooting attack
    def splashAttack(self):

        # have a waiting period before the attack happens 
            self.splashWait += 1
            
        # once the delay has reached a certain value, then shoot
            if (self.splashWait >= 149):

        # if the attack delay has not reached a certain value 
                if (self.splash < 99):
                    enemyBullet1 = EnemyBullet(self.leftCannonRect.centerx - 4, self.leftCannonRect.top + self.leftCannonRect.height - 10, 10, 20, random.randint(0, 2), random.uniform(3.5, 7.5))
                    enemyBullet2 = EnemyBullet(self.leftCannonRect.centerx - 4, self.leftCannonRect.top + self.leftCannonRect.height - 10, 10, 20, random.randint(-2, 0), random.uniform(3.5, 7.5))
                    enemyBullet3 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 10, 10, 20, random.randint(0, 2), random.uniform(3.5, 7.5))
                    enemyBullet4 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 10, 10, 20, random.randint(-2, 0), random.uniform(3.5, 7.5))        
                    
            # have the left cannon shoot even if the right cannon is dead 
                    if (self.leftCannonHP > 0 and self.rightCannonHP <= 0 and count % 3 == 0):
                        enemyBullets.add(enemyBullet1, enemyBullet2)

            # have the right cannon shoot even if the left cannon is dead 
                    elif (self.rightCannonHP > 0 and self.leftCannonHP <= 0 and count % 3 == 0):
                        enemyBullets.add(enemyBullet3, enemyBullet4)

            # if neither of them are dead, then have both of the cannons shoot 
                    elif (count % 3 == 0):
                        enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4)
                        
            # increase the attack time delay
                    self.splash += 1

                else:
                    self.splash = 0
                    self.splashWait = 0
                    self.wait = -150
                    self.attack = 0
    
    # function that executes a basic spray attack
    def sprayAttack(self):

    # increase the shot delay 
        self.sprayShootDelay += 1

    # if the left cannon delay is less than 99 and the left cannon is not dead 
        if (self.leftSpray < 99 and self.leftCannonHP > 0):

            # if the shooting delay is divisble by ten, then shoot 
            if (self.sprayShootDelay % 10 == 0):
                enemyBullet1 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 0, 5)
                enemyBullet2 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 1, 5)    
                enemyBullet3 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 2, 5)    
                enemyBullet4 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 3, 5)    
                enemyBullet5 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 4, 5)    
                enemyBullet6 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 5, 5)
                enemyBullet7 = EnemyBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.top + self.leftCannonRect.height - 5, 10, 20, 6, 5)            
                enemyBullets.add(enemyBullet1, enemyBullet2, enemyBullet3, enemyBullet4, enemyBullet5, enemyBullet6, enemyBullet7)

        # increasing the delay of the left cannon shooting 
            self.leftSpray += 1

    # if the left cannon's shooting delay has reached a certain value, have the right cannon shoot if it is not dead
        elif ((self.leftSpray >= 99 and self.rightSpray < 200 and self.rightCannonHP > 0) or (self.rightSpray < 99 and self.rightCannonHP > 0)):

        # once the shooting delay reaches 200 and is divisible by ten, then shoot 
            if (self.sprayShootDelay % 10 == 0) and (self.sprayShootDelay > 200):
                enemyBullet8 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, 0, 5)
                enemyBullet9 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -1, 5)    
                enemyBullet10 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -2, 5)    
                enemyBullet11 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -3, 5)    
                enemyBullet12 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -4, 5)    
                enemyBullet13 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -5, 5)
                enemyBullet14 = EnemyBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.top + self.rightCannonRect.height - 7, 10, 20, -6, 5)            
                enemyBullets.add(enemyBullet8, enemyBullet9, enemyBullet10, enemyBullet11, enemyBullet12, enemyBullet13, enemyBullet14)
            self.rightSpray += 1

        else:
            self.leftSpray = 0
            self.rightSpray = 0
            self.sprayShootDelay = 0
            self.wait = -100
            self.attack = 0

    # function that executes a circular shooting attack
    def circularAttack(self):

    # set the value for the angle to be shot at 
        angle = 20

    # increase the shot delay 
        self.circularDelay += 1

    # if the right cannon delay is less than 99 and the right cannon is not dead 
        if (self.rightCircular < 99 and self.rightCannonHP > 0):

        # once the shot delay is divisible by ten, then shoot 
            if (self.circularDelay % 10 == 0):

        # create twelve bullets and increment the angle by twenty each time a bullet is shot
                for x in range (12):
                    enemyBullet = EnemyCircularBullet(self.rightCannonRect.centerx - 4, self.rightCannonRect.centery + (self.rightCannonRect.height / 2) - 10, 10, 20, angle)
                    enemyBullets.add(enemyBullet)
                    angle -= 20 if angle <= 140 else 140

        # increase the delay of the right cannon shooting 
            self.rightCircular += 1

    # if the right cannon's shooting delay has reached a certain value, have the left cannon shoot if it is not dead 
        elif ((self.rightCircular >= 99 and self.leftCircular < 99 and self.leftCannonHP > 0) or (self.leftCircular < 99 and self.leftCannonHP > 0)): 

        # setting the angle back to twenty 
            angle = 20

        # once the shot delay is divisible by ten, then shoot 
            if (self.circularDelay % 10 == 0):

        # create twelve bullets and increment the angle by twenty each time a bullet is shot
                for x in range (12):
                    enemyBullet = EnemyCircularBullet(self.leftCannonRect.centerx - 2, self.leftCannonRect.centery + (self.leftCannonRect.height / 2) - 8, 10, 20, angle)
                    enemyBullets.add(enemyBullet)
                    angle -= 20 if angle <= 140 else 140
            
        # increase the delay of the left cannon shooting 
            self.leftCircular += 1

        else:
            self.circularDelay = 0
            self.rightCircular = 0
            self.leftCircular = 0 
            self.attack = 0
            self.wait = -200

    # function that will execute a rotating shooting attack
    def rotatingAttack(self, screen):

    # start incrementing the delay 
        self.rotatingDelay += 5

        # the direction of the cannon
        global direction
        direction = pygame.Vector2(0, 1)

        # pivot point for cannon rotation
        leftPivot = self.leftCannonRect.x + (self.leftCannonRect.width / 2), self.leftCannonRect.y + 10

        # the offset that the rectangle will rotate by
        offset = pygame.math.Vector2(0, 50)

        # increasing the angle for rotation
        self.angle += self.leftCannonAngleSpeed

        # if the right cannon still has health
        if (self.rightCannonHP > 0):

            # making the original image invisible
            self.rightCannon = transparent

            # pivot point for cannon rotation
            rightPivot = self.rightCannonRect.x + (self.rightCannonRect.width / 2), self.rightCannonRect.y + 10

            # rotating the image
            rightRotatedImage, rightRect, direction = rotate(self.rightCannonCopy, self.angle, rightPivot, offset)
            rightHit, rightRect2, direction2 = rotate(pygame.image.load('sprites/Enemies/Boss_GunHit.png'), self.angle, rightPivot, offset)

            # making a copy of the rotated image so the shooting will be aligned with the image of the cannon
            rightPivotCopy = rightRect.centerx + 1, rightRect.centery - 20
            rightRotatedImageCopy, rightRectCopy, direction = rotate(self.rightCannonCopy, self.angle, rightPivotCopy, offset)
            rightRectCopy.bottom += 20
            rightPos = pygame.Vector2(rightRectCopy.center)

            # blitting the rotated images to its rectangle based on whether the cannon has been hit or not 
            if (rightCannonHit == True):
                screen.blit(rightHit, rightRect2)

            else:
                screen.blit(rightRotatedImage, rightRect)

            # the delay between each shot
            if (self.rotatingDelay % 40 == 0):
                enemyBullet = EnemyRotatingBullet(bulletImg, 10, 20, rightPos, direction.normalize(), 20) 
                enemyBullets.add(enemyBullet)

        # if the left cannon still has health 
        if (self.leftCannonHP > 0):

            # making the original image invisible
            self.leftCannon = transparent

            # pivot point for cannon rotation
            leftPivot = self.leftCannonRect.x + (self.leftCannonRect.width / 2), self.leftCannonRect.y + 10

            # rotating the image
            leftRotatedImage, leftRect, direction = rotate(self.leftCannonCopy, self.angle, leftPivot, offset)
            leftHit, leftRect2, direction2 = rotate(pygame.image.load('sprites/Enemies/Boss_GunHit.png'), self.angle, leftPivot, offset)

            # making a copy of the rotated image so the shooting will be aligned with the image of the cannon
            leftPivotCopy = leftRect.centerx + 1, leftRect.centery - 20
            leftRotatedImageCopy, leftRectCopy, direction = rotate(self.leftCannonCopy, self.angle, leftPivotCopy, offset)
            leftRectCopy.bottom += 20
            leftPos = pygame.Vector2(leftRectCopy.center)

            # blitting the rotated images to its rectangle based on whether the cannon has been hit or not 
            if (leftCannonHit == True):
                screen.blit(leftHit, leftRect2)

            else:
                screen.blit(leftRotatedImage, leftRect)

            # the delay between each shot
            if (self.rotatingDelay % 40 == 0):
                enemyBullet = EnemyRotatingBullet(bulletImg, 10, 20, leftPos, direction.normalize(), 20) 
                enemyBullets.add(enemyBullet)

        # preventing the cannon from rotating over 90 degrees in either direction 
        if (self.angle >= 90):
            self.leftCannonAngleSpeed *= -1
            self.rightCannonAngleSpeed *= -1
            self.rotateCount += 1

        elif (self.angle <= -90):
            self.leftCannonAngleSpeed *= -1
            self.rightCannonAngleSpeed *= -1
            self.rotateCount += 1

    # if it has rotated 90 degress twice and its angle is zero
        if (self.rotateCount == 2) and (self.angle >= 0):

        # if the left cannon is not dead 
            if (self.leftCannonHP > 0):

        # have the left cannon be equal to its previously made copy 
                self.leftCannon = self.leftCannonCopy

        # if the right cannon is not dead 
            if (self.rightCannonHP > 0):

        # have the right cannon be equal to its previously made copy 
                self.rightCannon = self.rightCannonCopy

            self.rotateCount = 0
            self.rotatingDelay = 0
            self.attack = 0
            self.wait = 0


# function that rotates a surface given a surface, angle, pivot, and offset
# returns the rotated surface, its rectangle, and the rectangles direction
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
movetime = 0
right = False
left = False
evadingEnemyAlive = False
leftCannonHit = False
rightCannonHit = False
paused = False
boss = False

# loading in bullet images
bulletImg = pygame.image.load('sprites/Misc/Bullets.png')
enemyBulletImg = pygame.image.load('sprites/Misc/Enemy_Bullets.png')

# load in explosion images
explosion = [pygame.image.load('sprites/Misc/Explosion.png'), pygame.image.load('sprites/Misc/Explosion2.png'), \
             pygame.image.load('sprites/Misc/Explosion3.png'), pygame.image.load('sprites/Misc/Explosion4.png')]

# transparent image
transparent = pygame.image.load('sprites/Misc/transparent.png')

# loading in enemy images  
kamikaze = [pygame.image.load("sprites/Enemies/Kamikaze.png"), pygame.image.load("sprites/Enemies/Kamikaze2.png")]
kamikazeHit = [pygame.image.load("sprites/Enemies/KamikazeHit.png"), pygame.image.load("sprites/Enemies/Kamikaze2Hit.png")]

normal = [pygame.image.load("sprites/Enemies/Normal.png"),  pygame.image.load("sprites/Enemies/Normal2.png")]
normalHit = [pygame.image.load("sprites/Enemies/NormalHit.png"),  pygame.image.load("sprites/Enemies/Normal2Hit.png")]
normalInvul = [pygame.image.load("sprites/Enemies/NormalInvul.png"),  pygame.image.load("sprites/Enemies/Normal2Invul.png")]

spray = [pygame.image.load("sprites/Enemies/Spray.png"), pygame.image.load("sprites/Enemies/Spray2.png")]
sprayHit = [pygame.image.load("sprites/Enemies/SprayHit.png"), pygame.image.load("sprites/Enemies/Spray2Hit.png")]

healer2 = [pygame.image.load("sprites/Enemies/Healer.png"), pygame.image.load("sprites/Enemies/Healer2.png")]
healerHit2 = [pygame.image.load("sprites/Enemies/HealerHit.png"), pygame.image.load("sprites/Enemies/Healer2Hit.png")]
healer = [pygame.image.load("sprites/Enemies/Healer3.png"), pygame.image.load("sprites/Enemies/Healer4.png")]
healerHit = [pygame.image.load("sprites/Enemies/Healer3Hit.png"), pygame.image.load("sprites/Enemies/Healer4Hit.png")]

brokenGun = [pygame.image.load("sprites/Enemies/Boss_Gun_Broken.png"), pygame.image.load("sprites/Enemies/Boss_Gun_Broken2.png")]
brokenSkull = [pygame.image.load("sprites/Enemies/Boss_Skull_Broken.png"), pygame.image.load("sprites/Enemies/Boss_Skull_Broken2.png")]

# loading in the start images
startButtonImg = pygame.image.load('sprites/Misc/FinalPi2.png')
selectedStartButtonImg = pygame.image.load('sprites/Misc/FinalPi.png')
toggleStraight = [pygame.image.load('sprites/Toggle/Toggel.png'), pygame.image.load('sprites/Toggle/Toggel2.png')]
toggleWide = [pygame.image.load('sprites/Toggle/Toggel3.png'), pygame.image.load('sprites/Toggle/Toggel4.png')]
health = [pygame.image.load("sprites/Misc/Fuel_Cell_Empty.png"), pygame.image.load("sprites/Misc/Fuel_Cell1.png"), pygame.image.load("sprites/Misc/Fuel_Cell2.png"), \
          pygame.image.load("sprites/Misc/Fuel_Cell3.png"), pygame.image.load("sprites/Misc/Fuel_Cell4.png"), pygame.image.load("sprites/Misc/Fuel_Cell5.png"), \
          pygame.image.load("sprites/Misc/Fuel_Cell6.png"), pygame.image.load("sprites/Misc/Fuel_Cell7.png"), pygame.image.load("sprites/Misc/Fuel_Cell8.png"), \
          pygame.image.load("sprites/Misc/Fuel_Cell9.png"), pygame.image.load("sprites/Misc/Fuel_Cell_Full.png")]

# sprites
Ship = pygame.image.load("sprites/Player/Player_Ship.png")
Ship2 = pygame.image.load("sprites/Player/Player_Ship2.png")
Left = pygame.image.load("sprites/Player/Player_Ship_Left.png")
Left2 = pygame.image.load("sprites/Player/Player_Ship_Left2.png")
Right = pygame.image.load("sprites/Player/Player_Ship_Right.png")
Right2 = pygame.image.load("sprites/Player/Player_Ship_Right2.png")

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

# creating sprite group for the enemies
enemies = pygame.sprite.Group()
enemySprites = [kamikaze, normal, spray, healer]

# background
bg = pygame.image.load("sprites/Misc/City_Background.png")

'''uncomment the line that contains the enemy you want to spawn'''
#enemies.add(KamikazeEnemy(enemySprites[0], 40, 3, 3, player))
#enemies.add(NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6)))
#enemies.add(NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6)))
#enemies.add(NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6)))
#enemies.add(SplashEnemy(enemySprites[2], 60, 0, 6))
#enemies.add(EvadingEnemy(enemySprites[3], 60, 5, 5, player))
#enemies.add(Boss(100))

clock = pygame.time.Clock()

pygame.display.set_caption("FinalPi")

# creating joystick object
stickX = (WIDTH - (WIDTH / 6))
stickY = (HEIGHT - (HEIGHT / 8))
joystick = Circle(stickX, stickY, TRANSPARENT, 15)

# creating the toggle button object
toggleX = (WIDTH - (5 * WIDTH / 6) - 44)
toggleY = (HEIGHT - (HEIGHT / 8) - 20)
toggleButton = Button(None, 56, 44, toggleX, toggleY)

# function that will check if mouse is over the joystick
within = (lambda x, low, high: low <= x <= high)

# titleMusic = pygame.mixer.music.load("Final Pi Music/title-1.wav")
# waveMusic = pygame.mixer.music.load("Final Pi Music/wave-1.wav")
# bossMusic = pygame.mixer.music.load("Final Pi Music/boss-1.wav")
buttonSound = pygame.mixer.Sound("Final Pi Music/buttonPush.wav")


# function that handles the start menu 
def menu():

    global bgCount
    global bgCount2

    menu = True
        
    startButton = StartButton(startButtonImg)

    pygame.mixer.music.load("Final Pi Music/title-1.wav")

    pygame.mixer.music.play(-1)

    while (menu == True):

        try:
            # redraw the background
            screen.blit(bg, (0, bgCount))
            screen.blit(bg, (0, bgCount2))

            # increment the y position of the background
            bgCount += 2
            bgCount2 += 2

            # reset the y positions of the background
            # to above the other background once off-screen
            if (bgCount >= 720):
                bgCount = bgCount2 - 1235

            if (bgCount2 >= 720):
                bgCount2 = bgCount -1235


            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    menu = False

                if (startButton.clicked()):
                    buttonSound.play()
                    pygame.mixer.music.load("Final Pi Music/wave-1.wav")
                    menu = False
                    game()
                        
            startButton.update(screen)
                
            pygame.display.update()

        except pygame.error:

            return

    pygame.quit()


# function that handles the main game loop
def game():

    global left
    global right
    global paused
    global count
    global bgCount
    global bgCount2
    global dt
    global boss
    global enemyBullets
    global bullets

    # list that will hold all bullet objects
    bullets = pygame.sprite.Group()

    # list that will hold all enemy bullet objects 
    enemyBullets = pygame.sprite.Group()

    # list that will contain the player object
    playerObj = pygame.sprite.Group()

    # creating player object 
    player = Player(char, WIDTH / 2 - 20, HEIGHT + 100, 35, 40, 10)
    playerObj.add(player)

    # creating level system
    levelOne = pygame.sprite.Group()
    levelOne.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))

    levelTwo = pygame.sprite.Group()
    levelTwo.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelTwo.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelTwo.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))

    levelThree = pygame.sprite.Group()
    levelThree.add(KamikazeEnemy(enemySprites[0], 40, 3, 3, player))

    levelFour = pygame.sprite.Group()
    levelFour.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelFour.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelFour.add(KamikazeEnemy(enemySprites[0], 40, 3, 3, player))

    levelFive = pygame.sprite.Group()
    levelFive.add((SplashEnemy(enemySprites[2], 60, 0, 6)))

    levelSix = pygame.sprite.Group()
    levelSix.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelSix.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelSix.add((SplashEnemy(enemySprites[2], 60, 0, 6)))

    levelSeven = pygame.sprite.Group()
    levelSeven.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelSeven.add(EvadingEnemy(enemySprites[3], 30, 5, 5, player))

    levelEight = pygame.sprite.Group()
    levelEight.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelEight.add((NormalEnemy(enemySprites[1], 30, random.randint(-6, 6), random.randint(-6, 6))))
    levelEight.add(EvadingEnemy(enemySprites[3], 30, 5, 5, player))

    bossLevel = pygame.sprite.Group()
    bossLevel.add(Boss(100))

    # will count the delay between each shot
    shootTime = 0

    # boolean that will check if the player is clicking on the joystick
    selected = False

    # boolean that will control the state of the game (running or not running)
    running = True

    # select the beginning level(default is 1 to play the full game)
    level = 1

    # variable that checks whether or not the game is over 
    gameOver = False

    pygame.mixer.music.play(-1)

    if (level == 9):
        pygame.mixer.music.load("Final Pi Music/boss-1.wav")

    # main game loop
    while (running == True):

        if (level == 9 and boss == False):
            pygame.mixer.music.load("Final Pi Music/boss-1.wav")
            pygame.mixer.music.play(-1)
            boss = True

        # Will add pause function later 
        if (paused == False):

                dt = clock.tick(fps)
                
                toggleButton = ToggleButton(toggleStraight[0])

                if (player.alive()):
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

                        # if the left mouse button has been clicked
                        if (event.button == 1):
                            pos = pygame.mouse.get_pos()

                            # if the mouse is within the joystick
                            if ((within(pos[0], *joystick.x_boundary)
                                and within(pos[1], *joystick.y_boundary))):
                                selected = True

                            # toggle from straight shot to V shot
                            if (toggleButton.clicked() and Player.straightShot == True):
                                buttonSound.play()
                                Player.straightShot = False
                                Player.vShot = True

                            # toggle from V shot to straight shot
                            elif (toggleButton.clicked() and Player.vShot == True):
                                buttonSound.play()
                                Player.vShot = False 
                                Player.straightShot = True

                    # if the mouse button has been released
                    elif (event.type == pygame.MOUSEBUTTONUP):

                        #move the joystick back to the center of the d-pad
                        joystick.rect.centerx, joystick.rect.centery = stickX, stickY
                        selected = False

                # if the mouse cursor is over the joystick and the mouse is being pressed
                if (selected):
                    joystick.pos = pygame.mouse.get_pos()
                    joystick.recalc_boundary()
                    joystick.rect.centerx, joystick.rect.centery = pygame.mouse.get_pos()

                    # range checking to make sure the joystick doesn't move beyond the d-pad
                    if (joystick.pos[0] <= (stickX - 20)):
                        pygame.mouse.set_pos((stickX - 19), joystick.pos[1])
                
                    elif (joystick.pos[0] >= (stickX + 20)):
                        pygame.mouse.set_pos((stickX + 19), joystick.pos[1])

                    if (joystick.pos[1] <= (stickY - 20)):
                        pygame.mouse.set_pos(joystick.pos[0], (stickY - 19))

                    elif (joystick.pos[1] >= (stickY + 20)):
                        pygame.mouse.set_pos(joystick.pos[0], (stickY + 19))

                # move the joystick back to the middle of the d-pad
                else:
                    joystick.pos = (stickX, stickY)
                    joystick.recalc_boundary()

                # redraw the background
                screen.blit(bg, (0, bgCount))
                screen.blit(bg, (0, bgCount2))
                # increment the y position of the background
                bgCount += 3
                bgCount2 += 3
                # reset the y positions of the background
                # to above the other background once off-screen
                if (bgCount >= 720):
                    bgCount = bgCount2 - 1235

                if (bgCount2 >= 720):
                    bgCount2 = bgCount -1235

                # refreshing the player to check for any action
                playerObj.update(screen)

                if (level == 1):
                    levelOne.draw(screen)
                    levelOne.update(screen)
                    #if (player.hp < 10):
                        #player.hp += 1

                elif (level == 2):
                    levelTwo.draw(screen)
                    levelTwo.update(screen)

                elif (level == 3):
                    levelThree.draw(screen)
                    levelThree.update(screen)
                    if (player.hp < 8):
                        player.hp += 1
                    
                elif (level == 4):
                    levelFour.draw(screen)
                    levelFour.update(screen)

                elif (level == 5):
                    levelFive.draw(screen)
                    levelFive.update(screen)
                    if (player.hp < 6):
                        player.hp += 1

                elif (level == 6):
                    levelSix.draw(screen)
                    levelSix.update(screen)

                elif (level == 7):
                    levelSeven.draw(screen)
                    levelSeven.update(screen)
                    if (player.hp < 4):
                        player.hp += 1

                elif (level == 8):
                    levelEight.draw(screen)
                    levelEight.update(screen)

                elif (level == 9):
                    bossLevel.draw(screen)
                    bossLevel.update(screen)

                # drawing and refreshing enemy bullets list to check for any action in enemy bullet object
                enemyBullets.draw(screen)
                enemyBullets.update(screen, enemyBulletImg)

                # drawing and refreshing the bullets list to check for any action in bullet object
                bullets.update(screen, bulletImg)
                bullets.draw(screen)
                
                if (gameOver == False):
                
                    # health bar
                    screen.blit(health[player.hp], (stickX, stickY - 300))

                    # blit the UI
                    # joystick
                    screen.blit(joystick.image, joystick.rect)

                    # arrows
                    screen.blit(rightImg, (stickX + 20, stickY - 15))
                    screen.blit(leftImg, (stickX - 55, stickY - 15))
                    screen.blit(upImg, (stickX - 15, stickY - 55))
                    screen.blit(downImg, (stickX - 15, stickY + 20))

                    # toggle
                    toggleButton.update(screen)

                # if the player is alive display the proper animation
                if (player.alive()):
                    # if the player is hit, have the player sprite flash during iFrames
                    if (player.hit == True):
                        if (player.hitDelay % 2 == 0):
                            # if not moving left or right
                            if (left == False and right == False):
                                screen.blit(char[count // 6], (player.rect.x - 25, player.rect.y - 5))
                            # if character moving left
                            elif (left == True):
                                 screen.blit(charLeft[count // 6], (player.rect.x - 20, player.rect.y - 5))
                            # if character moving right
                            elif (right == True):
                                screen.blit(charRight[count // 6], (player.rect.x - 30, player.rect.y - 5))

                    # if the player has not been hit, display the sprites normally
                    # if not moving left or right
                    elif (left == False and right == False):
                        screen.blit(char[count // 6], (player.rect.x - 25, player.rect.y - 5))
                    # if character moving left
                    elif (left == True):
                         screen.blit(charLeft[count // 6], (player.rect.x - 20, player.rect.y - 5))
                    # if character moving right
                    elif (right == True):
                        screen.blit(charRight[count // 6], (player.rect.x - 30, player.rect.y - 5))

                    # reset the count to prevent errors from exceeding list length   
                    if (count + 1 >= 12):
                        count = 0
                    # increment the count to display the next sprite in the lists
                    count += 1

                    # reset the left and right values to false
                    left = False
                    right = False

                else:
                    gameOver = True
                    gameOverButton = StartButton(startButtonImg)
                    gameOverButton.update(screen)

                    if gameOverButton.clicked():
                        running = False
                        menu()
                
                if len(levelOne) <= 0:
                    level = 2

                if len(levelTwo) <= 0:
                    level = 3

                if len(levelThree) <= 0:
                    level = 4

                if len(levelFour) <= 0:
                    level = 5

                if len(levelFive) <= 0:
                    level = 6

                if len(levelSix) <= 0:
                    level = 7

                if len(levelSeven) <= 0:
                    level = 8

                if len(levelEight) <= 0:

                    if player.hp < 4:
                        player.hp = 4
                        
                    level = 9

                if len(bossLevel) <= 0:
                    gameOver = True
                    victoryButton = StartButton(startButtonImg)
                    victoryButton.update(screen)
                    player.hp = 0 

                    if victoryButton.clicked():
                        running = False
                        menu()

                # update the display
                pygame.display.update()

        elif (paused == True):
            pause()

    pygame.quit()
    
# start the game by initializing the menu function
menu()