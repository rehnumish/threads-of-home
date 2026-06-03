"""Main non-challenge screens for the game."""

import os
import pygame

from settings import (
    WIDTH, HEIGHT,
    CREAM, DARK, BROWN, LIGHT_BROWN, RED, WHITE, BLUE, GREEN, YELLOW, PURPLE, GREY
)
from ui import draw_text, draw_wrapped_text, draw_button
from quilt import draw_quilt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_IMAGE_CACHE = {}


def load_screen_image(filename, size=None, treat_black_as_transparent=False):
    """Load and optionally scale a UI image."""
    cache_key = (filename, size, treat_black_as_transparent)
    if cache_key in _IMAGE_CACHE:
        return _IMAGE_CACHE[cache_key]

    path = os.path.join(BASE_DIR, "assets", "map", filename)

    try:
        image = pygame.image.load(path).convert_alpha()

        if treat_black_as_transparent:
            image = image.copy()
            image.set_colorkey((0, 0, 0))

        if size is not None:
            image = pygame.transform.smoothscale(image, size)

        _IMAGE_CACHE[cache_key] = image
        return image
    except (pygame.error, FileNotFoundError):
        return None


def draw_shadow_text(screen, text, font, colour, x, y, center=False, shadow_colour=(245, 235, 214), offset=2):
    """Draw readable text with a soft light shadow."""
    draw_text(screen, text, font, shadow_colour, x + offset, y + offset, center=center)
    return draw_text(screen, text, font, colour, x, y, center=center)


def draw_card(screen, rect, fill=(255, 250, 245, 215), border=DARK):
    """Draw a soft card panel."""
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 0))
    pygame.draw.rect(panel, fill, panel.get_rect(), border_radius=20)
    pygame.draw.rect(panel, border, panel.get_rect(), width=3, border_radius=20)
    screen.blit(panel, rect.topleft)


def draw_non_challenge_background(screen, veil_alpha=0):
    """Draw the shared non-challenge background."""
    bg = load_screen_image("map_background.png", (WIDTH, HEIGHT))
    if bg is not None:
        screen.blit(bg, (0, 0))
    else:
        screen.fill(CREAM)

    if veil_alpha > 0:
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((245, 235, 214, veil_alpha))
        screen.blit(veil, (0, 0))

def point_in_circle(point, center, radius):
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    return dx * dx + dy * dy <= radius * radius


