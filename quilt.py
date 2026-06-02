"""Quilt rendering for 5 separate Nokshi Katha section PNGs."""

import math
import os
import pygame

from settings import DARK, BROWN, WHITE, DARK_GREY
from ui import draw_text



SECTION_CONFIG = {
    "festival": {
        "file": "top_left.png",
        "rect": pygame.Rect(190, 0, 190, 380),
        "label": "Festival",
    },
    "river": {
        "file": "bottom_left.png",
        "rect": pygame.Rect(0, 0, 190, 190),
        "label": "River",
    },
    "rhythm": {
        "file": "bottom_right.png",
        "rect": pygame.Rect(380, 0, 190, 190),
        "label": "Rhythm",
    },
    "food": {
        "file": "top_right.png",
        "rect": pygame.Rect(0, 190, 190, 190),
        "label": "Food",
    },
    "symbols": {
        "file": "center_tall.png",
        "rect": pygame.Rect(380, 190, 190, 190),
        "label": "Symbols",
    },
}

QUILT_WIDTH = 570
QUILT_HEIGHT = 380

_loaded_images = {}


def load_section_image(filename, width, height):
    """Load and scale one quilt section image."""
    cache_key = (filename, width, height)
    if cache_key in _loaded_images:
        return _loaded_images[cache_key]

    path = os.path.join("assets", "quilt", filename)

    try:
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.smoothscale(image, (width, height))
        _loaded_images[cache_key] = image
        return image
    except pygame.error:
        return None
    except FileNotFoundError:
        return None


def draw_stitch_border(screen, rect, colour, animation_tick=0, animated=False):
    """Draw stitch marks around the whole quilt."""
    spacing = 18
    offset = animation_tick % spacing if animated else 0

    for x in range(rect.left + 8 - offset, rect.right - 8, spacing):
        pygame.draw.line(screen, colour, (x, rect.top + 6), (x + 8, rect.top + 6), 2)
        pygame.draw.line(screen, colour, (x, rect.bottom - 6), (x + 8, rect.bottom - 6), 2)

    for y in range(rect.top + 8 - offset, rect.bottom - 8, spacing):
        pygame.draw.line(screen, colour, (rect.left + 6, y), (rect.left + 6, y + 8), 2)
        pygame.draw.line(screen, colour, (rect.right - 6, y), (rect.right - 6, y + 8), 2)


def draw_sparkles(screen, rect, animation_tick):
    """Draw sparkle animation over a revealed tile."""
    for i in range(5):
        x = rect.left + 20 + ((animation_tick * 2 + i * 41) % max(1, rect.width - 40))
        y = rect.top + 20 + ((animation_tick + i * 31) % max(1, rect.height - 40))
        pulse = int(2 + 2 * abs(math.sin(animation_tick * 0.12 + i)))
        pygame.draw.circle(screen, WHITE, (x, y), pulse)


def draw_blurred_cover(screen, rect, reveal_progress, label, fonts, animation_tick):
    """Cover unrevealed portion of a tile with a fabric-like blur overlay."""
    cover_height = int(rect.height * (1 - reveal_progress))
    if cover_height <= 0:
        return

    cover_rect = pygame.Rect(rect.left, rect.top, rect.width, cover_height)

    overlay = pygame.Surface((cover_rect.width, cover_rect.height), pygame.SRCALPHA)
    overlay.fill((215, 205, 190, 210))

    # Fake blur/fabric texture
    for i in range(-cover_rect.height, cover_rect.width, 18):
        start_x = i + int(6 * math.sin(animation_tick * 0.05))
        pygame.draw.line(
            overlay,
            (120, 110, 100, 65),
            (start_x, 0),
            (start_x + cover_rect.height, cover_rect.height),
            3,
        )

    for i in range(20):
        dot_x = (i * 31 + animation_tick) % max(1, cover_rect.width)
        dot_y = (i * 23 + animation_tick // 2) % max(1, cover_rect.height)
        pygame.draw.circle(overlay, (255, 255, 255, 45), (dot_x, dot_y), 3)

    screen.blit(overlay, cover_rect.topleft)

    if reveal_progress == 0:
        draw_text(screen, "UNSTITCHED", fonts["small"], DARK_GREY, rect.centerx, rect.centery - 10, center=True)
        draw_text(screen, label, fonts["tiny"], DARK_GREY, rect.centerx, rect.centery + 16, center=True)


def draw_missing_notice(screen, quilt_rect, fonts, missing_files):
    """Show warning if images are missing."""
    if not missing_files:
        return

    draw_text(screen, "Missing quilt files:", fonts["tiny"], DARK, quilt_rect.centerx, quilt_rect.bottom + 10, center=True)
    draw_text(screen, ", ".join(missing_files), fonts["tiny"], DARK, quilt_rect.centerx, quilt_rect.bottom + 28, center=True)


def draw_quilt(screen, x, y, patch_size, patches, reveal_progress, fonts, animation_tick):
    """Draw the 5-section quilt."""
    quilt_rect = pygame.Rect(x, y, QUILT_WIDTH, QUILT_HEIGHT)

    # background cloth
    pygame.draw.rect(screen, (235, 217, 190), quilt_rect, border_radius=18)

    missing_files = []

    for key, config in SECTION_CONFIG.items():
        local_rect = config["rect"]
        filename = config["file"]
        label = config["label"]

        section_rect = pygame.Rect(
            x + local_rect.x,
            y + local_rect.y,
            local_rect.width,
            local_rect.height,
        )

        image = load_section_image(filename, local_rect.width, local_rect.height)
        if image is not None:
            screen.blit(image, section_rect.topleft)
        else:
            missing_files.append(filename)
            pygame.draw.rect(screen, (220, 210, 195), section_rect)
            pygame.draw.rect(screen, DARK, section_rect, 2)

        draw_blurred_cover(
            screen,
            section_rect,
            reveal_progress[key],
            label,
            fonts,
            animation_tick,
        )

        if patches[key] and reveal_progress[key] > 0.85:
            draw_sparkles(screen, section_rect, animation_tick)

    # outer border
    pygame.draw.rect(screen, DARK, quilt_rect, width=5, border_radius=18)
    draw_stitch_border(screen, quilt_rect, DARK, animation_tick, animated=True)

    draw_missing_notice(screen, quilt_rect, fonts, missing_files)


def update_reveal_progress(patches, reveal_progress, speed=0.025):
    """Advance reveal animation for completed sections."""
    for key in reveal_progress:
        if patches[key] and reveal_progress[key] < 1.0:
            reveal_progress[key] = min(1.0, reveal_progress[key] + speed)