import random
import math

class AI():
	def __init__(self, layers, activations):
		# Initialization
		self.layers = [[0] * layer for layer in layers]
		self.weights = []
		if (len(activations) != len(layers) - 1):
			raise Exception('Error')
		self.activations = activations
		self.maxFrames = 100
		self.reset()
	
	def reset(self):
		# Resets the AI's state
		self.framesSinceLastGate = 0
		self.frames = 0
		self.gates = 0
		self.fitness = 0
		self.distance = 0

	def initWeights(self):
		# Every weight is initialized to a random value between -1 and 1
		weights = []
		for index in range(len(self.layers) - 1):
			layer = []
			for _ in self.layers[index + 1]:
				neuron = []
				for _ in self.layers[index]:
					neuron.append(random.uniform(-1, 1))
				layer.append(neuron)
			weights.append(layer)
		self.weights = weights

	def mutate(self):
		# Mutation function
		for i in range(len(self.weights)):
			for j in range(len(self.weights[i])):
				for k in range(len(self.weights[i][j])):
					# Each weight has a 5% chances to be modified
					if (random.randint(1, 100) <= 5):
						x = self.weights[i][j][k] + random.uniform(-1, 1)
						x = max(min(x, 1), -1)
						self.weights[i][j][k] = x

	def setInputs(self, inputs):
		# Checks the number of inputs, if everything's ok set them in the input layer
		if (len(inputs) != len(self.layers[0])):
			raise Exception('Error')
		self.layers[0] = inputs.copy()

	def forwardPropagation(self):
		# Simple forward propagation layer by layer
		for layerIndex in range(1, len(self.layers)):
			for neuronIndex in range(len(self.layers[layerIndex])):
				value = 0
				for previousNeuronIndex in range(len(self.layers[layerIndex - 1])):
					value += self.layers[layerIndex - 1][previousNeuronIndex] * self.weights[layerIndex - 1][neuronIndex][previousNeuronIndex]
				self.layers[layerIndex][neuronIndex] = eval('self.' + self.activations[layerIndex - 1])(value)
		return self.layers[len(self.layers) - 1].copy()
	
	def sigmoid(self, x):
		# Simple sigmoid function
		return 1 / (1 + math.exp(-x))

	def binary(self, x):
		# Returns 1 if x is positive, else 0
		return 1 if x > 0 else 0
