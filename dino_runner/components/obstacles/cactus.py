from dino_runner.components.obstacles.obstacle import Obstacle
from random import randint

class Cactus(Obstacle):
    def __init__(self, images, y_pos):
        self.cactus_type = randint(0, 2)
        super().__init__(images[self.cactus_type])
        self.rect.y = y_pos
    