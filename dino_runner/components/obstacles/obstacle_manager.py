from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS
from random import randint
import pygame

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.y_pos = 330
        self.y_l_pos = 305

    def random_obstacle(self):
        if randint(0, 1) == 0:
            self.obstacles.append(Cactus(SMALL_CACTUS, self.y_pos))
        elif randint(0, 1) == 1:
            self.obstacles.append(Cactus(LARGE_CACTUS, self.y_l_pos))
        
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