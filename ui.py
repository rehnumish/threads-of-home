"""Reusable user-interface drawing helpers."""

import pygame
from settings import DARK, LIGHT_BROWN


def draw_text(screen, text, font, colour, x, y, center=False):
    """Draw text on the screen and return its rectangle."""
    surface = font.render(text, True, colour)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
    return rect


def draw_wrapped_text(screen, text, font, colour, x, y, max_width, line_gap=8):
    """Draw wrapped text within a maximum width."""
    words = text.split()
    line = ""
    current_y = y

    for word in words:
        test_line = f"{line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            draw_text(screen, line, font, colour, x, current_y)
            current_y += font.get_height() + line_gap
            line = word

    if line:
        draw_text(screen, line, font, colour, x, current_y)


def draw_button(screen, text, font, x, y, w, h, base_colour=LIGHT_BROWN, text_colour=DARK):
    """Draw a clickable button and return its pygame.Rect."""
    rect = pygame.Rect(x, y, w, h)
    mouse_pos = pygame.mouse.get_pos()

    colour = base_colour
    if rect.collidepoint(mouse_pos):
        colour = tuple(min(c + 25, 255) for c in base_colour)

    pygame.draw.rect(screen, colour, rect, border_radius=14)
    pygame.draw.rect(screen, DARK, rect, width=3, border_radius=14)
    draw_text(screen, text, font, text_colour, rect.centerx, rect.centery, center=True)
    return rect
