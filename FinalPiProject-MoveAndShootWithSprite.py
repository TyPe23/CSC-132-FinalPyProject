import pygame
import time
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

	def update(self, screen):

		if self.pressed() == False:
			pygame.draw.polygon(screen, LIGHTBLUE, self.points, 0)
	
		else:
			pygame.draw.polygon(screen, BLUE, self.points, 0)

	#function that checks if a button has been pressed or not
	def pressed(self):

		#check if the mouse has been clicked
		click = pygame.mouse.get_pressed()

		#get the mouse's position
		mouse_pos = pygame.mouse.get_pos()

		if click[0] == 1 and self.rect.collidepoint(mouse_pos):
			return True

		else:
			return False


#class that will create the player (must include a sprite)
class Player(pygame.sprite.Sprite):

	def __init__(self, sprite, x, y, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.sprite = sprite
		self.image =  pygame.Surface((width, height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, screen):

		#creates the sprite wherever the rectangle is at
		screen.blit(self.sprite, self.rect)
		
		#creating all the buttons 
		upButton = Button([(590, 720), (610, 690), (630, 720)], 40, 30, 590, 690)
		rightButton = Button([(635, 730), (665, 750), (635, 770)], 30, 40, 635, 730)
		downButton = Button([(630, 780), (610, 810), (590, 780)], 40, 30, 590, 780)
		leftButton = Button([(582, 730), (552, 750), (582, 770)], 30, 40, 552, 730)

		buttonList = [upButton, rightButton, downButton, leftButton]

		#refreshing buttons to see if they have been clicked
		for button in buttonList:
			button.update(screen)

		if upButton.pressed():
			self.rect.y -= 3

		elif rightButton.pressed():
			self.rect.x += 3

		elif downButton.pressed():
			self.rect.y += 3

		elif leftButton.pressed():
			self.rect.x -= 3

	#function that creates a bullet object 
	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top, 10, 20)
		bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width, height))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

	def update(self, screen, bulletImg):

		#blit the given sprite to the bullet rect
		screen.blit(bulletImg, self.rect)

		#make it shoot upwards
		self.rect.y -= 11

		#if it goes off the screen then kill it
		if self.rect.bottom < 0:
			self.kill()


#list that will hold all bullet objects
bullets = pygame.sprite.Group()

#loading in and scaling bullet image 
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 20))

WIDTH = 700
HEIGHT = 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps = 60

BLUE = ((0,0,100))
LIGHTBLUE = ((0,0,255))
BLACK = ((0, 0, 0))

clock = pygame.time.Clock()

#loading in ship sprite and scaling it down
image = pygame.image.load('ship.png')
image = pygame.transform.scale(image, (40, 40))

pygame.display.set_caption("First Game")

#creating player object 
player = Player(image, 0, 300, 40, 40)

#will count the delay between each shot
shootTime = 0

#main game loop
running = True
while running == True:

	clock.tick(fps)
    
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#making the screen black
	screen.fill(BLACK)

	shootTime += 1

	if shootTime == 20:
		player.shoot()
		shootTime = 0

	#refreshing the player to check for any action
	player.update(screen)

	#refreshing the bullets list to check for any action in bullet object
	bullets.update(screen, bulletImg)
	bullets.draw(screen)

	pygame.display.flip()

pygame.quit()