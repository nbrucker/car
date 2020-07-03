import pygame
from pygame.math import Vector2
from copy import deepcopy

class Car():
	def __init__(self):
		self.path = 'assets/car.png'

		self.size = [40, 20]
		self.initialPosition = Vector2(250, 450)
		self.initialRotation = 180
		self.reset()

		self.image = pygame.image.load(self.path).convert_alpha()
		self.image = pygame.transform.scale(self.image, self.size)
		self.original = self.image
		self.image = pygame.transform.rotate(self.image, self.rotation)
	
		self.rect = self.image.get_rect(center=self.position)

	def update(self):
		self.position += self.velocity.rotate(-self.rotation)

		self.image = pygame.transform.rotate(self.original, self.rotation)
		self.rect.center = self.position
		self.rect = self.image.get_rect(center=self.rect.center)
	
	def reset(self):
		self.position = deepcopy(self.initialPosition)
		self.velocity = Vector2(0, 0)
		self.rotation = self.initialRotation
		self.alive = True
