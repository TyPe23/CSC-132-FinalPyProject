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
			self.rect.y -= 3

		if pygame.sprite.collide_rect(rightButton, joystick):
			self.rect.x += 3

		if pygame.sprite.collide_rect(downButton, joystick):
			self.rect.y += 3			

		if pygame.sprite.collide_rect(leftButton, joystick):
			self.rect.x -= 3			

	#function that creates a bullet object 
	def shoot(self):

		if len(bullets) < 7:
			bullet = Bullet(self.rect.centerx, self.rect.top, 10, 20)
			bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width, height))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

	def update(self, screen, bulletImg):

		#blit the given sprite to the bullet rect
		screen.blit(bulletImg, self.rect)

		#if it goes off the screen then kill it
		if self.rect.bottom < 0:
			self.kill()
		
		#make it shoot upwards
		self.rect.y -= 11


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


#list that will hold all sprite objects
all_sprites = pygame.sprite.Group()

#list that will hold all bullet objects
bullets = pygame.sprite.Group()

#loading in and scaling bullet image 
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 20))

WIDTH = 700
HEIGHT = 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps = 30

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
all_sprites.add(player)

#will count the delay between each shot
shootTime = 0

#creating joystick object
joystick = Circle(610, 750, BLUE, 15)
all_sprites.add(joystick)

#function that will check if mouse is over the joystick
within = lambda x, low, high: low <= x <= high

#boolean that will check if the player is clicking on the joystick
selected = False

#main game loop
running = True
while running == True:

	clock.tick(fps)
	
	shootTime += 1

	if shootTime == 10:
		player.shoot()
		shootTime = 0
    
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:

			#if the left mouse button has been clicked
			if event.button == 1:
				pos = pygame.mouse.get_pos()

				#if the mouse is within the joystick
				if (within(pos[0], *joystick.x_boundary)
        		and within(pos[1], *joystick.y_boundary)):
					selected = True
		
		elif event.type == pygame.MOUSEBUTTONUP:
			joystick.rect.centerx, joystick.rect.centery = 610, 750
			selected = False

	if selected:
		joystick.pos = pygame.mouse.get_pos()
		joystick.recalc_boundary()
		joystick.rect.centerx, joystick.rect.centery = pygame.mouse.get_pos()

		if joystick.pos[0] <= 592:
			pygame.mouse.set_pos((593, joystick.pos[1]))
		
		elif joystick.pos[0] >= 625:
			pygame.mouse.set_pos((624, joystick.pos[1]))

		if joystick.pos[1] <= 730:
			pygame.mouse.set_pos((joystick.pos[0], 731))

		elif joystick.pos[1] >= 770:
			pygame.mouse.set_pos((joystick.pos[0], 769))

	#move the joystick back to the middle of the d-pad
	elif not selected:
		joystick.pos = (610, 750)
		joystick.recalc_boundary()

	#making the screen black
	screen.fill(BLACK)
	
	#refreshing the player to check for any action
	player.update(screen)

	#refreshing the bullets list to check for any action in bullet object
	bullets.update(screen, bulletImg)
	bullets.draw(screen)

	all_sprites.draw(screen)

	screen.blit(joystick.image, joystick.rect)
	screen.blit(player.sprite, player.rect)

	pygame.draw.circle(screen, joystick.color, 
	joystick.pos, joystick.radius)

	pygame.display.update()

pygame.quit()