import pygame

class Laser(pygame.sprite.Sprite):
	def __init__(self, pos, height, speed):
		super().__init__()
		self.image = pygame.Surface((4,20))
		self.image.fill('white')
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height = height

	def move_laser(self):
		self.rect.y += self.speed

	def destroy(self):
		if self.rect.y < -50 or self.rect.y > self.height:
			self.kill()

	def update(self):
		self.move_laser()
		self.destroy()



