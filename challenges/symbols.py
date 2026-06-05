"""Symbols challenge for Threads of Home."""

import random
import webbrowser
import pygame

from settings import CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY, DARK_GREY, ORANGE, RED
from ui import draw_text, draw_button


LESSONS = [
    {
        "heading": "What Is a Symbol?",
        "body": (
            "A symbol is something small that can stand for a bigger idea. "
            "A flower, animal, fish, flag, or bird can remind people of a country. "
            "Symbols help people remember a place, even when they live far away from it."
        ),
        "wiki": "https://en.wikipedia.org/wiki/National_symbols_of_Bangladesh",
    },
    {
        "heading": "National Flower",
        "body": (
            "The Shapla, or White Water Lily, is the national flower of Bangladesh. "
            "It grows in ponds, lakes, and rivers. It shows purity, simplicity, and natural beauty."
        ),
        "wiki": "https://en.wikipedia.org/wiki/Nymphaea_nouchali",
    },
    {
        "heading": "National Animal",
        "body": (
            "The Royal Bengal Tiger is the national animal of Bangladesh. "
            "It is connected with the Sundarbans and represents strength, courage, and pride."
        ),
        "wiki": "https://en.wikipedia.org/wiki/Bengal_tiger",
    },
    {
        "heading": "National Fish",
        "body": (
            "The Hilsa, or Ilish, is the national fish of Bangladesh. "
            "It is found in rivers like the Padma and Meghna and is loved by many Bangladeshi families."
        ),
        "wiki": "https://en.wikipedia.org/wiki/Ilish",
    },
    {
        "heading": "National Bird",
        "body": (
            "The Doyel, or Oriental Magpie Robin, is the national bird of Bangladesh. "
            "It is a small black and white bird known for its sweet song."
        ),
        "wiki": "https://en.wikipedia.org/wiki/Oriental_magpie-robin",
    },
    {
        "heading": "National Flag",
        "body": (
            "The flag of Bangladesh has a green background and a red circle. "
            "The green shows the land and nature. The red circle shows the rising sun and the sacrifice "
            "of people during the 1971 Liberation War."
        ),
        "wiki": "https://en.wikipedia.org/wiki/Flag_of_Bangladesh",
    },
    {
        "heading": "Your Mission",
        "body": (
            "You will answer one quiz page at a time. "
            "Choose the correct option to unlock that symbol on the board."
        ),
        "wiki": "https://en.wikipedia.org/wiki/National_symbols_of_Bangladesh",
    },
]


QUIZZES = [
    {
        "heading": "National Flower",
        "question": "Which one is Shapla, the national flower of Bangladesh?",
        "answer": "Waterlily",
        "options": ["Marigold", "Lotus", "Waterlily", "Rose", "Sunflower"],
        "note": "Correct. Shapla is the national flower of Bangladesh.",
    },
    {
        "heading": "Royal Bengal Tiger",
        "question": "Which one is the national animal of Bangladesh?",
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
        "note": "Correct. Doyel is the national bird of Bangladesh.",
    },
]


SYMBOL_LABELS = ["Shapla", "Tiger", "Hilsa", "Flag", "Bird"]


OPTION_IMAGES = {
    "Marigold": "Marigold.jpg",
    "Lotus": "lotus.webp",
    "Waterlily": "Waterlily.webp",
    "Rose": "rose.jpeg",
    "Sunflower": "sunflower.jpg",
    "Elephant": "elephant.webp",
    "Royal Bengal Tiger": "Tiger.jpg",
    "Deer": "Deer.webp",
    "Lion": "Lion.webp",
    "Crocodile": "Crocodile.jpg",
    "Rohu": "Rohu.jpg",
    "Salmon": "Salmon.jpg",
    "Anchovy": "Anchovy.jpg",
    "Hilsa": "Hilsa.webp",
    "Catfish": "Catfish.jpg",
    "Bangladesh Flag": "Bangladesh_flag.jpg",
    "Japan Flag": "Japan_flag.jpg",
    "Pakistan Flag": "Pakistan_flag.jpg",
    "India Flag": "India_flag.jpg",
    "Nepal Flag": "Nepal_flag.jpg",
    "Kingfisher": "Kingfisher.jpeg",
    "Doyel": "Magpie_robin.jpg",
    "Asian Koel": "Asian_koel.jpg",
    "Myna": "Myna.jpg",
    "Cockatoo": "Cockatoo.jpg",
}


IMAGE_CACHE = {}


def draw_centered_words(screen, text, font, colour, center_x, y, max_width):
    words = text.split()
    line = ""

    for word in words:
        test_line = line + " " + word
        test_line = test_line.strip()

        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            draw_text(screen, line, font, colour, center_x, y, center=True)
            y += font.get_height() + 8
            line = word

    if line != "":
        draw_text(screen, line, font, colour, center_x, y, center=True)
        y += font.get_height() + 8

    return y


