"""River challenge for Threads of Home."""

import random
import webbrowser
import pygame

from settings import CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY, DARK_GREY
from ui import draw_text, draw_button


class RiverChallenge:
    """Learn about Bangladesh's river culture through a boat route challenge."""

    def __init__(self):
        self.lesson_pages = [
            {
                "heading": "Bangladesh and Rivers",
                "body": (
                    "Rivers are a big part of life in Bangladesh. They are not just water in the background. "
                    "Rivers help shape where people live, how people travel, how crops grow, and how families "
                    "find food. Many stories, songs, and memories are connected to river life."
                ),
                "wiki": "https://en.wikipedia.org/wiki/List_of_rivers_of_Bangladesh",
            },
            {
                "heading": "The Lifelines of Bangladesh",
                "body": (
                    "The mighty Padma river is home to the beloved hilsa fish, which fishermen have caught "
                    "for generations to feed their families and sell at market. The wide Meghna river flows "
                    " south until it meets the great Bay of Bengal, carrying the waters of many rivers with it "
                    "to the sea. The restless Jamuna river shifts and changes course every year, reshaping the "
                    "land and the lives of the people who live on its banks."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Padma_River",
            },
            {
                "heading": "Padma, Jamuna, Meghna",
                "body": (
                    "In this challenge, you will follow three major river names: Padma, Jamuna, and Meghna. "
                    "Think about rivers as paths that connect people, food, travel, land, and culture."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Jamuna_River_(Bangladesh)",
            },
        ]

        self.options = ["Padma", "Jamuna", "Meghna"]
        self.river_wikis = {
            "Padma": "https://en.wikipedia.org/wiki/Padma_River",
            "Jamuna": "https://en.wikipedia.org/wiki/Jamuna_River_(Bangladesh)",
            "Meghna": "https://en.wikipedia.org/wiki/Meghna_River",
        }
        self.river_photo = None
        self.card_photos = {}
        self.reset()

    def reset(self):
        self.mode = "lesson"
        self.lesson_index = 0
        self.current_step = 0
        self.completed = False
        self.message = self.lesson_pages[0]["body"]
        self.success_particles = []
        self.completed_answers = []
        self.dragging_option = None
        self.drag_offset = (0, 0)
        self.shuffled_options = self.options[:]
        random.shuffle(self.shuffled_options)

    def update(self):
        for particle in self.success_particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.12
            particle["life"] -= 1

        self.success_particles = [p for p in self.success_particles if p["life"] > 0]

    def add_success_particles(self, centre):
        for _ in range(24):
            self.success_particles.append({
                "x": centre[0],
                "y": centre[1],
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-4, -1),
                "life": random.randint(24, 42),
                "colour": random.choice([WHITE, GREEN, YELLOW, DARK_GREY]),
            })

    def draw_particles(self, screen):
        for p in self.success_particles:
            pygame.draw.circle(screen, p["colour"], (int(p["x"]), int(p["y"])), 4)

    def draw_centered_wrapped_text(self, screen, text, font, colour, center_x, y, max_width, line_gap=8):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        current_y = y
        for line in lines:
            draw_text(screen, line, font, colour, center_x, current_y, center=True)
            current_y += font.get_height() + line_gap

    def load_river_photo(self):
        if self.river_photo is not None:
            return self.river_photo

        try:
            image = pygame.image.load("assets/river/river.webp").convert_alpha()
            image = pygame.transform.smoothscale(image, (360, 260))
            self.river_photo = image
            return image
        except (pygame.error, FileNotFoundError):
            return None

    def load_card_photo(self, filename):
        if filename in self.card_photos:
            return self.card_photos[filename]

        try:
            image = pygame.image.load("assets/river/" + filename).convert_alpha()
            image = pygame.transform.smoothscale(image, (190, 100))
            self.card_photos[filename] = image
            return image
        except (pygame.error, FileNotFoundError):
            return None

    def draw_lesson(self, screen, fonts):
        screen.fill(CREAM)
        page = self.lesson_pages[self.lesson_index]

        draw_text(screen, "River", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Match river name to the correct photo.", fonts["small"], BROWN, 500, 105, center=True)

        card = pygame.Rect(105, 145, 790, 380)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)

        if self.lesson_index == 2:
            photo = self.load_river_photo()
            photo_rect = pygame.Rect(card.centerx - 180, card.y + 125, 360, 260)

            self.draw_centered_wrapped_text(
                screen, page["body"], fonts["small"], DARK,
                card.centerx, card.y + 90, card.width - 90, line_gap=4
            )

            if photo is not None:
                pygame.draw.rect(screen, (225, 240, 245), photo_rect, border_radius=16)
                pygame.draw.rect(screen, DARK, photo_rect, width=3, border_radius=16)
                screen.blit(photo, photo_rect.topleft)
        else:
            self.draw_centered_wrapped_text(
                screen, page["body"], fonts["body"], DARK,
                card.centerx, card.y + 115, card.width - 90, line_gap=10
            )

        draw_text(
            screen,
            f"Learning page {self.lesson_index + 1} of {len(self.lesson_pages)}",
            fonts["small"],
            DARK_GREY,
            500,
            550,
            center=True,
        )

        back_button = draw_button(screen, "Back to Map", fonts["small"], 60, 610, 150, 55, GREY)
        padma_button = draw_button(screen, "Padma Wiki", fonts["small"], 230, 610, 140, 55, YELLOW)
        jamuna_button = draw_button(screen, "Jamuna Wiki", fonts["small"], 390, 610, 150, 55, YELLOW)
        meghna_button = draw_button(screen, "Meghna Wiki", fonts["small"], 560, 610, 150, 55, YELLOW)
        next_text = "Start Challenge" if self.lesson_index == len(self.lesson_pages) - 1 else "Next"
        next_button = draw_button(screen, next_text, fonts["small"], 735, 610, 170, 55, GREEN, WHITE)

        return {
            "back": back_button,
            "padma": padma_button,
            "jamuna": jamuna_button,
            "meghna": meghna_button,
            "next": next_button,
        }

    def draw_river_scene(self, screen, fonts):
        """Draw a river story board instead of a random boat journey."""
        scene = pygame.Rect(50, 140, 900, 310)
        pygame.draw.rect(screen, (205, 232, 242), scene, border_radius=18)
        pygame.draw.rect(screen, DARK, scene, width=3, border_radius=18)

        draw_text(
            screen,
            "River Story Board",
            fonts["heading"],
            BROWN,
            scene.centerx,
            scene.y + 30,
            center=True,
        )

        river_cards = [
            {
                "name": "Padma",
                "story": "Hilsa fish and food culture.",
                "photo": "padma_hilsa.jpg",
                "x": scene.x + 150,
            },
            {
                "name": "Jamuna",
                "story": "Wide river and changing land.",
                "photo": "jamuna_island.jpg",
                "x": scene.x + 420,
            },
            {
                "name": "Meghna",
                "story": "Waterways to the Bay of Bengal.",
                "photo": "meghna_estuary.jpg",
                "x": scene.x + 690,
            },
        ]

        target_rects = {}

        for card in river_cards:
            unlocked = card["name"] in self.completed_answers

            card_rect = pygame.Rect(card["x"] - 105, scene.y + 70, 210, 120)
            target_rects[card["name"]] = card_rect

            fill_colour = (230, 245, 250) if unlocked else (220, 225, 225)
            border_colour = GREEN if unlocked else DARK_GREY

            pygame.draw.rect(screen, fill_colour, card_rect, border_radius=16)
            pygame.draw.rect(screen, border_colour, card_rect, width=3, border_radius=16)

            photo = self.load_card_photo(card["photo"])

            if photo is not None:
                photo_rect = photo.get_rect(center=card_rect.center)
                screen.blit(photo, photo_rect)

            clue_rect = pygame.Rect(card_rect.x - 15, card_rect.bottom + 12, card_rect.width + 30, 70)
            self.draw_centered_wrapped_text(
                screen,
                card["story"],
                fonts["small"],
                DARK,
                clue_rect.centerx,
                clue_rect.y,
                clue_rect.width,
                line_gap=4,
            )

        return target_rects

    def draw_choice_card(self, screen, fonts, text, rect):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        done = text in self.completed_answers

        fill = (210, 242, 215) if done else ((255, 245, 210) if hovered else WHITE)

        pygame.draw.rect(screen, fill, rect, border_radius=16)
        pygame.draw.rect(screen, GREEN if hovered else DARK, rect, width=3, border_radius=16)

        draw_text(screen, text, fonts["body"], DARK, rect.centerx, rect.centery, center=True)

        if done:
            draw_text(screen, "DONE", fonts["tiny"], GREEN, rect.centerx, rect.bottom - 12, center=True)

    def choice_home_rect(self, index):
        start_x = 190
        return pygame.Rect(start_x + index * 210, 475, 180, 80)

    def correct_drop(self, option, target_name, target_rect):
        if option == target_name:
            self.completed_answers.append(option)
            self.add_success_particles(target_rect.center)
            self.current_step = len(self.completed_answers)

            if len(self.completed_answers) >= len(self.options):
                self.completed = True
                self.message = "You matched all three rivers."
            else:
                self.message = "Correct. Match another river name to its photo."
        else:
            self.message = "Good try. " + option + " does not match that photo."

    def draw_puzzle(self, screen, fonts):
        screen.fill(CREAM)
        draw_text(screen, "River", fonts["title"], DARK, 500, 35, center=True)
        draw_text(screen, "Match river name to the correct photo.", fonts["small"], BROWN, 500, 88, center=True)
        target_rects = self.draw_river_scene(screen, fonts)

        card_rects = {}
        for i, option in enumerate(self.shuffled_options):
            rect = self.choice_home_rect(i)

            if option == self.dragging_option:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rect = pygame.Rect(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1], 180, 90)

            card_rects[option] = rect
            self.draw_choice_card(screen, fonts, option, rect)

        self.draw_particles(screen)

        if self.message != "":
            draw_text(screen, self.message, fonts["small"], BROWN, 500, 575, center=True)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 190, 615, 210, 50, GREY)
        reset_button = draw_button(screen, "Reset", fonts["body"], 430, 615, 150, 50, YELLOW)

        done_button = None
        if self.completed:
            done_button = draw_button(screen, "Stitch Quilt Section", fonts["body"], 610, 615, 270, 50, GREEN, WHITE)

        return {
            "cards": card_rects,
            "targets": target_rects,
            "back": back_button,
            "reset": reset_button,
            "done": done_button,
        }

    def draw(self, screen, fonts):
        if self.mode == "lesson":
            return self.draw_lesson(screen, fonts)
        return self.draw_puzzle(screen, fonts)

    def handle_click(self, mouse_pos, buttons):
        if self.mode == "lesson":
            if buttons["back"].collidepoint(mouse_pos):
                return "back"

            if buttons["padma"].collidepoint(mouse_pos):
                webbrowser.open(self.river_wikis["Padma"], new=2, autoraise=False)
                return None

            if buttons["jamuna"].collidepoint(mouse_pos):
                webbrowser.open(self.river_wikis["Jamuna"], new=2, autoraise=False)
                return None

            if buttons["meghna"].collidepoint(mouse_pos):
                webbrowser.open(self.river_wikis["Meghna"], new=2, autoraise=False)
                return None

            if buttons["next"].collidepoint(mouse_pos):
                if self.lesson_index < len(self.lesson_pages) - 1:
                    self.lesson_index += 1
                    self.message = self.lesson_pages[self.lesson_index]["body"]
                else:
                    self.mode = "puzzle"
                    self.message = "Drag each river name onto the matching photo."

            return None

        if buttons["back"].collidepoint(mouse_pos):
            return "back"

        if buttons["reset"].collidepoint(mouse_pos):
            self.reset()
            return None

        if self.completed:
            if buttons["done"] is not None and buttons["done"].collidepoint(mouse_pos):
                return "complete"
            return None

        for option, rect in buttons["cards"].items():
            if rect.collidepoint(mouse_pos) and option not in self.completed_answers:
                self.dragging_option = option
                self.drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                return None

        return None

    def handle_release(self, mouse_pos, buttons):
        if self.dragging_option is None:
            return None

        dropped_option = self.dragging_option
        self.dragging_option = None

        for target_name, target_rect in buttons["targets"].items():
            if target_rect.collidepoint(mouse_pos):
                self.correct_drop(dropped_option, target_name, target_rect)
                return None

        self.message = "Drag a river name onto one of the photo cards."
        return None
