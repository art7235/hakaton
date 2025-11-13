"""
Модель данных Person.
"""

import os
import pygame
from config import PHOTO_PATHS

class Person:
    """
    Класс, представляющий человека в IT-экосистеме.
    """

    def __init__(self, name, age, profession, description, prediction,
                 company, key_relationships, graph_role):
        self.name = name
        self.age = age
        self.profession = profession
        self.description = description
        self.prediction = prediction
        self.company = company
        self.key_relationships = key_relationships
        self.graph_role = graph_role
        self.connections = []
        self.connection_weights = {}

        self.photo_path = PHOTO_PATHS.get(name, "")
        self.load_photo()

    def load_photo(self):
        """Загружает и подготавливает фотографии."""
        try:
            if os.path.exists(self.photo_path):
                original_photo = pygame.image.load(self.photo_path)
                self.photo_small = pygame.transform.scale(original_photo, (80, 80))
                self.photo_large = pygame.transform.scale(original_photo, (180, 180))
            else:
                self.photo_small = None
                self.photo_large = None
        except Exception as e:
            print(f"Ошибка загрузки фото {self.photo_path}: {e}")
            self.photo_small = None
            self.photo_large = None

    def add_connection(self, person_name, weight):
        """Добавляет связь с другим человеком."""
        self.connections.append(person_name)
        self.connection_weights[person_name] = weight

    def __str__(self):
        return f"Person({self.name}, {self.profession})"