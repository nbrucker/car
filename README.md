# Car AI

The goal of this project was to create an AI that would learn how to drive a car on a 2D track.

The AI is using a genetic algorithm to evolve. Each generation is composed of 10 individuals.
The neural network is made up of:
- An input layer of 18 neurons.
- An hidden layer of 10 neurons with a sigmoid activation.
- An output layer of 4 neurons with a binary activation.

The car is rewarded each time it passes a gate.
Gates are simple line drawn throughout the tracks.
There is only one gate activated at a time, when a gate is passed the next one gets activated.

The car sees in 8 directions around itself.
The neural network is fed:
- 16 values of the distance to the gate and to the wall in each of those 8 directions.
- 1 value for the rotation of the car.
- 1 value for the velocity of the car.

The car has then 4 possible actions since the neural network has an output layer of 4 neurons, go forward, go backward, turn left and turn right.

All the 10 individuals will play simultaneously and each will die if they hit a wall or do not pass a gate within 100 frames.
When every individuals is dead we then calculate the fitness of each of them.
Here's the fitness calculation function:
```python
(distance / frames) + (gates * 500)
```
'distance' is the distance traveled by the car.\
'frames' is the number of frames that the car stayed alive for.\
'gates' is the number of gates that the car passed.

We put such a big emphasis on gates to entice the car to pass them as fast as possible.

After calculating the fitness for each individual in the current generation we create 9 children.
For each child we choose 2 parents from the previous generation.
Here comes in play our genetic algorithm.
The parents are chosen randomly but the higher the fitness of an individual is, the higher chances are for him to be picked as a parent.
The weights of the child are a mix of the weights of both of his parents, each child then has an 80% chances to mutate.
If the child mutates every single one of his weights has a 5% chances to be modified to a new, random value.

The 9 children are then put in the next generation along with the best individual from the previous one (The individual with the highest fitness).

## Installation

Use the package manager pip to install pygame and shapely.

```bash
pip install pygame shapely
```

## Usage

```bash
python src/main.py
```
