import pygame
from dino_runner.utils.constants import FONT_BOLD

class Score:
    def __init__(self):
        self.points = 0

    def update(self, game):
        self.points += 1
        if self.points % 400 == 0:
            game.game_speed += 2

    def draw(self, screen):
        font = pygame.font.Font(FONT_BOLD, 30)
        message = font.render((f'Score: {self.points}'), True, (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (1000, 40)
        screen.blit(message, message_rect)