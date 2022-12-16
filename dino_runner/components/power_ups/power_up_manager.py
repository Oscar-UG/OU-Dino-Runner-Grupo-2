from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.components.power_ups.shield import Shield
from random import randint
import pygame

class PowerUpManager:
    def __init__(self):
        self.power_ups: list[PowerUp] = []
        self.when_appers = 0
        self.sound_bonus = pygame.mixer.Sound('dino_runner/assets/Sounds/sound_bonus.wav')

    def generate_power_up(self, score):
        if not self.power_ups and self.when_appers == score:
            self.power_ups.append(Shield())
            self.when_appers += randint(200, 300)

    def update(self, game_speed, score, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if power_up.rect.colliderect(player.rect):
                self.sound_bonus.play()
                power_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(power_up)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appers = randint(200, 300)
        