"""
Компоненты пользовательского интерфейса.
"""

import pygame
from config import *

class UIComponents:
    """Класс для отрисовки компонентов интерфейса."""

    def __init__(self, screen):
        self.screen = screen

    def draw_search_bar(self, search_text):
        """Отрисовывает строку поиска с лупой."""
        search_width = min(600, WIDTH - 200)
        search_rect = pygame.Rect(50, 50, search_width, 45)
        pygame.draw.rect(self.screen, WHITE, search_rect)
        pygame.draw.rect(self.screen, BLACK, search_rect, 2)

        text_surface = FONT_MEDIUM.render(search_text, True, BLACK)
        self.screen.blit(text_surface, (search_rect.x + 50, search_rect.y + 12))

        lupа_x = search_rect.x + 15
        lupа_y = search_rect.y + 15

        pygame.draw.circle(self.screen, BLACK, (lupа_x + 8, lupа_y + 8), 8, 2)
        pygame.draw.line(self.screen, BLACK, (lupа_x + 13, lupа_y + 13),
                         (lupа_x + 20, lupа_y + 20), 2)

        return search_rect

    def draw_person_card(self, person, x, y, width, height):
        """Отрисовывает карточку человека."""
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height))
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 1)

        photo_rect = pygame.Rect(x + 15, y + 10, 80, 80)
        if person.photo_small is not None:
            self.screen.blit(person.photo_small, photo_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, photo_rect)

        name_text = FONT_MEDIUM.render(person.name, True, BLACK)
        self.screen.blit(name_text, (x + 110, y + 15))

        profession_text = FONT_SMALL.render(f"{person.profession} | {person.company}", True, GRAY)
        self.screen.blit(profession_text, (x + 110, y + 45))

        connections_text = FONT_SMALL.render(f"Связей: {len(person.connections)}", True, BLUE)
        self.screen.blit(connections_text, (x + 110, y + 65))

        detail_button = pygame.Rect(x + width - 130, y + height - 40, 110, 30)
        pygame.draw.rect(self.screen, BLUE, detail_button)
        detail_text = FONT_SMALL.render("Подробнее", True, WHITE)
        text_rect = detail_text.get_rect(center=detail_button.center)
        self.screen.blit(detail_text, text_rect)

        return detail_button

    def draw_pagination(self, current_page, total_pages):
        """Отрисовывает элементы пагинации."""
        buttons = []

        if current_page > 0:
            left_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 50, 50)
            pygame.draw.rect(self.screen, BLUE, left_button)
            pygame.draw.polygon(self.screen, WHITE, [
                (left_button.centerx + 8, left_button.centery - 12),
                (left_button.centerx - 8, left_button.centery),
                (left_button.centerx + 8, left_button.centery + 12)
            ])
            buttons.append(("left", left_button))

        if current_page < total_pages - 1:
            right_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 100, 50, 50)
            pygame.draw.rect(self.screen, BLUE, right_button)
            pygame.draw.polygon(self.screen, WHITE, [
                (right_button.centerx - 8, right_button.centery - 12),
                (right_button.centerx + 8, right_button.centery),
                (right_button.centerx - 8, right_button.centery + 12)
            ])
            buttons.append(("right", right_button))

        page_text = FONT_MEDIUM.render(f"Страница {current_page + 1} из {max(1, total_pages)}", True, BLACK)
        page_rect = page_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        self.screen.blit(page_text, page_rect)

        return buttons