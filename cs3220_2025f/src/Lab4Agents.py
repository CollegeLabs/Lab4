from src.agents import ProblemSolvingMazeAgentBFS
import numpy as np
import random


class UniformCostAgent():
    def __init__(self):
        self.performance = 0

class IterativeDLSAgent():
    def __init__(self):
        self.performance = 0

class EnemyShip():
    def __init__(self):
        size=7
        self.power = (random.randint(10, 40)*(size*size))/100
