import pygame

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = '../graphics/' + color + '.png'
		self.image = pygame.image.load(file_path)
		self.rect = self.image.get_rect(topleft=(x,y))
		self.point = {'red':100, 'green':200, 'yellow':300}
		self.value = self.point[color]

	def move_alien(self,direction):
		self.rect.x += direction

	def update(self,direction):
		self.move_alien(direction)

class Extra(pygame.sprite.Sprite):
	def __init__(self,side,width):
		super().__init__()
		self.image = pygame.image.load('../graphics/extra.png')
		if side == 'right':
			x = width + 100
			self.speed = -3
		else:
			x = -100
			self.speed = 3
		self.rect = self.image.get_rect(topleft=(x,60))

	def update(self):
		self.rect.x += self.speed