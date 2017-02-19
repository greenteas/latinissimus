import pygame
import random
import vocabList as vocab

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

def generateRandomList(latin_list):
	arr = latin_list
	random.shuffle(arr)
	vocabulary = arr[:10]
	return vocabulary

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
		self.image = pygame.image.load('right_odysseus.png')
		self.hitbox_offset = 5
		self.rect = pygame.Rect(self.x+self.hitbox_offset, self.y, self.width-3*self.hitbox_offset, self.height-self.hitbox_offset)
		gameDisplay.blit(self.image, [self.x, self.y, self.width, self.height])

	def update_image(self,lead_y, direction):
		file_name = direction + '_odysseus.png'
		self.image = pygame.image.load(file_name)
		self.rect = pygame.Rect(self.x+self.hitbox_offset, self.y, self.width-3*self.hitbox_offset, self.height-self.hitbox_offset)
		#pygame.draw.rect(gameDisplay, black, self.rect)
		#if self.attack_state:
			#sword_hitbox(self)
		gameDisplay.blit(self.image, [self.x, lead_y, self.width, self.height])
	
class sword_hitbox(pygame.sprite.Sprite):
	def __init__(self):
		self.sword_height = 0
		self.sword_length = 0
		self.rect = pygame.Rect(0,0,1,1)

	def set(self, player):
		self.sword_height= player.height
		self.sword_length= 40
		self.rect = pygame.Rect(player.x+player.width,player.y, self.sword_length, self.sword_height)
		#self.sword_hitbox = pygame.draw.rect(gameDisplay, black, self.rect)
	
	def reset(self):
		self.sword_height = 0
		self.sword_length = 0
		self.rect = pygame.Rect(0,0,1,1)

	def update_hitbox(self, player):
		self.sword_height: player.height
		self.rect = pygame.Rect(player.x+player.width,player.y, self.sword_length, self.sword_height)
		#self.sword_hitbox = pygame.draw.rect(gameDisplay, black, self.rect)

class Cyclop(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.word = random.choice(generateRandomList(vocab.latin))

		print(self.word)

		self.block_size = 50
		self.travel = random.randrange(6)
		self.image = pygame.image.load('monster.png')
		self.rect = self.image.get_rect()
		self.rect.x = display_width*0.9
		self.rect.y = display_height*.8
		text = font.render(self.word, True, black)
		text_rect = text.get_rect(left=self.rect.x, top= self.rect.y + self.block_size)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(self.image, [self.rect.x, self.rect.y, self.block_size, self.block_size])
		self.speedx = - random.randrange(2,4)	

	def update(self):
		self.rect = self.rect.move(self.speedx,0)
		text = font.render(self.word, True, black)
		text_rect = text.get_rect(left=self.rect.x - self.speedx, top= self.rect.y - self.block_size)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(self.image,[self.rect.x, self.rect.y, self.block_size, self.block_size])
		

def text_objects(text,color):
	textSurface = font.render(text, True, color) # render text
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
	textSurf, textRect = text_objects(msg,color) 
	textRect.center = (display_width/2), (display_height/2)
	gameDisplay.blit(textSurf,textRect)

def update_word():
	print(random.choice(generateRandomList(vocab.latin)))

def gameloop():
	#Game Stuff
	gameExit = False
	gameOver = False
	update_word()
	player = Odysseus()

	clock = pygame.time.Clock()
	FSP = 35
	y_start_pos = display_height*.8
	bottom = y_start_pos
	
	all_sprites = pygame.sprite.Group()
	cyclops = pygame.sprite.Group()
		
	create_Cyclopes = pygame.USEREVENT+1
	pygame.time.set_timer(create_Cyclopes,3000)

	sword = sword_hitbox()
	count = 0

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
			if event.type == create_Cyclopes:
				c = Cyclop()
				all_sprites.add(c)
				cyclops.add(c)

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
			sword.set(player)
		else:
			player.attack_delay_counter = 0
			player.attack_state = False
			sword.reset()
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
	
		if pygame.sprite.spritecollideany(player, cyclops):
			gameOver = True
		if pygame.sprite.spritecollideany(sword, cyclops):
			count +=1
			#print(count)

		gameDisplay.fill(white)
		player.update_image(player.y, player.direction)
		cyclops.update()
		all_sprites.update()
		pygame.display.update()
		clock.tick(FSP)




gameloop()