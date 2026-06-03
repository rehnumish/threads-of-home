"""Symbols challenge for Threads of Home.

This version uses separate quiz pages:
- each page teaches one symbol
- each page has multiple similar options
- the player chooses the correct one
"""

import random
import pygame

from settings import CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY, DARK_GREY, ORANGE, RED, BLUE
from ui import draw_text, draw_wrapped_text, draw_button


class SymbolsChallenge:
    """Learn about symbols of Bangladesh through separate quiz pages."""

    def __init__(self):
        self.lesson_pages = [
            {
                "heading": "What Is a Symbol?",
                "body": (
                    "A symbol is something small that can stand for a bigger idea. "
                    "A flower, animal, fish, flag, or map can remind people of a country. "
                    "Symbols help people remember a place, even when they live far away from it."
                ),
            },
            {
                "heading": "National Flower",
                "body": (
                    "The Shapla, or White Water Lily, is the national flower of Bangladesh and can be seen floating beautifully on ponds, "
                    "lakes, and rivers across the country. It blooms in water, which perfectly represents Bangladesh as a land of rivers and "
                    "water bodies. The Shapla is a symbol of purity, simplicity, and natural beauty. It is even featured on the national emblem "
                    "of Bangladesh, showing how important it is to the nation."
                ),
                },
            {
                "heading": "National Animal",
                "body": (
                    "The Royal Bengal Tiger is strongly connected with the Sundarbans. The Royal Bengal Tiger is the national animal of Bangladesh and "
                    "is one of the most powerful and majestic animals in the world. It lives in the Sundarbans, the world's largest mangrove forest"
                    " shared by Bangladesh and India. The tiger represents strength, courage, and pride, which are values the people of Bangladesh hold dear."
                    " It is an endangered species, meaning there are very few left, so Bangladesh works hard to protect them. "
                    
                ),
                },
            {
                "heading": "National Fish",
                "body": (
                    "The Hilsha, or Ilish, is the national fish of Bangladesh and is loved by almost every Bangladeshi family. It is found mainly in the rivers"
                    " like the Padma and Meghna, and is famous for its delicious taste. Hilsha represents the river culture of Bangladesh, as the country is "
                    "crisscrossed by hundreds of rivers. Every year, catching and eating Hilsha is a big part of festivals and daily life. "
                ),
               },
            {
                "heading": "National Bird",
                "body": (
                    "The Doyel, or Oriental Magpie Robin, is the national bird of Bangladesh and is known for its sweet and melodious singing. It is a small but"
                    " beautiful black and white bird that can be found in gardens, parks, forests, and villages all across the country. The Doyel sings most"
                    " beautifully in the early morning, and its cheerful song represents the joy and liveliness of the people of Bangladesh. It is so loved by the"
                    " nation that it is featured on Bangladeshi currency notes. "
                ),
               },

            {
                "heading": "National Flag",
                "body": (
                    "A flag represents a country. "
                    "The flag of Bangladesh has a green field referring to the natural greenery of this monsoon land and a red circle, "
                    "referring to the the rising sun over Bengal, as well as the blood shed by the Bengalis who died fighting for the "
                    "country's independence during the 1971 Liberation War. The red disc is deliberately placed slightly off-center (toward the pole side)."
                ),
               },
            
            {
                "heading": "Your Mission",
                "body": (
                    "You will answer one quiz page at a time. "
                    "Each page will teach you about one symbol, then give you several options. "
                    "Choose the correct option to unlock that symbol on the board."
                ),
            },
        ]

        self.quiz_pages = [
    {
        "heading": "National Flower",
        "question": "Which one is Shapla, the national flower of Bangladesh?",
        "answer": "Waterlily",
        "options": ["Marigold","Lotus", "Waterlily", "Rose", "Sunflower"],
        "note": "Correct. Shapla is the national flower of Bangladesh.",
    },
    {
        "heading": "Royal Bengal Tiger",
        "question": "Which animal is the Royal Bengal Tiger?",
        "answer": "Royal Bengal Tiger",
        "options": ["Elephant", "Royal Bengal Tiger", "Deer", "Lion", "Crocodile"],
        "note": "Correct. The Royal Bengal Tiger is connected with the Sundarbans and strength.",
    },
    {
        "heading": "National Fish",
        "question": "Which fish is the national fish of Bangladesh?",
        "answer": "Hilsa",
        "options": ["Rohu", "Salmon", "Anchovy", "Hilsa", "Catfish"],
        "note": "Correct. Hilsa is the national fish of Bangladesh.",
    },
    {
        "heading": "National Flag",
        "question": "Which option represents the flag of Bangladesh?",
        "answer": "Bangladesh Flag",
        "options": ["Bangladesh Flag", "Japan Flag", "Pakistan Flag", "India Flag", "Nepal Flag"],
        "note": "Correct. The Bangladesh flag represents the country.",
    },
    {
        "heading": "National Bird of Bangladesh",
        "question": "Which option shows the national bird of Bangladesh?",
        "answer": "Doyel",
        "options": ["Kingfisher", "Doyel", "Asian Koel", "Myna", "Cockatoo"],
        "note": "Correct. The map shows the shape and place of Bangladesh.",
    },
]

        self.reset()

    def reset(self):
        self.mode = "lesson"
        self.lesson_index = 0
        self.current_quiz = 0
        self.completed = False
        self.message = self.lesson_pages[0]["body"]
        self.success_particles = []
        self.unlocked_symbols = []
        self.feedback = ""

    def update(self):
        for p in self.success_particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["dy"] += 0.12
            p["life"] -= 1

        self.success_particles = [p for p in self.success_particles if p["life"] > 0]

    def add_success_particles(self, centre):
        for _ in range(24):
            self.success_particles.append({
                "x": centre[0],
                "y": centre[1],
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-4, -1),
                "life": random.randint(24, 42),
                "colour": random.choice([WHITE, GREEN, YELLOW, ORANGE, RED]),
            })

    def draw_particles(self, screen):
        for p in self.success_particles:
            pygame.draw.circle(screen, p["colour"], (int(p["x"]), int(p["y"])), 4)

    def draw_centered_wrapped_text(self, screen, text, font, colour, center_x, y, max_width, line_gap=8, paragraph_gap=14):
        """Draw wrapped text centered line by line, supporting paragraph breaks."""
        paragraphs = text.split("\n")
        current_y = y

        for paragraph in paragraphs:
            paragraph = paragraph.strip()

            if paragraph == "":
                current_y += paragraph_gap
                continue

            words = paragraph.split()
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

            for line in lines:
                draw_text(screen, line, font, colour, center_x, current_y, center=True)
                current_y += font.get_height() + line_gap

            current_y += paragraph_gap

        return current_y

    def draw_lesson(self, screen, fonts):
        screen.fill(CREAM)
        page = self.lesson_pages[self.lesson_index]

        draw_text(screen, "Symbols", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learn first, then answer symbol quizzes.", fonts["small"], BROWN, 500, 105, center=True)

        card = pygame.Rect(95, 135, 890, 400)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)

        self.draw_centered_wrapped_text(
            screen,
            page["body"],
            fonts["body"],
            DARK,
            card.centerx,
            card.y + 115,
            card.width - 90,
            line_gap=10,
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
        next_text = "Start Quiz" if self.lesson_index == len(self.lesson_pages) - 1 else "Next"
        next_button = draw_button(screen, next_text, fonts["body"], 555, 610, 210, 55, GREEN, WHITE)

        return {"back": back_button, "next": next_button}

    def draw_symbol_board(self, screen, fonts):
        board = pygame.Rect(65, 105, 870, 90)
        pygame.draw.rect(screen, (230, 244, 225), board, border_radius=18)
        pygame.draw.rect(screen, DARK, board, width=3, border_radius=18)

        labels = ["Shapla", "Tiger", "Hilsa", "Flag", "Map"]

        for i, label in enumerate(labels):
            x = board.x + 95 + i * 170
            unlocked = i < len(self.unlocked_symbols)

            fill = GREEN if unlocked else (210, 210, 210)
            pygame.draw.circle(screen, fill, (x, board.y + 45), 30)
            pygame.draw.circle(screen, DARK, (x, board.y + 45), 30, 2)

            text = label if unlocked else "?"
            draw_text(screen, text, fonts["tiny"], DARK, x, board.y + 45, center=True)

    

    def draw_option_card(self, screen, fonts, text, rect):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)

        fill = (255, 245, 210) if hovered else WHITE

        pygame.draw.rect(screen, fill, rect, border_radius=16)
        pygame.draw.rect(screen, GREEN if hovered else DARK, rect, width=3, border_radius=16)

        self.draw_centered_wrapped_text(
            screen,
            text,
            fonts["small"],
            DARK,
            rect.centerx,
            rect.y + 18,
            rect.width - 20,
            line_gap=4,
            paragraph_gap=0,
        )

    def draw_question_panel(self, screen, fonts, quiz):
    
        panel = pygame.Rect(80, 225, 840, 150)
        pygame.draw.rect(screen, WHITE, panel, border_radius=18)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=18)

        draw_text(
            screen,
            quiz["heading"],
            fonts["heading"],
            BROWN,
            panel.centerx,
            panel.y + 38,
            center=True,
        )

        self.draw_centered_wrapped_text(
            screen,
            quiz["question"],
            fonts["body"],
            DARK,
            panel.centerx,
            panel.y + 90,
            panel.width - 80,
            line_gap=8,
            paragraph_gap=0,
        )


    def draw_puzzle(self, screen, fonts):
        screen.fill(CREAM)

        draw_text(screen, "Symbols", fonts["title"], DARK, 500, 35, center=True)

        self.draw_symbol_board(screen, fonts)

        if self.completed:
            final_card = pygame.Rect(115, 230, 770, 230)
            pygame.draw.rect(screen, WHITE, final_card, border_radius=20)
            pygame.draw.rect(screen, DARK, final_card, width=3, border_radius=20)

            draw_text(
                screen,
                "Symbols complete",
                fonts["heading"],
                BROWN,
                final_card.centerx,
                final_card.y + 55,
                center=True,
            )

            self.draw_centered_wrapped_text(
                screen,
                "You completed the symbols section. Symbols help people remember a place, its nature, its stories, and its identity.",
                fonts["body"],
                DARK,
                final_card.centerx,
                final_card.y + 120,
                final_card.width - 90,
                line_gap=10,
            )

            self.draw_particles(screen)

            back_button = draw_button(screen, "Back to Map", fonts["body"], 190, 615, 210, 50, GREY)
            reset_button = draw_button(screen, "Reset", fonts["body"], 430, 615, 150, 50, YELLOW)
            done_button = draw_button(screen, "Stitch Quilt Section", fonts["body"], 610, 615, 270, 50, GREEN, WHITE)

            return {
                "cards": {},
                "back": back_button,
                "reset": reset_button,
                "done": done_button,
            }

        quiz = self.quiz_pages[self.current_quiz]

        draw_text(
            screen,
            f"Quiz page {self.current_quiz + 1} of {len(self.quiz_pages)}",
            fonts["small"],
            DARK_GREY,
            500,
            200,
            center=True,
        )

        self.draw_question_panel(screen, fonts, quiz)

        card_rects = {}

        start_x = 95
        start_y = 410
        card_w = 160
        card_h = 90
        gap = 18

        for i, option in enumerate(quiz["options"]):
            x = start_x + i * (card_w + gap)
            rect = pygame.Rect(x, start_y, card_w, card_h)

            self.draw_option_card(screen, fonts, option, rect)

            card_rects[option] = rect

        if self.feedback:
            self.draw_centered_wrapped_text(
                screen,
                self.feedback,
                fonts["small"],
                BROWN,
                500,
                525,
                780,
                line_gap=6,
            )

        self.draw_particles(screen)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 190, 615, 210, 50, GREY)
        reset_button = draw_button(screen, "Reset", fonts["body"], 430, 615, 150, 50, YELLOW)

        return {
            "cards": card_rects,
            "back": back_button,
            "reset": reset_button,
            "done": None,
        }

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
                    self.feedback = ""

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

        quiz = self.quiz_pages[self.current_quiz]

        for option, rect in buttons["cards"].items():
            if rect.collidepoint(mouse_pos):
                if option == quiz["answer"]:
                    self.add_success_particles(rect.center)
                    self.unlocked_symbols.append(quiz["answer"])
                    self.feedback = quiz["note"]

                    self.current_quiz += 1

                    if self.current_quiz >= len(self.quiz_pages):
                        self.completed = True
                    else:
                        self.feedback = ""

                else:
                    self.feedback = (
                        f"Good try. {option} is not the correct answer for this page. "
                        "Read the clue again and choose another option."
                    )

                return None

        return None