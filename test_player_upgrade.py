import unittest
from player import Player

class TestPlayer(unittest.TestCase):
    def test_upgrade_attribute(self):
        # Créer une instance de Player pour le test
        player = Player(800, 600)

        # Tableau de valeurs pour tester la méthode upgrade_attribute
        test_values = [
            ("max_hp", 2, 10),  # (attribut, niveau initial,valeur)
            ("max_range", 4, 102),
            ("attack_speed", 5, 1.1),
            ("damage", 8, 10)
        ]

        # Exécuter la méthode upgrade_attribute pour chaque valeur de test
        for attribute, initial_level, expected_level in test_values:
            with self.subTest(attribute=attribute):
                # Affecter le niveau initial à l'attribut du joueur
                player.upgrade_levels[attribute] = initial_level
                player.attributes[attribute] = player.formulas[attribute](initial_level)

                # Appeler la méthode upgrade_attribute
                player.upgrade_attribute(attribute)
                print(player.upgrade_levels[attribute])

                # Vérifier si le niveau de l'attribut a été mis à jour correctement
                self.assertEqual(player.upgrade_levels[attribute], initial_level)
                self.assertEqual(player.attributes[attribute], player.formulas[attribute](initial_level))


if __name__ == '__main__':
    unittest.main()
