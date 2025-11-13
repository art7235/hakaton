"""
Основной класс приложения.
"""

import pygame
import os
from person import Person
from helpers import *
from ui_components import UIComponents
from config import *

class SearchApp:
    """Главный класс приложения."""

    def __init__(self, screen):
        self.screen = screen
        self.ui = UIComponents(screen)
        self.people = []
        self.filtered_people = []
        self.current_page = 0
        self.people_per_page = PEOPLE_PER_PAGE
        self.search_text = ""
        self.active_screen = "main"
        self.selected_person = None
        self.connection_threshold = CONNECTION_THRESHOLD
        self.ads_data = []
        self.ads_buttons = []

        self.create_it_ecosystem()
        self.calculate_all_connections()
        self.filtered_people = self.people.copy()
        self.load_ads()

    def create_it_ecosystem(self):
        """Создает начальный набор данных."""
        people_data = [
            {
                "name": "Аркадий Волож", "age": 59,
                "profession": "Сооснователь Яндекс", "company": "Яндекс",
                "description": "Создатель крупнейшей IT-экосистемы России. Под его руководством Яндекс вырос из стартапа в компанию с тысячами сотрудников.",
                "prediction": "Продолжит развивать экосистему Яндекс на международной арене, фокусируясь на AI и облачных технологиях.",
                "key_relationships": ["Все, кто работал в Яндексе", "Михаил Парахин", "Александр Правдин"],
                "graph_role": "Центральный узел IT-экосистемы"
            },
            {
                "name": "Михаил Парахин", "age": 45,
                "profession": "CEO Ozon Ex-CEO Яндекс Маркет", "company": "Ozon",
                "description": "Ключевой руководитель, перешедший из Яндекс в Ozon. Связывает две крупнейшие IT-компании России.",
                "prediction": "Превратит Ozon в экосистему по образцу Яндекс, интегрируя финтех и облачные сервисы.",
                "key_relationships": ["Аркадий Волож", "Команда Ozon", "Бывшая команда Яндекс Маркета"],
                "graph_role": "Мост между Яндекс и Ozon"
            },
            {
                "name": "Александр Правдин", "age": 38,
                "profession": "Tech Director Яндекс Маркет", "company": "Яндекс",
                "description": "Технический специалист, связывающий мир разработки инструментов и их практического применения.",
                "prediction": "Возглавит разработку новых AI-инструментов для e-commerce.",
                "key_relationships": ["Аркадий Волож", "Бывшие коллеги из JetBrains", "Михаил Парахин"],
                "graph_role": "Технический мост разработки"
            },
            {
                "name": "Сергей Брин", "age": 50,
                "profession": "Сооснователь Google", "company": "Google",
                "description": "Один из создателей крупнейшей поисковой системы мира. Символизирует глобальные IT-связи.",
                "prediction": "Продолжит инвестировать в прорывные технологии и AI-стартапы.",
                "key_relationships": ["Все в глобальной IT-индустрии", "Российские IT-предприниматели"],
                "graph_role": "Глобальные международные связи"
            },
            {
                "name": "Павел Дуров", "age": 39,
                "profession": "Основатель VK Telegram", "company": "Telegram",
                "description": "Создатель альтернативной IT-экосистемы. Известен независимой позицией и фокусом на privacy.",
                "prediction": "Telegram станет ведущей платформой для Web3 и децентрализованных приложений.",
                "key_relationships": ["Конкуренты Яндекс", "Глобальное IT-сообщество"],
                "graph_role": "Независимый кластер экосистема"
            },
            {
                "name": "Артем Инютин", "age": 42,
                "profession": "Основатель Avito", "company": "Avito",
                "description": "Создатель крупнейшей площадки онлайн-объявлений в России. Превратил стартап в компанию с миллиардной оценкой.",
                "prediction": "Расширит экосистему маркетплейсов и выведет компанию на новые рынки Восточной Европы.",
                "key_relationships": ["IT-сообщество", "Инвесторы", "Экосистема e-commerce"],
                "graph_role": "Лидер e-commerce"
            },
            {
                "name": "Герман Греф", "age": 60,
                "profession": "CEO Сбербанк", "company": "Сбербанк",
                "description": "Превратил Сбербанк из традиционного банка в технологическую компанию. Связывает IT и государственные структуры.",
                "prediction": "Сбербанк станет полноценной IT-корпорацией с фокусом на AI и big data.",
                "key_relationships": ["Все IT-компании, работающие со Сбером", "Артем Инютин", "Аркадий Волож"],
                "graph_role": "Мост государство и IT"
            }
        ]

        for data in people_data:
            person = Person(**data)
            self.people.append(person)

    def load_ads(self):
        """Загружает рекламные материалы."""
        self.ads_data = [
            {
                "id": "contrast",
                "type": "image",
                "surface": self.load_ad_image("contrast")
            },
            {
                "id": "rock_band",
                "type": "image",
                "surface": self.load_ad_image("rock_band")
            },
            {
                "id": "your_ad",
                "type": "placeholder"
            }
        ]

    def load_ad_image(self, ad_name):
        """Загружает рекламное изображение."""
        try:
            image_path = ADS_PATHS.get(ad_name)
            if image_path and image_path != "placeholder" and os.path.exists(image_path):
                image = pygame.image.load(image_path)
                return pygame.transform.scale(image, (240, 100))
        except Exception as e:
            print(f"Ошибка загрузки рекламы {ad_name}: {e}")
        return None

    def calculate_all_connections(self):
        """Вычисляет все связи между людьми."""
        print("Вычисление автоматических связей...")

        for i, person1 in enumerate(self.people):
            person1.connections = []
            person1.connection_weights = {}

            for j, person2 in enumerate(self.people):
                if i == j:
                    continue

                weight = calculate_connection_weight(person1, person2)
                person1.connection_weights[person2.name] = weight

                if weight >= self.connection_threshold:
                    person1.connections.append(person2.name)

            print(f"{person1.name}: {len(person1.connections)} связей")

    def find_person_by_name(self, name):
        """Находит человека по имени."""
        for person in self.people:
            if person.name == name:
                return person
        return None

    def get_connected_people(self, person):
        """Возвращает список связанных людей."""
        connected = []
        for connection_name in person.connections:
            connected_person = self.find_person_by_name(connection_name)
            if connected_person:
                weight = person.connection_weights.get(connection_name, 0)
                connected.append((connected_person, weight))

        connected.sort(key=lambda x: x[1], reverse=True)
        return connected

    def draw_background(self):
        """Отрисовывает фон."""
        background = load_background()
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(LIGHT_GRAY)

    def draw_detail_screen(self):
        """Отрисовывает экран детальной информации."""
        if not self.selected_person:
            return

        person = self.selected_person
        connected_people = self.get_connected_people(person)

        self.draw_background()

        # Центрируем окно
        content_width = min(1200, WIDTH - 160)
        content_height = HEIGHT - 160
        content_x = (WIDTH - content_width) // 2
        content_y = 80

        content_rect = pygame.Rect(content_x, content_y, content_width, content_height)
        pygame.draw.rect(self.screen, WHITE, content_rect)
        pygame.draw.rect(self.screen, BLACK, content_rect, 2)

        # Кнопка "Назад"
        back_button = pygame.Rect(content_x + 20, content_y + 20, 100, 40)
        pygame.draw.rect(self.screen, BLUE, back_button)
        back_text = FONT_MEDIUM.render("Назад", True, WHITE)
        text_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, text_rect)

        # Внутренние отступы
        inner_margin = 40
        info_x = content_x + inner_margin
        info_y = content_y + 100

        photo_rect = pygame.Rect(info_x, info_y, 180, 180)
        if person.photo_large is not None:
            self.screen.blit(person.photo_large, photo_rect)
        else:
            pygame.draw.rect(self.screen, GRAY, photo_rect)

        text_x = info_x + 200

        name_text = FONT_LARGE.render(person.name, True, BLACK)
        self.screen.blit(name_text, (text_x, info_y))

        age_text = FONT_MEDIUM.render(f"Возраст: {person.age}", True, BLACK)
        self.screen.blit(age_text, (text_x, info_y + 40))

        profession_text = FONT_MEDIUM.render(f"Профессия: {person.profession}", True, BLACK)
        self.screen.blit(profession_text, (text_x, info_y + 70))

        company_text = FONT_MEDIUM.render(f"Компания: {person.company}", True, BLUE)
        self.screen.blit(company_text, (text_x, info_y + 100))

        role_text = FONT_MEDIUM.render(f"Роль в сети: {person.graph_role}", True, GREEN)
        self.screen.blit(role_text, (text_x, info_y + 130))

        conn_count_text = FONT_MEDIUM.render(f"Автоматических связей: {len(person.connections)}", True, PURPLE)
        self.screen.blit(conn_count_text, (text_x, info_y + 160))

        # Ширина текста с учетом внутренних отступов
        text_width = content_width - 2 * inner_margin - 200

        desc_y = info_y + 200
        desc_title = FONT_MEDIUM.render("Описание:", True, BLACK)
        self.screen.blit(desc_title, (info_x, desc_y))

        desc_lines = wrap_text(person.description, FONT_SMALL, text_width)
        for i, line in enumerate(desc_lines):
            desc_line = FONT_SMALL.render(line, True, BLACK)
            self.screen.blit(desc_line, (info_x, desc_y + 30 + i * 25))

        conn_y = desc_y + 30 + len(desc_lines) * 25 + 20
        conn_title = FONT_MEDIUM.render("Автоматически найденные связи:", True, BLACK)
        self.screen.blit(conn_title, (info_x, conn_y))

        connection_buttons = []
        button_x = info_x
        button_y = conn_y + 30

        for connected_person, weight in connected_people:
            # Проверяем, помещается ли кнопка в текущей строке
            max_button_x = content_x + content_width - inner_margin - 240
            if button_x > max_button_x:
                button_x = info_x
                button_y += 40

            connection_color = get_connection_strength_color(weight)

            conn_button = pygame.Rect(button_x, button_y, 240, 30)
            pygame.draw.rect(self.screen, connection_color, conn_button)

            conn_text = FONT_SMALL.render(f"{connected_person.name} ({weight:.1f})", True, WHITE)
            text_rect = conn_text.get_rect(center=conn_button.center)
            self.screen.blit(conn_text, text_rect)

            connection_buttons.append((connected_person, conn_button))
            button_x += 250

        pred_y = button_y + 50
        pred_title = FONT_MEDIUM.render("Прогноз развития:", True, BLACK)
        self.screen.blit(pred_title, (info_x, pred_y))

        pred_lines = wrap_text(person.prediction, FONT_SMALL, text_width)
        for i, line in enumerate(pred_lines):
            pred_line = FONT_SMALL.render(line, True, BLACK)
            self.screen.blit(pred_line, (info_x, pred_y + 30 + i * 25))

        return back_button, connection_buttons

    def search_people(self):
        """Выполняет поиск людей."""
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
        """Главный цикл приложения."""
        running = True
        detail_buttons = []
        pagination_buttons = []
        connection_buttons = []

        while running:
            self.draw_background()

            if self.active_screen == "main":
                search_button = self.ui.draw_search_bar(self.search_text)

                start_index = self.current_page * self.people_per_page
                end_index = start_index + self.people_per_page
                current_people = self.filtered_people[start_index:end_index]

                detail_buttons = []
                for i, person in enumerate(current_people):
                    card_y = 120 + i * 120
                    card_width = min(900, WIDTH - 100)
                    detail_button = self.ui.draw_person_card(person, 50, card_y, card_width, 110)
                    detail_buttons.append((person, detail_button))

                # Отрисовываем рекламу
                self.ads_buttons = self.ui.draw_ads_panel(self.ads_data)

                total_pages = (len(self.filtered_people) + self.people_per_page - 1) // self.people_per_page
                pagination_buttons = self.ui.draw_pagination(self.current_page, total_pages)

            elif self.active_screen == "detail":
                back_button, connection_buttons = self.draw_detail_screen()
                pagination_buttons = [("back", back_button)]

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
                        search_button = self.ui.draw_search_bar(self.search_text)
                        if search_button.collidepoint(mouse_pos):
                            self.search_people()

                        for person, button in detail_buttons:
                            if button.collidepoint(mouse_pos):
                                self.selected_person = person
                                self.active_screen = "detail"

                        # Обработка кликов по рекламе
                        for ad_id, ad_rect in self.ads_buttons:
                            if ad_rect.collidepoint(mouse_pos):
                                print(f"Клик по рекламе: {ad_id}")

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

                        for connected_person, conn_button in connection_buttons:
                            if conn_button.collidepoint(mouse_pos):
                                self.selected_person = connected_person

            pygame.display.flip()

        pygame.quit()