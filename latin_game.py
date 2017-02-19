import pygame
import numpy as np
import random
import vocabList as vocab
import time
import sys


pygame.init()

black = (0,0,0)
white = (255,255,255)
brown = (176, 154, 141)

#Window Sizes
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Latinissmimus')
font = pygame.font.Font('Roboto-Light.ttf', 25, bold = True) #size25
insfont = pygame.font.Font('Roboto-Light.ttf', 16)

locations = [(display_height*.8)]

random.seed(int(time.time()))

def generateRandomList(latin_list):
	arr = latin_list
	random.shuffle(arr)
	vocabulary = arr[:8]
	return vocabulary

class Odysseus(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.x = display_width*.2
		self.y = display_height*.8
		self.direction = "right"
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
		self.count = 0
		self.block_size = 40
		self.image = pygame.image.load('monster.png')
		# self.rect = self.image.get_rect()
		# self.rect.x = display_width*1.05
		# self.rect.y = display_height*.8
		self.rect = pygame.Rect(display_width*1.5, display_height*.8, 10, 40)
		font.set_bold(False)
		text = font.render(self.word, True, (220,220,220))
		text_rect = text.get_rect(left=self.rect.x, top= self.rect.y + self.block_size)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(self.image, [self.rect.x, self.rect.y, self.block_size, self.block_size])
		self.speedx = - 3	

	def update(self):
		self.rect = self.rect.move(self.speedx,0)
		font.set_bold(False)
		text = font.render(self.word, True, (220,220,220))
		text_rect = text.get_rect(left=self.rect.x - self.speedx, top= self.rect.y - self.block_size)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(self.image,[self.rect.x, self.rect.y, self.block_size, self.block_size])
	

def update_word():
	random.seed(int(time.time()))
	return random.choice(generateRandomList(vocab.latin))	

def text_objects(text,color):
	textSurface = font.render(text, True, color) # render text
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
	textSurf, textRect = text_objects(msg,color) 
	textRect.center = (display_width/2), (display_height/2)
	gameDisplay.blit(textSurf,textRect)

def updateHearts(lives): 
	if (lives!=0):
		filename = str(lives) + "-Hearts.png"
		heartsImage = pygame.image.load(filename)
		if lives == 1:
			block_width = 70 
		elif lives == 2:
			block_width = 138
		else:
			block_width = 200
		gameDisplay.blit(heartsImage,[display_width-200, 30, 25, 25])

def main_menu():
	main_menuloop = True

	while main_menuloop:
		for event in pygame.event.get():
				# if player quits game, exit out of two while loops
				if event.type == pygame.QUIT:
					main_menuloop = False
				if event.type == pygame.KEYDOWN:
					main_menuloop = False
					story()

		bg = pygame.image.load('title.png')
		gameDisplay.blit(bg, bg.get_rect())
		instruction1 = insfont.render("Help Ulysseus take on the Cyclopes!", True, (220,220,220))
		instruction2 = insfont.render("Jump over Cyclopes with incorrect Latin translations of English words with UP ARROW.", True, (220,220,200))
		instruction3 = insfont.render("Attack the Cyclops with the correct translation with Z.", True,(220,220,200))
		instruction4 = insfont.render("Touching Cyclopes or hitting the wrong Cyclopes will cost lives, so be careful!",True, (220,220,200))
			
		gameDisplay.blit(instruction1, [275, display_height/2, display_width*.8, 200])
		gameDisplay.blit(instruction2, [100, display_height/2+20, display_width*.8, 200])
		gameDisplay.blit(instruction3, [175, display_height/2+40, display_width*.8, 200])
		gameDisplay.blit(instruction4, [125, display_height/2+60, display_width*.8, 200])

		pygame.display.update()

def story():
	storyloop = True
	poly_pos_x = display_width
	poly_intro_x = -display_width
	poly_intro2_y = display_height
	move_poly = 20

	while storyloop:
		for event in pygame.event.get():
				# if player quits game, exit out of two while loops
				if event.type == pygame.QUIT:
					storyloop = False
				if event.type == pygame.KEYDOWN:
					main_menuloop = False
					learningLoop()

		gameDisplay.fill(brown)
		polyph = pygame.image.load("polyph.png")
		poly_intro = pygame.image.load("polyintro.png")
		poly_intro2 = pygame.image.load("polyintro2.png")
		gameDisplay.blit(polyph, [poly_pos_x, 0, display_width, display_height])
		gameDisplay.blit(poly_intro, [poly_intro_x, 0, display_width, display_height])
		gameDisplay.blit(poly_intro2, [0, poly_intro2_y, display_width, display_height])


		if poly_pos_x > 0:
			poly_pos_x -= move_poly

		if poly_pos_x <= 0 and poly_intro_x < 0:
			poly_intro_x += move_poly

		if poly_pos_x <= 0 and poly_intro_x >=0 and poly_intro2_y > 0:
			poly_intro2_y -= move_poly

		pygame.display.update()


def learningLoop():
	#vocabulary = generateRandomList(vocab.latin)
	learn_loop = True

	

	while learn_loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				learn_loop = False
			#if event.type == pygame.KEYDOWN:
				#learn_loop = False
				#gameloop()
		
		
		#vocab0 = vocabulary[:4]
		#vocab1 = vocabulary[4:]

		gameDisplay.fill((200,230,230))
		#pygame.draw.rect(gameDisplay, (0,0,0), [100, 100, 50, 50])
		font.set_bold(False)
		text = font.render("Learn the Vocabulary", True, (220,220,220))

		for x in range(30,display_width-30,190):
			pygame.draw.rect(gameDisplay, white, [x,120, 170, 170])
			pygame.draw.rect(gameDisplay, white, [x,320, 170, 170])

		pygame.display.update()

def gameloop():
	#Game Stuff
	

	gameExit = False
	gameOver = False
	latin_word_to_guess = update_word()
	eng_translation = vocab.dict[latin_word_to_guess]
	player = Odysseus()

	clock = pygame.time.Clock()
	FSP = 35
	y_start_pos = display_height*.8
	bottom = y_start_pos
	
	all_sprites = pygame.sprite.Group()
	cyclops = pygame.sprite.Group()
		
	create_Cyclopes = pygame.USEREVENT+1
	pygame.time.set_timer(create_Cyclopes,2000)

	sword = sword_hitbox()
	count = 0
	lives = 3
	score = 0

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
		
		collided_list = pygame.sprite.spritecollide(sword, cyclops, True)
		collided_list2 = pygame.sprite.spritecollide(player, cyclops, True)

		if len(collided_list2) != 0:
			lives = lives - 1
		for collision in collided_list:
			if (vocab.dict[collision.word] == eng_translation):
				score = score + 1
				latin_word_to_guess = update_word()
				eng_translation = vocab.dict[latin_word_to_guess]
			else:
				lives = lives - 1

		if (lives == 0):
			gameOver = True
		
		

		#gameDisplay.fill(white)
		bg = pygame.image.load('bg.png')
		gameDisplay.blit(bg, bg.get_rect())
		player.update_image(player.y, player.direction)

		updateHearts(lives)

		# Display the word to guess
		font.set_bold(True)
		text1 = font.render("word to guess: ", True, (32,32,32))
		text2 = font.render(eng_translation, True, (190,190,190))
		text3 = font.render("Score:" + str(score), True, (32,32,32))
		text_rect1 = text1.get_rect(left = 30, top = 35)
		text_rect2 = text2.get_rect(left = 30, top = 65)
		text_rect3 = text3.get_rect(left = display_width-180, top = 80) 
		gameDisplay.blit(text1, text_rect1)
		gameDisplay.blit(text2, text_rect2)
		gameDisplay.blit(text3, text_rect3)
		# Display the lives
		cyclops.update()
		all_sprites.update()
		pygame.display.update()
		clock.tick(FSP)



#learningLoop()
main_menu()
#story()