from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, DINO_DEAD
from random import randint
import pygame

class ObstacleManager:
    Y_S_POS = 330
    Y_L_POS = 305

    def __init__(self):
        self.obstacles = []

    def generate_random_obstacles(self):
        obs_random = randint(0, 2)
        if obs_random == 0:
            self.obstacles.append(Cactus(SMALL_CACTUS, self.Y_S_POS))
        elif obs_random == 1:
            self.obstacles.append(Cactus(LARGE_CACTUS, self.Y_L_POS))
        elif obs_random == 2:
            self.obstacles.append(Bird())
        
    def update(self, game):
        if len(self.obstacles) == 0:
            self.generate_random_obstacles()

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if obstacle.rect.colliderect(game.player.rect):
                game.player.image = DINO_DEAD
                pygame.time.delay(200)
                game.playing = False
                game.death_counts += 1

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []