import pygame
import math


class BattleSystem:
    def __init__(self, player, enemies_list):
        """
        Initialise un système de combat.

        :param player: Le joueur participant au combat.
        :param enemies_list: Une liste d'ennemis en jeu.
        :pre: player est une instance de la classe Player,
        enemies_list est une liste non vide d'instances de la classe Enemy.
        :post: Un nouveau système de combat est créé avec les joueurs et ennemis fournis,
         les temps d'attaque sont initialisés.

        """
        self.player = player
        self.enemies_list = enemies_list
        self.last_attack_time = pygame.time.get_ticks()
        self.enemies_dead = []  # Liste pour stocker les ennemis morts

    def update(self):
        """
        Met à jour le système de combat en tentant d'attaquer l'ennemi le plus proche à portée.
        :pre: Aucune.
        :post: Le système de combat est mis à jour, les attaques sont effectuées si les conditions sont remplies.
        """
        self._try_attack()

    def _try_attack(self):
        """
        Tente une attaque si suffisamment de temps s'est écoulé depuis la dernière attaque.
        :pre: Aucune.
        :post: Une attaque est tentée si suffisamment de temps s'est écoulé depuis la dernière attaque.
        """
        current_time = pygame.time.get_ticks()
        attack_interval = 1000 / self.player.attributes['attack_speed']

        if current_time - self.last_attack_time > attack_interval:
            self._attack_nearest_enemy()
            self.last_attack_time = current_time

    def _find_nearest_enemy_within_range(self):
        """
        Cherche l'ennemi le plus proche à portée du joueur.
        :return: L'instance d'Enemy la plus proche à portée, ou None si aucun ennemi n'est à portée.
        :pre: Aucune.
        :post: L'ennemi le plus proche à portée est renvoyé, ou None si aucun ennemi n'est à portée.
        """
        if not self.enemies_list:
            return None

        # Filtrons d'abord la liste pour n'inclure que les ennemis à portée
        enemies_within_range = [enemy for enemy in self.enemies_list if
                                self._distance(self.player.x, self.player.y, enemy.position[0], enemy.position[1]) <=
                                self.player.attributes['max_range']]

        # Si aucun ennemi à portée, retourner None
        if not enemies_within_range:
            return None

        # Trouver l'ennemi le plus proche parmi ceux à portée
        return min(enemies_within_range,
                   key=lambda enemy: self._distance(self.player.x, self.player.y, enemy.position[0], enemy.position[1]))

    def _attack_nearest_enemy(self):
        """
        Attaque l'ennemi le plus proche à portée.
        :pre: Aucune.
        :post: L'ennemi le plus proche à portée est attaqué.
        """
        nearest_enemy = self._find_nearest_enemy_within_range()
        if nearest_enemy:
            self._inflict_damage(nearest_enemy)

    def _inflict_damage(self, enemy):
        """
        Inflige des dégâts à un ennemi et gère son statut de vie.
        :param enemy: L'instance d'Enemy à attaquer.
        :pre: enemy est une instance de la classe Enemy.
        :post: L'ennemi reçoit des dégâts, et s'il tombe à 0 HP, il est ajouté à la liste des ennemis morts.
        """
        enemy.take_damage(self.player.attributes['damage'])
        if enemy.hp <= 0:
            self.enemies_dead.append(enemy)
            self._remove_dead_enemies()

    def _remove_dead_enemies(self):
        """
        Supprime les ennemis morts de la liste des ennemis en jeu.
        :pre: Aucune.
        :post: Les instances d'Enemy mortes sont retirées de la liste des ennemis en jeu.
        """
        for dead_enemy in self.enemies_dead:
            if dead_enemy in self.enemies_list:
                self.enemies_list.remove(dead_enemy)
        self.enemies_dead.clear()

    @staticmethod
    def _distance(x1, y1, x2, y2):
        """
        Calcule la distance entre deux points (x1, y1) et (x2, y2).
        :param x1: Coordonnée x du premier point.
        :param y1: Coordonnée y du premier point.
        :param x2: Coordonnée x du deuxième point.
        :param y2: Coordonnée y du deuxième point.
        :return: La distance entre les deux points.
        :pre: Aucune.
        :post: La distance entre les deux points est renvoyée.
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
