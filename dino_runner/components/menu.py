from dino_runner.utils.constants import FONT_BOLD, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

class Menu:
    def __init__(self):
        self.half_screen_width = SCREEN_WIDTH // 2
        self.half_screen_height = SCREEN_HEIGHT // 2

    def menu_view(self, screen, text, y_pos=None, x_pos=None):
        font = pygame.font.Font(FONT_BOLD, 30)
        message = font.render(text, True, (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (self.half_screen_width - (x_pos or 0), self.half_screen_height - (y_pos or 0))
        screen.blit(message, message_rect)

    def draw_image(self, screen, image, x_pos, y_pos):
        screen.blit(image, (self.half_screen_width - (x_pos or 0), self.half_screen_height - (y_pos or 0)))