import time

import pygame
import math


class Player:
    def __init__(
            self,
            screen_width,
            screen_height,
            hp_level=1,
            max_range_level=1,
            attack_speed_level=1,
            damage_level=1,
            money=0
    ):
        # Paramètres initiaux pour les dimensions de l'écran et la position du joueur
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = self.screen_width / 2
        self.y = self.screen_height / 2
        self.radius = 10  # Le rayon du cercle représentant le joueur
        self.money = money
        self.blinking = False
        self.blink_duration = 2  # Durée de clignotement en secondes
        self.blink_start_time = 0  # Moment où le clignotement a commencé

        # Dictionnaire stockant les niveaux d'amélioration pour chaque attribut
        self.upgrade_levels = {
            'max_hp': hp_level,
            'max_range': max_range_level,
            'attack_speed': attack_speed_level,
            'damage': damage_level,
        }

        # Dictionnaire contenant des fonctions pour calculer la valeur de chaque attribut en fonction de son niveau
        self.formulas = {
            'max_hp': lambda n: 10 + (n - 1) * math.log(10 + n),
            'max_range': lambda n: 100 * (1.02 ** (n - 1)),
            'attack_speed': lambda n: 1 + (n - 1) * (0.1 * n),
            'damage': lambda n: n * 10
        }

        self.price_formulas = {
            'max_hp': lambda n: 10 * n,
            'max_range': lambda n: 10 * n,
            'attack_speed': lambda n: 10 * n,
            'damage': lambda n: 10 * n
        }

        # Dictionnaire qui stocke les valeurs actuelles de chaque attribut
        self.attributes = {key: func(self.upgrade_levels[key]) for key, func in self.formulas.items()}
        self.current_hp = self.attributes['max_hp']

        # Création d'une surface pour le cercle représentant le joueur
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # Dessine un cercle sur cette surface
        pygame.draw.circle(self.image, (64, 96, 124), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (173, 216, 230), (self.radius, self.radius), self.radius - 2)
        pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius / 2)
        self.current_time = time.time()

    def draw(self, screen):
        # Affiche le joueur sur l'écran pour chaque frame
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        # Dessine également la portée maximale du joueur
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.attributes['max_range'], 1)

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        self.money -= amount

    def upgrade_attribute(self, attribute):
        # Calcule le coût de la mise à niveau
        cost = self.get_upgrade_cost(attribute)
        # Vérifie si le joueur a suffisamment d'argent
        if self.money >= cost:
            self.blinking = False

            # Déduit le coût de l'argent du joueur
            self.remove_money(cost)
            # Effectue la mise à niveau
            if attribute in self.upgrade_levels:
                self.upgrade_levels[attribute] += 1
                self.attributes[attribute] = self.formulas[attribute](self.upgrade_levels[attribute])

        if self.money < cost:
            if not self.blinking:
                self.blinking = True

            if self.blinking:
                self.blink_start_time = time.time()
                if self.blink_start_time - self.current_time >= self.blink_duration :
                    self.blinking = False
                    self.current_time = time.time()

    def get_upgrade_cost(self, attribute):
        if attribute in self.price_formulas:
            return self.price_formulas[attribute](self.upgrade_levels[attribute])
        return 0
