import pygame
import sys
import os
from collections import defaultdict

# Инициализация Pygame
pygame.init()

# Получаем размеры родительского экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("IT-Экосистема России: Умный поиск связей")

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
font_small = pygame.font.SysFont('Arial', 16)
font_medium = pygame.font.SysFont('Arial', 20)
font_large = pygame.font.SysFont('Arial', 24)


# Загрузка фона
def load_background():
    try:
        background = pygame.image.load("background.jpg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background
    except:
        print("Файл background.jpg не найден! Используется стандартный фон.")
        return None


background_image = load_background()


class Person:
    """Класс для представления человека в IT-экосистеме"""

    def __init__(self, name, age, profession, description, prediction, photo_path,
                 company, key_relationships, graph_role):
        self.name = name
        self.age = age
        self.profession = profession
        self.description = description
        self.prediction = prediction
        self.photo_path = photo_path
        self.company = company
        self.key_relationships = key_relationships
        self.graph_role = graph_role
        self.connections = []  # Будет заполнено автоматически
        self.connection_weights = {}  # Веса связей

        self.load_photo()

    def load_photo(self):
        """Загружает фото из файла"""
        try:
            if os.path.exists(self.photo_path):
                original_photo = pygame.image.load(self.photo_path)
                self.photo_small = pygame.transform.scale(original_photo, (80, 80))
                self.photo_large = pygame.transform.scale(original_photo, (180, 180))
            else:
                self.photo_small = None
                self.photo_large = None
                print(f"Файл {self.photo_path} не найден!")
        except Exception as e:
            print(f"Ошибка загрузки фото {self.photo_path}: {e}")
            self.photo_small = None
            self.photo_large = None


class SearchApp:
    def __init__(self, screen):
        self.screen = screen
        self.people = []
        self.filtered_people = []
        self.current_page = 0
        self.people_per_page = 5
        self.search_text = ""
        self.active_screen = "main"
        self.selected_person = None
        self.connection_threshold = 0.3  # Порог для отображения связей

        # Создаем людей и автоматически вычисляем связи
        self.create_it_ecosystem()
        self.calculate_all_connections()
        self.filtered_people = self.people.copy()

    def create_it_ecosystem(self):
        """Создание людей IT-экосистемы России"""

        people_data = [
            {
                "name": "Аркадий Волож",
                "age": 59,
                "profession": "Сооснователь Яндекс",
                "description": "Создатель крупнейшей IT-экосистемы России. Под его руководством Яндекс вырос из стартапа в компанию с тысячами сотрудников.",
                "prediction": "Продолжит развивать экосистему Яндекс на международной арене, фокусируясь на AI и облачных технологиях.",
                "photo_path": "person1.jpg",
                "company": "Яндекс",
                "key_relationships": ["Все, кто работал в Яндексе", "Михаил Парахин", "Александр Правдин"],
                "graph_role": "Центральный узел IT-экосистемы"
            },
            {
                "name": "Михаил Парахин",
                "age": 45,
                "profession": "CEO Ozon Ex-CEO Яндекс Маркет",
                "description": "Ключевой руководитель, перешедший из Яндекс в Ozon. Связывает две крупнейшие IT-компании России.",
                "prediction": "Превратит Ozon в экосистему по образцу Яндекс, интегрируя финтех и облачные сервисы.",
                "photo_path": "person2.jpg",
                "company": "Ozon",
                "key_relationships": ["Аркадий Волож", "Команда Ozon", "Бывшая команда Яндекс Маркета"],
                "graph_role": "Мост между Яндекс и Ozon"
            },
            {
                "name": "Александр Правдин",
                "age": 38,
                "profession": "Tech Director Яндекс Маркет",
                "description": "Технический специалист, связывающий мир разработки инструментов и их практического применения.",
                "prediction": "Возглавит разработку новых AI-инструментов для e-commerce.",
                "photo_path": "person3.jpg",
                "company": "Яндекс",
                "key_relationships": ["Аркадий Волож", "Бывшие коллеги из JetBrains", "Михаил Парахин"],
                "graph_role": "Технический мост разработки"
            },
            {
                "name": "Сергей Брин",
                "age": 50,
                "profession": "Сооснователь Google",
                "description": "Один из создателей крупнейшей поисковой системы мира. Символизирует глобальные IT-связи.",
                "prediction": "Продолжит инвестировать в прорывные технологии и AI-стартапы.",
                "photo_path": "person4.jpg",
                "company": "Google",
                "key_relationships": ["Все в глобальной IT-индустрии", "Российские IT-предприниматели"],
                "graph_role": "Глобальные международные связи"
            },
            {
                "name": "Павел Дуров",
                "age": 39,
                "profession": "Основатель VK Telegram",
                "description": "Создатель альтернативной IT-экосистемы. Известен независимой позицией и фокусом на privacy.",
                "prediction": "Telegram станет ведущей платформой для Web3 и децентрализованных приложений.",
                "photo_path": "person5.jpg",
                "company": "Telegram",
                "key_relationships": ["Конкуренты Яндекс", "Глобальное IT-сообщество"],
                "graph_role": "Независимый кластер экосистема"
            },
            {
                "name": "Олег Тиньков",
                "age": 56,
                "profession": "Основатель Тинькофф Банк",
                "description": "Предприниматель, связавший IT и традиционный банкинг. Создал первый полностью цифровой банк в России.",
                "prediction": "Продолжит экспансию в международный финтех, несмотря на вызовы.",
                "photo_path": "person6.jpg",
                "company": "Тинькофф",
                "key_relationships": ["IT-сообщество", "Финтех-стартапы", "Герман Греф"],
                "graph_role": "Мост IT и финтех"
            },
            {
                "name": "Герман Греф",
                "age": 60,
                "profession": "CEO Сбербанк",
                "description": "Превратил Сбербанк из традиционного банка в технологическую компанию. Связывает IT и государственные структуры.",
                "prediction": "Сбербанк станет полноценной IT-корпорацией с фокусом на AI и big data.",
                "photo_path": "person7.jpg",
                "company": "Сбербанк",
                "key_relationships": ["Все IT-компании, работающие со Сбером", "Олег Тиньков", "Аркадий Волож"],
                "graph_role": "Мост государство и IT"
            }
        ]

        for data in people_data:
            person = Person(**data)
            self.people.append(person)

    def calculate_connection_weight(self, person1, person2):
        """Вычисляет вес связи между двумя людьми (0-1)"""
        if person1.name == person2.name:
            return 0

        weight = 0

        # 1. Компания (самый сильный фактор - 0.4 балла)
        if person1.company == person2.company:
            weight += 0.4

        # 2. Общие слова в профессии (0.3 балла)
        prof1_words = set(person1.profession.lower().split())
        prof2_words = set(person2.profession.lower().split())
        common_prof_words = prof1_words & prof2_words
        if common_prof_words:
            weight += 0.3 * min(len(common_prof_words) / 2, 1)

        # 3. Общие слова в роли графа (0.2 балла)
        role1_words = set(person1.graph_role.lower().split())
        role2_words = set(person2.graph_role.lower().split())
        common_role_words = role1_words & role2_words
        if common_role_words:
            weight += 0.2 * min(len(common_role_words), 1)

        # 4. Общие ключевые слова в описании (0.1 балла)
        desc1_words = set(person1.description.lower().split()[:20])  # Берем первые 20 слов
        desc2_words = set(person2.description.lower().split()[:20])
        common_desc_words = desc1_words & desc2_words
        weight += 0.1 * min(len(common_desc_words) / 5, 1)

        return min(weight, 1.0)  # Ограничиваем максимум 1.0

    def calculate_all_connections(self):
        """Автоматически вычисляет все связи между людьми"""
        print("Вычисление автоматических связей...")

        for i, person1 in enumerate(self.people):
            person1.connections = []
            person1.connection_weights = {}

            for j, person2 in enumerate(self.people):
                if i == j:
                    continue

                weight = self.calculate_connection_weight(person1, person2)
                person1.connection_weights[person2.name] = weight

                # Добавляем в связи если вес выше порога
                if weight >= self.connection_threshold:
                    person1.connections.append(person2.name)

            print(f"{person1.name}: {len(person1.connections)} связей")

    def find_person_by_name(self, name):
        """Находит человека по имени"""
        for person in self.people:
            if person.name == name:
                return person
        return None

    def get_connected_people(self, person):
        """Возвращает список связанных людей с весами"""
        connected = []
        for connection_name in person.connections:
            connected_person = self.find_person_by_name(connection_name)
            if connected_person:
                weight = person.connection_weights.get(connection_name, 0)
                connected.append((connected_person, weight))

        # Сортируем по весу связей (от сильных к слабым)
        connected.sort(key=lambda x: x[1], reverse=True)
        return connected

    def get_connection_strength_color(self, weight):
        """Возвращает цвет в зависимости от силы связи"""
        if weight > 0.7:
            return RED  # Очень сильная связь
        elif weight > 0.5:
            return ORANGE  # Сильная связь
        elif weight > 0.3:
            return GREEN  # Средняя связь
        else:
            return BLUE  # Слабая связь

    def draw_background(self):
        """Отрисовка фона"""
        if background_image:
            self.screen.blit(background_image, (0, 0))
        else:
            self.screen.fill(LIGHT_GRAY)

    def draw_search_bar(self):
        """Отрисовка строки поиска с лупой внутри"""
        search_width = min(600, WIDTH - 200)
        search_rect = pygame.Rect(50, 50, search_width, 45)
        pygame.draw.rect(self.screen, WHITE, search_rect)
        pygame.draw.rect(self.screen, BLACK, search_rect, 2)

        # Текст в поле ввода
        text_surface = font_medium.render(self.search_text, True, BLACK)
        self.screen.blit(text_surface, (search_rect.x + 50, search_rect.y + 12))

        # Лупа внутри поля поиска (черная)
        lupа_x = search_rect.x + 15
        lupа_y = search_rect.y + 15

        # Рисуем лупy (черную)
        pygame.draw.circle(self.screen, BLACK, (lupа_x + 8, lupа_y + 8), 8, 2)
        pygame.draw.line(self.screen, BLACK, (lupа_x + 13, lupа_y + 13),
                         (lupа_x + 20, lupа_y + 20), 2)

        # Область клика для поиска (вся строка поиска)
        search_button = search_rect.copy()

        return search_button

    def draw_person_card(self, person, x, y, width, height):
        """Отрисовка карточки человека"""
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height))
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 1)

        # Фото
        photo_rect = pygame.Rect(x + 15, y + 10, 80, 80)
        if person.photo_small is not None:
            self.screen.blit(person.photo_small, photo_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, photo_rect)

        # ФИО
        name_text = font_medium.render(person.name, True, BLACK)
        self.screen.blit(name_text, (x + 110, y + 15))

        # Профессия и компания
        profession_text = font_small.render(f"{person.profession} | {person.company}", True, GRAY)
        self.screen.blit(profession_text, (x + 110, y + 45))

        # Количество связей
        connections_text = font_small.render(f"Связей: {len(person.connections)}", True, BLUE)
        self.screen.blit(connections_text, (x + 110, y + 65))

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

        # Кнопка "Назад"
        if self.current_page > 0:
            left_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 50, 50)
            pygame.draw.rect(self.screen, BLUE, left_button)
            pygame.draw.polygon(self.screen, WHITE, [
                (left_button.centerx + 8, left_button.centery - 12),
                (left_button.centerx - 8, left_button.centery),
                (left_button.centerx + 8, left_button.centery + 12)
            ])
            buttons.append(("left", left_button))

        # Кнопка "Вперед"
        if self.current_page < total_pages - 1:
            right_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 100, 50, 50)
            pygame.draw.rect(self.screen, BLUE, right_button)
            pygame.draw.polygon(self.screen, WHITE, [
                (right_button.centerx - 8, right_button.centery - 12),
                (right_button.centerx + 8, right_button.centery),
                (right_button.centerx - 8, right_button.centery + 12)
            ])
            buttons.append(("right", right_button))

        # Номер страницы
        page_text = font_medium.render(f"Страница {self.current_page + 1} из {max(1, total_pages)}", True, BLACK)
        page_rect = page_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        self.screen.blit(page_text, page_rect)

        return buttons

    def draw_detail_screen(self):
        """Отрисовка экрана с детальной информацией о человеке"""
        if not self.selected_person:
            return

        person = self.selected_person
        connected_people = self.get_connected_people(person)

        # Фон
        self.draw_background()

        # Белый фон для контента
        content_rect = pygame.Rect(40, 40, WIDTH - 80, HEIGHT - 80)
        pygame.draw.rect(self.screen, WHITE, content_rect)
        pygame.draw.rect(self.screen, BLACK, content_rect, 2)

        # Кнопка "Назад"
        back_button = pygame.Rect(40, 40, 100, 40)
        pygame.draw.rect(self.screen, BLUE, back_button)
        back_text = font_medium.render("Назад", True, WHITE)
        text_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, text_rect)

        # Основная информация
        info_x = 80
        info_y = 120

        # Фото
        photo_rect = pygame.Rect(info_x, info_y, 180, 180)
        if person.photo_large is not None:
            self.screen.blit(person.photo_large, photo_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, photo_rect)

        # Информация справа от фото
        text_x = info_x + 200

        name_text = font_large.render(person.name, True, BLACK)
        self.screen.blit(name_text, (text_x, info_y))

        age_text = font_medium.render(f"Возраст: {person.age}", True, BLACK)
        self.screen.blit(age_text, (text_x, info_y + 40))

        profession_text = font_medium.render(f"Профессия: {person.profession}", True, BLACK)
        self.screen.blit(profession_text, (text_x, info_y + 70))

        company_text = font_medium.render(f"Компания: {person.company}", True, BLUE)
        self.screen.blit(company_text, (text_x, info_y + 100))

        # Роль в графе
        role_text = font_medium.render(f"Роль в сети: {person.graph_role}", True, GREEN)
        self.screen.blit(role_text, (text_x, info_y + 130))

        # Количество связей
        conn_count_text = font_medium.render(f"Автоматических связей: {len(person.connections)}", True, PURPLE)
        self.screen.blit(conn_count_text, (text_x, info_y + 160))

        # Описание
        desc_y = info_y + 200
        desc_title = font_medium.render("Описание:", True, BLACK)
        self.screen.blit(desc_title, (info_x, desc_y))

        desc_lines = self.wrap_text(person.description, font_small, WIDTH - 160)
        for i, line in enumerate(desc_lines):
            desc_line = font_small.render(line, True, BLACK)
            self.screen.blit(desc_line, (info_x, desc_y + 30 + i * 25))

        # Связанные люди в сети
        conn_y = desc_y + 30 + len(desc_lines) * 25 + 20
        conn_title = font_medium.render("Автоматически найденные связи:", True, BLACK)
        self.screen.blit(conn_title, (info_x, conn_y))

        # Кнопки связанных людей с индикацией силы связи
        connection_buttons = []
        button_x = info_x
        button_y = conn_y + 30

        for connected_person, weight in connected_people:
            if button_x + 250 > WIDTH - 80:
                button_x = info_x
                button_y += 40

            # Цвет кнопки в зависимости от силы связи
            connection_color = self.get_connection_strength_color(weight)

            conn_button = pygame.Rect(button_x, button_y, 240, 30)
            pygame.draw.rect(self.screen, connection_color, conn_button)

            # Текст с именем и силой связи
            conn_text = font_small.render(
                f"{connected_person.name} ({weight:.1f})",
                True, WHITE
            )
            text_rect = conn_text.get_rect(center=conn_button.center)
            self.screen.blit(conn_text, text_rect)

            connection_buttons.append((connected_person, conn_button))
            button_x += 250

        # Предсказание
        pred_y = button_y + 50
        pred_title = font_medium.render("Прогноз развития:", True, BLACK)
        self.screen.blit(pred_title, (info_x, pred_y))

        pred_lines = self.wrap_text(person.prediction, font_small, WIDTH - 160)
        for i, line in enumerate(pred_lines):
            pred_line = font_small.render(line, True, BLACK)
            self.screen.blit(pred_line, (info_x, pred_y + 30 + i * 25))

        return back_button, connection_buttons

    def wrap_text(self, text, font, max_width):
        """Разбивает текст на строки"""
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
        """Поиск людей по профессии и имени"""
        if not self.search_text.strip():
            self.filtered_people = self.people.copy()
        else:
            search_lower = self.search_text.lower()
            self.filtered_people = [
                person for person in self.people
                if search_lower in person.profession.lower() or
                   search_lower in person.name.lower() or
                   search_lower in person.company.lower() or
                   search_lower in person.graph_role.lower()
            ]

        self.current_page = 0

    def run(self):
        """Основной цикл приложения"""
        running = True
        detail_buttons = []
        pagination_buttons = []
        connection_buttons = []

        while running:
            self.draw_background()

            if self.active_screen == "main":
                search_button = self.draw_search_bar()

                start_index = self.current_page * self.people_per_page
                end_index = start_index + self.people_per_page
                current_people = self.filtered_people[start_index:end_index]

                detail_buttons = []
                for i, person in enumerate(current_people):
                    card_y = 120 + i * 120
                    card_width = min(900, WIDTH - 100)
                    detail_button = self.draw_person_card(person, 50, card_y, card_width, 110)
                    detail_buttons.append((person, detail_button))

                pagination_buttons = self.draw_pagination()

            elif self.active_screen == "detail":
                back_button, connection_buttons = self.draw_detail_screen()
                pagination_buttons = [("back", back_button)]

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
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                        else:
                            self.search_text += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.active_screen == "main":
                        search_button = self.draw_search_bar()
                        if search_button.collidepoint(mouse_pos):
                            self.search_people()

                        for person, button in detail_buttons:
                            if button.collidepoint(mouse_pos):
                                self.selected_person = person
                                self.active_screen = "detail"

                        for button_type, button_rect in pagination_buttons:
                            if button_rect.collidepoint(mouse_pos):
                                if button_type == "left":
                                    self.current_page -= 1
                                elif button_type == "right":
                                    self.current_page += 1

                    elif self.active_screen == "detail":
                        for button_type, button_rect in pagination_buttons:
                            if button_rect.collidepoint(mouse_pos) and button_type == "back":
                                self.active_screen = "main"

                        # Обработка кликов по связанным людям
                        for connected_person, conn_button in connection_buttons:
                            if conn_button.collidepoint(mouse_pos):
                                self.selected_person = connected_person
                                # остаемся на экране деталей, но для нового человека

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = SearchApp(screen)
    app.run()