"""
Главный запускаемый файл приложения.
"""

import pygame
import sys
from search_app import SearchApp

# Инициализация Pygame
pygame.init()

# Получаем размеры родительского экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("IT-Экосистема России: Умный поиск связей")


def main():
    """
    Точка входа в приложение.
    """
    try:
        app = SearchApp(screen)
        app.run()
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()