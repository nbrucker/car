import pygame

class Game():
	def __init__(self):
		self.width = 960
		self.height = 540
		self.cars = []
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.track = pygame.transform.scale(pygame.image.load('assets/track.png').convert_alpha(), (self.width, self.height))
		self.stop = False
		self.gates = []
	
	def draw(self):
		self.screen.fill([255, 255, 255])
		for gate in self.gates:
			pygame.draw.line(self.screen, [255, 0, 0], gate[0], gate[1])
		for car in self.cars:
			if (car.alive):
				self.screen.blit(car.image, car.rect)
		self.screen.blit(self.track, [0, 0])