def triangle_area(a, b, c):
    return abs((a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2.0)


def point_in_triangle(point, a, b, c):
    whole = triangle_area(a, b, c)
    p1 = triangle_area(point, b, c)
    p2 = triangle_area(a, point, c)
    p3 = triangle_area(a, b, point)
    return abs(whole - (p1 + p2 + p3)) < 1.0


def get_map_target(mouse_pos):
    """Return which map option the mouse is really over."""
    quilt_center = (500, 340)
    quilt_radius = 170

    symbols_points = [(280, 700), (720, 700), (500, 455)]

    # priority matters: middle circle first, then cone, then background quadrants
    if point_in_circle(mouse_pos, quilt_center, quilt_radius):
        return "quilt"

    if point_in_triangle(mouse_pos, *symbols_points):
        return "symbols"

    if mouse_pos[1] < 350:
        if mouse_pos[0] < 500:
            return "festival"
        return "food"
    else:
        if mouse_pos[0] < 500:
            return "river"
        return "rhythm"
    

def draw_map_panel(screen, rect, filename, label, fonts, hovered, completed=False, shape="rect", shape_data=None):
    """Draw one map option panel."""
    image = load_screen_image(filename, (rect.width, rect.height), treat_black_as_transparent=True)

    if image is not None:
        screen.blit(image, rect.topleft)
    else:
        pygame.draw.rect(screen, LIGHT_BROWN, rect, border_radius=18)
        pygame.draw.rect(screen, WHITE, rect, width=3, border_radius=18)

    # dark overlay only on non-hovered items
    if not hovered and image is not None:
        overlay = pygame.mask.from_surface(image).to_surface(
            setcolor=(0, 0, 0, 115),
            unsetcolor=(0, 0, 0, 0)
        )
        screen.blit(overlay, rect.topleft)

    elif not hovered:
        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 115))
        screen.blit(overlay, rect.topleft)

    # hover outline by shape
    if hovered:
        if shape == "circle":
            pygame.draw.circle(screen, WHITE, shape_data["center"], shape_data["radius"], 4)
        elif shape == "triangle":
            pygame.draw.polygon(screen, WHITE, shape_data["points"], 4)
        else:
            pygame.draw.rect(screen, WHITE, rect, width=4)

    # smaller label pill instead of big strip
    label_width = max(150, fonts["map_label"].size(label)[0] + 34)
    label_rect = pygame.Rect(0, 0, label_width, 48)

    if shape == "circle":
        label_rect.center = (shape_data["center"][0], shape_data["center"][1] + 130)
    elif shape == "triangle":
        label_rect.center = (shape_data["label_pos"][0], shape_data["label_pos"][1])
    else:
        label_rect.center = (rect.centerx, rect.bottom - 28)

    pill = pygame.Surface((label_rect.width, label_rect.height), pygame.SRCALPHA)
    pill.fill((0, 0, 0, 0))
    pygame.draw.rect(pill, (0, 0, 0, 110 if hovered else 135), pill.get_rect(), border_radius=18)
    pygame.draw.rect(pill, WHITE, pill.get_rect(), width=2, border_radius=18)
    screen.blit(pill, label_rect.topleft)

    draw_shadow_text(
        screen,
        label,
        fonts["map_label"],
        WHITE,
        label_rect.centerx,
        label_rect.centery,
        center=True
    )

    if completed:
        badge = pygame.Rect(rect.x + 14, rect.y + 14, 80, 28)
        badge_surface = pygame.Surface((badge.width, badge.height), pygame.SRCALPHA)
        pygame.draw.rect(badge_surface, (62, 145, 89, 220), badge_surface.get_rect(), border_radius=12)
        pygame.draw.rect(badge_surface, WHITE, badge_surface.get_rect(), width=2, border_radius=12)
        screen.blit(badge_surface, badge.topleft)
        draw_text(screen, "DONE", fonts["tiny"], WHITE, badge.centerx, badge.centery, center=True)

    return rect
