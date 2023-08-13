import pygame


class Button:
    def __init__(self, x, y, width, height, color, text='', attribute=None, player=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.attribute = attribute  # Attribut à mettre à jour
        self.player = player  # Le joueur est maintenant un attribut du bouton
        self.stored_price = 0 if not player else player.get_upgrade_cost(self.attribute)  # Initialiser le prix stocké

        if text:
            self.text = text
        else:
            if len(self.attribute) <= 3:
                self.text = self.attribute.replace("_", " ").upper()
            else:
                self.text = self.attribute.replace("_", " ").title()

    def draw(self, window):
        border_thickness = 3
        shadow_offset = 5

        # Rects definitions
        shadow_rect = (self.x + shadow_offset, self.y + shadow_offset, self.width, self.height)
        border_rect = (self.x - border_thickness, self.y - border_thickness,
                       self.width + 2 * border_thickness, self.height + 2 * border_thickness)
        main_rect = (self.x, self.y, self.width, self.height)

        # Draw shadow, border and main button
        pygame.draw.rect(window, (70, 70, 70), shadow_rect)
        pygame.draw.rect(window, (0, 0, 0), border_rect)
        pygame.draw.rect(window, self.color, main_rect)

        # Draw text on the button
        if self.text:
            font = pygame.font.Font(None, 24)

            # Affichage de l'attribut (texte principal) à gauche du bouton
            margin = 10  # Une marge pour espacer le texte des bords du bouton
            text_x = self.x + margin
            text_y = self.y + (self.height - font.size(self.text)[1]) / 2
            window.blit(font.render(self.text, 1, (0, 0, 0)), (text_x, text_y))

            # Affichage du prix à droite du bouton
            price_text = font.render(f"Prix: {self.stored_price}", 1, (255, 0, 0))
            price_text_x = self.x + self.width - price_text.get_width() - margin
            window.blit(price_text, (price_text_x, text_y))

    def is_over(self, pos):
        # Check if mouse position is inside the button
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def click_action(self):
        try:
            if self.attribute and self.player:
                # Obtenir le coût d'amélioration actuel
                current_price = self.player.get_upgrade_cost(self.attribute)

                # Vérifier si le joueur peut se permettre l'amélioration
                if self.player.money >= current_price:  # Utilisez l'attribut d'argent du joueur pour la comparaison
                    # Appliquer l'amélioration
                    self.player.upgrade_attribute(self.attribute)

                    # Mettre à jour le prix stocké pour l'affichage
                    self.stored_price = self.player.get_upgrade_cost(self.attribute) or 0
                else:
                    raise ValueError("Fonds insuffisants pour l'amélioration")

            else:
                raise AttributeError("Attribut non défini ou joueur non défini")

        except ValueError as ve:
            print(f"Erreur : {ve}")
        except AttributeError as ae:
            print(f"Erreur : {ae}")