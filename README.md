# Car AI

The goal of this project was to create an AI that would learn how to drive a car on a track.

The AI is using a genetic algorithm to evolve. Each generation is composed of 10 individuals.
The neural network is made up of a input layer of 18 neurons, an hidden layer of 10 neurons with
a sigmoid activation and an output layer of 4 neurons with a binary activation.

The car see in 8 directions around it. The neural network is then fed the distance to the gate and
to the wall in each of those directions, we also add the rotation of the car and it's velocity.
The car has then 4 possible actions, go forward, go backward, turn left and turn right.

All the 10 individuals will play at the same and die if they hit a wall or don't do any actions
for a 100 frames. When every individuals are dead we then calculate the fitness of each of them.
Here's how to fitness is calculate:
```python
(distance / frames) + (gates * 500)
```
Distance is the distance traveled by the car.\
Frames are the number of frames that the car stayed alive for.\
Gates is the number of gates that the car passed.

After calculating all the fitness we create 9 children. For each child we choose 2 parents from the previous generation.
The parents are chosen randomly but the higher the fitness of an individual are, the higher chances there is for him
to be picked. The weights of the child is a mix of the weights of his parents, each child then has an 80% chances to
mutate. If the child mutates every single one of his weights has a 5% chances to be modified to a new, random value.

The 9 children are then put in the next generation along with the best individual from the previous one.

## Installation

This program requires pygame and shapely to be installed.

```bash
pip install pygame shapely
```

## Usage

```bash
python src/main.py
```
