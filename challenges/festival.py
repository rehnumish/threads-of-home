"""Pohela Boishakh puzzle challenge.


The player builds a Pohela Boishakh celebration scene by placing cultural items
into the correct glowing areas. 
"""
import math
import random
import webbrowser
import pygame

from settings import (
    CREAM, DARK, BROWN, RED, WHITE, BLUE, GREEN, YELLOW, GREY,
    DARK_GREY, BLACK, ORANGE, PINK, PURPLE
)
from ui import draw_text, draw_wrapped_text, draw_button


class FestivalChallenge:
    """A guided Pohela Boishakh scene-building puzzle."""

    def __init__(self):
        self.lesson_pages = [
            {
                "heading": "Alpana and Dhol",
                "body": (
                    "Pohela Boishakh is the Bengali New Year. Many celebrations begin by making a space feel welcoming. "
                    "Alpana is handpainted floor art made with white patterns, flowers, circles, and traditional designs. "
                    "It decorates the courtyard and invites people into the celebration. The dhol is a traditional drum that brings rhythm, "
                    "energy, and togetherness. Its sound helps people feel that the festival has begun."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Pohela_Boishakh",
            },
            {
                "heading": "Mongol Shovajatra",
                "body": (
                    "Mongol Shovajatra means a procession for well-being. It is a colourful Bengali New Year procession "
                    "where people walk together with handmade masks, animals, birds, and folk art. The masks are not only decoration. "
                    "They show courage, imagination, and hope for a better year. This procession celebrates community, creativity, "
                    "and standing together."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Mangal_Shobhajatra",
            },
            {
                "heading": "Pitha and Red-White Outfit",
                "body": (
                    "Food and clothing also carry festival memory. Pitha is a traditional Bengali snack often made and shared "
                    "with family during special times. Sharing food makes the celebration feel warm and welcoming. Red and white "
                    "outfits are strongly connected with Pohela Boishakh. Wearing these colours helps people feel part of the "
                    "same joyful Bengali New Year tradition."
                ),
                "wiki": "https://en.wikipedia.org/wiki/Pitha",
            },
        ]

        self.scene_zones = {
            "courtyard": {
                "label": "Courtyard",
                "rect": pygame.Rect(75, 190, 180, 135),
                "colour": (248, 241, 224),
            },
            "music": {
                "label": "Music Corner",
                "rect": pygame.Rect(295, 190, 180, 135),
                "colour": (246, 226, 167),
            },
            "procession": {
                "label": "Procession",
                "rect": pygame.Rect(515, 190, 180, 135),
                "colour": (245, 210, 210),
            },
            "food": {
                "label": "Food Table",
                "rect": pygame.Rect(735, 190, 180, 135),
                "colour": (250, 226, 180),
            },
            "outfit": {
                "label": "Outfit Stand",
                "rect": pygame.Rect(405, 350, 190, 125),
                "colour": (235, 218, 246),
            },
        }

        self.items = [
            {
                "name": "Handpainted design (Alpana)",
                "zone": "courtyard",
                "home": (105, 520),
                "image": "alpana.webp",
                "note": "Alpana is decorative floor art. In this scene it belongs in the courtyard, where it welcomes people into the celebration.",
            },
            {
                "name": "Drum (Dhol)",
                "zone": "music",
                "home": (255, 520),
                "image": "Dhol.jpg",
                "note": "The dhol is a drum. It belongs in the music corner because rhythm helps create the energy of the festival.",
            },
            {
                "name": "Mask",
                "zone": "procession",
                "home": (405, 520),
                "image": "mask.jpg",
                "note": "Colourful masks are connected with Mangal Shobhajatra, a festive procession for Bengali New Year.",
            },
            {
                "name": "Pitha",
                "zone": "food",
                "home": (555, 520),
                "image": "pitha2.jpg",
                "note": "Pitha belongs on the food table. Food connects festivals with family, memory, and sharing.",
            },
            {
                "name": "Red-White Outfit",
                "zone": "outfit",
                "home": (705, 520),
                "image": "outfit.jpg",
                "note": "Red and white clothing is commonly associated with Pohela Boishakh celebration outfits.",
            },
            {
                "name": "Barbie",
                "zone": "decoy",
                "home": (855, 520),
                "image": "barbie.jpg",
                "note": "This might be fun, but it does not help complete this Pohela Boishakh scene.",
            },
        ]

        self.images = {}
        for item in self.items:
            try:
                self.images[item["name"]] = pygame.image.load("assets/festival/" + item["image"]).convert_alpha()
            except (pygame.error, FileNotFoundError):
                self.images[item["name"]] = None

        self.reset()

    def reset(self):
        """Reset the puzzle to its starting state."""
        self.mode = "lesson"
        self.lesson_index = 0
        self.placed_items = {}
        self.message = self.lesson_pages[0]["body"]
        self.completed = False
        self.success_particles = []
        self.mistake_flash = 0
        self.last_completed_item = None
        self.dragging_item = None
        self.drag_offset = (0, 0)
        self.shuffled_items = self.items[:]
        random.shuffle(self.shuffled_items)

        if self.shuffled_items == self.items:
            first_item = self.shuffled_items.pop(0)
            self.shuffled_items.append(first_item)

    def draw_lesson(self, screen, fonts):
        screen.fill(CREAM)
        page = self.lesson_pages[self.lesson_index]

        draw_text(screen, "Pohela Boishakh", fonts["title"], DARK, 500, 55, center=True)
        draw_text(screen, "Learn first, then build the celebration.", fonts["small"], BROWN, 500, 105, center=True)

        card = pygame.Rect(105, 145, 790, 380)
        pygame.draw.rect(screen, WHITE, card, border_radius=20)
        pygame.draw.rect(screen, DARK, card, width=3, border_radius=20)

        draw_text(screen, page["heading"], fonts["heading"], BROWN, card.centerx, card.y + 45, center=True)
        draw_wrapped_text(screen, page["body"], fonts["body"], DARK, card.x + 45, card.y + 105, card.width - 90, 10)

        page_text = "Learning page " + str(self.lesson_index + 1) + " of " + str(len(self.lesson_pages))
        draw_text(screen, page_text, fonts["small"], DARK_GREY, 500, 550, center=True)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 130, 610, 190, 55, GREY)
        wiki_button = draw_button(screen, "Wikipedia", fonts["body"], 390, 610, 180, 55, YELLOW)

        if self.lesson_index == len(self.lesson_pages) - 1:
            next_text = "Start Challenge"
        else:
            next_text = "Next"

        next_button = draw_button(screen, next_text, fonts["body"], 650, 610, 190, 55, GREEN, WHITE)

        return {"back": back_button, "wiki": wiki_button, "next": next_button}

    def item_rect(self, item, animation_tick):
        """Return the current rectangle for an item, including gentle bobbing animation."""
        # Placed items move to the centre of their assigned zone.
        if item["name"] in self.placed_items:
            zone_rect = self.scene_zones[item["zone"]]["rect"]
            return pygame.Rect(zone_rect.centerx - 55, zone_rect.centery - 35, 110, 70)

        if item in self.shuffled_items:
            tray_index = self.shuffled_items.index(item)
            home_x = 105 + tray_index * 150
            home_y = 520
        else:
            home_x, home_y = item["home"]

        bob = int(5 * math.sin(animation_tick * 0.06 + home_x))
        return pygame.Rect(home_x, home_y + bob, 120, 72)

    def add_success_particles(self, centre):
        """Create small animated particles when a correct item is placed."""
        for _ in range(24):
            self.success_particles.append({
                "x": centre[0],
                "y": centre[1],
                "dx": random.uniform(-3.0, 3.0),
                "dy": random.uniform(-4.5, -1.0),
                "life": random.randint(25, 45),
                "colour": random.choice([RED, YELLOW, GREEN, WHITE, ORANGE]),
            })

    def update_particles(self):
        """Move and fade particles."""
        for particle in self.success_particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.15
            particle["life"] -= 1

        living_particles = []
        for particle in self.success_particles:
            if particle["life"] > 0:
                living_particles.append(particle)
        self.success_particles = living_particles

    def draw_particles(self, screen):
        """Draw success particles."""
        for particle in self.success_particles:
            pygame.draw.circle(
                screen,
                particle["colour"],
                (int(particle["x"]), int(particle["y"])),
                4,
            )

    def draw_zone(self, screen, zone_key, zone, fonts, animation_tick):
        """Draw a target zone in the festival scene."""
        rect = zone["rect"]

        pygame.draw.rect(screen, zone["colour"], rect, border_radius=16)
        pygame.draw.rect(screen, BROWN, rect, width=3, border_radius=16)

        draw_text(screen, zone["label"], fonts["tiny"], DARK, rect.centerx, rect.y + 16, center=True)

        # Decorative dotted stitch line inside each zone
        for x in range(rect.left + 18, rect.right - 18, 22):
            pygame.draw.circle(screen, BROWN, (x, rect.bottom - 18), 3)

    def draw_item_icon(self, screen, item, rect, fonts, animation_tick):
        """Draw a photo card."""
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        placed = item["name"] in self.placed_items

        pygame.draw.rect(screen, WHITE, rect, border_radius=14)
        pygame.draw.rect(screen, GREEN if hovered else DARK, rect, width=4, border_radius=14)

        image = self.images[item["name"]]
        if image is not None:
            image_area = pygame.Rect(rect.x + 8, rect.y + 8, rect.width - 16, rect.height - 16)
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
            draw_text(screen, "PLACED", fonts["tiny"], GREEN, rect.centerx, rect.y + 9, center=True)
        elif hovered:
            label = pygame.Rect(rect.x, rect.bottom - 24, rect.width, 24)
            label_surface = pygame.Surface((label.width, label.height), pygame.SRCALPHA)
            pygame.draw.rect(label_surface, (255, 255, 255, 220), label_surface.get_rect(), border_radius=8)
            screen.blit(label_surface, label.topleft)
            draw_text(screen, item["name"], fonts["tiny"], DARK, label.centerx, label.centery, center=True)

    def draw_instruction_panel(self, screen, fonts):
        """Draw the teaching/clue panel."""
        panel = pygame.Rect(70, 75, 860, 90)
        pygame.draw.rect(screen, WHITE, panel, border_radius=16)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=16)

        if self.completed:
            heading = "Scene complete"
        else:
            heading = "Festival scene"

        draw_text(screen, heading, fonts["small"], BROWN, panel.x + 20, panel.y + 12)
        draw_wrapped_text(screen, self.message, fonts["small"], DARK, panel.x + 20, panel.y + 40, panel.width - 40)

    def draw(self, screen, fonts):
        """Draw the challenge and return clickable rectangles."""
        if self.mode == "lesson":
            return self.draw_lesson(screen, fonts)

        animation_tick = pygame.time.get_ticks() // 16

        screen.fill(CREAM)
        draw_text(screen, "Pohela Boishakh Prep Puzzle", fonts["title"], DARK, 500, 35, center=True)
        self.draw_instruction_panel(screen, fonts)

        # Draw scene zones
        zone_rects = {}
        for key, zone in self.scene_zones.items():
            self.draw_zone(screen, key, zone, fonts, animation_tick)
            zone_rects[key] = zone["rect"]

        # Draw item tray
        tray = pygame.Rect(60, 495, 880, 100)
        pygame.draw.rect(screen, (230, 211, 184), tray, border_radius=18)
        pygame.draw.rect(screen, BROWN, tray, width=3, border_radius=18)
        draw_text(screen, "Item tray: drag each photo to its matching place.", fonts["tiny"], DARK, 500, 505, center=True)

        item_rects = {}
        for item in self.shuffled_items:
            rect = self.item_rect(item, animation_tick)
            if item["name"] == self.dragging_item:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rect = pygame.Rect(mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1], 120, 72)
            item_rects[item["name"]] = rect
            self.draw_item_icon(screen, item, rect, fonts, animation_tick)

        self.draw_particles(screen)

        back_button = draw_button(screen, "Back to Map", fonts["body"], 205, 625, 210, 50, GREY)
        reset_button = draw_button(screen, "Reset Puzzle", fonts["body"], 445, 625, 180, 50, YELLOW)
        done_button = None

        if self.completed:
            done_button = draw_button(screen, "Stitch Quilt Section", fonts["body"], 655, 625, 245, 50, GREEN, WHITE)

        return {
            "items": item_rects,
            "zones": zone_rects,
            "back": back_button,
            "reset": reset_button,
            "done": done_button,
        }

    def handle_click(self, mouse_pos, buttons):
        """Handle click interactions. Return 'complete', 'back', or None."""
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
                    self.message = "Drag each festival photo to its matching place."

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

        selected_data = None
        for item in self.items:
            if item["name"] == self.dragging_item:
                selected_data = item

        self.dragging_item = None

        if selected_data is None:
            return None

        for zone_key, zone_rect in buttons["zones"].items():
            if zone_rect.collidepoint(mouse_pos):
                if selected_data["zone"] == zone_key:
                    self.placed_items[selected_data["name"]] = zone_key
                    self.last_completed_item = selected_data["name"]
                    self.add_success_particles(zone_rect.center)
                    self.message = selected_data["note"]

                    if len(self.placed_items) == 5:
                        self.completed = True
                        self.message = (
                            "You built the Pohela Boishakh scene. It is made from art, music, "
                            "procession, food, clothing, and family memory. Now, stitch the quilt to reveal the festival section. "
                        )
                else:
                    self.mistake_flash = 15
                    self.message = "Good try. " + selected_data["note"]

                return None

        self.message = "Drag each festival photo to its matching place."
        return None

    def update(self):
        """Update animation state."""
        self.update_particles()

        if self.mistake_flash > 0:
            self.mistake_flash -= 1
