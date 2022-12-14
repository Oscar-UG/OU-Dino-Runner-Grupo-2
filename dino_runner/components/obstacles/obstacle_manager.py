from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from random import randint
import pygame

class ObstacleManager:
    Y_S_POS = 330
    Y_L_POS = 305

    def __init__(self):
        self.obstacles = []

    def random_obstacle(self):
        obs_random = randint(0, 2)

        if obs_random == 0:
            self.obstacles.append(Cactus(SMALL_CACTUS, self.Y_S_POS))
        elif obs_random == 1:
            self.obstacles.append(Cactus(LARGE_CACTUS, self.Y_L_POS))
        elif obs_random == 2:
            self.obstacles.append(Bird(BIRD))
        
    def update(self, game):
        if len(self.obstacles) == 0:
            self.random_obstacle()

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if obstacle.rect.colliderect(game.player.rect):
                pygame.time.delay(500)
                game.playing = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)