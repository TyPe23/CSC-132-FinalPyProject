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


class StartButton(Button):
	def __init__(self, sprite):
		Button.__init__(self, points = None, width = 300, height = 100, x = 300, y = 300)
		self.sprite = sprite
		self.image.fill(BLUE)

	def update(self, screen):
		screen.blit(self.sprite, self.rect)

		mouse_pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse_pos):
			screen.blit(selectedStartButtonImg, self.rect) 

	def clicked(self):
		mouse_pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if self.rect.collidepoint(mouse_pos) and click[0] == 1:
			return True

		else:
			return False


#class that will create the player (must include a sprite)
class Player(pygame.sprite.Sprite):

	def __init__(self, sprite, x, y, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.sprite = sprite
		self.image =  pygame.Surface((width, height)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, screen):

		if self.rect.bottom > HEIGHT - 30:
			self.rect.y -= 6

		#creating all the buttons 
		upButton = Button([(590, 720), (610, 690), (630, 720)], 40, 30, 590, 690)
		rightButton = Button([(635, 730), (665, 750), (635, 770)], 30, 40, 635, 730)
		downButton = Button([(630, 780), (610, 810), (590, 780)], 40, 30, 590, 780)
		leftButton = Button([(582, 730), (552, 750), (582, 770)], 30, 40, 552, 730)

		buttonList = [upButton, rightButton, downButton, leftButton]

		for button in buttonList:

			if not pygame.sprite.collide_rect(button, joystick):
				pygame.draw.polygon(screen, BLUE, button.points, 0)
			
			else:
				pygame.draw.polygon(screen, LIGHTBLUE, button.points, 0)

		if pygame.sprite.collide_rect(upButton, joystick):
			self.rect.y -= 9

		if pygame.sprite.collide_rect(rightButton, joystick):
			self.rect.x += 9

		if pygame.sprite.collide_rect(downButton, joystick):
			self.rect.y += 9			

		if pygame.sprite.collide_rect(leftButton, joystick):
			self.rect.x -= 9	
	

	#function that creates a bullet object 
	def shoot(self):
		if self.rect.bottom <= HEIGHT - 30:
			bullet1 = Bullet(self.rect.centerx, self.rect.top, 10, 20, 1, -11)
			bullet2 = Bullet(self.rect.centerx, self.rect.top, 10, 20, -1, -11)
			bullets.add(bullet1, bullet2)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, vx, vy):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width, height)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x_speed = vx
		self.y_speed = vy

	def update(self, screen, bulletImg):

		#blit the given sprite to the bullet rect
		screen.blit(bulletImg, self.rect)

		#if it goes off the screen then kill it
		if self.rect.bottom < 0:
			self.kill()
		
		#make it shoot upwards
		self.rect.x +=  self.x_speed
		self.rect.y += self.y_speed


