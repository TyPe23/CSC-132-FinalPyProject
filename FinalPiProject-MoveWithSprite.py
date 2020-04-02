import pygame
import time
from pygame.locals import *
pygame.init()


fps = 60

clock = pygame.time.Clock()

window = (500, 500)
screen = pygame.display.set_mode(window)

image = pygame.image.load('ship.png')
image = pygame.transform.scale(image, (64, 64))

pygame.display.set_caption("First Game")

LIME = ((180, 255, 100))
PINK = ((255,100,180))
TAN = ((230,220,170))
BLACK = ((0, 0, 0))


#rectangle that will be controlled by dpad
player_rect = pygame.Rect(0, 0, 64, 64)

#rectangle that will move the player_rect up
up_rect = pygame.Rect(300, 100, 50, 50)

#rectangle that will move the player_rect down
down_rect = pygame.Rect(300, 180, 50, 50)

running = True
while running == True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

        #get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()

	    #check if the mouse has been pressed or not
        click = pygame.mouse.get_pressed()

		#if your mouse is over the up_rect and the left side of the mouse is clicked
     	if up_rect.collidepoint(mouse_pos) and click[0] == 1:
			direction = "up"

		#if your mouse is over the down_rect and the left side of the mouse is clicked	
        elif down_rect.collidepoint(mouse_pos) and click[0] == 1:
			direction = "down"

        else:
			direction = "stop"

	#if the direction is up, move the y position up
	if direction == "up":
		player_rect.y -= 3
	
	#if the direction is down, move the y position down
	elif direction == "down":
		player_rect.y += 3

	#if the direction is stop, do not move 
	elif direction == "stop":
		player_rect.y += 0


	#fill the window with the color black
	screen.fill(BLACK)

	#creating the rectangles 
	screen.blit(image, player_rect)
	pygame.draw.rect(screen, TAN, up_rect)
	pygame.draw.rect(screen, LIME, down_rect)

	clock.tick(fps)
	pygame.display.update()

pygame.quit()