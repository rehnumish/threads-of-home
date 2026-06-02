"""Pohela Boishakh puzzle challenge.


The player builds a Pohela Boishakh celebration scene by placing cultural items
into the correct glowing areas. The challenge uses:
- sequential puzzle steps
- click-to-select and click-to-place interaction
- animated item bobbing
- pulsing target areas
- success particles
- teaching feedback after each action
"""

import math
import random
import pygame

from settings import (
    CREAM, DARK, BROWN, RED, WHITE, BLUE, GREEN, YELLOW, GREY,
    DARK_GREY, BLACK, ORANGE, PINK, PURPLE
)
from ui import draw_text, draw_wrapped_text, draw_button


class FestivalChallenge:
    """A guided Pohela Boishakh scene-building puzzle."""

    def __init__(self):
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
                "name": "Alpana",
                "zone": "courtyard",
                "home": (105, 520),
                "colour": WHITE,
                "note": "Alpana is decorative floor art. In this scene it belongs in the courtyard, where it welcomes people into the celebration.",
            },
            {
                "name": "Dhol",
                "zone": "music",
                "home": (255, 520),
                "colour": YELLOW,
                "note": "The dhol is a drum. It belongs in the music corner because rhythm helps create the energy of the festival.",
            },
            {
                "name": "Mask",
                "zone": "procession",
                "home": (405, 520),
                "colour": RED,
                "note": "Colourful masks are connected with Mangal Shobhajatra, a festive procession for Bengali New Year.",
            },
            {
                "name": "Pitha",
                "zone": "food",
                "home": (555, 520),
                "colour": ORANGE,
                "note": "Pitha belongs on the food table. Food connects festivals with family, memory, and sharing.",
            },
            {
                "name": "Red-White Outfit",
                "zone": "outfit",
                "home": (705, 520),
                "colour": PINK,
                "note": "Red and white clothing is commonly associated with Pohela Boishakh celebration outfits.",
            },
            {
                "name": "Random Toy",
                "zone": "decoy",
                "home": (855, 520),
                "colour": BLUE,
                "note": "This might be fun, but it does not help complete this Pohela Boishakh scene.",
            },
        ]

        self.steps = [
            {
                "zone": "courtyard",
                "clue": "First, prepare the entrance. Bengali New Year celebrations often use decorative floor patterns to welcome people. Which item should go in the courtyard?",
            },
            {
                "zone": "music",
                "clue": "Now add sound. A festival feels alive when rhythm leads the crowd. Which item belongs in the music corner?",
            },
            {
                "zone": "procession",
                "clue": "Next, build the procession. Mangal Shobhajatra is known for colourful symbolic masks and folk art. Which item belongs there?",
            },
            {
                "zone": "food",
                "clue": "Now make the celebration feel like family. Traditional sweets and snacks are shared during festive gatherings. What goes on the food table?",
            },
            {
                "zone": "outfit",
                "clue": "Finally, dress for the day. Red and white are strongly associated with Pohela Boishakh. What belongs on the outfit stand?",
            },
        ]

        self.reset()

    def reset(self):
        """Reset the puzzle to its starting state."""
        self.current_step = 0
        self.selected_item = None
        self.placed_items = {}
        self.message = self.steps[0]["clue"]
        self.completed = False
        self.success_particles = []
        self.mistake_flash = 0
        self.last_completed_item = None

    def current_zone_key(self):
        """Return the zone key required for the current puzzle step."""
        if self.current_step >= len(self.steps):
            return None
        return self.steps[self.current_step]["zone"]

    def item_rect(self, item, animation_tick):
        """Return the current rectangle for an item, including gentle bobbing animation."""
        home_x, home_y = item["home"]

        # Placed items move to the centre of their assigned zone.
        if item["name"] in self.placed_items:
            zone_rect = self.scene_zones[item["zone"]]["rect"]
            return pygame.Rect(zone_rect.centerx - 55, zone_rect.centery - 35, 110, 70)

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

        self.success_particles = [p for p in self.success_particles if p["life"] > 0]

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
        required_zone = self.current_zone_key()
        is_active = zone_key == required_zone and not self.completed

        pygame.draw.rect(screen, zone["colour"], rect, border_radius=16)

        if is_active:
            pulse = int(4 + 3 * abs(math.sin(animation_tick * 0.08)))
            pygame.draw.rect(screen, GREEN, rect.inflate(pulse, pulse), width=5, border_radius=18)
        else:
            pygame.draw.rect(screen, BROWN, rect, width=3, border_radius=16)

        draw_text(screen, zone["label"], fonts["tiny"], DARK, rect.centerx, rect.y + 16, center=True)

        # Decorative dotted stitch line inside each zone
        for x in range(rect.left + 18, rect.right - 18, 22):
            pygame.draw.circle(screen, BROWN, (x, rect.bottom - 18), 3)

    def draw_item_icon(self, screen, item, rect, fonts, animation_tick):
        """Draw a simple shape-based item icon."""
        selected = self.selected_item == item["name"]
        placed = item["name"] in self.placed_items

        bg_colour = item["colour"]
        if placed:
            bg_colour = tuple(max(0, c - 20) for c in bg_colour)

        pygame.draw.rect(screen, bg_colour, rect, border_radius=14)
        pygame.draw.rect(screen, GREEN if selected else DARK, rect, width=4, border_radius=14)

        name = item["name"]

        if name == "Alpana":
            pygame.draw.circle(screen, RED, rect.center, 20)
            pygame.draw.circle(screen, WHITE, rect.center, 9)
            for dx, dy in [(0, -28), (0, 28), (-28, 0), (28, 0)]:
                pygame.draw.circle(screen, RED, (rect.centerx + dx, rect.centery + dy), 6)

        elif name == "Dhol":
            pygame.draw.ellipse(screen, BROWN, (rect.centerx - 35, rect.centery - 24, 70, 22))
            pygame.draw.rect(screen, BROWN, (rect.centerx - 35, rect.centery - 14, 70, 38))
            pygame.draw.ellipse(screen, YELLOW, (rect.centerx - 35, rect.centery + 12, 70, 22))
            pygame.draw.line(screen, DARK, (rect.centerx - 45, rect.centery - 25), (rect.centerx + 45, rect.centery + 25), 3)

        elif name == "Mask":
            pygame.draw.ellipse(screen, ORANGE, (rect.centerx - 30, rect.centery - 30, 60, 58))
            pygame.draw.circle(screen, DARK, (rect.centerx - 14, rect.centery - 8), 5)
            pygame.draw.circle(screen, DARK, (rect.centerx + 14, rect.centery - 8), 5)
            pygame.draw.arc(screen, DARK, (rect.centerx - 18, rect.centery + 4, 36, 18), 0, 3.14, 3)

        elif name == "Pitha":
            pygame.draw.circle(screen, WHITE, rect.center, 26)
            pygame.draw.circle(screen, ORANGE, rect.center, 18)
            pygame.draw.circle(screen, WHITE, rect.center, 7)

        elif name == "Red-White Outfit":
            pygame.draw.polygon(screen, WHITE, [
                (rect.centerx, rect.centery - 30),
                (rect.centerx - 27, rect.centery + 28),
                (rect.centerx + 27, rect.centery + 28),
            ])
            pygame.draw.line(screen, RED, (rect.centerx - 20, rect.centery), (rect.centerx + 20, rect.centery), 5)

        elif name == "Random Toy":
            pygame.draw.circle(screen, PURPLE, rect.center, 24)
            pygame.draw.circle(screen, WHITE, (rect.centerx - 8, rect.centery - 5), 5)
            pygame.draw.circle(screen, WHITE, (rect.centerx + 8, rect.centery - 5), 5)
            pygame.draw.rect(screen, DARK, (rect.centerx - 16, rect.centery + 10, 32, 5))

        label_colour = DARK if item["colour"] != BLUE else WHITE
        if placed:
            draw_text(screen, "PLACED", fonts["tiny"], GREEN, rect.centerx, rect.y + 9, center=True)
        else:
            draw_text(screen, name, fonts["tiny"], label_colour, rect.centerx, rect.bottom - 16, center=True)

    def draw_instruction_panel(self, screen, fonts):
        """Draw the teaching/clue panel."""
        panel = pygame.Rect(70, 75, 860, 90)
        pygame.draw.rect(screen, WHITE, panel, border_radius=16)
        pygame.draw.rect(screen, DARK, panel, width=3, border_radius=16)

        if self.completed:
            heading = "Scene complete"
        else:
            heading = f"Puzzle step {self.current_step + 1} of {len(self.steps)}"

        draw_text(screen, heading, fonts["small"], BROWN, panel.x + 20, panel.y + 12)
        draw_wrapped_text(screen, self.message, fonts["small"], DARK, panel.x + 20, panel.y + 40, panel.width - 40)

    def draw(self, screen, fonts):
        """Draw the challenge and return clickable rectangles."""
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
        draw_text(screen, "Item tray: click an item, then click the glowing area.", fonts["tiny"], DARK, 500, 505, center=True)

        item_rects = {}
        for item in self.items:
            rect = self.item_rect(item, animation_tick)
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
        if buttons["back"].collidepoint(mouse_pos):
            return "back"

        if buttons["reset"].collidepoint(mouse_pos):
            self.reset()
            return None

        if self.completed:
            if buttons["done"] is not None and buttons["done"].collidepoint(mouse_pos):
                return "complete"
            return None

        # Select an item from the tray or already visible objects.
        for item in self.items:
            if item["name"] in self.placed_items:
                continue

            if buttons["items"][item["name"]].collidepoint(mouse_pos):
                self.selected_item = item["name"]

                if item["zone"] == "decoy":
                    self.message = item["note"] + " Try using the clue to find a cultural item."
                else:
                    self.message = item["note"] + " Now place it in the glowing area if it matches the clue."
                return None

        # Place the selected item into a zone.
        if self.selected_item is not None:
            for zone_key, zone_rect in buttons["zones"].items():
                if zone_rect.collidepoint(mouse_pos):
                    selected_data = next(item for item in self.items if item["name"] == self.selected_item)
                    required_zone = self.current_zone_key()

                    if selected_data["zone"] == required_zone and zone_key == required_zone:
                        self.placed_items[self.selected_item] = zone_key
                        self.last_completed_item = self.selected_item
                        self.add_success_particles(zone_rect.center)

                        self.current_step += 1
                        self.selected_item = None

                        if self.current_step >= len(self.steps):
                            self.completed = True
                            self.message = (
                                "You built the Pohela Boishakh scene. Notice how the celebration is not one object: "
                                "it is made from art, music, procession, food, clothing, and family memory."
                            )
                        else:
                            self.message = self.steps[self.current_step]["clue"]

                    else:
                        self.mistake_flash = 15
                        self.message = (
                            "Good try. This puzzle is teaching the meaning, not testing you. "
                            f"{selected_data['note']} Look again at the glowing area and clue."
                        )

                    return None

        return None

    def update(self):
        """Update animation state."""
        self.update_particles()

        if self.mistake_flash > 0:
            self.mistake_flash -= 1