#class that creates the circle inside the joypad
class Circle(pygame.sprite.Sprite):
	def __init__(self, x, y, color, radius):
		pygame.sprite.Sprite.__init__(self)
		self.pos = (x, y)
		self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
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
	def __init__(self, sprite, hp, x_speed, y_speed):
		pygame.sprite.Sprite.__init__(self)
		self.sprite = sprite
		self.image = pygame.Surface((128, 128)).convert_alpha()
		self.image.fill((255, 255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint(0 + self.rect.width, WIDTH - self.rect.width)
		self.rect.bottom = -150

		self.x_speed = x_speed
		self.y_speed = y_speed

		self.hp = hp

		collisionRectPos = (self.rect.left + 30, self.rect.top + 32)
		collisionRectSize = (self.rect.width - 60, self.rect.height - 32)
		self.collisionrect = pygame.Rect(collisionRectPos, collisionRectSize, width = 1)

	def update(self, screen):
		pass

	def checkCollision(self):
		for bullet in bullets:
			if pygame.sprite.collide_rect(self, bullet):
				if self.hp > 0:
					self.hp -= 1
				else:
					self.kill()
				bullet.kill()

	def alive(self):
		if self.hp > 0:
			return True
		else:
			return False

	def updateMove(self):
		pass

	def shoot(self):
		pass


class NormalEnemy(Enemy):
	def __init__(self, sprite, hp, x_speed, y_speed):
		Enemy.__init__(self, sprite, hp, x_speed, y_speed)
		self.sprite = sprite
		self.hp = hp
		self.x_speed = x_speed if x_speed > 2 or x_speed < -2 else 3
		self.y_speed = y_speed if x_speed > 2 or x_speed < -2 else 3
		self.xdirection = 1
		self.ydirection = 1
		self.enemyBullets = pygame.sprite.Group()

	def update(self, screen):

		pygame.draw.rect(screen, (0, 0, 225), self.collisionrect)

		self.enemyBullets.draw(screen)
		self.enemyBullets.update(screen, bulletImg)

		screen.blit(self.sprite, self.rect) 
		self.checkCollision()

		if self.rect.top < 0:
			self.rect.y += 6

		else:
			self.shoot()

			self.rect.x += self.x_speed * self.xdirection
			self.rect.y += self.y_speed * self.ydirection

			if (self.rect.left <= 0) or (self.rect.left + self.rect.width >= WIDTH):
				self.xdirection *= -1
				self.y_speed = random.uniform(3, 6)

			if (self.rect.bottom > 450) or (self.rect.top <= 0): 
				self.ydirection *= -1
				self.x_speed = random.uniform(3, 6)
		
	def shoot(self):
		if random.randrange(15) == 0:
			enemyBullet = Bullet(self.rect.centerx, self.rect.top + self.rect.height, 10, 20, 0, 9)
			self.enemyBullets.add(enemyBullet)


class SplashEnemy(Enemy):
	def __init__(self, sprite, hp, x_speed, y_speed):
		Enemy.__init__(self, sprite, hp, x_speed, y_speed)
		self.sprite = sprite
		self.hp = hp
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.enemyBullets = pygame.sprite.Group()

	def update(self, screen):

		self.enemyBullets.draw(screen)
		self.enemyBullets.update(screen, bulletImg)

		screen.blit(self.sprite, self.rect) 
		self.checkCollision()

		if self.rect.bottom < 400:
			self.rect.y += self.y_speed

		else:
			self.rect.y += 0
			self.shoot()

	def shoot(self):
			enemyBullet1 = Bullet(self.rect.centerx, self.rect.top + self.rect.height, 10, 20, random.randint(0, 2), random.uniform(3.5, 7.5))
			enemyBullet2 = Bullet(self.rect.centerx, self.rect.top + self.rect.height, 10, 20, random.randint(-2, -0), random.uniform(3.5, 7.5))
			self.enemyBullets.add(enemyBullet1, enemyBullet2)


class EvadingEnemy(Enemy):

	edge = False
	leftMove = False
	rightMove = False

	def __init__(self, sprite, hp, x_speed, y_speed, player):	
		Enemy.__init__(self, sprite, hp, x_speed, y_speed)
		self.sprite = sprite
		self.hp = 10
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.player = player

	def update(self, screen):

		screen.blit(self.sprite, self.rect)

		self.offScreen()

		if self.rect.top < 300:
			self.rect.y += 12

		else:
			if EvadingEnemy.edge == False and EvadingEnemy.leftMove == False and EvadingEnemy.rightMove == False:

				if (self.rect.x < self.player.rect.x):
					self.rect.x -= self.x_speed
            
				elif self.rect.x > self.player.rect.x:
					self.rect.x += self.x_speed

			elif EvadingEnemy.edge == True and self.offScreen() == 1:
				EvadingEnemy.leftMove = True

			elif EvadingEnemy.edge == True and self.offScreen() == 2:
				EvadingEnemy.rightMove = True
	
			if EvadingEnemy.leftMove == True:
				if (self.rect.x < self.player.rect.x):
					self.rect.x += 0

				else:
					self.leftScreenCollison()

			elif EvadingEnemy.rightMove == True:
				if self.rect.x > self.player.rect.x:
					self.rect.x += 0
				
				else:
					self.rightScreenCollison()

	def offScreen(self):
		if (self.rect.left <= 0):
			EvadingEnemy.edge = True
			return 1

		if(self.rect.left + self.rect.width >= 700):
			EvadingEnemy.edge = True
			return 2

	def leftScreenCollison(self):
		if self.rect.x <= 100:
			self.rect.x += self.x_speed

		else:
			EvadingEnemy.leftMove = False
			EvadingEnemy.edge = False

	def rightScreenCollison(self):
		if self.rect.x >= 510:
			self.rect.x -= self.x_speed

		else:
			EvadingEnemy.rightMove = False
			EvadingEnemy.edge = False


class KamikazeEnemy(Enemy):
	def __init__(self, sprite, hp, x_speed, y_speed, player):	
		Enemy.__init__(self, sprite, hp, x_speed, y_speed)
		self.sprite = sprite
		self.hp = 10
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.player = player

	def update(self, screen):

		screen.blit(self.sprite, self.rect)

		#self.checkCollision()

		if self.rect.top < 0:
			self.rect.y += 6

		else:
			if (self.rect.x < self.player.rect.x):
				self.rect.x += self.x_speed
            
			elif self.rect.x > self.player.rect.x:
				self.rect.x -= self.x_speed
				
			if self.rect.y < self.player.rect.y:
				self.rect.y += self.y_speed
            
			elif self.rect.y > self.player.rect.y:
				self.rect.y -= self.y_speed


WIDTH = 700
HEIGHT = 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#loading in and scaling bullet image 
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 20))

#loading in enemy images  
enemy1 = pygame.image.load('Enemy1.png')
enemy2 = pygame.image.load('Enemy2.png')

