"""Main non-challenge screens for the game."""

import pygame

from settings import WIDTH, HEIGHT, CREAM, DARK, BROWN, LIGHT_BROWN, WHITE, GREEN, GREY
from ui import draw_text, draw_button
from quilt import draw_quilt


SYMBOLS_POINTS = [(280, 700), (725, 700), (500, 355)]
SYMBOLS_RECT = pygame.Rect(280, 455, 460, 280)

background_image = None
festival_image = None
food_image = None
river_image = None
rhythm_image = None
symbols_image = None
quilt_image = None


def load_map_image(filename, size=None, black_is_clear=False):
    try:
        image = pygame.image.load("assets/map/" + filename).convert_alpha()

        if black_is_clear:
            image.set_colorkey((0, 0, 0))

        if size is not None:
            image = pygame.transform.smoothscale(image, size)

        return image
    except (pygame.error, FileNotFoundError):
        return None


def load_images_once():
    global background_image
    global festival_image
    global food_image
    global river_image
    global rhythm_image
    global symbols_image
    global quilt_image

    if background_image is None:
        background_image = load_map_image("map_background.png", (WIDTH, HEIGHT))
        festival_image = load_map_image("festival.png", (500, 350), black_is_clear=True)
        food_image = load_map_image("food.png", (500, 350), black_is_clear=True)
        river_image = load_map_image("river.png", (500, 350), black_is_clear=True)
        rhythm_image = load_map_image("rythm.png", (500, 350), black_is_clear=True)
        symbols_image = load_map_image("symbols.png", black_is_clear=True)
        quilt_image = load_map_image("quilt.png", (336, 336), black_is_clear=True)


def draw_shadow_text(screen, text, font, colour, x, y, center=False):
    draw_text(screen, text, font, CREAM, x + 2, y + 2, center=center)
    draw_text(screen, text, font, colour, x, y, center=center)


def draw_card(screen, rect):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 245, 238, 238), panel.get_rect(), border_radius=22)
    pygame.draw.rect(panel, DARK, panel.get_rect(), width=3, border_radius=22)
    screen.blit(panel, rect.topleft)


def draw_background(screen, veil_alpha=0):
    load_images_once()

    if background_image is not None:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(CREAM)

    if veil_alpha > 0:
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((245, 235, 214, veil_alpha))
        screen.blit(veil, (0, 0))


def draw_centered_words(screen, text, font, colour, center_x, y, max_width, line_gap=8):
    words = text.split()
    line = ""

    for word in words:
        test_line = line + " " + word
        test_line = test_line.strip()

        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            draw_text(screen, line, font, colour, center_x, y, center=True)
            y += font.get_height() + line_gap
            line = word

    if line != "":
        draw_text(screen, line, font, colour, center_x, y, center=True)
        y += font.get_height() + line_gap

    return y


def point_in_circle(point, center, radius):
    x_distance = point[0] - center[0]
    y_distance = point[1] - center[1]
    return x_distance * x_distance + y_distance * y_distance <= radius * radius


def triangle_area(a, b, c):
    area = (
        a[0] * (b[1] - c[1])
        + b[0] * (c[1] - a[1])
        + c[0] * (a[1] - b[1])
    ) / 2
    return abs(area)


def point_in_triangle(point, a, b, c):
    big_area = triangle_area(a, b, c)
    area_1 = triangle_area(point, b, c)
    area_2 = triangle_area(a, point, c)
    area_3 = triangle_area(a, b, point)
    return abs(big_area - (area_1 + area_2 + area_3)) < 1.5


def get_map_target(mouse_pos):
    if point_in_circle(mouse_pos, (500, 350), 168):
        return "quilt"

    if point_in_triangle(mouse_pos, SYMBOLS_POINTS[0], SYMBOLS_POINTS[1], SYMBOLS_POINTS[2]):
        return "symbols"

    if mouse_pos[1] < 350:
        if mouse_pos[0] < 500:
            return "festival"
        return "food"

    if mouse_pos[0] < 500:
        return "river"

    return "rhythm"


def draw_label(screen, text, fonts, x, y, hovered=False):
    width = fonts["map_label"].size(text)[0] + 42

    if width < 155:
        width = 155

    rect = pygame.Rect(0, 0, width, 48)
    rect.center = (x, y)

    label_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    if hovered:
        fill = (255, 255, 255, 210)
        border = DARK
        text_colour = DARK
    else:
        fill = (0, 0, 0, 140)
        border = WHITE
        text_colour = WHITE

    pygame.draw.rect(label_surface, fill, label_surface.get_rect(), border_radius=18)
    pygame.draw.rect(label_surface, border, label_surface.get_rect(), width=2, border_radius=18)
    screen.blit(label_surface, rect.topleft)
    draw_text(screen, text, fonts["map_label"], text_colour, rect.centerx, rect.centery, center=True)

    return rect


