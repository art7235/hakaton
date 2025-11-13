import pygame
import sys

# Инициализация Pygame
pygame.init()

# Получаем размеры родительского экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Поиск по профессиям")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (100, 150, 255)

# Шрифты
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 22)
font_large = pygame.font.SysFont('Arial', 26)


class Person:
    """Класс для представления человека"""

    def __init__(self, name, age, profession, description, prediction, photo_path):
        self.name = name  # ФИО
        self.age = age  # Возраст
        self.profession = profession  # Профессия
        self.description = description  # Описание человека
        self.prediction = prediction  # Предсказание о будущем
        self.photo_path = photo_path  # Путь к файлу с фото


class SearchApp:
    def __init__(self, screen):
        self.screen = screen  # Сохраняем экран как атрибут класса
        self.people = []  # Хранилище людей
        self.filtered_people = []  # Отфильтрованные люди
        self.current_page = 0  # Текущая страница
        self.people_per_page = 5  # Количество людей на странице
        self.search_text = ""  # Текст в строке поиска
        self.active_screen = "main"  # Активный экран ("main" или "detail")
        self.selected_person = None  # Выбранный человек для детального просмотра

        # Создаем тестовых людей (7 пустых карточек)
        self.create_sample_people()
        self.filtered_people = self.people.copy()

    def create_sample_people(self):
        """Создание 7 пустых карточек людей для заполнения"""
        # Для фото используйте файлы с именами: person1.jpg, person2.jpg, ..., person7.jpg
        # Положите их в папку с проектом или укажите полный путь

        for i in range(7):
            person = Person(
                name=f"ФИО Человека {i + 1}",
                age=25 + i,
                profession=f"Профессия {i + 1}",
                description=f"Описание человека {i + 1}. Здесь будет подробная информация о человеке, его достижениях и опыте работы.",
                prediction=f"Предсказание для человека {i + 1}. Здесь будет текст с предсказанием о будущем в профессиональной сфере.",
                photo_path=f"person{i + 1}.jpg"  # Имя файла фото
            )
            self.people.append(person)

    def draw_search_bar(self):
        """Отрисовка строки поиска"""
        # Поле ввода (уменьшил ширину)
        search_width = min(600, WIDTH - 200)
        search_rect = pygame.Rect(50, 50, search_width, 45)
        pygame.draw.rect(self.screen, WHITE, search_rect)
        pygame.draw.rect(self.screen, BLACK, search_rect, 2)

        # Текст в поле ввода
        text_surface = font_medium.render(self.search_text, True, BLACK)
        self.screen.blit(text_surface, (search_rect.x + 10, search_rect.y + 12))

        # Кнопка поиска (лупа)
        search_button = pygame.Rect(search_rect.right + 10, 50, 60, 45)
        pygame.draw.rect(self.screen, BLUE, search_button)

        # Рисуем лупу (упрощенная версия)
        pygame.draw.circle(self.screen, WHITE, (search_button.centerx, search_button.centery), 12, 2)
        pygame.draw.line(self.screen, WHITE, (search_button.centerx + 6, search_button.centery + 6),
                         (search_button.centerx + 14, search_button.centery + 14), 2)

        return search_button

    def draw_person_card(self, person, x, y, width, height):
        """Отрисовка карточки человека"""
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, WHITE, card_rect)
        pygame.draw.rect(self.screen, BLACK, card_rect, 1)

        # Место для фото (заглушка)
        photo_rect = pygame.Rect(x + 15, y + 10, 80, 80)
        pygame.draw.rect(self.screen, GRAY, photo_rect)

        # Если есть фото, загружаем его (в реальном коде)
        # try:
        #     photo = pygame.image.load(person.photo_path)
        #     photo = pygame.transform.scale(photo, (80, 80))
        #     self.screen.blit(photo, photo_rect)
        # except:
        #     pygame.draw.rect(self.screen, GRAY, photo_rect)

        # ФИО
        name_text = font_medium.render(person.name, True, BLACK)
        self.screen.blit(name_text, (x + 110, y + 15))

        # Профессия
        profession_text = font_small.render(person.profession, True, GRAY)
        self.screen.blit(profession_text, (x + 110, y + 45))

        # Кнопка "Подробнее"
        detail_button = pygame.Rect(x + width - 130, y + height - 40, 110, 30)
        pygame.draw.rect(self.screen, BLUE, detail_button)
        detail_text = font_small.render("Подробнее", True, WHITE)
        text_rect = detail_text.get_rect(center=detail_button.center)
        self.screen.blit(detail_text, text_rect)

        return detail_button

    def draw_pagination(self):
        """Отрисовка кнопок пагинации"""
        buttons = []

        total_pages = (len(self.filtered_people) + self.people_per_page - 1) // self.people_per_page

        # Кнопка "Назад" (стрелка влево) - теперь выше надписи
        if self.current_page > 0:
            left_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 50, 50)  # Подняли выше
            pygame.draw.rect(self.screen, BLUE, left_button)

            # Рисуем стрелку влево
            pygame.draw.polygon(self.screen, WHITE, [
                (left_button.centerx + 8, left_button.centery - 12),
                (left_button.centerx - 8, left_button.centery),
                (left_button.centerx + 8, left_button.centery + 12)
            ])
            buttons.append(("left", left_button))

        # Кнопка "Вперед" (стрелка вправо) - теперь выше надписи
        if self.current_page < total_pages - 1:
            right_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 100, 50, 50)  # Подняли выше
            pygame.draw.rect(self.screen, BLUE, right_button)

            # Рисуем стрелку вправо
            pygame.draw.polygon(self.screen, WHITE, [
                (right_button.centerx - 8, right_button.centery - 12),
                (right_button.centerx + 8, right_button.centery),
                (right_button.centerx - 8, right_button.centery + 12)
            ])
            buttons.append(("right", right_button))

        # Номер страницы (рисуем ПОД кнопками)
        page_text = font_medium.render(f"Страница {self.current_page + 1} из {max(1, total_pages)}", True, BLACK)
        page_rect = page_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))  # Опустили ниже
        self.screen.blit(page_text, page_rect)

        return buttons

    def draw_detail_screen(self):
        """Отрисовка экрана с детальной информацией о человеке"""
        if not self.selected_person:
            return

        person = self.selected_person

        # Фон
        self.screen.fill(LIGHT_GRAY)

        # Кнопка "Назад"
        back_button = pygame.Rect(40, 40, 100, 40)
        pygame.draw.rect(self.screen, BLUE, back_button)
        back_text = font_medium.render("Назад", True, WHITE)
        text_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, text_rect)

        # Основная информация
        info_x = max(40, WIDTH // 12)  # Адаптивный отступ
        info_y = 120

        # Место для фото
        photo_rect = pygame.Rect(info_x, info_y, 180, 180)
        pygame.draw.rect(self.screen, GRAY, photo_rect)

        # Если есть фото, загружаем его (в реальном коде)
        try:
            photo = pygame.image.load(person.photo_path)
            photo = pygame.transform.scale(photo, (180, 180))
            self.screen.blit(photo, photo_rect)
        except:
            pygame.draw.rect(self.screen, GRAY, photo_rect)

        # Текстовая информация
        text_x = info_x + 200
        max_text_width = WIDTH - text_x - 40  # Ограничиваем ширину текста

        name_text = font_large.render(person.name, True, BLACK)
        self.screen.blit(name_text, (text_x, info_y))

        age_text = font_medium.render(f"Возраст: {person.age}", True, BLACK)
        self.screen.blit(age_text, (text_x, info_y + 40))

        profession_text = font_medium.render(f"Профессия: {person.profession}", True, BLACK)
        self.screen.blit(profession_text, (text_x, info_y + 75))

        # Описание
        desc_y = info_y + 200
        desc_title = font_medium.render("Описание:", True, BLACK)
        self.screen.blit(desc_title, (info_x, desc_y))

        # Многострочный текст описания
        desc_lines = self.wrap_text(person.description, font_small, WIDTH - 2 * info_x)
        for i, line in enumerate(desc_lines):
            desc_line = font_small.render(line, True, BLACK)
            self.screen.blit(desc_line, (info_x, desc_y + 35 + i * 25))

        # Предсказание
        pred_y = desc_y + 35 + len(desc_lines) * 25 + 25
        pred_title = font_medium.render("Предсказание о будущем:", True, BLACK)
        self.screen.blit(pred_title, (info_x, pred_y))

        # Многострочный текст предсказания
        pred_lines = self.wrap_text(person.prediction, font_small, WIDTH - 2 * info_x)
        for i, line in enumerate(pred_lines):
            pred_line = font_small.render(line, True, BLACK)
            self.screen.blit(pred_line, (info_x, pred_y + 35 + i * 25))

        return back_button

    def wrap_text(self, text, font, max_width):
        """Разбивает текст на строки, чтобы он помещался в заданную ширину"""
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

    def search_people(self):
        """Поиск людей по профессии"""
        if not self.search_text.strip():
            self.filtered_people = self.people.copy()
        else:
            search_lower = self.search_text.lower()
            self.filtered_people = [
                person for person in self.people
                if search_lower in person.profession.lower() or
                   search_lower in person.name.lower()
            ]

        self.current_page = 0  # Сбрасываем на первую страницу

    def run(self):
        """Основной цикл приложения"""
        running = True
        detail_buttons = []
        pagination_buttons = []

        while running:
            # ИСПРАВЛЕНО: используем self.screen вместо screen
            self.screen.fill(LIGHT_GRAY)

            if self.active_screen == "main":
                # Основной экран
                search_button = self.draw_search_bar()

                # Отображаем людей на текущей странице
                start_index = self.current_page * self.people_per_page
                end_index = start_index + self.people_per_page
                current_people = self.filtered_people[start_index:end_index]

                detail_buttons = []
                for i, person in enumerate(current_people):
                    card_y = 120 + i * 110
                    card_width = min(900, WIDTH - 100)  # Ограничиваем ширину карточки
                    detail_button = self.draw_person_card(person, 50, card_y, card_width, 100)
                    detail_buttons.append((person, detail_button))

                # Пагинация
                pagination_buttons = self.draw_pagination()

            elif self.active_screen == "detail":
                # Экран детальной информации
                back_button = self.draw_detail_screen()
                pagination_buttons = [("back", back_button)] if back_button else []

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if self.active_screen == "main":
                        if event.key == pygame.K_BACKSPACE:
                            self.search_text = self.search_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.search_people()
                        elif event.key == pygame.K_ESCAPE:  # Выход по ESC
                            running = False
                        else:
                            self.search_text += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.active_screen == "main":
                        # Проверяем кнопку поиска
                        search_button = self.draw_search_bar()
                        if search_button.collidepoint(mouse_pos):
                            self.search_people()

                        # Проверяем кнопки "Подробнее"
                        for person, button in detail_buttons:
                            if button.collidepoint(mouse_pos):
                                self.selected_person = person
                                self.active_screen = "detail"

                        # Проверяем кнопки пагинации
                        for button_type, button_rect in pagination_buttons:
                            if button_rect.collidepoint(mouse_pos):
                                if button_type == "left":
                                    self.current_page -= 1
                                elif button_type == "right":
                                    self.current_page += 1

                    elif self.active_screen == "detail":
                        # Проверяем кнопку "Назад"
                        for button_type, button_rect in pagination_buttons:
                            if button_rect.collidepoint(mouse_pos) and button_type == "back":
                                self.active_screen = "main"

            pygame.display.flip()

        pygame.quit()
        sys.exit()


# Запуск приложения
if __name__ == "__main__":
    app = SearchApp(screen)  # Передаем screen в конструктор
    app.run()