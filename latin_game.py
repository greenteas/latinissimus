import pygame
import numpy as np
import random
import vocabList as vocab
import time
import sys
from os import path

pygame.init()

# set default colors
black = (0,0,0)
white = (255,255,255)
brown = (176, 154, 141)

# window Sizes
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Latinissmimus')
icon = pygame.image.load("monster.png")
pygame.display.set_icon(icon)

# set fonts
sm_font = pygame.font.Font('Roboto-Light.ttf', 16, bold = False) 
sm_b_font = pygame.font.Font('Roboto-Medium.ttf', 16, bold = False)
font = pygame.font.Font('Roboto-Light.ttf', 25, bold = True) 
large_font = pygame.font.Font('Roboto-Medium.ttf', 48, bold = False)
headerfont = pygame.font.Font('Roboto-Light.ttf', 36)
insfont = pygame.font.Font('Roboto-Light.ttf', 16)

# current_vocab_list - stores the vocabulary words currently being tested
global current_vocab_list 
current_vocab_list = []
locations = [(display_height*.8)]

random.seed(int(time.time()))

# generateRandomList -  returns a randomly generated list of Latin words
def generateRandomList(latin_list):
	arr = latin_list
	random.shuffle(arr)
	global current_vocab_list 
	current_vocab_list = arr[:8]
	return current_vocab_list

# the Odysseus class is used to create Odysseus, the main character
class Odysseus(pygame.sprite.Sprite):

	# initialize Odysseus sprite
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.x = display_width*.2
		self.y = display_height*.8
		self.direction = "right"
		self.height = 50
		self.width = 50

		# variables that will allow the sprite to smoothly jump
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

	# update_image - updates the image of the sprite based on the direction it is facing
	def update_image(self,lead_y, direction):
		file_name = direction + '_odysseus.png'
		self.image = pygame.image.load(file_name)
		self.rect = pygame.Rect(self.x+self.hitbox_offset, self.y, self.width-3*self.hitbox_offset, self.height-self.hitbox_offset)
		gameDisplay.blit(self.image, [self.x, lead_y, self.width, self.height])
		
# the sword hit_box class will create the hit box region for the sword
# the hit box will detect collisions with the Cyclops
class sword_hitbox(pygame.sprite.Sprite):

	# initialize the sword of Odysseus
	def __init__(self):
		self.sword_height = 0
		self.sword_length = 0
		self.rect = pygame.Rect(0,0,1,1)

	# set - sets the hit box on the sword
	def set(self, player):
		self.sword_height= player.height
		self.sword_length= 40
		self.rect = pygame.Rect(player.x+player.width,player.y, self.sword_length, self.sword_height)
		#self.sword_hitbox = pygame.draw.rect(gameDisplay, black, self.rect)
	
	# reset - resets the hit box away from the sword
	def reset(self):
		self.sword_height = 0
		self.sword_length = 0
		self.rect = pygame.Rect(0,0,1,1)

	# update_hitbox - update the position of the hit box based on movement of Odysseus
	def update_hitbox(self, player):
		self.sword_height: player.height
		self.rect = pygame.Rect(player.x+player.width,player.y, self.sword_length, self.sword_height)
		#self.sword_hitbox = pygame.draw.rect(gameDisplay, black, self.rect)

# Cyclop class creates a Cyclopes sprite for the enemy characters in the game
class Cyclop(pygame.sprite.Sprite):

	# initialize the Cyclop sprite
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		# word will be the word assigned to each Cyclops
		self.word = random.choice(current_vocab_list)

		# variables that will allow us to control image and movement of the Cyclops
		self.block_size = 50
		self.image = pygame.image.load('monster.png')
		self.rect = pygame.Rect(display_width*1.5, display_height*.8, 10, 40)
		font.set_bold(False)
		text = font.render(self.word, True, (220,220,220))
		text_rect = text.get_rect(left=self.rect.x, top= self.rect.y + self.block_size)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(self.image, [self.rect.x, self.rect.y, self.block_size, self.block_size])
		self.speedx = - 3	

	# update - group function that will update the movements and positions of each sprite from the group
	def update(self):
		self.rect = self.rect.move(self.speedx,0)
		font.set_bold(False)
		text = font.render(self.word, True, (220,220,220))
		text_rect = text.get_rect(left=self.rect.x - self.speedx, top= self.rect.y - self.block_size)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(self.image,[self.rect.x, self.rect.y, self.block_size, self.block_size])
	
# text_objects - renders font
def text_objects(text,color):
	textSurface = font.render(text, True, color) # render text
	return textSurface, textSurface.get_rect()

#  message_to_screen - function that displays message to screen
def message_to_screen(msg, color):
	textSurf, textRect = text_objects(msg,color) 
	textRect.center = (display_width/2), (display_height/2)
	gameDisplay.blit(textSurf,textRect)

# updateHearts - updates the lives of Odysseus
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