def draw_map_image(screen, image, rect):
    if image is not None:
        screen.blit(image, rect.topleft)
    else:
        pygame.draw.rect(screen, LIGHT_BROWN, rect)


def draw_symbols_piece(screen):
    pygame.draw.polygon(screen, (75, 120, 205), SYMBOLS_POINTS)

    image = symbols_image

    if image is None:
        return

    max_width = SYMBOLS_RECT.width * 0.68
    max_height = SYMBOLS_RECT.height * 0.55
    scale = min(max_width / image.get_width(), max_height / image.get_height())

    new_width = int(image.get_width() * scale)
    new_height = int(image.get_height() * scale)
    image = pygame.transform.smoothscale(image, (new_width, new_height))

    image_x = SYMBOLS_RECT.centerx - image.get_width() // 2
    image_y = SYMBOLS_RECT.top + int(SYMBOLS_RECT.height * 0.74) - image.get_height() // 2
    screen.blit(image, (image_x, image_y))


def draw_quilt_piece(screen):
    rect = pygame.Rect(332, 182, 336, 336)
    pygame.draw.circle(screen, (112, 222, 139), rect.center, 168)
    draw_map_image(screen, quilt_image, rect)


def draw_overlay(screen, shape, hovered):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    if hovered:
        fill = (255, 255, 255, 55)
        border = WHITE
    else:
        fill = (0, 0, 0, 70)
        border = None

    if shape["kind"] == "rect":
        pygame.draw.rect(overlay, fill, shape["rect"])

        if hovered:
            pygame.draw.rect(overlay, border, shape["rect"], width=4)

    elif shape["kind"] == "triangle":
        pygame.draw.polygon(overlay, fill, SYMBOLS_POINTS)

        if hovered:
            pygame.draw.polygon(overlay, border, SYMBOLS_POINTS, width=4)

    elif shape["kind"] == "circle":
        if not hovered:
            fill = (0, 0, 0, 20)

        pygame.draw.circle(overlay, fill, (500, 350), 168)

        if hovered:
            pygame.draw.circle(overlay, border, (500, 350), 168, width=4)

    screen.blit(overlay, (0, 0))


