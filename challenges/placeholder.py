"""Placeholder challenge screen for challenges not implemented yet."""

from settings import CREAM, DARK, BROWN, GREEN, GREY, WHITE
from ui import draw_text, draw_button


def draw_placeholder_challenge(screen, fonts, title, description):
    """Draw a temporary challenge screen."""
    screen.fill(CREAM)
    draw_text(screen, title, fonts["title"], DARK, 500, 100, center=True)
    draw_text(screen, description, fonts["body"], DARK, 500, 180, center=True)

    draw_text(screen, "Prototype version:", fonts["heading"], BROWN, 500, 280, center=True)
    draw_text(screen, "Click complete to unlock this Nokshi Katha section.", fonts["body"], DARK, 500, 325, center=True)

    complete_button = draw_button(screen, "Complete Challenge", fonts["body"], 360, 440, 280, 60, GREEN, WHITE)
    back_button = draw_button(screen, "Back to Map", fonts["body"], 390, 525, 220, 55, GREY)

    return {"complete": complete_button, "back": back_button}