# main_menu - displays the main menu that welcomes the user to play the game
def main_menu():
	main_menuloop = True

	while main_menuloop:
		for event in pygame.event.get():
				# if player quits game, exit out of two while loops
				if event.type == pygame.QUIT:
					main_menuloop = False
					pygame.quit()
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

# story - displays the intermediate screen that will show after the main_menu and the vocabulary display
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
				pygame.quit()
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

# learningLoop - displays the vocabulary words for the user to learn before playing the game
def learningLoop():
	# generate a list of words using the generateRandomList(vocab.latin) function
	global current_vocab_list 
	current_vocab_list = generateRandomList(vocab.latin)
	print(current_vocab_list)
	learn_loop = True

	while learn_loop:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				learn_loop = False
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				learn_loop = False
				gameloop()
		
		
		vocab0 = current_vocab_list[:4]
		vocab1 = current_vocab_list[4:]

		gameDisplay.fill((174,207,198))
		
		
		# x - the x position for the text that will be displayed
		x = 40
		
		for i in range(4):
			filename0 = vocab.dict[vocab0[i]]+'.png'
			filename1 = vocab.dict[vocab1[i]]+'.png'
			image1 = pygame.image.load(path.join('pictures/',filename0))
			image2 = pygame.image.load(path.join('pictures/',filename1))
			gameDisplay.blit(image1, [x, 110, 170, 170])
			gameDisplay.blit(image2, [x, 350, 170, 170])
			text1 = sm_b_font.render(vocab0[i]+':', True, (10,10,10))
			text2 = sm_font.render(vocab.dict[vocab0[i]], True, (32,32,32)) 
			text3 = sm_b_font.render(vocab1[i]+':', True, (10,10,10))
			text4 = sm_font.render(vocab.dict[vocab1[i]], True, (32,32,32)) 
			text_rect1 = text1.get_rect(left = x, top = 285)
			text_rect2 = text2.get_rect(left = x, top = 305)
			text_rect3 = text2.get_rect(left = x, top = 525)
			text_rect4 = text2.get_rect(left = x, top = 545)
			gameDisplay.blit(text1, text_rect1)
			gameDisplay.blit(text2, text_rect2)
			gameDisplay.blit(text3, text_rect3)
			gameDisplay.blit(text4, text_rect4)
			x = x + 190
		text = large_font.render("LEARN THE VOCABULARY", True, (0,0,0))
		text_rect = text.get_rect(left = 120, top = 20)
		instruction = font.render("Press spacebar to play", True, (25,25,25))
		instruction_rect = instruction.get_rect(left = display_width/2 -125, top = 70)
		gameDisplay.blit(text, text_rect)
		gameDisplay.blit(instruction, instruction_rect)
		pygame.display.update()

# youWin - displays the youWin screen
def youWin():
	you_Win = True
	while you_Win:

		gameDisplay.fill((178,158,181))
		message_to_screen("You win! Press C to play again, press Q to quit.", white)
		pygame.display.update()
		global current_vocab_list  
		current_vocab_list = []
		for event in pygame.event.get():
			# if player quits game, exit out of two while loops
			if event.type == pygame.QUIT:
				gameExit = True
				gameOver = False
				you_Win = False
				pygame.quit()
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_q: # if the player quits
					gameExit = True
					gameOver = False 
					you_Win = False
					main_menu()
				if event.key == pygame.K_c: # if the player continues game
					you_Win = False
					learningLoop() 

# gameloop - displays the actual game
def gameloop():
	#Game Stuff
	

	gameExit = False
	gameOver = False
	you_Win = False
	global current_vocab_list 
	latin_word_to_guess = current_vocab_list[0]
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

		### ---- GAME OVER SCREEN ---- ###
		while gameOver == True:

			gameDisplay.fill(black)
			message_to_screen("game over, press C to play again or Q to quit", white)
			pygame.display.update()
			current_vocab_list = []
			for event in pygame.event.get():
				# if player quits game, exit out of two while loops
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
					pygame.quit()
				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_q: # if the player quits
						gameExit = True
						gameOver = False 
						main_menu()
					if event.key == pygame.K_c: # if the player continues game
						learningLoop() 

		### ---- GAME SCREEN ---- ####
		for event in pygame.event.get():
			if event.type == create_Cyclopes:
				c = Cyclop()
				all_sprites.add(c)
				cyclops.add(c)

			if event.type == pygame.QUIT:
				gameExit = True
				gameOver = False
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and player.middle_of_jump == False:
					player.change_y= -player.travel_step
					player.middle_of_jump = True
				# NOTE: REMOVE BOTTOM TWO LINES ONCE WE HAVE CYCLOPS 
				if event.key == pygame.K_z:
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
				count = count + 1
				latin_word_to_guess = current_vocab_list[count]
				eng_translation = vocab.dict[latin_word_to_guess]
			else:
				lives = lives - 1

		if (lives == 0):
			gameOver = True
		
		if (count == 8):
			you_Win = True
			youWin()

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



main_menu()
story()
learningLoop()