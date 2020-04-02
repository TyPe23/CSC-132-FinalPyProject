import pygame
import time
from pygame.locals import *
pygame.init()


fps = 60

clock = pygame.time.Clock()

win = pygame.display.set_mode((480, 320))

pygame.display.set_caption("First Game")

screenWidth = 500

x = 50
y = 450
width = 40
height = 60
vel = 5

LIME = ((180, 255, 100))
PINK = ((255,100,180))
TAN = ((230,220,170))
BLACK = ((0, 0, 0))


player_rect = pygame.Rect(0, 0, 64, 64)

up_rect = pygame.Rect(300, 100, 50, 50)
down_rect = pygame.Rect(300, 180, 50, 50)

running = True
while running == True:

	mouse_pos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		mouse_pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if up_rect.collidepoint(mouse_pos) and click[0] == 1:
			direction = "up"
		elif down_rect.collidepoint(mouse_pos) and click[0] == 1:
			direction = "down"
		elif click[0] == 0:
			direction = "stop"

	if direction == "up":
		player_rect.centery -= 3
	
	elif direction == "down":
		player_rect.centery += 3

	elif direction == "stop":
		player_rect.centery += 0

	if player_rect.bottom > 480:
		direction == "up"
		time.sleep(.01)
		direction == "down"
	
	if player_rect.top < 0:
		direction = "stop"

	win.fill(BLACK)

	pygame.draw.rect(win, PINK, player_rect)
	pygame.draw.rect(win, TAN, up_rect)
	pygame.draw.rect(win, LIME, down_rect)

	clock.tick(fps)
	pygame.display.update()

pygame.quit()