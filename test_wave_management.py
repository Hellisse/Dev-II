import unittest
from unittest.mock import Mock
from wave_management import WaveManagement  # Assurez-vous que le chemin d'importation est correct


class TestWaveManagement(unittest.TestCase):
    def test_generate_enemy(self):
        # Créer une instance de WaveManagement avec un mock pour la liste d'ennemis
        enemy_list_mock = Mock()
        wave_manager = WaveManagement((800, 600), enemy_list_mock)

        # Tableau de valeurs pour tester la méthode generate_enemy
        # Tableau de valeurs pour tester la méthode generate_enemy
        test_values = [
            ("SlowEnemy", 100, 0.25),
            ("FastEnemy", 30, 1),
            ("RegularEnemy", 50, 0.5)
        ]

        # Exécuter la méthode generate_enemy pour chaque valeur de test
        for enemy_type, expected_hp, expected_speed in test_values:
            with self.subTest(enemy_type=enemy_type):
                # Appeler la méthode generate_enemy
                wave_manager.generate_enemy()

                # Vérifier si un ennemi a été ajouté à la liste
                self.assertTrue(enemy_list_mock.append.called)

                # Récupérer l'ennemi ajouté
                added_enemy = enemy_list_mock.append.call_args[0][0]
                # Vérifier les attributs de l'ennemi ajouté
                if enemy_type.strip() == type(added_enemy).__name__.strip():
                    if added_enemy.hp == expected_hp:
                        print("HP OK")
                    if added_enemy.speed == expected_speed:
                        print("SPEED OK")
                    if type(added_enemy).__name__ == wave_manager.ENEMY_STATS[enemy_type]["class"].__name__:
                        print("TYPE OK")


if __name__ == '__main__':
    unittest.main()