def draw_menu(screen, fonts):
    draw_background(screen, veil_alpha=20)

    card = pygame.Rect(120, 35, 760, 530)
    draw_card(screen, card)

    draw_text(screen, "Threads of Home", fonts["title"], DARK, 500, 105, center=True)
    draw_text(screen, "Stitching a Nokshi Katha", fonts["heading"], BROWN, 500, 175, center=True)

    draw_centered_words(
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
    draw_background(screen, veil_alpha=35)

    card = pygame.Rect(70, 35, 860, 610)
    draw_card(screen, card)

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

    draw_centered_words(screen, story_text, fonts["body"], DARK, 500, 155, 760, line_gap=10)

    continue_button = draw_button(screen, "Continue", fonts["body"], 390, 555, 220, 60)

    return {"continue": continue_button}


def draw_map(screen, fonts, patches):
    draw_background(screen)

    mouse_pos = pygame.mouse.get_pos()
    hovered = get_map_target(mouse_pos)

    shapes = {
        "festival": {"kind": "rect", "rect": pygame.Rect(0, 0, 500, 350), "label": (245, 320)},
        "food": {"kind": "rect", "rect": pygame.Rect(500, 0, 500, 350), "label": (745, 320)},
        "river": {"kind": "rect", "rect": pygame.Rect(0, 350, 500, 350), "label": (235, 635)},
        "rhythm": {"kind": "rect", "rect": pygame.Rect(500, 350, 500, 350), "label": (760, 635)},
        "symbols": {"kind": "triangle", "label": (500, 635)},
        "quilt": {"kind": "circle", "label": (500, 490)},
    }

    draw_map_image(screen, festival_image, shapes["festival"]["rect"])
    draw_map_image(screen, food_image, shapes["food"]["rect"])
    draw_map_image(screen, river_image, shapes["river"]["rect"])
    draw_map_image(screen, rhythm_image, shapes["rhythm"]["rect"])

    for key in ["festival", "food", "river", "rhythm"]:
        draw_overlay(screen, shapes[key], hovered == key)

    draw_symbols_piece(screen)
    draw_overlay(screen, shapes["symbols"], hovered == "symbols")

    draw_quilt_piece(screen)
    draw_overlay(screen, shapes["quilt"], hovered == "quilt")

    title_rect = pygame.Rect(250, 42, 500, 64)
    title_panel = pygame.Surface((title_rect.width, title_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(title_panel, (0, 0, 0, 145), title_panel.get_rect(), border_radius=12)
    screen.blit(title_panel, title_rect.topleft)
    draw_text(screen, "Choose a Cultural Challenge", fonts["heading"], WHITE, 500, 74, center=True)

    buttons = {}
    buttons["festival"] = draw_label(screen, "Festival", fonts, 245, 320, hovered == "festival")
    buttons["food"] = draw_label(screen, "Food", fonts, 745, 320, hovered == "food")
    buttons["river"] = draw_label(screen, "River", fonts, 235, 635, hovered == "river")
    buttons["rhythm"] = draw_label(screen, "Rhythm", fonts, 760, 635, hovered == "rhythm")
    buttons["symbols"] = draw_label(screen, "Symbols", fonts, 500, 635, hovered == "symbols")
    buttons["quilt"] = draw_label(screen, "Nokshi Katha", fonts, 500, 490, hovered == "quilt")

    for key in ["festival", "food", "river", "rhythm", "symbols"]:
        if patches[key]:
            label_x = shapes[key]["label"][0]
            label_y = shapes[key]["label"][1]
            badge = pygame.Rect(label_x - 58, label_y - 70, 116, 30)
            badge_surface = pygame.Surface((badge.width, badge.height), pygame.SRCALPHA)
            pygame.draw.rect(badge_surface, (62, 145, 89, 220), badge_surface.get_rect(), border_radius=12)
            pygame.draw.rect(badge_surface, WHITE, badge_surface.get_rect(), width=2, border_radius=12)
            screen.blit(badge_surface, badge.topleft)
            draw_text(screen, "DONE", fonts["tiny"], WHITE, badge.centerx, badge.centery, center=True)

    completed = 0

    for value in patches.values():
        if value:
            completed += 1

    info_rect = pygame.Rect(18, 650, 170, 36)
    info_panel = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(info_panel, (0, 0, 0, 145), info_panel.get_rect(), border_radius=10)
    screen.blit(info_panel, info_rect.topleft)
    draw_text(screen, "Revealed: " + str(completed) + " / 5", fonts["small"], WHITE, info_rect.centerx, info_rect.centery, center=True)

    final_button = None

    if all(patches.values()):
        final_button = draw_button(screen, "View Completed Quilt", fonts["small"], 760, 645, 210, 40, GREEN, WHITE)

    buttons["final"] = final_button
    buttons["_hit_test"] = get_map_target

    return buttons


def draw_quilt_screen(screen, fonts, patches, reveal_progress, animation_tick):
    draw_background(screen, veil_alpha=55)

    card = pygame.Rect(120, 35, 760, 630)
    draw_card(screen, card)

    draw_shadow_text(screen, "Nokshi Katha Progress", fonts["title"], DARK, 500, 78, center=True)
    draw_quilt(screen, 215, 140, 190, patches, reveal_progress, fonts, animation_tick)

    completed = 0

    for value in patches.values():
        if value:
            completed += 1

    draw_text(screen, str(completed) + " of 5 memory sections revealed", fonts["body"], DARK, 500, 590, center=True)

    back_button = draw_button(screen, "Back to Map", fonts["body"], 390, 615, 220, 45, GREY)
    return {"back": back_button}


def draw_final_screen(screen, fonts, patches, reveal_progress, animation_tick):
    draw_background(screen, veil_alpha=55)

    card = pygame.Rect(120, 25, 760, 645)
    draw_card(screen, card)

    draw_shadow_text(screen, "The Nokshi Katha is Complete", fonts["title"], DARK, 500, 68, center=True)
    draw_quilt(screen, 215, 130, 190, patches, reveal_progress, fonts, animation_tick)

    message = "Identity is stitched memory by memory, just like a Nokshi Katha."
    draw_text(screen, message, fonts["body"], DARK, 500, 585, center=True)

    back_button = draw_button(screen, "Return to Map", fonts["body"], 390, 615, 220, 45, GREY)
    return {"back": back_button}
