import pygame
import os
import random

"""This file is for game props and player only"""

class Coin(pygame.sprite.Sprite):
	""" Class for coin creation """
	def __init__(self):
		super().__init__()

		self.coin_animation_group = [] #Array to store png for animation
		self.current_coin = 0
		self.image = pygame.image.load("./Art/Coin/goldCoin1.png")
		self.image = pygame.transform.smoothscale(self.image, (35, 35))
		self.rect = self.image.get_rect()
		self.movement = 1
			
		for image in os.listdir("./Art/Coin/"): #Loop to add png to array for animation
			self.coin_animation_group.append(pygame.image.load(f"./Art/Coin/{image}")) 

	def update(self):
		if self.movement < 4: #Moves the coin at the same speed as the ground
			self.movement += 0.001
		self.rect.x -= self.movement
		
		if int(self.current_coin) >= 9: #Animates the coin
			self.current_coin = 0
		else:
			self.current_coin += 0.15

		self.image = self.coin_animation_group[int(self.current_coin)-1]

class Flag(pygame.sprite.Sprite):
	"""Class for creation of flags. A flag is the winning sign.
	If you hit the flag witch is on the last platform you complete the game"""

	def __init__(self):
		super().__init__()
		self.sheet_flag = pygame.image.load("./Art/Flags/flag_complete.png")
		self.animate = 0
		self.image = self.get_image(self.animate, 202, 324, 4)
		self.rect = self.image.get_rect()
		self.movement = 1
	
	def update(self):
		self.image = self.get_image(int(self.animate), 202, 324, 4) #Animates the flag by updating self.animate as the wanted frame
		self.animate += .3 #speed of animation
		if self.animate > 10:
			self.animate = 0
		
		if self.movement < 4: #Moves the flag at the same speed as the ground
			self.movement += 0.001
		self.rect.x -= self.movement

	def get_image(self, frame, width, height, scale): #Function to cut the image of the flag in 10 pieces. 
		image = pygame.Surface((width, height)).convert_alpha()
		image.fill((255,255,255))
		image.blit(self.sheet_flag, (0,0), (frame*width,0, width, height))
		image = pygame.transform.scale(image,(width / scale, height / scale)) #scales the flag if needed
		image.set_colorkey((255,255,255)) #Sets background of the flag to transparent

		return image #returns the complete image

class Cloud(pygame.sprite.Sprite):
	"""This class cretes clouds witch float on the top side of the screen"""
	def __init__(self):
		super().__init__()
		self.W = random.randrange(150, 250)
		self.H = self.W-20	
		self.posX = random.randrange(self.W, 640) #Random position X
		self.posY = random.randrange(self.H, 240) #Random position Y
		self.image = pygame.image.load("./Art/cloud.png")
		self.image = pygame.transform.scale(self.image, (self.W, self.H)) #Scales the clouds to be of different sizes
		self.rect = self.image.get_rect(topleft=(self.posX - self.W, self.posY - self.H))
		self.animate = 0

	def update(self): 
		"""Animates the clouds"""
		if self.animate <= 2:
			self.animate += 0.08
			self.rect = (self.rect[0], self.rect[1] - int(self.animate))
		else:
			self.animate = -2
			self.rect = (self.rect[0], self.rect[1] - int(self.animate))

class Platform(pygame.sprite.Sprite):
	""" Creates a platform the user can jump on """

	def __init__(self, stack, iOfStack):
		""" Block/Platform constructor, creates blocks based on stack amount """
		super().__init__()
		self.group_of_blocks = []
		
		for block in os.listdir("./Art/Blocks/SetOfBlocks"): #Populates array of blocks
			self.group_of_blocks.append(pygame.image.load(f"./Art/Blocks/SetOfBlocks/{block}"))
		
		if stack == 1: #If the provided stack is of one block, we return a one block image
			self.image = pygame.image.load("./Art/Blocks/stone.png")
		
		elif stack == 2: #If provided stack is of two block, we return the first and last blocks of the list
			if iOfStack == 0:
				self.image = self.group_of_blocks[0]
			else:
				self.image = self.group_of_blocks[2]
		
		else: #if stack is of three or more we return in order the blocks
			if iOfStack == 0:
				self.image = self.group_of_blocks[0]
			elif iOfStack == stack - 1:
				self.image = self.group_of_blocks[2]
			else:
				self.image = self.group_of_blocks[1]
 		
		self.image = pygame.transform.smoothscale(self.image, (60, 30))
		self.rect = self.image.get_rect()
		self.movement = 1
	
	def update(self):
		"""Makes the platforms move to the left and makes
		 them faster and faster until 4 pixels pers frame
		 this is to make the game harder"""
		if self.movement < 4:
			self.movement += 0.001
		self.rect.x -= self.movement

