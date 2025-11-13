"""
Вспомогательные функции приложения.
"""

import pygame
from config import BACKGROUND_PATH, RED, ORANGE, GREEN, BLUE

def load_background():
    """Загружает фоновое изображение."""
    try:
        from config import WIDTH, HEIGHT
        background = pygame.image.load(BACKGROUND_PATH)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background
    except Exception as e:
        print(f"Не удалось загрузить фон: {e}")
        return None

def wrap_text(text, font, max_width):
    """Разбивает текст на строки."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = font.size(test_line)[0]

        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def calculate_connection_weight(person1, person2):
    """Вычисляет вес связи между двумя людьми."""
    if person1.name == person2.name:
        return 0

    weight = 0

    if person1.company == person2.company:
        weight += 0.4

    prof1_words = set(person1.profession.lower().split())
    prof2_words = set(person2.profession.lower().split())
    common_prof_words = prof1_words & prof2_words
    if common_prof_words:
        weight += 0.3 * min(len(common_prof_words) / 2, 1)

    role1_words = set(person1.graph_role.lower().split())
    role2_words = set(person2.graph_role.lower().split())
    common_role_words = role1_words & role2_words
    if common_role_words:
        weight += 0.2 * min(len(common_role_words), 1)

    desc1_words = set(person1.description.lower().split()[:20])
    desc2_words = set(person2.description.lower().split()[:20])
    common_desc_words = desc1_words & desc2_words
    weight += 0.1 * min(len(common_desc_words) / 5, 1)

    return min(weight, 1.0)

def get_connection_strength_color(weight):
    """Определяет цвет для визуализации силы связи."""
    if weight > 0.7:
        return RED
    elif weight > 0.5:
        return ORANGE
    elif weight > 0.3:
        return GREEN
    else:
        return BLUE