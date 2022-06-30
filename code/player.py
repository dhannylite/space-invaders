import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('../graphics/player.png')
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = 5
		self.width = pos[0] * 2
		self.height = pos[1]
		self.ready = True
		self.cooldown = 600
		self.laser_time = 0
		self.lasers = pygame.sprite.Group()
		self.music = pygame.mixer.Sound('../audio/laser.wav')
		self.music.set_volume(0.2)
	
	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed

		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		elif keys[pygame.K_SPACE] and self.ready:
			self.shoot()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()

	def shoot(self):
		self.lasers.add(Laser(self.rect.center,self.height,-5))
		self.music.play()


	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			# print(current_time,self.laser_time)
			if current_time - self.laser_time > self.cooldown:
				self.ready = True 


	def constraint(self):
		if self.rect.right > self.width:
			self.rect.right = self.width
		if self.rect.left < 0:
			self.rect.left = 0


	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()