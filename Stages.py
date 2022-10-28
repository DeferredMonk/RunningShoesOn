import pygame
import Props
import random

"""This file is reserved for the classes of the different stages"""

#Global variables
BLUE = (0,213,255)

class MainMenu(pygame.sprite.Sprite):
	"""Creates everything needed for the main menu"""

	def __init__(self):
		self.text_group = pygame.sprite.Group() #Group for texts for main menu

		title = Props.Text("RUNNING SHOES ON!!!", "./Art/Fonts/04B_30__.TTF", 30, (0, 7, 222), 320, 0, False, True)
		pressToPlay = Props.Text("Press SPACE to play!", "./Art/Fonts/04B_30__.TTF", 25, (255, 255, 255), 320, 300, True, False)

		self.text_group.add(title, pressToPlay)

	def update(self): #Update
		self.text_group.update((255, 255, 255))
	
	def draw(self, screen): #Draw to screen
		self.text_group.draw(screen)

class GameOver(pygame.sprite.Sprite):
	"""Game over screen, for when the player falls out of map"""

	def __init__(self, player):
		self.text_group = pygame.sprite.Group() #Creates a group for the text
		title = Props.Text("GAME OVER!", "./Art/Fonts/04B_30__.TTF", 30, (0, 0, 0), 320, 0, False, True)
		pressToPlay = Props.Text("Press SPACE to restart!", "./Art/Fonts/04B_30__.TTF", 25, (255, 255, 255), 320, 330, True, False)
		self.score = Props.Text(f"You've collected a total of {player.score} coins!", "./Art/Fonts/04B_30__.TTF", 15, (0, 0, 0), 320, 270, False, False)
		self.text_group.add(title, pressToPlay) #Adds the text to the group

	def update(self, player): #Update
		self.score = Props.Text(f"You've collected a total of {player.score} coins!", "./Art/Fonts/04B_30__.TTF", 15, (0, 0, 0), 320, 270, False, False) #Updates the score
		self.text_group.update((255, 255, 255))
	
	def draw(self, screen): #Draw to screen
		self.text_group.draw(screen)
		screen.blit(self.score.image, self.score.rect)

class Victory(pygame.sprite.Sprite):
	"""A screen for when you complete the game"""

	def __init__(self, player):
		self.text_group = pygame.sprite.Group() #group for text
		title = Props.Text("CONGRATULATIONS!", "./Art/Fonts/04B_30__.TTF", 30, (0, 255, 0), 320, 0, False, True)
		pressToPlay = Props.Text("Press SPACE to play again!", "./Art/Fonts/04B_30__.TTF", 25, (255, 255, 255), 320, 330, True, False)
		self.score = Props.Text(f"You've collected a total of {player.score} coins!", "./Art/Fonts/04B_30__.TTF", 15, (0, 255, 0), 320, 270, False, False)
		self.text_group.add(title, pressToPlay)

	def update(self, player): #Update
		self.score = Props.Text(f"You've collected a total of {player.score} coins!", "./Art/Fonts/04B_30__.TTF", 15, (0, 0, 0), 320, 270, False, False) #Updates score
		self.text_group.update((255, 255, 255))
	
	def draw(self, screen): #Draw to screen
		self.text_group.draw(screen)
		screen.blit(self.score.image, self.score.rect)
	
class MainGame(object):
	""" This is a generic super-class used to define a level.
		Create a child class for each level with level-specific
		info. """
 
	def __init__(self, player):
		""" Constructor. Pass in a handle to player. Needed for when moving platforms
			collide with the player. """
		self.platform_list = pygame.sprite.Group()
		self.coin_list = pygame.sprite.Group()
		self.cloud_list = pygame.sprite.Group()
		self.player = player
		self.score = Props.Text(f"Score: {self.player.score}", "./Art/Fonts/04B_30__.TTF", 15, (255,255,255), 5,5, False, False)
		self.createPlatform(50) #Create the terrain
		
		for cloud in self.cloudCreator(): #Create the clouds
			self.cloud_list.add(cloud)

	# Update everythign on this level
	def update(self):
		""" Update everything in this level."""
		self.score = Props.Text(f"Score: {self.player.score}", "./Art/Fonts/04B_30__.TTF", 15, (255,255,255), 5,5, False, False)
		self.platform_list.update()
		self.cloud_list.update()
		self.coin_list.update()
		self.ending.update()
	def draw(self, screen):
		""" Draw everything on this level. """
		# Draw the background
		screen.fill(BLUE)
 
		# Draw all the sprite lists that we have
		screen.blit(self.score.image, (5,5))
		self.cloud_list.draw(screen)
		self.platform_list.draw(screen)
		self.coin_list.draw(screen)
		screen.blit(self.ending.image, self.ending.rect)
	
	def createPlatform(self, amountOfStacks):
		"""Creates a platform based on random cordinates
		in addition it creates coins on every fifth platform
		and a flag on the last platform which enables 
		the game to finish as a victory"""

		for platform in self.startingPlatform(): #adds starting platform to platform group
			self.platform_list.add(platform)

		i = 1
		ranXmin, ranXmax = (490, 640)

		while i < amountOfStacks:	#Creates inserted amount of platforms, for the player to jump on
			ranXmin, ranXmax = ranXmin + 300, ranXmax + 300 
			randomX, randomY = random.randrange(ranXmin , ranXmax), random.randrange(300, 450) #the X cordinates for blocks to be placed
			amountOfBlocks = random.randrange(1, 5) #Stack of connected blocks

			for stack in self.platformGenerator(randomX, randomY, amountOfBlocks):
				self.platform_list.add(stack)

			if i % 5 == 0: #Adds a coin for the player to collect every 5 platforms in a random height
				x = random.randrange(randomX, randomX+(60*amountOfBlocks))
				y = randomY - random.randrange(30, 200)
				self.coin_list.add(self.coinMaker(x, y))
					
			i += 1
			if i == amountOfStacks:
				self.ending = Props.Flag()
				self.ending.rect.x = randomX + 30
				self.ending.rect.bottom = stack.rect.top
				
			
	def startingPlatform(self):
		"""This generator creates the 5 block starting platform
		This platform is always the same"""
		X = 200
		x = 0
		while x < 5:
			block = Props.Platform(5, x)
			block.rect.center = X, 380
			X += 60
			x += 1
			yield block

	def cloudCreator(self):		#Generator that creates clouds
		i = 0
		while i < 5:
			i += 1
			cloud = Props.Cloud()
			yield cloud

	def platformGenerator(self, X, Y, stack):
		y = 0
		while y < stack:
			block = Props.Platform(stack, y)
			block.rect.x, block.rect.y = X, Y #Block position
			block.player = self.player
			X += block.image.get_width()
			y += 1
			yield block
	
	def coinMaker(self, X, Y):
		coin = Props.Coin()
		coin.rect.topleft = (X,Y)

		return coin