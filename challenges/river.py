"""River challenge for Threads of Home."""

import math
import random
import pygame

from settings import CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY, DARK_GREY, BLUE
from ui import draw_text, draw_wrapped_text, draw_button


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
            },
            {
                "heading": "Padma, Jamuna, Meghna",
                "body": (
                    "In this challenge, you will follow three major river names: Padma, Jamuna, and Meghna. "
                    "Think about rivers as paths that connect people, food, travel, land, and culture."
                ),
            },
        ]

        self.steps = [
            {
                "prompt": "This river is strongly connected with Hilsa fish and food culture. Which river is it?",
                "answer": "Padma",
                "note": "The Padma is strongly connected with Hilsa fish, which is an important part of Bangladeshi food culture.",
            },
            {
                "prompt": "This river is very wide and powerful. It changes land, creates chars, and affects how people live near it. Which river is it?",
                "answer": "Jamuna",
                "note": "The Jamuna is a large river system. It can shape land and create river islands called chars.",
            },
            {
                "prompt": "This river is connected with many waterways and helps carry water toward the Bay of Bengal. Which river is it?",
                "answer": "Meghna",
                "note": "The Meghna is a major river connected with water routes and the flow toward the Bay of Bengal.",
            },
        ]

        self.options = ["Padma", "Jamuna", "Meghna"]
        self.reset()

    def reset(self):
        self.mode = "lesson"
        self.lesson_index = 0
        self.current_step = 0
        self.completed = False
        self.message = self.lesson_pages[0]["body"]
        self.success_particles = []
        self.completed_answers = []

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
                "colour": random.choice([WHITE, GREEN, YELLOW, BLUE]),
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

    def draw_lesson(self, screen, fonts):
        screen.fill(CREAM)
        page = self.lesson_pages[self.lesson_index]

        draw_text(screen, "River", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learn first, then guide the boat.", fonts["small"], BROWN, 500, 105, center=True)

        card = pygame.Rect(105, 145, 790, 380)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)
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

        back_button = draw_button(screen, "Back to Map", fonts["body"], 235, 610, 210, 55, GREY)
        next_text = "Start Challenge" if self.lesson_index == len(self.lesson_pages) - 1 else "Next"
        next_button = draw_button(screen, next_text, fonts["body"], 555, 610, 210, 55, GREEN, WHITE)

        return {"back": back_button, "next": next_button}

    def draw_instruction_panel(self, screen, fonts):
        panel = pygame.Rect(65, 70, 870, 105)
        pygame.draw.rect(screen, WHITE, panel, border_radius=16)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=16)

        heading = "Journey complete" if self.completed else f"River step {self.current_step + 1} of {len(self.steps)}"
        draw_text(screen, heading, fonts["small"], BROWN, panel.x + 20, panel.y + 12)
        draw_wrapped_text(screen, self.message, fonts["small"], DARK, panel.x + 20, panel.y + 42, panel.width - 40)

    def draw_river_scene(self, screen, fonts):
        """Draw a river story board instead of a random boat journey."""
        scene = pygame.Rect(80, 195, 840, 220)
        pygame.draw.rect(screen, (205, 232, 242), scene, border_radius=18)
        pygame.draw.rect(screen, DARK, scene, width=3, border_radius=18)

        draw_text(
            screen,
            "River Story Board",
            fonts["heading"],
            BROWN,
            scene.centerx,
            scene.y + 32,
            center=True,
        )

        river_cards = [
            {
                "name": "Padma",
                "story": "Hilsa fish and food culture",
                "icon": "fish",
                "x": scene.x + 150,
            },
            {
                "name": "Jamuna",
                "story": "Wide river and changing land",
                "icon": "char",
                "x": scene.x + 420,
            },
            {
                "name": "Meghna",
                "story": "Waterways to the Bay of Bengal",
                "icon": "waves",
                "x": scene.x + 690,
            },
        ]

        for card in river_cards:
            unlocked = card["name"] in self.completed_answers

            card_rect = pygame.Rect(card["x"] - 105, scene.y + 75, 210, 120)

            fill_colour = (230, 245, 250) if unlocked else (220, 225, 225)
            border_colour = GREEN if unlocked else DARK_GREY

            pygame.draw.rect(screen, fill_colour, card_rect, border_radius=16)
            pygame.draw.rect(screen, border_colour, card_rect, width=3, border_radius=16)

            draw_text(
                screen,
                card["name"],
                fonts["body"],
                DARK,
                card_rect.centerx,
                card_rect.y + 24,
                center=True,
            )

            if unlocked:
                self.draw_river_icon(screen, card["icon"], card_rect.centerx, card_rect.y + 68)
                draw_text(
                    screen,
                    card["story"],
                    fonts["tiny"],
                    DARK,
                    card_rect.centerx,
                    card_rect.bottom - 18,
                    center=True,
                )
            else:
                draw_text(
                    screen,
                    "Story locked",
                    fonts["small"],
                    DARK_GREY,
                    card_rect.centerx,
                    card_rect.y + 72,
                    center=True,
                )

    def draw_river_icon(self, screen, icon_type, x, y):
        """Draw simple icons for each river story."""
        if icon_type == "fish":
            # fish body
            pygame.draw.ellipse(screen, BLUE, (x - 32, y - 14, 52, 28))
            pygame.draw.polygon(screen, BLUE, [
                (x + 18, y),
                (x + 42, y - 16),
                (x + 42, y + 16),
            ])
            pygame.draw.circle(screen, WHITE, (x - 18, y - 4), 5)
            pygame.draw.circle(screen, DARK, (x - 18, y - 4), 2)

        elif icon_type == "char":
            # river island / char
            pygame.draw.ellipse(screen, (190, 150, 90), (x - 45, y + 5, 90, 24))
            pygame.draw.polygon(screen, GREEN, [
                (x - 20, y + 5),
                (x - 6, y - 25),
                (x + 8, y + 5),
            ])
            pygame.draw.polygon(screen, GREEN, [
                (x + 8, y + 5),
                (x + 22, y - 20),
                (x + 35, y + 5),
            ])

        elif icon_type == "waves":
            # flowing water
            for i in range(3):
                points = []
                wave_y = y - 18 + i * 16
                for px in range(x - 45, x + 50, 12):
                    py = wave_y + int(5 * math.sin(px * 0.12))
                    points.append((px, py))
                pygame.draw.lines(screen, BLUE, False, points, 4)


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

    def draw_puzzle(self, screen, fonts):
        screen.fill(CREAM)
        draw_text(screen, "River", fonts["title"], DARK, 500, 35, center=True)
        self.draw_instruction_panel(screen, fonts)
        self.draw_river_scene(screen, fonts)

        card_rects = {}
        start_x = 190
        for i, option in enumerate(self.options):
            rect = pygame.Rect(start_x + i * 210, 455, 180, 90)
            card_rects[option] = rect
            self.draw_choice_card(screen, fonts, option, rect)

        self.draw_particles(screen)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 190, 615, 210, 50, GREY)
        reset_button = draw_button(screen, "Reset", fonts["body"], 430, 615, 150, 50, YELLOW)

        done_button = None
        if self.completed:
            done_button = draw_button(screen, "Stitch Quilt Section", fonts["body"], 610, 615, 270, 50, GREEN, WHITE)

        return {"cards": card_rects, "back": back_button, "reset": reset_button, "done": done_button}

    def draw(self, screen, fonts):
        if self.mode == "lesson":
            return self.draw_lesson(screen, fonts)
        return self.draw_puzzle(screen, fonts)

    def handle_click(self, mouse_pos, buttons):
        if self.mode == "lesson":
            if buttons["back"].collidepoint(mouse_pos):
                return "back"

            if buttons["next"].collidepoint(mouse_pos):
                if self.lesson_index < len(self.lesson_pages) - 1:
                    self.lesson_index += 1
                    self.message = self.lesson_pages[self.lesson_index]["body"]
                else:
                    self.mode = "puzzle"
                    self.message = self.steps[0]["prompt"]

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

        current = self.steps[self.current_step]

        for option, rect in buttons["cards"].items():
            if rect.collidepoint(mouse_pos):
                if option == current["answer"]:
                    self.completed_answers.append(option)
                    self.add_success_particles(rect.center)
                    self.current_step += 1

                    if self.current_step >= len(self.steps):
                        self.completed = True
                        self.message = (
                            "You completed the river journey! Click on the quilt to watch the rivers come to life."
                        )
                    else:
                        self.message = self.steps[self.current_step]["prompt"]
                else:
                    self.message = (
                        f"Good try. {option} is not the answer for this clue. "
                        "Look at the clue again and choose the river it asks for."
                    )

                return None

        return None