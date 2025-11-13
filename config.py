"""
Настройки и константы приложения.
"""

import pygame
import os

# Инициализация pygame
pygame.init()

# Размеры экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (100, 150, 255)
GREEN = (100, 200, 100)
ORANGE = (255, 165, 0)
PURPLE = (180, 100, 240)
RED = (255, 100, 100)

# Шрифты
FONT_SMALL = pygame.font.SysFont('Arial', 16)
FONT_MEDIUM = pygame.font.SysFont('Arial', 20)
FONT_LARGE = pygame.font.SysFont('Arial', 24)

# Настройки приложения
PEOPLE_PER_PAGE = 5
CONNECTION_THRESHOLD = 0.3

# Пути к файлам
BACKGROUND_PATH = os.path.join("assets", "background.jpg")
PHOTO_PATHS = {
    "Аркадий Волож": os.path.join("assets", "person1.jpg"),
    "Михаил Парахин": os.path.join("assets", "person2.jpg"),
    "Александр Правдин": os.path.join("assets", "person3.jpg"),
    "Сергей Брин": os.path.join("assets", "person4.jpg"),
    "Павел Дуров": os.path.join("assets", "person5.jpg"),
    "Артем Инютин": os.path.join("assets", "person6.jpg"),
    "Герман Греф": os.path.join("assets", "person7.jpg")
}

# Пути к рекламным изображениям
ADS_PATHS = {
    "contrast": os.path.join("assets", "ads", "contrast.jpg"),
    "rock_band": os.path.join("assets", "ads", "rock_band.jpg"),
    "your_ad": "placeholder"
}