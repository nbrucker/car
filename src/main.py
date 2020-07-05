# External import
import pygame
import random
import math
from copy import deepcopy
from shapely.geometry import LineString, Point
from pygame.math import Vector2

# Local import
from ai import AI
from game import Game
from car import Car

def printOutput(generation, fitness, gates, frames, distance):
	# Prints in a nice format
	print('-' * 20)
	print('Best Of Generation {}'.format(generation))
	print('Fitness: {}'.format(fitness))
	print('Gates: {}'.format(gates))
	print('Frames: {}'.format(frames))
	print('Distance: {}'.format(distance))

def selectParent(ais, fitnessSum):
	# This function allows us to randomly pick a parent, the chances of each individual to be picked are based on their fitness
	rand = random.uniform(0, fitnessSum)
	currentSum = 0
	for ai in ais:
		currentSum += ai.fitness
		if (currentSum > rand):
			return ai

def getFitnessSum(ais):
	# Returns the sum of every individual's fitness
	fitnessSum = 0
	for ai in ais:
		fitnessSum += ai.fitness
	return fitnessSum

def mixWeights(a, b):
	# Mixes the parents weights to create the child
	# Creates a copy of the weights of parentA in order to have the same structure
	weights = deepcopy(a)
	for i in range(len(weights)):
		for j in range(len(weights[i])):
			for k in range(len(weights[i][j])):
				# Each weight is randomly copied from one of the 2 parents
				weights[i][j][k] = (a[i][j][k] if random.randint(0, 1) == 0 else b[i][j][k])
	return weights

