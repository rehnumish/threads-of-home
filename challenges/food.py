"""Food challenge: Serve the Family.

The player first learns about Bangladeshi food culture, then builds a meal
using real item photos.

Food items:
- Bhaat = rice
- Fish = important in Bangladeshi meals
- Achar = pickles
- Mishti = sweets used to express enjoyment, hospitality, and festivities
- Pitha = traditional Bengali cake/snack
"""

import os
import math
import random
import pygame

from settings import (
    CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY,
    DARK_GREY, ORANGE, RED
)
from ui import draw_text, draw_wrapped_text, draw_button


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FoodChallenge:
    """A guided Bangladeshi food learning and placement challenge."""

    def __init__(self):
        self.image_cache = {}

        self.scene_zones = {
            "main_plate": {
                "label": "Main Plate",
                "rect": pygame.Rect(95, 220, 190, 135),
                "colour": (248, 241, 224),
            },
            "fish_side": {
                "label": "Fish Side",
                "rect": pygame.Rect(315, 220, 190, 135),
                "colour": (232, 242, 248),
            },
            "pickle_bowl": {
                "label": "Small Bowl",
                "rect": pygame.Rect(535, 220, 170, 135),
                "colour": (245, 235, 210),
            },
            "sweet_plate": {
                "label": "Sweet Plate",
                "rect": pygame.Rect(735, 220, 170, 135),
                "colour": (255, 230, 225),
            },
            "snack_plate": {
                "label": "Snack Plate",
                "rect": pygame.Rect(405, 375, 190, 120),
                "colour": (250, 226, 180),
            },
        }

        self.items = [
            {
                "name": "Bhaat",
                "zone": "main_plate",
                "home": (85, 535),
                "image": "bhaat.png",
                "note": "Bhaat means rice. Rice is one of the main foods in many Bangladeshi meals.",
            },
            {
                "name": "Fish",
                "zone": "fish_side",
                "home": (235, 535),
                "image": "fish.png",
                "note": "Fish is important in Bangladeshi food culture. Bangladesh is often connected with rice and fish.",
            },
            {
                "name": "Achar",
                "zone": "pickle_bowl",
                "home": (385, 535),
                "image": "achar.png",
                "note": "Achar means pickles. It adds a sharp, tangy, or spicy taste beside the meal.",
            },
            {
                "name": "Mishti",
                "zone": "sweet_plate",
                "home": (535, 535),
                "image": "mishti.png",
                "note": "Mishti means sweets. Families express enjoyment, hospitality, and festivities with mishti.",
            },
            {
                "name": "Pitha",
                "zone": "snack_plate",
                "home": (685, 535),
                "image": "pitha.png",
                "note": "Pitha is a traditional Bengali cake or snack, often connected with family gatherings and special times.",
            },
            {
                "name": "Burger",
                "zone": "decoy",
                "home": (835, 535),
                "image": "burger.png",
                "note": "This may be tasty, but this challenge is about foods strongly connected with Bangladeshi family meals.",
            },
        ]

        self.lesson_pages = [
            {
                "heading": "Why Food Matters",
                "body": (
                    "In many Bangladeshi families, food is more than something people eat. "
                    "Food is a way to show care. When someone visits, families often offer food "
                    "to make them feel welcome. Cooking and sharing food can show love, respect, "
                    "and hospitality."
                ),
            },
            {
                "heading": "Rice and Fish Nation",
                "body": (
                    "Bangladesh has many rivers, wetlands, ponds, and farming areas. Because of this, "
                    "rice and fish became a big part of everyday food. Bhaat is the rice that often "
                    "sits at the centre of the meal, and fish is one of the most important foods served "
                    "with it."
                ),
            },
            {
                "heading": "A Meal Has Balance",
                "body": (
                    "A Bangladeshi meal is not only one food. Bhaat gives the meal its base. Fish adds "
                    "the main flavour and connects the meal to rivers and daily life. Achar adds a strong "
                    "sour, spicy, or tangy taste. Each item has a different job on the plate."
                ),
            },
            {
                "heading": "Mishti and Pitha",
                "body": (
                    "Mishti is connected with happiness. Families express enjoyment, hospitality, and "
                    "festivities with mishti. Pitha is often connected with home, seasons, and family "
                    "gatherings. These foods carry memories because people remember who made them, "
                    "when they ate them, and who they shared them with."
                ),
            },
            {
                "heading": "Now Build the Meal",
                "body": (
                    "Now you will build a Bangladeshi family meal. Do not only match the words. "
                    "Think about what each food does. Which food is the base? Which one connects "
                    "to rivers? Which one adds strong taste? Which foods show celebration and family memory?"
                ),
            },
        ]

        self.steps = [
            {
                "zone": "main_plate",
                "clue": "Start with the heart of the meal. Which item means rice?",
            },
            {
                "zone": "fish_side",
                "clue": "Bangladesh is often connected with rice and fish. What should be served with the bhaat?",
            },
            {
                "zone": "pickle_bowl",
                "clue": "Now add something small with a strong tangy or spicy taste. Which item belongs in the small bowl?",
            },
            {
                "zone": "sweet_plate",
                "clue": "Families express enjoyment, hospitality, and festivities with this. Which item belongs on the sweet plate?",
            },
            {
                "zone": "snack_plate",
                "clue": "Finally, add a traditional Bengali cake or snack often connected with family gatherings.",
            },
        ]

        self.reset()

    def reset(self):
        """Reset the challenge."""
        self.mode = "lesson"
        self.lesson_index = 0
        self.current_step = 0
        self.selected_item = None
        self.placed_items = {}
        self.completed = False
        self.success_particles = []
        self.message = self.lesson_pages[0]["body"]
        self.mistake_flash = 0

    def current_zone_key(self):
        """Return required zone for current step."""
        if self.current_step >= len(self.steps):
            return None
        return self.steps[self.current_step]["zone"]

    def image_path(self, filename):
        """Return full path for a food image."""
        return os.path.join(BASE_DIR, "assets", "food", filename)

    def load_food_image(self, filename, max_width, max_height):
    
        cache_key = (filename, max_width, max_height)
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        path = self.image_path(filename)

        try:
            image = pygame.image.load(path).convert_alpha()

            original_width = image.get_width()
            original_height = image.get_height()

            scale = min(max_width / original_width, max_height / original_height)

            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            image = pygame.transform.smoothscale(image, (new_width, new_height))
            self.image_cache[cache_key] = image
            return image

        except (pygame.error, FileNotFoundError):
            return None

    def item_rect(self, item, animation_tick):
        """Return item rectangle."""
        if item["name"] in self.placed_items:
            zone_rect = self.scene_zones[item["zone"]]["rect"]
            return pygame.Rect(zone_rect.centerx - 55, zone_rect.centery - 38, 110, 76)

        home_x, home_y = item["home"]
        bob = int(5 * math.sin(animation_tick * 0.06 + home_x))
        return pygame.Rect(home_x, home_y + bob, 120, 78)

    def add_success_particles(self, centre):
        """Create success particles."""
        for _ in range(24):
            self.success_particles.append({
                "x": centre[0],
                "y": centre[1],
                "dx": random.uniform(-3.0, 3.0),
                "dy": random.uniform(-4.5, -1.0),
                "life": random.randint(25, 45),
                "colour": random.choice([GREEN, YELLOW, WHITE, ORANGE, RED]),
            })

    def update_particles(self):
        """Move particles."""
        for particle in self.success_particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.15
            particle["life"] -= 1

        self.success_particles = [p for p in self.success_particles if p["life"] > 0]

    def draw_particles(self, screen):
        """Draw particles."""
        for particle in self.success_particles:
            pygame.draw.circle(
                screen,
                particle["colour"],
                (int(particle["x"]), int(particle["y"])),
                4,
            )

    def draw_lesson(self, screen, fonts):
        """Draw the learning material before the puzzle."""
        screen.fill(CREAM)

        page = self.lesson_pages[self.lesson_index]

        draw_text(screen, "Serve the Family", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learning first, challenge after.", fonts["body"], BROWN, 500, 110, center=True)

        card = pygame.Rect(120, 165, 760, 335)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)
        draw_wrapped_text(screen, page["body"], fonts["body"], DARK, card.x + 45, card.y + 105, card.width - 90, 12)

        draw_text(
            screen,
            f"Learning page {self.lesson_index + 1} of {len(self.lesson_pages)}",
            fonts["small"],
            DARK_GREY,
            500,
            525,
            center=True,
        )

        back_button = draw_button(screen, "Back to Map", fonts["body"], 235, 600, 210, 55, GREY)
        next_text = "Start Challenge" if self.lesson_index == len(self.lesson_pages) - 1 else "Next"
        next_button = draw_button(screen, next_text, fonts["body"], 555, 600, 210, 55, GREEN, WHITE)

        return {
            "back": back_button,
            "next": next_button,
        }

    def draw_instruction_panel(self, screen, fonts):
        """Draw clue panel."""
        panel = pygame.Rect(70, 75, 860, 95)
        pygame.draw.rect(screen, WHITE, panel, border_radius=16)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=16)

        heading = "Meal complete" if self.completed else f"Food step {self.current_step + 1} of {len(self.steps)}"
        draw_text(screen, heading, fonts["small"], BROWN, panel.x + 20, panel.y + 12)
        draw_wrapped_text(screen, self.message, fonts["small"], DARK, panel.x + 20, panel.y + 42, panel.width - 40)

    def draw_zone(self, screen, zone_key, zone, fonts, animation_tick):
        """Draw a placement zone."""
        rect = zone["rect"]
        required_zone = self.current_zone_key()
        is_active = zone_key == required_zone and not self.completed

        pygame.draw.rect(screen, zone["colour"], rect, border_radius=16)

        if is_active:
            pulse = int(4 + 3 * abs(math.sin(animation_tick * 0.08)))
            pygame.draw.rect(screen, GREEN, rect.inflate(pulse, pulse), width=5, border_radius=18)
        else:
            pygame.draw.rect(screen, BROWN, rect, width=3, border_radius=16)

        draw_text(screen, zone["label"], fonts["tiny"], DARK, rect.centerx, rect.y + 14, center=True)

    def draw_item_photo(self, screen, item, rect, fonts):
        """Draw a real item photo with correct aspect ratio."""
        selected = self.selected_item == item["name"]
        placed = item["name"] in self.placed_items

        pygame.draw.rect(screen, WHITE, rect, border_radius=14)
        pygame.draw.rect(screen, GREEN if selected else DARK, rect, width=4, border_radius=14)

        image_area = pygame.Rect(rect.x + 7, rect.y + 7, rect.width - 14, rect.height - 30)
        image = self.load_food_image(item["image"], image_area.width, image_area.height)

        if image is not None:
            image_x = image_area.centerx - image.get_width() // 2
            image_y = image_area.centery - image.get_height() // 2
            screen.blit(image, (image_x, image_y))
        else:
            draw_text(screen, "Missing photo", fonts["tiny"], DARK_GREY, rect.centerx, rect.centery - 8, center=True)
            draw_text(screen, item["image"], fonts["tiny"], DARK_GREY, rect.centerx, rect.centery + 12, center=True)

        if placed:
            draw_text(screen, "PLACED", fonts["tiny"], GREEN, rect.centerx, rect.y + 8, center=True)
        else:
            draw_text(screen, item["name"], fonts["tiny"], DARK, rect.centerx, rect.bottom - 12, center=True)

    def draw_puzzle(self, screen, fonts):
        """Draw the food puzzle."""
        animation_tick = pygame.time.get_ticks() // 16

        screen.fill(CREAM)
        draw_text(screen, "Serve the Family", fonts["title"], DARK, 500, 35, center=True)
        self.draw_instruction_panel(screen, fonts)

        zone_rects = {}
        for key, zone in self.scene_zones.items():
            self.draw_zone(screen, key, zone, fonts, animation_tick)
            zone_rects[key] = zone["rect"]

        tray = pygame.Rect(55, 515, 890, 100)
        pygame.draw.rect(screen, (230, 211, 184), tray, border_radius=18)
        pygame.draw.rect(screen, BROWN, tray, width=3, border_radius=18)
        draw_text(screen, "Item tray: click a photo, then click the glowing area.", fonts["tiny"], DARK, 500, 522, center=True)

        item_rects = {}
        for item in self.items:
            rect = self.item_rect(item, animation_tick)
            item_rects[item["name"]] = rect
            self.draw_item_photo(screen, item, rect, fonts)

        self.draw_particles(screen)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 200, 635, 210, 45, GREY)
        reset_button = draw_button(screen, "Reset", fonts["body"], 445, 635, 150, 45, YELLOW)
        done_button = None

        if self.completed:
            done_button = draw_button(screen, "Stitch Quilt Section", fonts["body"], 635, 635, 260, 45, GREEN, WHITE)

        return {
            "items": item_rects,
            "zones": zone_rects,
            "back": back_button,
            "reset": reset_button,
            "done": done_button,
        }

    def draw(self, screen, fonts):
        """Draw either lesson or puzzle."""
        if self.mode == "lesson":
            return self.draw_lesson(screen, fonts)

        return self.draw_puzzle(screen, fonts)

    def handle_click(self, mouse_pos, buttons):
        """Handle mouse clicks."""
        if self.mode == "lesson":
            if buttons["back"].collidepoint(mouse_pos):
                return "back"

            if buttons["next"].collidepoint(mouse_pos):
                if self.lesson_index < len(self.lesson_pages) - 1:
                    self.lesson_index += 1
                    self.message = self.lesson_pages[self.lesson_index]["body"]
                else:
                    self.mode = "puzzle"
                    self.message = self.steps[0]["clue"]

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

        for item in self.items:
            if item["name"] in self.placed_items:
                continue

            if buttons["items"][item["name"]].collidepoint(mouse_pos):
                self.selected_item = item["name"]

                if item["zone"] == "decoy":
                    self.message = item["note"] + " Try choosing one of the Bangladeshi food items."
                else:
                    self.message = item["note"] + " Now place it in the glowing area if it matches the clue."

                return None

        if self.selected_item is not None:
            for zone_key, zone_rect in buttons["zones"].items():
                if zone_rect.collidepoint(mouse_pos):
                    selected_data = next(item for item in self.items if item["name"] == self.selected_item)
                    required_zone = self.current_zone_key()

                    if selected_data["zone"] == required_zone and zone_key == required_zone:
                        self.placed_items[self.selected_item] = zone_key
                        self.add_success_particles(zone_rect.center)

                        self.current_step += 1
                        self.selected_item = None

                        if self.current_step >= len(self.steps):
                            self.completed = True
                            self.message = (
                                "You served a Bangladeshi family meal. Bhaat, fish, achar, mishti, and pitha "
                                "show how food can carry family memory, hospitality, celebration, and culture."
                            )
                        else:
                            self.message = self.steps[self.current_step]["clue"]

                    else:
                        self.mistake_flash = 15
                        self.message = (
                            "Good try. This challenge is for learning, not just testing. "
                            f"{selected_data['note']} Look again at the clue and glowing area."
                        )

                    return None

        return None

    def update(self):
        """Update animations."""
        self.update_particles()

        if self.mistake_flash > 0:
            self.mistake_flash -= 1