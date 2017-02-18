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

def message_to_screen(msg, color):
	screen_text = font.render(msg, True, color) #true for antialising
	gameDisplay.blit(screen_text, [display_width/2, display_height/2])

def gameloop():
	#Game Stuff
	gameExit = False
	gameOver = False
	clock = pygame.time.Clock()
	FSP = 30

	#Jump Variables
	block_size = 50
	y_start_pos = display_height*.8
	jump_max_height = y_start_pos-block_size*2
	change_y = 0
	travel_step = 50
	lead_y = y_start_pos
	lead_x = display_width*.2
	bottom = y_start_pos
	middle_of_jump = False
	at_max_height = False

	while not gameExit:
		while gameOver == True:
			gameDisplay.fill(black)
			message_to_screen("game over", white)
			pygame.display.update()

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_a and middle_of_jump == False:
						change_y= -travel_step
						middle_of_jump = True

		lead_y += change_y

		#change speeds mid jump for physics effects
		if middle_of_jump and not at_max_height:
			change_y +=travel_step/10
		elif middle_of_jump and at_max_height:
			change_y -=travel_step/10
		
		#make block go down after maximum height/ land on bottom	
		if lead_y == jump_max_height:
			change_y = travel_step
			at_max_height = True
		if lead_y >= bottom:
			change_y = 0
			middle_of_jump = False
			at_max_height = False

		gameDisplay.fill(white)
		pygame.draw.rect(gameDisplay, black, [lead_x,lead_y,block_size,block_size])
		pygame.display.update()

		clock.tick(FSP)

gameloop()