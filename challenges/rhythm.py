"""Rhythm challenge for Threads of Home."""

import random
import webbrowser
import pygame

from settings import CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY, DARK_GREY, PURPLE, ORANGE
from ui import draw_text, draw_wrapped_text, draw_button


class RhythmChallenge:
    """Learn about Bangla song traditions through a matching challenge."""

    def __init__(self):
        self.lesson_pages = [
            {
                "heading": "Songs Carry Stories",
                "body": (
                    "Music is a way people remember feelings, places, and stories. In Bangladesh, songs can be "
                    "connected to rivers, poetry, village life, faith, protest, and identity. A song can tell us "
                    "what people value and what they remember."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Music_of_Bangladesh",
            },
            {
                "heading": "River and Folk Songs",
                "body": (
                    "Bhatiyali is a folk song style connected with rivers and boatmen. On the wide rivers of Mymensingh and Sylhet, "
                    "when a boatman is alone on the water with nothing but sky above him, he sings Bhatiyali. The word itself comes from bhata: "
                    "the current that carries the boat downstream. These songs are slow, longing, and full of open space, the way only a man alone on a river can feel." 
                ),
                "wiki": "https://en.wikipedia.org/wiki/Bhatiyali",
            },
            {
                "heading": "Poets and Traditions (Rabindra Sangeet)",
                "body": (
                    "Rabindranath Tagore wrote songs that felt like the land itself was speaking: the monsoon rain, the mustard fields, the fishermen at dusk. "
                    "His music, called Rabindra Sangeet, became woven into Bengali life so deeply that Bangladesh chose one of his songs as its national anthem.\n\n"
                    ),
                "wiki": "https://en.wikipedia.org/wiki/Rabindra_Sangeet",
            },
            {
                "heading": "Nazrul Geeti",
                "body": (
                    "Bangladesh named Kazi Nazrul Islam its national poet, because his voice still sounds like the voice of people who refuse to give up. The British colonial government jailed and tormented"
                    " Nazrul for years because of his radical literary expressions. "
                    "His songs swung between fury and tenderness, revolution and devotion, love and grief. He is called the Rebel Poet and his music, Nazrul Geeti, carries that electricity even now.\n\n"
                ),
                "wiki": "https://en.wikipedia.org/wiki/Nazrul_Geeti",
            },
            {
                "heading": "Lalon Songs",
                "body": (
                    "Deep in the heart of Kushtia, a man with no caste, no religion, and no last name sat by the river and sang. Lalon Shah asked questions nobody dared to ask: who are you really, beneath"
                    "your religion and your name? His songs, called Baul songs, spread from village to village, carried by wandering singers with one-stringed instruments and open hearts. He belonged to everyone and no one."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Lalon",
            }

        ]

        self.steps = [
            {
                "prompt": "Which song style is connected with rivers and boatmen?",
                "answer": "Bhatiyali",
                "note": "Bhatiyali is a river and boatmen folk song style.",
            },
            {
                "prompt": "Which song tradition is connected with Rabindranath Tagore?",
                "answer": "Rabindra Sangeet",
                "note": "Rabindra Sangeet means songs by Rabindranath Tagore.",
            },
            {
                "prompt": "Which song tradition is connected with Kazi Nazrul Islam?",
                "answer": "Nazrul Geeti",
                "note": "Nazrul Geeti means songs by Kazi Nazrul Islam.",
            },
            {
                "prompt": "Which song tradition is connected with Lalon Fakir and Baul tradition?",
                "answer": "Lalon Geeti",
                "note": "Lalon Geeti is connected with Lalon Fakir and Baul tradition.",
            },
        ]

        self.options = ["Bhatiyali", "Rabindra Sangeet", "Nazrul Geeti", "Lalon Geeti"]
        self.option_images = {
            "Bhatiyali": "bhatiyali.jpg",
            "Rabindra Sangeet": "Rabindranath.webp",
            "Nazrul Geeti": "nazrul.jpg",
            "Lalon Geeti": "lalon.jpg",
        }
        self.images = {}

        for option in self.options:
            try:
                filename = self.option_images[option]
                self.images[option] = pygame.image.load("assets/rhythm/" + filename).convert_alpha()
            except (pygame.error, FileNotFoundError):
                self.images[option] = None

        self.reset()

    def reset(self):
        self.mode = "lesson"
        self.lesson_index = 0
        self.current_step = 0
        self.completed = False
        self.message = self.lesson_pages[0]["body"]
        self.success_particles = []
        self.completed_answers = []
        self.shuffled_options = self.options[:]
        random.shuffle(self.shuffled_options)

        if self.shuffled_options == self.options:
            first_option = self.shuffled_options.pop(0)
            self.shuffled_options.append(first_option)

    def update(self):
        for p in self.success_particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["dy"] += 0.12
            p["life"] -= 1

        living_particles = []
        for particle in self.success_particles:
            if particle["life"] > 0:
                living_particles.append(particle)
        self.success_particles = living_particles

    def add_success_particles(self, centre):
        for _ in range(24):
            self.success_particles.append({
                "x": centre[0],
                "y": centre[1],
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-4, -1),
                "life": random.randint(24, 42),
                "colour": random.choice([WHITE, GREEN, YELLOW, ORANGE]),
            })

    def draw_particles(self, screen):
        for p in self.success_particles:
            pygame.draw.circle(screen, p["colour"], (int(p["x"]), int(p["y"])), 4)

    def draw_image_in_box(self, screen, image, box):
        if image is None:
            return

        scale = min(box.width / image.get_width(), box.height / image.get_height())
        new_width = int(image.get_width() * scale)
        new_height = int(image.get_height() * scale)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
        image_rect = image.get_rect(center=box.center)
        screen.blit(image, image_rect)

    def draw_centered_wrapped_text(self, screen, text, font, colour, center_x, y, max_width, line_gap=8):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = current + " " + word
            test = test.strip()
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

        draw_text(screen, "Rhythm", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learn first, then match the song traditions.", fonts["small"], BROWN, 500, 105, center=True)

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
            "Learning page " + str(self.lesson_index + 1) + " of " + str(len(self.lesson_pages)),
            fonts["small"],
            DARK_GREY,
            500,
            550,
            center=True,
        )

        back_button = draw_button(screen, "Back to Map", fonts["body"], 130, 610, 190, 55, GREY)
        wiki_button = draw_button(screen, "Wikipedia", fonts["body"], 390, 610, 180, 55, YELLOW)
        next_text = "Start Challenge" if self.lesson_index == len(self.lesson_pages) - 1 else "Next"
        next_button = draw_button(screen, next_text, fonts["body"], 650, 610, 190, 55, GREEN, WHITE)

        return {"back": back_button, "wiki": wiki_button, "next": next_button}

    def draw_instruction_panel(self, screen, fonts):
        panel = pygame.Rect(65, 70, 870, 105)
        pygame.draw.rect(screen, WHITE, panel, border_radius=16)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=16)

        if self.completed:
            heading = "Gathering complete"
        else:
            heading = "Rhythm step " + str(self.current_step + 1) + " of " + str(len(self.steps))
        draw_text(screen, heading, fonts["small"], BROWN, panel.x + 20, panel.y + 12)

        message_y = panel.y + 42
        for line in self.message.split("\n"):
            draw_wrapped_text(screen, line, fonts["small"], DARK, panel.x + 20, message_y, panel.width - 40)
            message_y += fonts["small"].get_height() + 8

    def draw_music_scene(self, screen, fonts):
        scene = pygame.Rect(80, 195, 840, 220)
        pygame.draw.rect(screen, (238, 220, 245), scene, border_radius=18)
        pygame.draw.rect(screen, DARK, scene, width=3, border_radius=18)

        draw_text(screen, "Village music gathering", fonts["heading"], BROWN, scene.centerx, scene.y + 38, center=True)

        pygame.draw.rect(screen, (205, 172, 125), (scene.x + 160, scene.y + 150, 520, 35), border_radius=8)
        pygame.draw.rect(screen, DARK, (scene.x + 160, scene.y + 150, 520, 35), width=3, border_radius=8)

        for i in range(4):
            x = scene.x + 230 + i * 130
            pygame.draw.circle(screen, ORANGE, (x, scene.y + 120), 22)
            pygame.draw.rect(screen, PURPLE, (x - 18, scene.y + 142, 36, 45), border_radius=8)

        for i in range(len(self.completed_answers)):
            answer = self.completed_answers[i]
            image = self.images[answer]
            image_box = pygame.Rect(scene.x + 180 + i * 130, scene.y + 70, 100, 70)

            pygame.draw.rect(screen, WHITE, image_box, border_radius=12)
            pygame.draw.rect(screen, DARK, image_box, width=2, border_radius=12)

            if image is not None:
                self.draw_image_in_box(screen, image, image_box)

        note_places = [
            (scene.x + 155, scene.y + 72),
            (scene.x + 315, scene.y + 62),
            (scene.x + 485, scene.y + 62),
            (scene.x + 650, scene.y + 72),
        ]

        for i in range(len(self.completed_answers)):
            note_x, note_y = note_places[i]
            draw_text(screen, "♪", fonts["heading"], DARK, note_x, note_y, center=True)

    def draw_choice_card(self, screen, fonts, text, rect):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        done = text in self.completed_answers

        fill = (210, 242, 215) if done else ((255, 245, 210) if hovered else WHITE)

        pygame.draw.rect(screen, fill, rect, border_radius=16)
        pygame.draw.rect(screen, GREEN if hovered else DARK, rect, width=3, border_radius=16)

        image = self.images[text]
        image_box = pygame.Rect(rect.x + 10, rect.y + 8, rect.width - 20, 55)

        if image is not None:
            self.draw_image_in_box(screen, image, image_box)
        else:
            draw_text(screen, "Missing photo", fonts["tiny"], DARK_GREY, image_box.centerx, image_box.centery, center=True)

        self.draw_centered_wrapped_text(screen, text, fonts["tiny"], DARK, rect.centerx, rect.y + 68, rect.width - 20)

        if done:
            draw_text(screen, "DONE", fonts["tiny"], GREEN, rect.centerx, rect.bottom - 12, center=True)

    def draw_puzzle(self, screen, fonts):
        screen.fill(CREAM)
        draw_text(screen, "Rhythm", fonts["title"], DARK, 500, 35, center=True)
        self.draw_instruction_panel(screen, fonts)
        self.draw_music_scene(screen, fonts)

        card_rects = {}
        start_x = 80
        gap = 20
        card_width = 200

        for i in range(len(self.shuffled_options)):
            option = self.shuffled_options[i]
            rect = pygame.Rect(start_x + i * (card_width + gap), 455, card_width, 95)
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

            if buttons["wiki"].collidepoint(mouse_pos):
                page = self.lesson_pages[self.lesson_index]
                webbrowser.open(page["wiki"], new=2, autoraise=False)
                return None

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
                            "You completed the rhythm gathering. Click on the quilt to unfold song section on nokshi katha."
                        )
                    else:
                        self.message = (
                            "Correct. " + current["note"] + "\n"
                            "Next: " + self.steps[self.current_step]["prompt"]
                        )
                else:
                    self.message = (
                        "Good try. " + option + " is not the answer for this clue.\n"
                        "Clue: " + current["prompt"]
                    )

                return None

        return None
