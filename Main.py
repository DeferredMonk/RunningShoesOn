from multiprocessing import set_forkserver_preload
from platform import python_branch
from tkinter import CENTER, Toplevel
from turtle import right, title, width
import pygame
import CustomClasses, CustomFunctions

# GLOBAL VARIABLES
pygame.font.init()
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
movRight, movLeft, jump, jumpStartingPoint = False, False, False, 442

mainMenu = True
cloud_group = CustomFunctions.createClouds(5, CustomClasses.Cloud)

#Player

char = CustomClasses.Character(320, 400)

#Text section

text_group = pygame.sprite.Group()

title = CustomClasses.Text("RUNNING SHOES ON!!!", "04B_30__.TTF", 30, (0, 7, 222), 320, 0, False, True)
pressToPlay = CustomClasses.Text("Press SPACE to play!", "04B_30__.TTF", 25, (255, 255, 255), 320, 300, True, False)

text_group.add(title)
text_group.add(pressToPlay)

#Tile section

MainMenuTiles = CustomClasses.Tile("stoneHalf.png", 320, 442)
stackOfTiles = pygame.sprite.Group()
CustomFunctions.addToStackTiles(stackOfTiles, 5, 200, 442)
CustomFunctions.addToStackTiles(stackOfTiles, 2, 50, 300)
CustomFunctions.addToStackTiles(stackOfTiles, 1, 150, 402)




pygame.init()

while exit:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = False

		if event.type == pygame.KEYDOWN: #Button press ->

			if event.key == pygame.K_SPACE: #Exits Main menu game starts by pressing space
				mainMenu = False
			
			if mainMenu == False: #Return to main menu with esc
				if event.key == pygame.K_ESCAPE: 
					mainMenu = True
				if event.key == pygame.K_d:
					movRight = True
				if event.key == pygame.K_a:
					movLeft = True
				if len(collideTerrain) > 0:
					if event.key == pygame.K_SPACE:
						jump = True
				
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				movLeft = False
			elif event.key == pygame.K_d:
				movRight = False
			if event.key == pygame.K_SPACE:
					jump = False
		
	
	screen.fill((0,213,255))
	cloud_group.draw(screen)
	cloud_group.update()
	screen.blit(char.image, char.rect)
	collideTerrain = pygame.sprite.spritecollide(char, stackOfTiles, False)
	
	if mainMenu:	#If menu open
		screen.blit(MainMenuTiles.image, MainMenuTiles.rect)
		char.update(False, False, False)
		text_group.draw(screen)
		text_group.update((255, 255, 255))
			
		pygame.display.flip()
	if mainMenu == False:	#if menu closed
		
		if movRight:
			char.update(False, True, False)
		if movLeft:
			char.update(True, False, False)
			
		stackOfTiles.draw(screen)
		
		if jump:
			if len(collideTerrain) > 0:
				jumpStartingPoint = collideTerrain[0].Y

			char.update(False, False, True, jumpStartingPoint)
		
		

		elif len(collideTerrain) == 0 and jump == False:
			char.Y += 5
			char.rect = char.image.get_rect(topleft=(char.X, char.Y))

		if char.Y <= jumpStartingPoint - 160:
			jump = False
		print(collideTerrain)
		pygame.display.flip()
	
	clock.tick(60)
	
pygame.quit()
