import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser
from random import choice, randint

class Game:
	def __init__(self):
		player_sprite = Player((WIDTH/2,HEIGHT))
		self.player = pygame.sprite.GroupSingle(player_sprite)

		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.amount = 4
		self.dist = [num * (WIDTH / self.amount) for num in range(self.amount)]
		self.create_multiple_obstacle()

		self.alien = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup()
		self.direction = 1
		self.extra = pygame.sprite.Group()
		self.extra_spawn_time = randint(400,800)

		self.lives = 3
		self.live_surf = pygame.image.load('../graphics/player.png')
		self.start_x = WIDTH - ((self.live_surf.get_size()[0] * 2)) - 15
		self.score = 0
		self.font = pygame.font.Font('../font/Pixeled.ttf',15)

		music = pygame.mixer.Sound('../audio/music.wav')
		music.set_volume(0.2)
		music.play()

		self.explosion_music = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_music.set_volume(0.2)
		

	def create_obstacle(self, x_dist, y_dist):
		for row_index, row in enumerate(self.shape):
			for col_index, col in enumerate(row):
				if col == 'x':
					x = x_dist + col_index * self.block_size + 15
					y = y_dist + row_index * self.block_size
					block = obstacle.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)
		# for row_index, row in enumerate(self.shape):
		# 	for col_index, col in enumerate(row):
		# 		if col == 'x':
		# 			x = 100 + col_index * self.block_size
		# 			y = 280 + row_index * self.block_size
		# 			block = obstacle.Block(self.block_size,(241,79,80),x,y)
		# 			self.blocks.add(block)
		# for row_index, row in enumerate(self.shape):
		# 	for col_index, col in enumerate(row):
		# 		if col == 'x':
		# 			x = 200 + col_index * self.block_size
		# 			y = 280 + row_index * self.block_size
		# 			block = obstacle.Block(self.block_size,(241,79,80),x,y)
		# 			self.blocks.add(block)
		# for row_index, row in enumerate(self.shape):
		# 	for col_index, col in enumerate(row):
		# 		if col == 'x':
		# 			x = 300+col_index * self.block_size
		# 			y = 280 + row_index * self.block_size
		# 			block = obstacle.Block(self.block_size,(241,79,80),x,y)
		# 			self.blocks.add(block)

	def create_multiple_obstacle(self):
		for x_pos in self.dist:
			self.create_obstacle(x_pos,280)

	def run(self):		
		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		self.player.update()
		self.blocks.draw(screen)
		self.alien.draw(screen)
		self.alien.update(self.direction)
		self.check_direction()
		self.alien_lasers.update()
		self.alien_lasers.draw(screen)
		self.extra_alien_timer()
		self.extra.update()
		self.extra.draw(screen)
		self.collision()
		self.display_lives()
		self.display_score()

	def display_score(self):
		score_surf = self.font.render(f'Score: {self.score}',False,(4,254,64))
		score_rec = score_surf.get_rect(topleft=(0,0))
		screen.blit(score_surf,score_rec)

	def check_direction(self):
		aliens = self.alien.sprites()
		for alien in aliens:
			if alien.rect.right > WIDTH:
				self.direction = -1
				self.alien_down(2)
			elif alien.rect.left < 0:
				self.direction = 1
				self.alien_down(2)

	def alien_down(self,dist):
		if self.alien:
			for alien in self.alien.sprites():
				alien.rect.y += dist

	def alien_setup(self):
		for row_index, row in enumerate(range(3)):
			for col_index, col in enumerate(range(5)):
				x = col_index * 60 + 60
				y = row_index * 48 + 90
				if row_index == 0:
					alien_sprite = Alien('yellow',x,y)
				elif 1 <= row_index < 2:
					alien_sprite = Alien('green',x,y)
				else:
					alien_sprite = Alien('red',x,y)
				self.alien.add(alien_sprite)

	def display_lives(self):
		for live in range(self.lives-1):
			x = self.start_x + live * (self.live_surf.get_size()[0] + 10)
			screen.blit(self.live_surf,(x,10))

	def alien_shoot(self):
		if self.alien.sprites():
			random_alien = choice(self.alien.sprites())
			#print(self.alien.sprites())
			laser_sprite = Laser(random_alien.rect.center, HEIGHT, 2)
			self.alien_lasers.add(laser_sprite)

	def collision(self):
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				#print(self.player.sprite.lasers)
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()

				alien_hit = pygame.sprite.spritecollide(laser,self.alien,True)
				if alien_hit:
					self.score += alien_hit[0].value
					# print(self.score)
					laser.kill()
					self.explosion_music.play()

				if pygame.sprite.spritecollide(laser,self.extra,True):
					laser.kill()

		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					if self.lives == 0:
						pygame.quit()
						sys.exit()

		if self.alien:
			for alien in self.alien:
				pygame.sprite.spritecollide(alien,self.blocks,True)
				if pygame.sprite.spritecollide(alien,self.player,False):
					pygame.quit()
					sys.exit()




	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time < 0:
			self.extra.add(Extra(choice(['right','left']),WIDTH))
			self.extra_spawn_time = randint(400,800)



if __name__ == '__main__':
	pygame.init()
	WIDTH = 400
	HEIGHT = 400
	screen = pygame.display.set_mode((WIDTH,HEIGHT))
	clock = pygame.time.Clock()
	game = Game()
	alien_shoot_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(alien_shoot_timer,800)


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == alien_shoot_timer:
				game.alien_shoot()
		screen.fill((30,30,30))
		game.run()
		pygame.display.flip()
		clock.tick(60)