#loading in the start button images
startButtonImg = pygame.image.load('startButton.png')
selectedStartButtonImg = pygame.image.load('selectedStartButton.png')

#shrinking the start button images 
startButtonImg = pygame.transform.scale(startButtonImg, (300, 100))
selectedStartButtonImg = pygame.transform.scale(selectedStartButtonImg, (300, 100))

#list that will hold all sprite objects
all_sprites = pygame.sprite.Group()

#list that will hold all bullet objects
bullets = pygame.sprite.Group()

#loading in ship sprite and scaling it down
image = pygame.image.load('ship.png')
image = pygame.transform.scale(image, (40, 40))

#creating player object 
player = Player(image, WIDTH / 2, HEIGHT + 100, 40, 40)
all_sprites.add(player)

#creating sprite group for the enemies
enemies = pygame.sprite.Group()

enemySprites = [enemy1, enemy2]


'''uncomment the line that contains the enemy you want to spawn'''
#enemies.add(KamikazeEnemy(enemySprites[0], 10, 5, 5, player))
#enemies.add(NormalEnemy(random.choice(enemySprites), 15, random.randint(-6, 6), random.randint(-6, 6)))
#enemies.add(SplashEnemy(random.choice(enemySprites), 30, 0, 6))
#enemies.add(EvadingEnemy(enemySprites[0], 10, 5, 5, player))

fps = 30

BLUE = ((0,0,100))
LIGHTBLUE = ((0,0,255))
BLACK = ((0, 0, 0))
TRANSPARENT = (255, 255, 255, 0)
WHITE = ((255, 255, 255))
MAROON = ((115, 0, 0))

clock = pygame.time.Clock()

pygame.display.set_caption("First Game")

#creating joystick object
joystick = Circle(610, 750, BLUE, 15)
all_sprites.add(joystick)

#function that will check if mouse is over the joystick
within = lambda x, low, high: low <= x <= high

paused = False

movetime = 0

def menu():

	menu = True
	
	startButton = StartButton(startButtonImg)

	while menu == True:

		try:
			screen.fill(WHITE)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					menu = False

			if startButton.clicked():
				menu = False
				game()
			
			startButton.update(screen)
		
			pygame.display.update()

		except pygame.error:
			return

	pygame.quit()


def game():

	global paused

	#will count the delay between each shot
	shootTime = 0

	#boolean that will check if the player is clicking on the joystick
	selected = False

	#boolean that will control the state of the game (running or not running)
	running = True

	#main game loop
	while running == True:

		#Will add pause function later 
		if paused == False:

			clock.tick(fps)

			shootTime += 1

			if shootTime == 5:
				player.shoot()
				shootTime = 0
    
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.KEYDOWN:
					if event.button == K_ESCAPE:
						paused = True

				if event.type == pygame.MOUSEBUTTONDOWN:

					#if the left mouse button has been clicked
					if event.button == 1:
						pos = pygame.mouse.get_pos()

						#if the mouse is within the joystick
						if (within(pos[0], *joystick.x_boundary)
        				and within(pos[1], *joystick.y_boundary)):
							selected = True

				#if the mouse button has been released
				elif event.type == pygame.MOUSEBUTTONUP:

					#move the joystick back to the center of the d-pad
					joystick.rect.centerx, joystick.rect.centery = 610, 750
					selected = False

			#if the mouse cursor is over the joystick and the mouse is being pressed
			if selected:
				joystick.pos = pygame.mouse.get_pos()
				joystick.recalc_boundary()
				joystick.rect.centerx, joystick.rect.centery = pygame.mouse.get_pos()

				#range checking to make sure the joystick doesn't move beyond the d-pad
				if joystick.pos[0] <= 592:
					pygame.mouse.set_pos((593, joystick.pos[1]))
		
				elif joystick.pos[0] >= 625:
					pygame.mouse.set_pos((624, joystick.pos[1]))

				if joystick.pos[1] <= 730:
					pygame.mouse.set_pos((joystick.pos[0], 731))

				elif joystick.pos[1] >= 770:
					pygame.mouse.set_pos((joystick.pos[0], 769))

			#move the joystick back to the middle of the d-pad
			else:
				joystick.pos = (610, 750)
				joystick.recalc_boundary()

			screen.fill(MAROON)

			#drawing and refreshing the bullets list to check for any action in bullet object
			bullets.update(screen, bulletImg)
			bullets.draw(screen)

			#drawing and refreshing the enemies list to check for any action in enemy object
			enemies.draw(screen)
			enemies.update(screen)

			#refreshing the player to check for any action
			player.update(screen)

			#all_sprites.draw(screen)

			screen.blit(joystick.image, joystick.rect)
			screen.blit(player.sprite, player.rect)

			pygame.draw.circle(screen, joystick.color, 
			joystick.pos, joystick.radius)

			pygame.display.update()

		elif paused == True:
			pause()

	pygame.quit()

menu()