def load_symbol_image(option_name, max_width, max_height):
    filename = OPTION_IMAGES.get(option_name)

    if filename is None:
        return None

    key = (filename, max_width, max_height)

    if key in IMAGE_CACHE:
        return IMAGE_CACHE[key]

    try:
        image = pygame.image.load("assets/symbols/" + filename).convert_alpha()
        scale = min(max_width / image.get_width(), max_height / image.get_height())
        new_width = int(image.get_width() * scale)
        new_height = int(image.get_height() * scale)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
        IMAGE_CACHE[key] = image
        return image
    except (pygame.error, FileNotFoundError):
        return None


def draw_symbol_board(screen, fonts, unlocked_count):
    board = pygame.Rect(65, 105, 870, 90)
    pygame.draw.rect(screen, (230, 244, 225), board, border_radius=18)
    pygame.draw.rect(screen, DARK, board, width=3, border_radius=18)

    for i in range(len(SYMBOL_LABELS)):
        x = board.x + 95 + i * 170

        if i < unlocked_count:
            circle_colour = GREEN
            label = SYMBOL_LABELS[i]
        else:
            circle_colour = (210, 210, 210)
            label = "?"

        pygame.draw.circle(screen, circle_colour, (x, board.y + 45), 30)
        pygame.draw.circle(screen, DARK, (x, board.y + 45), 30, 2)
        draw_text(screen, label, fonts["tiny"], DARK, x, board.y + 45, center=True)


def draw_option_card(screen, fonts, option, rect):
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        fill = (255, 245, 210)
        outline = GREEN
    else:
        fill = WHITE
        outline = DARK

    pygame.draw.rect(screen, fill, rect, border_radius=16)
    pygame.draw.rect(screen, outline, rect, width=3, border_radius=16)
    draw_centered_words(screen, option, fonts["small"], DARK, rect.centerx, rect.y + 18, rect.width - 20)


def draw_flag_card(screen, option, rect):
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        fill = (255, 245, 210)
        outline = GREEN
    else:
        fill = WHITE
        outline = DARK

    pygame.draw.rect(screen, fill, rect, border_radius=16)
    pygame.draw.rect(screen, outline, rect, width=3, border_radius=16)

    image = load_symbol_image(option, rect.width - 20, rect.height - 20)

    if image is not None:
        image_rect = image.get_rect(center=rect.center)
        screen.blit(image, image_rect)


def flag_country_name(option):
    if option == "Bangladesh Flag":
        return "Bangladesh"
    if option == "Japan Flag":
        return "Japan"
    if option == "Pakistan Flag":
        return "Pakistan"
    if option == "India Flag":
        return "India"
    if option == "Nepal Flag":
        return "Nepal"
    return "that country"


def draw_hover_photo(screen, fonts, option):
    if option is None:
        return

    image = load_symbol_image(option, 200, 70)

    if image is None:
        return

    preview = pygame.Rect(390, 515, 220, 90)
    pygame.draw.rect(screen, WHITE, preview, border_radius=16)
    pygame.draw.rect(screen, DARK, preview, width=3, border_radius=16)

    image_rect = image.get_rect(center=preview.center)
    screen.blit(image, image_rect)


def draw_particles(screen, particles):
    for particle in particles:
        x = int(particle["x"])
        y = int(particle["y"])
        pygame.draw.circle(screen, particle["colour"], (x, y), 4)


