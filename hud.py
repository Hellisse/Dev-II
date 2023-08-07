import pygame
import time
from button import Button


class HUD:
    def __init__(self, player, screen_width, screen_height):
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.Font(None, 26)
        self.font_money = pygame.font.Font(None, 36)
        self.start_time = time.time()

        self.BUTTON_PROPERTIES = {
            'x': 10,
            'width': 200,
            'height': 40,
            'color': (0, 255, 0),
        }
        self.button_gap = 10
        self.buttons = self.generate_buttons(self.button_gap)

    def generate_buttons(self, gap):
        y_positions = [(i * (self.BUTTON_PROPERTIES['height'] + gap)) + 10 for i in range(len(self.player.attributes))]

        return [
            Button(self.BUTTON_PROPERTIES['x'], y, self.BUTTON_PROPERTIES['width'], self.BUTTON_PROPERTIES['height'],
                   self.BUTTON_PROPERTIES['color'], attribute=attribute, player=self.player)
            for y, attribute in zip(y_positions, self.player.attributes)]

    def draw(self, screen):
        # Appeler les méthodes individuelles pour dessiner chaque partie de l'HUD
        self.draw_money(screen)
        self.draw_time(screen)
        self.draw_stats(screen)
        for button in self.buttons:
            button.draw(screen)

    def draw_money(self, screen):
        # Dessiner l'argent du joueur en haut au milieu
        money_text = "Money: ${}".format(int(self.player.money))
        money_surface = self.font_money.render(money_text, True, (255, 255, 255))
        money_x = (self.screen_width - money_surface.get_width()) / 2
        screen.blit(money_surface, (money_x, 10))  # 10 pixels d'écart du haut

    def draw_time(self, screen):
        # Dessiner le temps écoulé depuis le début de la partie
        elapsed_time = int(time.time() - self.start_time)
        time_text = "Time: {:02d}:{:02d}".format(elapsed_time // 60, elapsed_time % 60)
        time_surface = self.font_money.render(time_text, True, (255, 255, 255))
        time_x = (self.screen_width - time_surface.get_width()) / 2
        screen.blit(time_surface, (
        time_x, 50))  # Affichez le temps sous l'affichage de l'argent avec un écart de 50 pixels depuis le haut

    def draw_stats(self, screen):
        # Générer la liste des stats avec le formatage correct des noms
        stats = [
            (name.replace("_", " ").upper() if len(name) <= 3 else name.replace("_", " ").title(), value)
            for name, value in self.player.attributes.items()
        ]

        # Calculez la largeur du nom de stat le plus long
        max_name_width = max(self.font.size(name)[0] for name, _ in stats)
        max_value_width = self.font.size(" : 999K 9 ")[0]

        x = self.screen_width - (max_name_width + max_value_width)  # Position x initiale
        y = 10  # Position y initiale

        for name, value in stats:
            self.render_stat_name(screen, x, y, name)
            self.render_stat_value(screen, x, y, max_name_width, value)
            y += 40  # Espace entre les stats

    def render_stat_name(self, screen, x, y, name):
        name_surface = self.font.render(name, True, (255, 255, 255))
        screen.blit(name_surface, (x, y))

    def render_stat_value(self, screen, x, y, max_name_width, value):
        if value < 10:
            value_text = ": {:.2f}".format(value)
        else:
            value_text = ": {}".format(int(value))
        value_surface = self.font.render(value_text, True, (255, 255, 255))
        screen.blit(value_surface, (x + max_name_width + 10, y))

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in self.buttons:
                if button.is_over(mouse_pos):
                    button.click_action()
