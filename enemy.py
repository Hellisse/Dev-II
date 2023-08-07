import pygame
from abc import ABC, abstractmethod
import math


class Enemy(ABC):
    def __init__(self, position, player_position, stats, size=(10, 10)):
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.position = list(position)
        self.player_position = player_position
        self.size = size

    def update(self):
        self.move()
        # Ajoutez d'autres mises à jour nécessaires ici, comme la gestion de la santé

    def move(self):
        if not self.has_reached_player():
            dx = self.player_position[0] - self.position[0]
            dy = self.player_position[1] - self.position[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            # Vecteur direction unitaire
            ux = dx / distance
            uy = dy / distance
            # Mise à jour de la position
            self.position[0] += ux * self.speed
            self.position[1] += uy * self.speed

    def has_reached_player(self):
        # La distance à vérifier est le rayon du joueur (la moitié de la taille)
        return math.sqrt(
            (self.position[0] - self.player_position[0]) ** 2 + (self.position[1] - self.player_position[1]) ** 2
        ) <= self.size[0]

    def draw(self, screen):
        pygame.draw.rect(screen, self.get_color(),
                         (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2, *self.size))

    @abstractmethod
    def get_color(self):
        pass

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def die(self):
        # Ici, vous pouvez gérer la suppression de l'ennemi du jeu
        pass


class SlowEnemy(Enemy):
    def __init__(self, position, player_position, stats):
        super().__init__(position=position, player_position=player_position, stats=stats)

    def get_color(self):
        return 0, 0, 255  # blue


class FastEnemy(Enemy):
    def __init__(self, position, player_position, stats):
        super().__init__(position=position, player_position=player_position, stats=stats)

    def get_color(self):
        return 255, 255, 0  # yellow


class RegularEnemy(Enemy):
    def __init__(self, position, player_position, stats):
        super().__init__(position=position, player_position=player_position, stats=stats)

    def get_color(self):
        return 0, 255, 0  # green
