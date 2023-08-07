import pygame
import math


class BattleSystem:
    def __init__(self, player, enemies_list):
        self.player = player
        self.enemies_list = enemies_list
        self.last_attack_time = pygame.time.get_ticks()
        self.enemies_dead = []  # Liste pour stocker les ennemis morts

    def update(self):
        self._try_attack()

    def _try_attack(self):
        # Vérifie si suffisamment de temps s'est écoulé depuis la dernière attaque
        current_time = pygame.time.get_ticks()
        attack_interval = 1000 / self.player.attributes['attack_speed']

        if current_time - self.last_attack_time > attack_interval:
            self._attack_nearest_enemy()
            self.last_attack_time = current_time

    def _find_nearest_enemy_within_range(self):
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
        nearest_enemy = self._find_nearest_enemy_within_range()
        if nearest_enemy:
            self._inflict_damage(nearest_enemy)

    def _inflict_damage(self, enemy):
        enemy.take_damage(self.player.attributes['damage'])
        if enemy.hp <= 0:
            self.enemies_dead.append(enemy)
            self._remove_dead_enemies()

    def _remove_dead_enemies(self):
        for dead_enemy in self.enemies_dead:
            if dead_enemy in self.enemies_list:
                self.enemies_list.remove(dead_enemy)
        self.enemies_dead.clear()

    @staticmethod
    def _distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