def main():
	pygame.init()
	game = Game()

	# Create 10 individuals and randomly initialize their weights
	ais = []
	for i in range(10):
		game.cars.append(Car())
		ai = AI([18, 10, 4], ['sigmoid', 'binary'])
		ai.initWeights()
		ais.append(ai)

	generation = 0
	while (not game.stop):
		game.draw()
		pygame.display.flip()

		allDead = True
		for i in range(len(game.cars)):
			car = game.cars[i]
			ai = ais[i]
			if (car.alive):
				cos = math.cos(math.radians(car.rotation))
				sin = math.sin(math.radians(car.rotation))

				# This blocks allows us to know is the car passed a gate
				# The first line is simply the gate
				line1 = LineString(game.gates[ai.gates % len(game.gates)])
				# The second line goes from the top left of the car to the bottom right of the car
				line2 = LineString([[(cos * (car.size[0] / 2)) - (sin * (car.size[1] / 2)), (-sin * (car.size[0] / 2)) - (cos * (car.size[1] / 2))] + Vector2(car.rect.center), [(-cos * (car.size[0] / 2)) + (sin * (car.size[1] / 2)), (sin * (car.size[0] / 2)) + (cos * (car.size[1] / 2))] + Vector2(car.rect.center)])
				# The third line goes from the top right of the car to the bottom left of the car
				line3 = LineString([[(cos * (car.size[0] / 2)) + (sin * (car.size[1] / 2)), (-sin * (car.size[0] / 2)) + (cos * (car.size[1] / 2))] + Vector2(car.rect.center), [(-cos * (car.size[0] / 2)) - (sin * (car.size[1] / 2)), (sin * (car.size[0] / 2)) - (cos * (car.size[1] / 2))] + Vector2(car.rect.center)])

				# Here we check if the second or the third line intersect the first one
				point1 = line1.intersection(line2)
				point2 = line1.intersection(line3)
				if (point1.geom_type == 'Point' or point2.geom_type == 'Point'):
					# If at least one of them does it means we are passing the gate
					ai.gates += 1
					ai.framesSinceLastGate = 0

				# This part allows us to see in 8 directions around the car
				directions = [
					[
						[cos * (car.size[0] / 2), -sin * (car.size[0] / 2)], # Starting position
						cos, # Step to take in the X axis
						-sin  # Step to take in the Y axis
					],
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
					# For each direction we basically cast a ray to find the closest wallz
					while (game.screen.get_at([int(position[0]), int(position[1])]) != (0, 0, 0, 255)):
						dead = False
						position = [position[0] + direction[1], position[1] + direction[2]]
					# If we reach a wall before taking a step it means we're in the wall and the car will die
					if (dead):
						car.alive = False
						break
					# The distance to the wall is then added to the array
					distance = max(abs(initial[0] - position[0]), abs(initial[1] - position[1]))
					distances.append(1 / distance)
					# By doing `1 / value` we ensure that every value in the array is between -1 and 1

					# After reaching the wall we check if the gate is between said wall and our starting point
					line1 = LineString([initial, position])
					line2 = LineString(game.gates[ai.gates % len(game.gates)])
					point = line1.intersection(line2)
					if (point.geom_type == 'Point'):
						# If it is we add the distance to the gate in the array
						point = Point(point)
						distances.append(1 / max(abs(point.x - initial[0]), abs(point.y - initial[1])))
					else:
						# If it isn't we add a really big number
						distances.append(1 / math.inf)
				
				if (car.alive):
					# We set the inputs in the neural network, the inputs are the distances, the velocity of the car and the rotation of the car
					ai.setInputs(distances + [1 / car.velocity.x if car.velocity.x != 0 else 0, 1 / car.rotation if car.rotation != 0 else 0])
					# We start the forward propagation!
					outputs = ai.forwardPropagation()

					# This part is pretty self explanatory
					if (outputs[0]):
						car.velocity.x += 1
					if (outputs[1]):
						car.velocity.x -= 1
					if (outputs[2]):
						car.rotation += 10
					if (outputs[3]):
						car.rotation -= 10
					if (outputs[0] == outputs[1] and car.velocity.x != 0):
						"""
						If the car get no instructions, or if the car gets the instructions to go forward and backward
						at the same time, and the car velocity isn't 0, then we slowly bring the velocity down to
						simulate the momentum and inertia of a real car
						"""
						car.velocity.x += -1 if car.velocity.x > 0 else 1
					car.velocity.x = max(-20, min(car.velocity.x, 20))

					car.update()
					ai.framesSinceLastGate += 1
					ai.frames += 1
					ai.distance += car.velocity.x
					if (ai.framesSinceLastGate >= ai.maxFrames or ai.frames >= 10000):
						# The car dies if it hasn't passed a gate in a while or if it's been alive for more than 10000 frames to force it to get better
						car.dead = True
					else:
						allDead = False
		
		if (allDead):
			# When all individuals are dead we calculate the fitness for each of them
			for ai in ais:
				ai.fitness = (ai.distance / ai.frames) + (ai.gates * 500)
				ai.fitness = max(ai.fitness, 0.1)
			
			fitnessSum = getFitnessSum(ais)
			# The new generation is made of children whose weights are a mix of the 2 parents, some of those children will also randomly mutate
			children = []
			for _ in range(len(ais) - 1):
				parentA = selectParent(ais, fitnessSum)
				parentB = selectParent(ais, fitnessSum)
				child = deepcopy(parentA)
				child.weights = mixWeights(parentA.weights, parentB.weights)
				if (random.randint(1, 100) <= 80):
					child.mutate()
				children.append(child)
			# We sort the old generation by it's members individual fitness, print the best individual and add it in the next generation
			ais.sort(key=lambda x: x.fitness, reverse=True)
			printOutput(generation, ais[0].fitness, ais[0].gates, ais[0].frames, ais[0].distance)
			ais = [ais[0]] + children
			generation += 1
			# Every individual is reseted before the next generation starts playing
			for i in range(len(game.cars)):
				game.cars[i].reset()
				game.cars[i].update()
				ais[i].reset()

		# Exit if the pygame window is closed or if escape is pressed
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				game.stop = True
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				game.stop = True

	pygame.quit()

if __name__ == "__main__":
	main()
