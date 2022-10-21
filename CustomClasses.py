import pygame, random

class Cloud(pygame.sprite.Sprite): #Class to create clouds
	def __init__(self, imgPath):
		super().__init__()
		self.W = random.randrange(150, 250)
		self.H = self.W-20
		self.posX = random.randrange(self.W, 640)
		self.posY = random.randrange(self.H, 240)
		self.image = pygame.image.load(imgPath)
		self.image = pygame.transform.scale(self.image, (self.W, self.H))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.posX - self.W, self.posY - self.H)
		self.animate = 0

	def update(self): # Makes em clouds move up & down
		
		if self.animate <= 2:
			self.animate += 0.08
			self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1] - int(self.animate))

		else:
			self.animate = -2
			self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1] - int(self.animate))

class Text(pygame.sprite.Sprite): # Class to create text
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
		if self.blink:																					#Makes text blink, using background color
			self.animate += 0.05
			if self.animate < 1.5 and self.animate >= 0:
				self.image = self.font.render(self.str, self.boolean, color)
			elif self.animate >= 1.5:
				self.image = self.font.render(self.str, self.boolean, (0,213,255))
				self.animate = -1
		
		if self.move:																					#Makes text moved down
			if self.Y < 240:
				self.Y += 3
				self.rect = self.image.get_rect(center=(self.X, self.Y - (self.image.get_height()/2)))
			


class Character(pygame.sprite.Sprite): #Character class for animation
	def __init__(self, X, Y):			#Arrays to store images for movement animation.
		super().__init__()	
		self.X = X
		self.Y = Y
		self.moveFront = []	
		self.currentPos = 0
		
		self.moveFront.append(pygame.image.load(f"georgeFront_0.png"))
		self.moveFront.append(pygame.image.load(f"georgeFront_1.png"))
		self.moveFront.append(pygame.image.load(f"georgeFront_2.png"))
		self.moveFront.append(pygame.image.load(f"georgeFront_3.png"))

		self.moveLeft = []

		self.moveLeft.append(pygame.image.load(f"georgeLeft_0.png"))
		self.moveLeft.append(pygame.image.load(f"georgeLeft_1.png"))
		self.moveLeft.append(pygame.image.load(f"georgeLeft_2.png"))
		self.moveLeft.append(pygame.image.load(f"georgeLeft_3.png"))

		self.moveRight = []
		
		self.moveRight.append(pygame.image.load(f"georgeRight_0.png"))
		self.moveRight.append(pygame.image.load(f"georgeRight_1.png"))
		self.moveRight.append(pygame.image.load(f"georgeRight_2.png"))
		self.moveRight.append(pygame.image.load(f"georgeRight_3.png"))

		self.image = self.moveFront[self.currentPos]
		self.rect = self.image.get_rect(midbottom=(self.X, self.Y))

	def update(self, left, right, jump, JY = 0): #Animates the characher to loop 4 different png files.

		if jump:
			if self.Y > JY - 200:
				self.Y -= 15
				self.rect = self.image.get_rect(topleft=(self.X, self.Y))
			print(self.Y, JY - 160, jump)

		if left: #Allows char movement to left
			self.image = self.moveLeft[int(self.currentPos)]
			self.currentPos += 0.8
			self.X -= 5
			self.rect = self.image.get_rect(midtop=(self.X, self.Y))
			
			if self.currentPos >= 4:
				self.currentPos = 0

			
		elif right: #Allows char movement to right
			self.X += 5
			self.image = self.moveRight[int(self.currentPos)]
			self.currentPos += 0.8
			
			self.rect = self.image.get_rect(midtop=(self.X, self.Y))
			
			if self.currentPos >= 4:
				self.currentPos = 0
			
		else:	#Makes mainmenu player animation
			self.currentPos += 0.1
			self.image = self.moveFront[int(self.currentPos)]

		if self.currentPos >= 3.9:
					self.currentPos = 0

class Tile(pygame.sprite.Sprite):
	def __init__(self, imgPath, X, Y):
		super().__init__()
		self.imgPath = imgPath #Tile to load
		self.X = X
		self.Y = Y
		self.image = pygame.image.load(self.imgPath)
		self.image = pygame.transform.scale(self.image, (60, 50))
		self.rect = self.image.get_rect()
		self.rect.topleft = (X, Y)

		