class SymbolsChallenge:
    """Learn about symbols of Bangladesh."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.mode = "lesson"
        self.lesson_index = 0
        self.quiz_index = 0
        self.unlocked_count = 0
        self.completed = False
        self.feedback = ""
        self.particles = []

    def add_particles(self, center):
        for i in range(24):
            particle = {
                "x": center[0],
                "y": center[1],
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-4, -1),
                "life": random.randint(24, 42),
                "colour": random.choice([WHITE, GREEN, YELLOW, ORANGE, RED]),
            }
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.12
            particle["life"] -= 1

        living_particles = []

        for particle in self.particles:
            if particle["life"] > 0:
                living_particles.append(particle)

        self.particles = living_particles

    def draw_lesson(self, screen, fonts):
        page = LESSONS[self.lesson_index]

        screen.fill(CREAM)

        draw_text(screen, "Symbols", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learn first, then answer symbol quizzes.", fonts["small"], BROWN, 500, 105, center=True)

        card = pygame.Rect(95, 135, 890, 400)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)
        draw_centered_words(screen, page["body"], fonts["body"], DARK, card.centerx, card.y + 115, card.width - 90)

        page_number = "Learning page " + str(self.lesson_index + 1) + " of " + str(len(LESSONS))
        draw_text(screen, page_number, fonts["small"], DARK_GREY, 500, 550, center=True)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 130, 610, 190, 55, GREY)
        wiki_button = draw_button(screen, "Wikipedia", fonts["body"], 390, 610, 180, 55, YELLOW)

        if self.lesson_index == len(LESSONS) - 1:
            next_words = "Start Quiz"
        else:
            next_words = "Next"

        next_button = draw_button(screen, next_words, fonts["body"], 650, 610, 190, 55, GREEN, WHITE)

        return {"back": back_button, "wiki": wiki_button, "next": next_button}

    def draw_quiz(self, screen, fonts):
        quiz = QUIZZES[self.quiz_index]

        screen.fill(CREAM)

        draw_text(screen, "Symbols", fonts["title"], DARK, 500, 35, center=True)
        draw_symbol_board(screen, fonts, self.unlocked_count)

        page_number = "Quiz page " + str(self.quiz_index + 1) + " of " + str(len(QUIZZES))
        draw_text(screen, page_number, fonts["small"], DARK_GREY, 500, 200, center=True)

        panel = pygame.Rect(80, 225, 840, 150)
        pygame.draw.rect(screen, WHITE, panel, border_radius=18)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=18)

        draw_text(screen, quiz["heading"], fonts["heading"], BROWN, panel.centerx, panel.y + 38, center=True)
        draw_centered_words(screen, quiz["question"], fonts["body"], DARK, panel.centerx, panel.y + 90, panel.width - 80)

        option_buttons = {}
        hovered_option = None

        for i in range(len(quiz["options"])):
            option = quiz["options"][i]
            rect = pygame.Rect(95 + i * 178, 410, 160, 90)

            if quiz["heading"] == "National Flag":
                draw_flag_card(screen, option, rect)
            else:
                draw_option_card(screen, fonts, option, rect)

            option_buttons[option] = rect

            if rect.collidepoint(pygame.mouse.get_pos()):
                hovered_option = option

        if quiz["heading"] != "National Flag":
            draw_hover_photo(screen, fonts, hovered_option)

        if self.feedback != "":
            if hovered_option is None:
                message_y = 525
            else:
                message_y = 385

            draw_centered_words(screen, self.feedback, fonts["small"], BROWN, 500, message_y, 780)

        draw_particles(screen, self.particles)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 190, 615, 210, 50, GREY)
        reset_button = draw_button(screen, "Reset", fonts["body"], 430, 615, 150, 50, YELLOW)

        return {"cards": option_buttons, "back": back_button, "reset": reset_button, "done": None}

    def draw_complete(self, screen, fonts):
        screen.fill(CREAM)

        draw_text(screen, "Symbols", fonts["title"], DARK, 500, 35, center=True)
        draw_symbol_board(screen, fonts, self.unlocked_count)

        final_card = pygame.Rect(115, 230, 770, 230)
        pygame.draw.rect(screen, WHITE, final_card, border_radius=20)
        pygame.draw.rect(screen, DARK, final_card, width=3, border_radius=20)

        draw_text(screen, "Symbols complete", fonts["heading"], BROWN, final_card.centerx, final_card.y + 55, center=True)

        final_message = (
            "You completed the symbols section. Symbols help people remember a place, "
            "its nature, its stories, and its identity."
        )
        draw_centered_words(screen, final_message, fonts["body"], DARK, final_card.centerx, final_card.y + 120, final_card.width - 90)

        draw_particles(screen, self.particles)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 190, 615, 210, 50, GREY)
        reset_button = draw_button(screen, "Reset", fonts["body"], 430, 615, 150, 50, YELLOW)
        done_button = draw_button(screen, "Stitch Quilt Section", fonts["body"], 610, 615, 270, 50, GREEN, WHITE)

        return {"cards": {}, "back": back_button, "reset": reset_button, "done": done_button}

    def draw(self, screen, fonts):
        if self.mode == "lesson":
            return self.draw_lesson(screen, fonts)

        if self.completed:
            return self.draw_complete(screen, fonts)

        return self.draw_quiz(screen, fonts)

    def handle_click(self, mouse_pos, buttons):
        if self.mode == "lesson":
            if buttons["back"].collidepoint(mouse_pos):
                return "back"

            if buttons["wiki"].collidepoint(mouse_pos):
                page = LESSONS[self.lesson_index]
                webbrowser.open(page["wiki"], new=2, autoraise=False)
                return None

            if buttons["next"].collidepoint(mouse_pos):
                if self.lesson_index < len(LESSONS) - 1:
                    self.lesson_index += 1
                else:
                    self.mode = "quiz"

            return None

        if buttons["back"].collidepoint(mouse_pos):
            return "back"

        if buttons["reset"].collidepoint(mouse_pos):
            self.reset()
            return None

        if self.completed:
            if buttons["done"].collidepoint(mouse_pos):
                return "complete"
            return None

        quiz = QUIZZES[self.quiz_index]

        for option in buttons["cards"]:
            rect = buttons["cards"][option]

            if rect.collidepoint(mouse_pos):
                if option == quiz["answer"]:
                    self.add_particles(rect.center)
                    self.feedback = quiz["note"]
                    self.unlocked_count += 1
                    self.quiz_index += 1

                    if self.quiz_index == len(QUIZZES):
                        self.completed = True
                    else:
                        self.feedback = ""
                else:
                    if quiz["heading"] == "National Flag":
                        country = flag_country_name(option)
                        self.feedback = "Good try. That is the flag of " + country + ". Try again."
                    else:
                        self.feedback = "Good try. " + option + " is not the correct answer. Try again."

                return None

        return None
