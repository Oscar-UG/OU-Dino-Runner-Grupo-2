import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import (RUNNING,
                                         JUMPING,
                                         DUCKING,
                                         DEFAULT_TYPE,
                                         DUCKING_SHIELD,
                                         RUNNING_SHIELD,
                                         JUMPING_SHIELD,
                                         SHIELD_TYPE,
                                         FONT_BOLD,
                                         SCREEN_WIDTH,
                                         SCREEN_HEIGHT)

RUNNING_ACTION = 'running'
JUMPING_ACTION = 'jumping'
DUCKING_ACTION = 'ducking'
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}


class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_DUCK_POS = 345
    JUMP_VELOCITY = 8.5

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0
        self.action = RUNNING_ACTION
        self.sound_jump = pygame.mixer.Sound(
            'dino_runner/assets/Sounds/sound_jump.wav')
        self.has_power_up = False
        self.power_up_time_up = 0
        self.half_screen_width = SCREEN_WIDTH // 2
        self.half_screen_height = SCREEN_HEIGHT // 2

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
        self.image = RUN_IMG[self.type][self.step // 5]
        self.reset_rect()
        self.step += 1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        y_pos = self.rect.y - self.jump_velocity * 4
        self.reset_rect(y_pos=y_pos)
        self.jump_velocity -= 0.8

        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.reset_rect()
            self.jump_velocity = self.JUMP_VELOCITY
            self.action = RUNNING_ACTION

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step // 5]
        self.reset_rect(y_pos=self.Y_DUCK_POS)
        self.step += 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def on_pick_power_up(self, power_up):
        self.has_power_up = True
        self.power_up_time_up = power_up.start_time + \
            (power_up.duration * 1000)
        self.type = power_up.type

    def draw_active_power_up(self, screen):
        if self.has_power_up:
            left_time = round(
                (self.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if left_time >= 0:
                font = pygame.font.Font(FONT_BOLD, 30)
                message = font.render(f'{self.type.capitalize()} enabled for {left_time} seconds', True, (0, 0, 0))
                message_rect = message.get_rect()
                message_rect.center = (self.half_screen_width, self.half_screen_height - 250)
                screen.blit(message, message_rect)
            else:
                self.type = DEFAULT_TYPE
                self.has_power_up = False
