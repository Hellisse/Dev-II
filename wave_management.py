import pygame
import math
import random
import importlib

enemies = importlib.import_module('enemy')


class WaveManagement:
    ENEMY_STATS = {
        "SlowEnemy": {"hp": 100, "speed": 0.25, "class": enemies.SlowEnemy},
        "FastEnemy": {"hp": 50, "speed": 1, "class": enemies.FastEnemy},
        "RegularEnemy": {"hp": 25, "speed": 0.5, "class": enemies.RegularEnemy}
    }
    ENEMY_SPAWN_RADIUS = 300
    spawn_time = 1000
    number_enemy = 1
    def __init__(self, screen_dimensions, enemy_list):
        self.screen_width, self.screen_height = screen_dimensions
        self.enemies_list = enemy_list
        self.last_enemy_generation_time = pygame.time.get_ticks()

    def generate_enemy(self):
        enemy_choice = random.choice(list(self.ENEMY_STATS.keys()))
        enemy_info = self.ENEMY_STATS[enemy_choice]
        x, y = self._generate_enemy_position()

        enemy_class = enemy_info["class"]
        enemy = enemy_class((x, y), (self.screen_width / 2, self.screen_height / 2), enemy_info)

        self.enemies_list.append(enemy)

    def _generate_enemy_position(self):
        angle = random.uniform(0, 2 * math.pi)
        x = self.screen_width / 2 + self.ENEMY_SPAWN_RADIUS * math.cos(angle)
        y = self.screen_height / 2 + self.ENEMY_SPAWN_RADIUS * math.sin(angle)
        return x, y

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_generation_time >= self.spawn_time:
            if self.spawn_time > 100:
                self.spawn_time -= 100
            else:
                if self.number_enemy < 10:
                    self.spawn_time = 1000
                    self.number_enemy += 1
            for i in range(self.number_enemy):
                self.generate_enemy()
            self.last_enemy_generation_time = current_time
        # self.ENEMY_STATS["SlowEnemy"]["speed"] += 0.01