def draw_wrapped_centered_text(screen, text, font, colour, center_x, y, max_width, line_gap=8):
    """Draw wrapped text centered line by line."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    current_y = y
    for line in lines:
        draw_text(screen, line, font, colour, center_x, current_y, center=True)
        current_y += font.get_height() + line_gap

    return current_y

def draw_menu(screen, fonts):
    """Draw the main menu."""
    draw_non_challenge_background(screen, veil_alpha=20)

    card = pygame.Rect(120, 35, 760, 530)

    panel = pygame.Surface((card.width, card.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 245, 238, 238), panel.get_rect(), border_radius=22)
    pygame.draw.rect(panel, DARK, panel.get_rect(), width=3, border_radius=22)
    screen.blit(panel, card.topleft)

    draw_text(
        screen,
        "Threads of Home",
        fonts["title"],
        DARK,
        500,
        105,
        center=True,
    )

    draw_text(
        screen,
        "Stitching a Nokshi Katha",
        fonts["heading"],
        BROWN,
        500,
        175,
        center=True,
    )

    draw_wrapped_centered_text(
        screen,
        "Complete cultural challenges to reveal a memory quilt.",
        fonts["body"],
        DARK,
        500,
        250,
        520,
        line_gap=10,
    )

    start_button = draw_button(screen, "Start Journey", fonts["body"], 380, 350, 240, 60)
    quit_button = draw_button(screen, "Quit", fonts["body"], 380, 430, 240, 60, GREY)

    return {"start": start_button, "quit": quit_button}


def draw_intro(screen, fonts):
    """Draw the story intro."""
    draw_non_challenge_background(screen, veil_alpha=35)

    card = pygame.Rect(70, 35, 860, 610)

    panel = pygame.Surface((card.width, card.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 245, 238, 238), panel.get_rect(), border_radius=22)
    pygame.draw.rect(panel, DARK, panel.get_rect(), width=3, border_radius=22)
    screen.blit(panel, card.topleft)

    draw_text(screen, "Story", fonts["title"], DARK, 500, 85, center=True)

    story_text = (
        "You are a Bangladeshi child growing up far from home. "
        "One day, your grandparent gives you an unfinished Nokshi Katha. "
        "This is no ordinary quilt. "
        "For centuries, women in Bengal stitched Nokshi Katha by hand, "
        "weaving memories, patterns, and stories into every thread. "
        "Now, its unfinished pieces are waiting for you. "
        "Each empty section holds a memory waiting to be discovered. "
        "Complete each challenge to stitch the stories of Bangladesh back together."
    )

    draw_wrapped_centered_text(
    screen,
    story_text,
    fonts["body"],
    DARK,
    500,
    155,
    760,
    line_gap=10,
    )

    continue_button = draw_button(screen, "Continue", fonts["body"], 390, 555, 220, 60)

    return {"continue": continue_button}



def point_in_circle(point, center, radius):
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    return dx * dx + dy * dy <= radius * radius


def triangle_area(a, b, c):
    return abs(
        (
            a[0] * (b[1] - c[1])
            + b[0] * (c[1] - a[1])
            + c[0] * (a[1] - b[1])
        ) / 2.0
    )


def point_in_triangle(point, a, b, c):
    whole = triangle_area(a, b, c)
    p1 = triangle_area(point, b, c)
    p2 = triangle_area(a, point, c)
    p3 = triangle_area(a, b, point)
    return abs(whole - (p1 + p2 + p3)) < 1.5


def get_map_target(mouse_pos):
    """Return the actual hovered map section using shapes, not overlapping rectangles."""
    quilt_center = (500, 350)
    quilt_radius = 168

    symbols_points = [
        (300, 700),
        (700, 700),
        (500, 395),
    ]

  
    # Circle first, then cone, then the four background regions.
    if point_in_circle(mouse_pos, quilt_center, quilt_radius):
        return "quilt"

    if point_in_triangle(mouse_pos, *symbols_points):
        return "symbols"

    if mouse_pos[1] < 350:
        if mouse_pos[0] < 500:
            return "festival"
        return "food"

    if mouse_pos[0] < 500:
        return "river"

    return "rhythm"


def draw_shape_overlay(screen, shape, hovered=False):
    """Draw dark overlay on non-hovered area or bright highlight on hovered area."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    if hovered:
        colour = (255, 255, 255, 55)
        border_colour = (255, 255, 255, 230)
        border_width = 4
    else:
        colour = (0, 0, 0, 70)
        border_colour = None
        border_width = 0

    if shape["type"] == "rect":
        pygame.draw.rect(overlay, colour, shape["rect"])

        if hovered:
            pygame.draw.rect(overlay, border_colour, shape["rect"], width=border_width)

    elif shape["type"] == "circle":
        pygame.draw.circle(overlay, colour, shape["center"], shape["radius"])

        if hovered:
            pygame.draw.circle(overlay, border_colour, shape["center"], shape["radius"], border_width)

    elif shape["type"] == "triangle":
        pygame.draw.polygon(overlay, colour, shape["points"])

        if hovered:
            pygame.draw.polygon(overlay, border_colour, shape["points"], border_width)

    screen.blit(overlay, (0, 0))


def draw_label_pill(screen, text, fonts, x, y, hovered=False):
    """Draw a readable label button."""
    label_width = max(155, fonts["map_label"].size(text)[0] + 42)
    label_rect = pygame.Rect(0, 0, label_width, 48)
    label_rect.center = (x, y)

    pill = pygame.Surface((label_rect.width, label_rect.height), pygame.SRCALPHA)

    if hovered:
        fill = (255, 255, 255, 210)
        border = (35, 30, 30, 240)
        text_colour = DARK
    else:
        fill = (0, 0, 0, 140)
        border = (255, 255, 255, 220)
        text_colour = WHITE

    pygame.draw.rect(pill, fill, pill.get_rect(), border_radius=18)
    pygame.draw.rect(pill, border, pill.get_rect(), width=2, border_radius=18)
    screen.blit(pill, label_rect.topleft)

    draw_text(screen, text, fonts["map_label"], text_colour, label_rect.centerx, label_rect.centery, center=True)

    return label_rect


