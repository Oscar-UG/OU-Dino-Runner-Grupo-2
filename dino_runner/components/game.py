import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.score import Score
from dino_runner.components.menu import Menu
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import (BG, 
                                        ICON, 
                                        SCREEN_HEIGHT, 
                                        SCREEN_WIDTH, 
                                        TITLE, 
                                        FPS, 
                                        DINO_START, 
                                        RESET, 
                                        GAME_OVER, 
                                        SHIELD_TYPE,
                                        HAMMER_TYPE,
                                        DINO_DEAD)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.score = Score()
        self.power_up_manager = PowerUpManager()
        self.menu = Menu()
        self.executing = False
        self.death_counts = 0
        self.sound_break = pygame.mixer.Sound('dino_runner/assets/Sounds/sound_break.wav')

    def execute(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.score.points = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.power_up_manager.update(self.game_speed, self.score.points, self.player)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.player.draw_active_power_up(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((192, 192, 192))
        if self.death_counts == 0:
            self.menu.draw_image(self.screen, DINO_START, 40, 150)
            self.menu.menu_view(self.screen, 'Press any key to start', -10)
        else:
            self.menu.draw_image(self.screen, GAME_OVER, 190, 160)
            self.menu.draw_image(self.screen, RESET, 40, 90)
            self.menu.menu_view(self.screen, 'Press any key to restart', -40)
            self.menu.menu_view(self.screen, f'Your score: {self.score.points}', -90)
            self.menu.menu_view(self.screen, f'Your deaths: {self.death_counts}', -140)
        pygame.display.update()
        self.handle_menu_event()

    def handle_menu_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def on_death(self, obstacle):
        has_shield = self.player.type == SHIELD_TYPE 
        has_hammer = self.player.type == HAMMER_TYPE
        if not has_shield and not has_hammer:
            self. player.image = DINO_DEAD
            self.draw()
            self.death_counts += 1
            self.playing = False
        elif has_hammer:
            self.obstacle_manager.obstacles.remove(obstacle)
            self.sound_break.play()
        return not has_shield and not has_hammer
