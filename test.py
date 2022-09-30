from platform import python_branch
from turtle import width
import pygame
import random

# GLOBAL VARIABLES
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Classes
class Cloud(pygame.sprite.Sprite):
	def __init__(self, posX, posY, W, H, imgPath):
		super().__init__()
		self.image = pygame.image.load(imgPath)
		self.image = pygame.transform.scale(self.image, (W, H))
		self.rect = self.image.get_rect()
		self.rect.topleft = (posX - W, posY - H)


# Clouds
amountOfClouds = 0
cloud_group = pygame.sprite.Group()

while amountOfClouds < 20: #Adds clouds to the game
	
	amountOfClouds += 1
	W = random.randrange(50, 200)
	H = W - 20
	
	cloud = Cloud(random.randrange(W, 640-W), random.randrange(H, 240), W, H, "cloud.png")
	cloud_group.add(cloud)

#Sun

sun = pygame.draw.circle(screen, ((100, 0, 0)), (640, 0), 500)

pygame.init()

while exit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = False
	
	screen.fill((0,213,255))
	cloud_group.draw(screen)
	sun
	pygame.display.flip()
	


pygame.quit()