def draw_map_piece(screen, filename, rect, backing=None):
    """Draw a map artwork piece, optionally with a backing shape behind it."""
    image = load_screen_image(filename, (rect.width, rect.height), treat_black_as_transparent=True)

    if backing == "circle":
        centre = rect.center
        radius = min(rect.width, rect.height) // 2

        # solid backing so other map sections do not show through transparent parts
        pygame.draw.circle(screen, (70, 135, 80), centre, radius)

    elif backing == "triangle":
        points = [
            (rect.centerx, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom),
        ]

        # solid backing for the symbols cone
        pygame.draw.polygon(screen, (45, 75, 120), points)

    if image is not None:
        screen.blit(image, rect.topleft)
    else:
        pygame.draw.rect(screen, (180, 150, 120), rect)


def draw_map(screen, fonts, patches):
    """Draw the challenge selection map with artwork pieces and shaped hover areas."""
    draw_non_challenge_background(screen, veil_alpha=0)

    mouse_pos = pygame.mouse.get_pos()
    hovered_key = get_map_target(mouse_pos)

    shapes = {
        "festival": {
            "type": "rect",
            "rect": pygame.Rect(0, 0, 500, 350),
            "label": (245, 320),
            "file": "festival.png",
        },
        "food": {
            "type": "rect",
            "rect": pygame.Rect(500, 0, 500, 350),
            "label": (745, 320),
            "file": "food.png",
        },
        "river": {
            "type": "rect",
            "rect": pygame.Rect(0, 350, 500, 350),
            "label": (235, 670),
            "file": "river.png",
        },
        "rhythm": {
            "type": "rect",
            "rect": pygame.Rect(500, 350, 500, 350),
            "label": (760, 670),
            "file": "rythm.png",
        },
        "symbols": {
            "type": "triangle",
            "points": [(300, 700), (700, 700), (500, 395)],
            "rect": pygame.Rect(300, 395, 400, 305),
            "label": (500, 670),
            "file": "symbols.png",
        },
        "quilt": {
            "type": "circle",
            "center": (500, 350),
            "radius": 168,
            "rect": pygame.Rect(332, 182, 336, 336),
            "label": (500, 490),
            "file": "quilt.png",
        },
    }

    # 1. Draw section artwork first
    draw_map_piece(screen, shapes["festival"]["file"], shapes["festival"]["rect"])
    draw_map_piece(screen, shapes["food"]["file"], shapes["food"]["rect"])
    draw_map_piece(screen, shapes["river"]["file"], shapes["river"]["rect"])
    draw_map_piece(screen, shapes["rhythm"]["file"], shapes["rhythm"]["rect"])

    # Symbols and quilt go on top because they overlap the lower/centre sections
    draw_map_piece(screen, shapes["symbols"]["file"], shapes["symbols"]["rect"], backing="triangle")
    draw_map_piece(screen, shapes["quilt"]["file"], shapes["quilt"]["rect"], backing="circle")

    # 2. Add dark overlay to non-hovered sections
    for key in ["festival", "food", "river", "rhythm", "symbols", "quilt"]:
        draw_shape_overlay(screen, shapes[key], hovered=(hovered_key == key))

    # 3. Title box
    title_rect = pygame.Rect(250, 42, 500, 64)
    title_panel = pygame.Surface((title_rect.width, title_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(title_panel, (0, 0, 0, 145), title_panel.get_rect(), border_radius=12)
    screen.blit(title_panel, title_rect.topleft)

    draw_text(
        screen,
        "Choose a Cultural Challenge",
        fonts["heading"],
        WHITE,
        title_rect.centerx,
        title_rect.centery,
        center=True,
    )

    # 4. Labels
    buttons = {}

    buttons["festival"] = draw_label_pill(
        screen, "Festival", fonts, *shapes["festival"]["label"], hovered=(hovered_key == "festival")
    )

    buttons["food"] = draw_label_pill(
        screen, "Food", fonts, *shapes["food"]["label"], hovered=(hovered_key == "food")
    )

    buttons["river"] = draw_label_pill(
        screen, "River", fonts, *shapes["river"]["label"], hovered=(hovered_key == "river")
    )

    buttons["rhythm"] = draw_label_pill(
        screen, "Rhythm", fonts, *shapes["rhythm"]["label"], hovered=(hovered_key == "rhythm")
    )

    buttons["symbols"] = draw_label_pill(
        screen, "Symbols", fonts, *shapes["symbols"]["label"], hovered=(hovered_key == "symbols")
    )

    buttons["quilt"] = draw_label_pill(
        screen, "Nokshi Katha", fonts, *shapes["quilt"]["label"], hovered=(hovered_key == "quilt")
    )

    # 5. Done badges
    for key in ["festival", "food", "river", "rhythm", "symbols"]:
        if patches[key]:
            badge_x = shapes[key]["label"][0] - 58
            badge_y = shapes[key]["label"][1] - 70

            badge = pygame.Rect(badge_x, badge_y, 116, 30)
            badge_surface = pygame.Surface((badge.width, badge.height), pygame.SRCALPHA)
            pygame.draw.rect(badge_surface, (62, 145, 89, 220), badge_surface.get_rect(), border_radius=12)
            pygame.draw.rect(badge_surface, WHITE, badge_surface.get_rect(), width=2, border_radius=12)
            screen.blit(badge_surface, badge.topleft)
            draw_text(screen, "DONE", fonts["tiny"], WHITE, badge.centerx, badge.centery, center=True)

    completed = sum(1 for value in patches.values() if value)

    info_rect = pygame.Rect(18, 650, 170, 36)
    info_panel = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(info_panel, (0, 0, 0, 145), info_panel.get_rect(), border_radius=10)
    screen.blit(info_panel, info_rect.topleft)

    draw_text(
        screen,
        f"Revealed: {completed} / 5",
        fonts["small"],
        WHITE,
        info_rect.centerx,
        info_rect.centery,
        center=True,
    )

    final_button = None
    if all(patches.values()):
        final_button = draw_button(screen, "View Completed Quilt", fonts["small"], 760, 645, 210, 40, GREEN, WHITE)

    buttons["final"] = final_button
    buttons["_hit_test"] = get_map_target

    return buttons


def draw_quilt_screen(screen, fonts, patches, reveal_progress, animation_tick):
    """Draw the quilt progress screen."""
    draw_non_challenge_background(screen, veil_alpha=55)

    card = pygame.Rect(120, 35, 760, 630)
    draw_card(screen, card)

    draw_shadow_text(screen, "Nokshi Katha Progress", fonts["title"], DARK, 500, 78, center=True)
    draw_quilt(screen, 215, 140, 190, patches, reveal_progress, fonts, animation_tick)

    completed = sum(1 for value in patches.values() if value)
    draw_text(screen, f"{completed} of 5 memory sections revealed", fonts["body"], DARK, 500, 590, center=True)

    back_button = draw_button(screen, "Back to Map", fonts["body"], 390, 615, 220, 45, GREY)
    return {"back": back_button}


def draw_final_screen(screen, fonts, patches, reveal_progress, animation_tick):
    """Draw the final completed quilt screen."""
    draw_non_challenge_background(screen, veil_alpha=55)

    card = pygame.Rect(120, 25, 760, 645)
    draw_card(screen, card)

    draw_shadow_text(screen, "The Nokshi Katha is Complete", fonts["title"], DARK, 500, 68, center=True)
    draw_quilt(screen, 215, 130, 190, patches, reveal_progress, fonts, animation_tick)

    message = "Identity is stitched memory by memory, just like a Nokshi Katha."
    draw_text(screen, message, fonts["body"], DARK, 500, 585, center=True)

    back_button = draw_button(screen, "Return to Map", fonts["body"], 390, 615, 220, 45, GREY)
    return {"back": back_button}