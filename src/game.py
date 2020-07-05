import pygame

class Game():
	def __init__(self):
		# Initialization
		self.width = 960
		self.height = 540
		self.cars = []
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.track = pygame.transform.scale(pygame.image.load('assets/track.png').convert_alpha(), (self.width, self.height))
		self.stop = False
		self.gates = [
			[[200, 400], [200, 540]],
			[[50, 450], [130, 390]],
			[[25, 290], [125, 290]],
			[[45, 140], [160, 160]],
			[[220, 30], [220, 130]],
			[[370, 60], [320, 140]],
			[[360, 230], [440, 170]],
			[[520, 210], [520, 310]],
			[[600, 150], [690, 190]],
			[[740, 25], [740, 125]],
			[[880, 70], [810, 140]],
			[[840, 220], [940, 220]],
			[[800, 340], [900, 340]],
			[[780, 400], [860, 500]],
			[[700, 400], [700, 540]],
			[[600, 400], [600, 540]],
			[[500, 400], [500, 540]],
			[[400, 400], [400, 540]],
			[[300, 400], [300, 540]]
		]
	
	def draw(self):
		# Set the white background
		self.screen.fill([255, 255, 255])

		# Draw every gate
		for gate in self.gates:
			pygame.draw.line(self.screen, [255, 0, 0], gate[0], gate[1])

		# Draw the cars
		for car in self.cars:
			if (car.alive):
				self.screen.blit(car.image, car.rect)

		# Draw the track
		self.screen.blit(self.track, [0, 0])
