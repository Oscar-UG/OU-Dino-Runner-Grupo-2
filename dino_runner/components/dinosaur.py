import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING

RUNNING_ACTION = 'running'
JUMPING_ACTION = 'jumping'
DUCKING_ACTION = 'ducking'

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_DUCK_POS = 345
    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.image = RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0
        self.action = RUNNING_ACTION
        self.sound_jump = pygame.mixer.Sound('dino_runner/assets/Sounds/sound_jump.mp3')

    def reset_rect(self, y_pos=None):
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = y_pos or self.Y_POS

    def update(self, user_input):
        if self.action == RUNNING_ACTION:
            self.run()
        elif self.action == JUMPING_ACTION:
            self.jump()
        elif self.action == DUCKING_ACTION:
            self.duck()

        if self.action != JUMPING_ACTION:
            if user_input[pygame.K_UP]:
                self.action = JUMPING_ACTION
                self.sound_jump.play()
            elif user_input[pygame.K_DOWN]:
                self.action = DUCKING_ACTION
            else:
                self.action = RUNNING_ACTION
            
        if self.step >= 9:
            self.step = 0

    def run(self):
        self.image = RUNNING[self.step // 5]
        self.reset_rect()
        self.step += 1

    def jump(self):
        self.image = JUMPING
        y_pos = self.rect.y - self.jump_velocity * 4
        self.reset_rect(y_pos=y_pos)
        self.jump_velocity -= 0.8

        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.reset_rect()
            self.jump_velocity = self.JUMP_VELOCITY
            self.action = RUNNING_ACTION
        
    def duck(self):
        self.image = DUCKING[self.step // 5]
        self.reset_rect(y_pos=self.Y_DUCK_POS)
        self.step += 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))