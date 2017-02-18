import pygame
import random

pygame.init()

black = (0,0,0)
white = (255,255,255)

#Window Sizes
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Latinissmimus')
font = pygame.font.SysFont(None,25) #size25

locations = [(display_height*.8)]
class Odysseus(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.x = display_width*.2
		self.y = display_height*.8
		self.direction = "right"
		self.lives = 3
		self.height = 50
		self.width = 50
		#Jump Variables
		self.jump_max_height = self.y-self.height*2
		self.change_y = 0
		self.middle_of_jump = False
		self.at_max_height = False
		self.attack_state= False
		self.travel_step = 50
		self.attack_delay = 60
		self.attack_delay_counter = 0
		self.image = pygame.image.load('right_odysseus.gif')
		#self.rect = [self.x+self.width*.9, self.y+self.height*.4, self.width*.3, self.height*.2]
		self.sword_boundary = [self.x+self.width*.9, self.y+self.height*.4, self.width*.3, self.height*.2]
		self.sword_hitbox = pygame.draw.rect(gameDisplay, black, self.sword_boundary)
		gameDisplay.blit(self.image, [self.x, self.y, self.width, self.height])

	def update_image(self,lead_y, direction):
		file_name = direction + '_odysseus.gif'
		self.image = pygame.image.load(file_name)
		#self.rect = [self.x+self.width*.9, self.y+self.height*.4, self.width*.3, self.height*.2]
		self.sword_boundary = [self.x+self.width*.9, self.y+self.height*.4, self.width*.3, self.height*.2]
		self.sword_hitbox = pygame.draw.rect(gameDisplay, black, self.sword_boundary)
		gameDisplay.blit(self.image, [self.x, lead_y, self.width, self.height])
	

class Cyclop(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.word = word
		#self.x = random.randrange(display_width*.6, display_width*.95)
		#self.y = display_height*.8
		self.block_size = 50
		self.travel = random.randrange(6)
		self.image = pygame.image.load('monster.png')
		
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(display_width*.6, display_width*.95) #display_width*.4
		self.rect.y = display_height*.8 #display_height*.4
		gameDisplay.blit(self.image, [self.rect.x, self.rect.y, self.block_size, self.block_size])
		self.speedx = - random.randrange(2,4)

	def update(self):
		self.rect = self.rect.move(self.speedx,0)
		#print(self.travel)
		#self.x = self.x - self.travel
		gameDisplay.blit(self.image, [self.rect.x, self.rect.y, self.block_size, self.block_size])
		#gameDisplay.blit(self.image, [self.x, self.y, self.block_size, self.block_size])
		

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

	player = Odysseus()

	clock = pygame.time.Clock()
	FSP = 30
	y_start_pos = display_height*.8
	bottom = y_start_pos
	
	all_sprites = pygame.sprite.Group()
	cyclops = pygame.sprite.Group()
		
	for i in range(5):
		c = Cyclop()
		all_sprites.add(c)
		cyclops.add(c)

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
				if event.key == pygame.K_UP and player.middle_of_jump == False:
					player.change_y= -player.travel_step
					player.middle_of_jump = True
				# NOTE: REMOVE BOTTOM TWO LINES ONCE WE HAVE CYCLOPS 
				elif event.key == pygame.K_x:	
					gameOver = True
				elif event.key == pygame.K_z:
					player.direction = "attack"
					player.attack_state = True

		player.y += player.change_y

		if player.attack_state == True and player.attack_delay_counter < player.attack_delay:
			player.attack_delay_counter += 10
		else:
			player.attack_delay_counter = 0
			player.attack_state = False
			if not player.attack_state:
				player.direction = "right"

		if player.middle_of_jump and not player.at_max_height:
			player.change_y +=player.travel_step/10
			if not player.attack_state:
				player.direction = "up"
		elif player.middle_of_jump and player.at_max_height:
			player.change_y -= player.travel_step/10
		elif player.direction != "attack":
			player.direction = "right"
		#make block go down after maximum height/ land on bottom	
		if player.y == player.jump_max_height:
			player.change_y = player.travel_step
			player.at_max_height = True
		if player.y >= bottom:
			player.change_y = 0
			player.middle_of_jump = False
			player.at_max_height = False
			player.y += player.change_y
		
		gameDisplay.fill(white)
		player.update_image(player.y, player.direction)
		cyclops.update()
		all_sprites.update()
		pygame.display.update()
		clock.tick(FSP)




gameloop()