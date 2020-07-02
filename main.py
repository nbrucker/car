import pygame
from copy import deepcopy
import shapely
from shapely.geometry import LineString, Point

from ai import *
from game import *
from car import *

def selectParent(ais, fitnessSum):
	rand = random.uniform(0, fitnessSum)
	currentSum = 0
	for ai in ais:
		currentSum += ai.fitness
		if (currentSum > rand):
			return ai

def getFitnessSum(ais):
	fitnessSum = 0
	for ai in ais:
		fitnessSum += ai.fitness
	return fitnessSum

def mixWeights(a, b):
	weights = deepcopy(a)
	for i in range(len(weights)):
		for j in range(len(weights[i])):
			for k in range(len(weights[i][j])):
				weights[i][j][k] = (a[i][j][k] if random.randint(0, 1) == 0 else b[i][j][k])
	return weights

def main():
	pygame.init()
	clock = pygame.time.Clock()
	fps = 10

	game = Game()
	game.gates.append([[200, 400], [200, 540]])
	game.gates.append([[50, 450], [130, 390]])
	game.gates.append([[25, 290], [125, 290]])
	game.gates.append([[45, 140], [160, 160]])
	game.gates.append([[220, 30], [220, 130]])
	game.gates.append([[370, 60], [320, 140]])
	game.gates.append([[360, 230], [440, 170]])
	game.gates.append([[520, 210], [520, 310]])
	game.gates.append([[600, 150], [690, 190]])
	game.gates.append([[740, 25], [740, 125]])
	game.gates.append([[880, 70], [810, 140]])
	game.gates.append([[840, 220], [940, 220]])
	game.gates.append([[800, 340], [900, 340]])
	game.gates.append([[780, 400], [860, 500]])
	game.gates.append([[700, 400], [700, 540]])
	game.gates.append([[600, 400], [600, 540]])
	game.gates.append([[500, 400], [500, 540]])
	game.gates.append([[400, 400], [400, 540]])
	game.gates.append([[300, 400], [300, 540]])

	ais = []
	for i in range(10):
		game.cars.append(Car())
		ai = AI([18, 10, 4], ['sigmoid', 'binary'])
		ai.initWeights()
		ais.append(ai)

	generation = 0
	while (not game.stop):
		# clock.tick(fps)
		game.draw()
		pygame.display.flip()

		allDead = True
		for i in range(len(game.cars)):
			car = game.cars[i]
			ai = ais[i]
			if (car.alive):
				cos = math.cos(math.radians(car.rotation))
				sin = math.sin(math.radians(car.rotation))

				line1 = LineString([[(cos * (car.size[0] / 2)) - (sin * (car.size[1] / 2)), (-sin * (car.size[0] / 2)) - (cos * (car.size[1] / 2))] + Vector2(car.rect.center), [(-cos * (car.size[0] / 2)) + (sin * (car.size[1] / 2)), (sin * (car.size[0] / 2)) + (cos * (car.size[1] / 2))] + Vector2(car.rect.center)])
				line2 = LineString(game.gates[ai.gates % len(game.gates)])
				point1 = line1.intersection(line2)

				line3 = LineString([[(cos * (car.size[0] / 2)) + (sin * (car.size[1] / 2)), (-sin * (car.size[0] / 2)) + (cos * (car.size[1] / 2))] + Vector2(car.rect.center), [(-cos * (car.size[0] / 2)) - (sin * (car.size[1] / 2)), (sin * (car.size[0] / 2)) - (cos * (car.size[1] / 2))] + Vector2(car.rect.center)])
				line4 = LineString(game.gates[ai.gates % len(game.gates)])
				point2 = line3.intersection(line4)

				if (point1.geom_type == 'Point' or point2.geom_type == 'Point'):
					ai.gates += 1
					ai.framesSinceLastGate = 0

				directions = [
					[[cos * (car.size[0] / 2), -sin * (car.size[0] / 2)], cos, -sin],
					[[sin * (car.size[1] / 2), cos * (car.size[1] / 2)], sin, cos],
					[[-cos * (car.size[0] / 2), sin * (car.size[0] / 2)], -cos, sin],
					[[-sin * (car.size[1] / 2), -cos * (car.size[1] / 2)], -sin, -cos],
					[[(cos * (car.size[0] / 2)) - (sin * (car.size[1] / 2)), (-sin * (car.size[0] / 2)) - (cos * (car.size[1] / 2))], cos - sin, -sin - cos],
					[[(cos * (car.size[0] / 2)) + (sin * (car.size[1] / 2)), (-sin * (car.size[0] / 2)) + (cos * (car.size[1] / 2))], cos + sin, -sin + cos],
					[[(-cos * (car.size[0] / 2)) + (sin * (car.size[1] / 2)), (sin * (car.size[0] / 2)) + (cos * (car.size[1] / 2))], -cos + sin, sin + cos],
					[[(-cos * (car.size[0] / 2)) - (sin * (car.size[1] / 2)), (sin * (car.size[0] / 2)) - (cos * (car.size[1] / 2))], -cos - sin, sin - cos]
				]

				distances = []
				for direction in directions:
					initial = direction[0] + Vector2(car.rect.center)
					position = initial
					dead = True
					while (game.screen.get_at([int(position[0]), int(position[1])]) != (0, 0, 0, 255)):
						dead = False
						position = [position[0] + direction[1], position[1] + direction[2]]
					if (dead):
						car.alive = False
						break
					distance = max(abs(initial[0] - position[0]), abs(initial[1] - position[1]))
					distances.append(1 / distance)
					line1 = LineString([initial, position])
					line2 = LineString(game.gates[ai.gates % len(game.gates)])
					point = line1.intersection(line2)
					if (point.geom_type == 'Point'):
						point = Point(point)
						distances.append(1 / max(abs(point.x - initial[0]), abs(point.y - initial[1])))
					else:
						distances.append(1 / math.inf)
				
				if (car.alive):
					ai.setInputs(distances + [1 / car.velocity.x if car.velocity.x != 0 else 0, 1 / car.rotation if car.rotation != 0 else 0])
					outputs = ai.forwardPropagation()

					if (outputs[0]):
						car.velocity.x += 1
					if (outputs[1]):
						car.velocity.x -= 1
					if (outputs[2]):
						car.rotation += 10
					if (outputs[3]):
						car.rotation -= 10
					if (outputs[0] == outputs[1] and car.velocity.x != 0):
						car.velocity.x += -1 if car.velocity.x > 0 else 1
					car.velocity.x = max(-20, min(car.velocity.x, 20))

					car.update()
					ai.framesSinceLastGate +=1
					ai.frames += 1
					ai.distance += car.velocity.x
					if (ai.framesSinceLastGate >= ai.maxFrames or ai.frames >= 10000):
						car.dead = True
					else:
						allDead = False
		
		if (allDead):
			for ai in ais:
				ai.fitness = (ai.distance / ai.frames) + (ai.gates * 500)
				ai.fitness = max(ai.fitness, 0.1)
			
			fitnessSum = getFitnessSum(ais)
			children = []
			for _ in range(len(ais) - 1):
				parentA = selectParent(ais, fitnessSum)
				parentB = selectParent(ais, fitnessSum)
				child = deepcopy(parentA)
				child.weights = mixWeights(parentA.weights, parentB.weights)
				if (random.randint(1, 100) <= 80):
					child.mutate()
				children.append(child)
			ais.sort(key=lambda x: x.fitness, reverse=True)
			print([generation, ais[0].fitness, ais[0].gates, ais[0].frames, ais[0].distance])
			ais = [ais[0]] + children
			generation += 1
			for i in range(len(game.cars)):
				game.cars[i].reset()
				game.cars[i].update()
				ais[i].reset()

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				game.stop = True
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				game.stop = True

	pygame.quit()

if __name__ == "__main__":
	main()
