from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD
from random import randint

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD[0])
        self.rect.y = randint(200, 330)
        self.step = 0

    def draw(self, screen):
        if self.step >= 9:
            self.step = 0
        screen.blit(BIRD[self.step//5], self.rect)
        self.step += 1