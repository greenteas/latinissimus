import pygame

pygame.init()

black = (0,0,0)
white = (255,255,255)

#Window Sizes
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Latinissmimus')
font = pygame.font.SysFont(None,25) #size25

class Odysseus():
	def __init__(self):
		self.x = display_width*.2
		self.y = display_height*.8
		self.direction = "right"
		self.lives = 3
		self.block_size = 50
		#Jump Variables
		self.jump_max_height = self.y-self.block_size*2
		self.change_y = 0
		self.middle_of_jump = False
		self.at_max_height = False
		self.travel_step = 50
		img = pygame.image.load('right_odysseus.gif')
		gameDisplay.blit(img, [self.x, self.y, self.block_size, self.block_size])

	def update_image(self,lead_y, direction):
		file_name = direction + '_odysseus.gif'
		img = pygame.image.load(file_name)
		gameDisplay.blit(img, [self.x, lead_y, self.block_size, self.block_size])
	

#class Cyclops():
	#def __init__(self,word):
		#self.x = display_width*.8
		#self.y = display_height*.8
		#self.block_size = 50
		#file_name = 'right_cyclops.gif'
		#img = pygame.image.load(file_name)
		#gameDisplay.blit(img, [self.x, lead_y, self.block_size, self.block_size])

def text_objects(text,color):
	textSurface = font.render(text, True, color) # render text
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
	textSurf, textRect = text_objects(msg,color) 
	textRect.center = (display_width/2), (display_height/2)
	gameDisplay.blit(textSurf,textRect)


def gameloop():
	#Game Stuff
	gameExit = False
	gameOver = False

	clock = pygame.time.Clock()
	FSP = 30
	block_size = 50
	y_start_pos = display_height*.8
	jump_max_height = y_start_pos-block_size*2
	change_y = 0
	travel_step = 50
	lead_y = y_start_pos
	bottom = y_start_pos
	middle_of_jump = False
	at_max_height = False
	direction = "right"
	lives = 3

	while not gameExit:
		while gameOver == True:
			gameDisplay.fill(black)
			message_to_screen("game over, press C to play again or Q to quit", white)
			pygame.display.update()

			for event in pygame.event.get():
				# if player quits game, exit out of two while loops
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_q: # if the player quits
						gameExit = True
						gameOver = False 

					if event.key == pygame.K_c: # if the player continues game
						gameloop() 

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
				gameOver = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and middle_of_jump == False:
					change_y= -travel_step
					middle_of_jump = True
				# NOTE: REMOVE BOTTOM TWO LINES ONCE WE HAVE CYCLOPS 
				elif event.key == pygame.K_x:	
					gameOver = True

		lead_y += change_y

		if middle_of_jump and not at_max_height:
			change_y +=travel_step/10
			key_pressed = "up"
		elif middle_of_jump and at_max_height:
			change_y -=travel_step/10
		else:
			key_pressed = "right"
		#make block go down after maximum height/ land on bottom	
		if lead_y == jump_max_height:
			change_y = travel_step
			at_max_height = True
		if lead_y >= bottom:
			change_y = 0
			middle_of_jump = False
			at_max_height = False
			lead_y += change_y

		gameDisplay.fill(white)
		player.update_image(lead_y, key_pressed)
		pygame.display.update()
		clock.tick(FSP)

player = Odysseus()
#cyclops = Cyclops("girl")
gameloop()