class Text(pygame.sprite.Sprite):
	"""Creates a prop of text based on the values inserted in the constructor"""
	
	def __init__(self, text, font, fontSize, color, X, Y, blink, move):
		super().__init__()
		self.move = move
		self.color = color
		self.str = text
		self.blink = blink
		self.boolean = True
		self.Y = Y
		self.X = X
		self.font = pygame.font.Font(font, fontSize)
		self.image = self.font.render(self.str, self.boolean, self.color)
		self.rect = self.image.get_rect(center=(self.X, self.Y - (self.image.get_height()/2)))
		self.animate = 0
	
	def update(self, color):
		if self.blink:			#Makes text blink, using background color
			self.animate += 0.05
			if self.animate < 1.5 and self.animate >= 0:
				self.image = self.font.render(self.str, self.boolean, color)
			elif self.animate >= 1.5:
				self.image = self.font.render(self.str, self.boolean, (0,213,255))
				self.animate = -1
		
		if self.move:	#Makes text moved down
			if self.Y < 240:
				self.Y += 3
				self.rect = self.image.get_rect(center=(self.X, self.Y - (self.image.get_height()/2)))
		
class Player(pygame.sprite.Sprite):
	""" This class represents the bar at the bottom that the player
		controls. """

	def __init__(self):
		""" Constructor function """
		super().__init__()
 
		# Create an image of the character
		self.George_move_left = []
		self.George_move_right = []
		self.current_animation = 0
		self.image = pygame.image.load("./Art/Character/GeorgeMovRight/georgeRight_0.png")
 
		#fill array with player movement for animation right
		for image in os.listdir("./Art/Character/GeorgeMovRight"):
			self.George_move_right.append(pygame.image.load(f"./Art/Character/GeorgeMovRight/{image}"))

		#fill array with player movement for animation left
		for image in os.listdir("./Art/Character/GeorgeMovleft"):
			self.George_move_left.append(pygame.image.load(f"./Art/Character/GeorgeMovLeft/{image}"))

		# Set a referance to the image rect.
		self.rect = self.image.get_rect()
 
		# Set speed vector of player
		self.change_x = 0
		self.change_y = 0
		self.movement = 1
		
		#Player score counter
		self.score = 0
 
		# List of sprites we can bump against
		self.level = None

	def update(self):
		""" Move the player. """
		# Gravity
		self.calc_grav()
 
		# Move left/right
		self.rect.x += self.change_x

		#animate movement right
		if self.change_x > 0:
			self.image = self.George_move_right[int(self.current_animation)]
			if self.current_animation > 3:
				self.current_animation = 0
			self.current_animation += .25
		if self.change_x == 0 and self.image in self.George_move_right: #If player stopped while facing right, character resets animation to face right standing
			self.image = self.George_move_right[0]
		
		if self.change_x < 0:
			self.image = self.George_move_left[int(self.current_animation)]
			if self.current_animation > 3:
				self.current_animation = 0
			self.current_animation += .25
		if self.change_x == 0 and self.image in self.George_move_left: #If player stopped while facing left, character resets animation to face left standing
			self.image = self.George_move_left[0]
 
		# See if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# If we are moving right,
			# set our right side to the left side of the item we hit
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right
 
		# Move up/down
		self.rect.y += self.change_y
 
		# Check and see if we hit anything
		self.block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in self.block_hit_list:
			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
		
				if self.change_x != 6:
					self.rect.x -= self.movement
 
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom
 
			# Stop our vertical movement
			self.change_y = 0
		if self.movement < 4:
			self.movement += 0.001

		#Collecting coins, removes them from the game
		coin_collection_list = pygame.sprite.spritecollide(self, self.level.coin_list, False)
		for coin in coin_collection_list:
			self.score += 1
			self.level.coin_list.remove(coin)
 
	def calc_grav(self):
		""" Calculate effect of gravity. """
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += .35
 
	def jump(self):
		""" Called when user hits 'jump' button. """
 
		# move down a bit and see if there is a platform below us.
		# Move down 2 pixels because it doesn't work well if we only move down
		# 1 when working with a platform moving down.
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 2
 
		# If it is ok to jump, set our speed upwards
		if len(platform_hit_list) > 0 or self.rect.bottom >= 480:
			self.change_y = -10
 
	# Player-controlled movement:
	def go_left(self):
		""" Called when the user hits a. """
		self.change_x = -6
 
	def go_right(self):
		""" Called when the user hits d. """

		self.change_x = 6
 
	def stop(self):
		""" Called when the user lets off the keyboard. """
		self.change_x = 0
 
