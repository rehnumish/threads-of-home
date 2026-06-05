"""Food challenge for Threads of Home."""

import random
import webbrowser
import pygame

from settings import CREAM, DARK, BROWN, WHITE, GREEN, YELLOW, GREY, DARK_GREY, ORANGE, RED
from ui import draw_text, draw_wrapped_text, draw_button


class FoodChallenge:
    """A simple food matching challenge."""

    def __init__(self):
        self.lesson_pages = [
            {
                "heading": "Why Food Matters",
                "body": (
                    "In many Bangladeshi families, food is more than something people eat. "
                    "Food is a way to show care. When someone visits, families often offer food "
                    "to make them feel welcome."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Bangladeshi_cuisine",
            },
            {
                "heading": "Rice and Fish Nation",
                "body": (
                    "Bangladesh has many rivers, wetlands, ponds, and farming areas. "
                    "Because of this, rice and fish became a big part of everyday food."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Bangladeshi_cuisine",
            },
            {
                "heading": "A Meal Has Balance",
                "body": (
                    "A Bangladeshi meal is not only one food. Bhaat gives the meal its base. "
                    "Fish adds flavour. Achar adds a sharp taste. Mishti and pitha connect food "
                    "with celebration and family memory."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Bengali_cuisine",
            },
            {
                "heading": "Now Build the Meal",
                "body": (
                    "Now you will build a Bangladeshi family meal. Choose the food photo, "
                    "then click the matching place on the table."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Bangladeshi_cuisine",
            },
        ]

        self.zones = [
            {
                "key": "main_plate",
                "label": "Main Plate",
                "rect": pygame.Rect(95, 220, 190, 135),
                "colour": (248, 241, 224),
            },
            {
                "key": "fish_side",
                "label": "A Must Side",
                "rect": pygame.Rect(315, 220, 190, 135),
                "colour": (232, 242, 248),
            },
            {
                "key": "pickle_bowl",
                "label": "Small Bowl",
                "rect": pygame.Rect(535, 220, 170, 135),
                "colour": (245, 235, 210),
            },
            {
                "key": "sweet_plate",
                "label": "Sweet Plate",
                "rect": pygame.Rect(735, 220, 170, 135),
                "colour": (255, 230, 225),
            },
            {
                "key": "snack_plate",
                "label": "Snack Plate",
                "rect": pygame.Rect(405, 375, 190, 120),
                "colour": (250, 226, 180),
            },
        ]

        self.items = [
            {
                "name": "Bhaat",
                "zone": "main_plate",
                "image": "bhaat.png",
                "note": "Bhaat means rice. It is often the base of the meal.",
            },
            {
                "name": "Fish",
                "zone": "fish_side",
                "image": "fish.png",
                "note": "Fish connects the meal to rivers and daily life.",
            },
            {
                "name": "Achar",
                "zone": "pickle_bowl",
                "image": "achar.png",
                "note": "Achar means pickles. It adds a sharp tangy taste.",
            },
            {
                "name": "Mishti",
                "zone": "sweet_plate",
                "image": "mishti.png",
                "note": "Mishti means sweets. Families share sweets for joy and hospitality.",
            },
            {
                "name": "Pitha",
                "zone": "snack_plate",
                "image": "pitha.png",
                "note": "Pitha is a traditional Bengali snack connected with home and family.",
            },
            {
                "name": "Burger",
                "zone": "decoy",
                "image": "burger.png",
                "note": "Burger is tasty, but this challenge is about Bangladeshi food.",
            },
        ]

        self.images = {}
        for item in self.items:
            try:
                self.images[item["name"]] = pygame.image.load("assets/food/" + item["image"]).convert_alpha()
            except (pygame.error, FileNotFoundError):
                self.images[item["name"]] = None

        self.reset()

    def reset(self):
        self.mode = "lesson"
        self.lesson_index = 0
        self.placed_items = {}
        self.completed = False
        self.particles = []
        self.message = self.lesson_pages[0]["body"]
        self.dragging_item = None
        self.drag_offset = (0, 0)

        self.shuffled_items = self.items[:]
        random.shuffle(self.shuffled_items)

        if self.shuffled_items == self.items:
            first_item = self.shuffled_items.pop(0)
            self.shuffled_items.append(first_item)

    def add_particles(self, center):
        for i in range(24):
            self.particles.append({
                "x": center[0],
                "y": center[1],
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-4, -1),
                "life": random.randint(25, 45),
                "colour": random.choice([GREEN, YELLOW, WHITE, ORANGE, RED]),
            })

    def update(self):
        for particle in self.particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.15
            particle["life"] -= 1

        alive = []
        for particle in self.particles:
            if particle["life"] > 0:
                alive.append(particle)
        self.particles = alive

    def draw_particles(self, screen):
        for particle in self.particles:
            pygame.draw.circle(
                screen,
                particle["colour"],
                (int(particle["x"]), int(particle["y"])),
                4,
            )

    def draw_lesson(self, screen, fonts):
        screen.fill(CREAM)
        page = self.lesson_pages[self.lesson_index]

        draw_text(screen, "Serve the Family", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learn first, challenge after.", fonts["body"], BROWN, 500, 110, center=True)

        card = pygame.Rect(120, 165, 760, 335)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)
        draw_wrapped_text(screen, page["body"], fonts["body"], DARK, card.x + 45, card.y + 105, card.width - 90, 12)

        page_text = "Learning page " + str(self.lesson_index + 1) + " of " + str(len(self.lesson_pages))
        draw_text(screen, page_text, fonts["small"], DARK_GREY, 500, 525, center=True)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 130, 600, 190, 55, GREY)
        wiki_button = draw_button(screen, "Wikipedia", fonts["body"], 390, 600, 180, 55, YELLOW)

        if self.lesson_index == len(self.lesson_pages) - 1:
            next_text = "Start Challenge"
        else:
            next_text = "Next"

        next_button = draw_button(screen, next_text, fonts["body"], 650, 600, 190, 55, GREEN, WHITE)

        return {"back": back_button, "wiki": wiki_button, "next": next_button}

    def draw_zone(self, screen, fonts, zone):
        rect = zone["rect"]

        pygame.draw.rect(screen, zone["colour"], rect, border_radius=16)
        pygame.draw.rect(screen, BROWN, rect, width=3, border_radius=16)

        draw_text(screen, zone["label"], fonts["tiny"], DARK, rect.centerx, rect.y + 14, center=True)

    def item_rect(self, item_number, item, animation_tick):
        if item["name"] in self.placed_items:
            for zone in self.zones:
                if zone["key"] == item["zone"]:
                    rect = zone["rect"]
                    return pygame.Rect(rect.centerx - 55, rect.centery - 38, 110, 76)

        x = 85 + item_number * 150
        bounce = (animation_tick + item_number * 3) % 10
        if bounce > 5:
            bounce = 10 - bounce

        return pygame.Rect(x, 535 + bounce, 120, 78)

    def draw_item(self, screen, fonts, item, rect):
        placed = item["name"] in self.placed_items

        pygame.draw.rect(screen, WHITE, rect, border_radius=14)
        pygame.draw.rect(screen, DARK, rect, width=4, border_radius=14)

        image = self.images[item["name"]]

        if image is not None:
            image_area = pygame.Rect(rect.x + 9, rect.y + 8, rect.width - 18, rect.height - 36)
            scale = min(image_area.width / image.get_width(), image_area.height / image.get_height())
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.smoothscale(image, (new_width, new_height))
            image_x = image_area.centerx - image.get_width() // 2
            image_y = image_area.centery - image.get_height() // 2
            screen.blit(image, (image_x, image_y))
        else:
            draw_text(screen, "Missing", fonts["tiny"], DARK_GREY, rect.centerx, rect.centery, center=True)

        if placed:
            draw_text(screen, "PLACED", fonts["tiny"], GREEN, rect.centerx, rect.y + 10, center=True)
        else:
            draw_text(screen, item["name"], fonts["tiny"], DARK, rect.centerx, rect.bottom - 12, center=True)

    def draw_puzzle(self, screen, fonts):
        screen.fill(CREAM)

        draw_text(screen, "Serve the Family", fonts["title"], DARK, 500, 35, center=True)

        panel = pygame.Rect(70, 75, 860, 95)
        pygame.draw.rect(screen, WHITE, panel, border_radius=16)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=16)

        draw_text(screen, "Build the meal", fonts["small"], BROWN, panel.x + 20, panel.y + 12)
        draw_wrapped_text(screen, self.message, fonts["small"], DARK, panel.x + 20, panel.y + 42, panel.width - 40)

        zone_rects = {}
        for zone in self.zones:
            self.draw_zone(screen, fonts, zone)
            zone_rects[zone["key"]] = zone["rect"]

        tray = pygame.Rect(55, 515, 890, 100)
        pygame.draw.rect(screen, (230, 211, 184), tray, border_radius=18)
        pygame.draw.rect(screen, BROWN, tray, width=3, border_radius=18)
        draw_text(screen, "Item tray: drag each photo to its matching place.", fonts["tiny"], DARK, 500, 522, center=True)

        item_rects = {}
        for i in range(len(self.shuffled_items)):
            item = self.shuffled_items[i]
            rect = self.item_rect(i, item, pygame.time.get_ticks() // 120)

            if item["name"] == self.dragging_item:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rect = pygame.Rect(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1], 120, 78)

            item_rects[item["name"]] = rect
            self.draw_item(screen, fonts, item, rect)

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
        if self.mode == "lesson":
            return self.draw_lesson(screen, fonts)
        return self.draw_puzzle(screen, fonts)

    def find_item(self, name):
        for item in self.items:
            if item["name"] == name:
                return item
        return None

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
                    self.message = "Drag each Bangladeshi food to the matching place on the table."

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

        for item in self.shuffled_items:
            if item["name"] in self.placed_items:
                continue

            if buttons["items"][item["name"]].collidepoint(mouse_pos):
                self.dragging_item = item["name"]
                rect = buttons["items"][item["name"]]
                self.drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                return None

        return None

    def handle_release(self, mouse_pos, buttons):
        if self.dragging_item is None:
            return None

        item = self.find_item(self.dragging_item)
        self.dragging_item = None

        for zone_name, zone_rect in buttons["zones"].items():
            if zone_rect.collidepoint(mouse_pos):
                if item["zone"] == zone_name and item["zone"] != "decoy":
                    self.placed_items[item["name"]] = zone_name
                    self.add_particles(zone_rect.center)
                    self.message = item["note"]

                    if len(self.placed_items) == 5:
                        self.completed = True
                        self.message = (
                            "You served a Bangladeshi family meal. Food can carry family memory, "
                            "hospitality, celebration, and culture."
                        )
                else:
                    self.message = "Good try. " + item["note"]

                return None

        self.message = "Drag each food photo to its matching place on the table."
        return None
