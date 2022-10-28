import pygame
import Props, Stages

# Colors
BLUE = (0,213,255)
 
# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480 

def main(Mainmenu):
	""" Main Program """
	pygame.init()
 
	# Set the height and width of the screen
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)
 
	pygame.display.set_caption("Running shoes on!") #Name the game
 
	# Create the player
	player = Props.Player()

	#Create interactive screens
	menu = Stages.MainMenu()
	game = Stages.MainGame(player)
	gg = Stages.GameOver(player)
	victoryscreen = Stages.Victory(player)
	
	Gameover = False
  
	#Create group of active sprites
	active_sprite_list = pygame.sprite.Group()
	
	#Setup player
	player.level = game
	player.rect.x = 320 - player.image.get_width()
	player.rect.y = -100

	active_sprite_list.add(player)
 
	# Loop until the user clicks the close button.
	done = False
 
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()
 
	# -------- Main Program Loop -----------
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a: #Move left
					player.go_left()
				if event.key == pygame.K_d:	#Move right
					player.go_right()
				if event.key == pygame.K_w: #Jump
					player.jump()
				if event.key == pygame.K_SPACE:
					if Mainmenu == True: #Start playing
						Mainmenu = False
					elif Gameover or victory:	#Restarts the game
						main(False)				

				if event.key == pygame.K_ESCAPE: #Restarts the session
					main(True)	
 
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a and player.change_x < 0: #Stops movement
					player.stop()
				if event.key == pygame.K_d and player.change_x > 0:	#Stops movement
					player.stop()

		victory = pygame.sprite.collide_rect(player, player.level.ending) #Checks for collision with flag
		
		# Update items in the level

		if Mainmenu: #Updates main menu if it is open
			menu.update()
		elif Gameover: #Updates gameover if it is open
			gg.update(player)
		elif victory:	#Updates victory screen if it is open
			victoryscreen.update(player)
		else:	#Updates the game
			game.update()
			active_sprite_list.update()

		# If the player gets near the right side, shift the world left (-x)
		if player.rect.right > SCREEN_WIDTH:
			player.rect.right = SCREEN_WIDTH
 
		# If the player gets near the left side, shift the world right (+x)
		if player.rect.left < 0:
			player.rect.left = 0

		# If player falls down GameOver!
		if player.rect.top > SCREEN_HEIGHT:
			Gameover = True
	
		# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

		game.draw(screen)
		active_sprite_list.draw(screen)
		if Mainmenu:
			menu.draw(screen)
		if Gameover:
			gg.draw(screen)
		if victory:
			victoryscreen.draw(screen)
 
		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
		# Limit to 60 frames per second
		clock.tick(60)
 
		# Updates the screen.
		pygame.display.flip()
 
	pygame.quit()
 
if __name__ == "__main__":
	main(True)