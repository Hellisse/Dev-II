import pygame
from player import Player
from hud import HUD
from wave_management import WaveManagement
from battle_system import BattleSystem

import importlib
enemies = importlib.import_module('enemy')


class Game:
    FPS = 60  # Frames per second
    BACKGROUND_COLOR = (0, 0, 0)  # Black color for background

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.player = Player(self.width, self.height)
        self.hud = HUD(self.player, self.width, self.height)

        # Load the background image
        self.background = pygame.image.load('background.jpg')
        # Resize the image to fit the window size
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.enemies_list = []
        self.last_enemy_generation_time = pygame.time.get_ticks()
        self.wave_management = WaveManagement((self.width, self.height), self.enemies_list)

        self.battle_system = BattleSystem(self.player, self.enemies_list)

    # generation d'un nouvelle enmeie de façon aléatoire

    def update(self):
        self.player.money += 10
        self.wave_management.update()  # Wave management first
        self.battle_system.update()    # Then, battle system

        # Update each enemy
        for enemy in self.enemies_list:
            enemy.update()

    def render(self):
        # Draw the background image
        self.window.blit(self.background, (0, 0))

        # Draw the player and the HUD
        self.player.draw(self.window)
        self.hud.draw(self.window)

        # Draw each enemy
        for enemy in self.enemies_list:
            enemy.draw(self.window)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.hud.handle_click(event)
        return True

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            running = self.handle_events()

            self.update()
            self.render()

            pygame.display.flip()

        pygame.quit()

