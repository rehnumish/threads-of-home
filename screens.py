"""Main non-challenge screens for the game."""

from settings import (
    CREAM, DARK, BROWN, LIGHT_BROWN, RED, WHITE, BLUE, GREEN, YELLOW, PURPLE, GREY
)
from ui import draw_text, draw_button
from quilt import draw_quilt


def draw_menu(screen, fonts):
    """Draw the main menu."""
    screen.fill(CREAM)
    draw_text(screen, "Threads of Home", fonts["title"], DARK, 500, 130, center=True)
    draw_text(screen, "Stitching a Nokshi Katha", fonts["heading"], BROWN, 500, 190, center=True)
    draw_text(screen, "Complete cultural challenges to reveal a memory quilt.", fonts["body"], DARK, 500, 250, center=True)

    start_button = draw_button(screen, "Start Journey", fonts["body"], 390, 340, 220, 60)
    quit_button = draw_button(screen, "Quit", fonts["body"], 390, 420, 220, 60, GREY)
    return {"start": start_button, "quit": quit_button}


def draw_intro(screen, fonts):
    """Draw the story intro."""
    screen.fill(CREAM)
    draw_text(screen, "Story", fonts["title"], DARK, 500, 100, center=True)

    story_lines = [
        "You are a Bangladeshi child growing up far from home.",
        "One day, your grandparent gives you an unfinished Nokshi Katha.",
        "This is no ordinary quilt.",
        "For centuries, women in Bengal stitched Nokshi Katha by hand, ",
        "weaving memories, patterns, and stories into every thread.",
        "Now, its unfinished pieces are waiting for you.",
        "Each empty section holds a memory waiting to be discovered.",
        "Complete each challenge to stitch the stories of Bangladesh back together.",
    ]

    for index, line in enumerate(story_lines):
        draw_text(screen, line, fonts["body"], DARK, 500, 200 + index * 45, center=True)

    continue_button = draw_button(screen, "Continue", fonts["body"], 390, 600, 220, 60)
    return {"continue": continue_button}


def draw_map(screen, fonts, patches):
    """Draw the challenge selection map."""
    screen.fill(CREAM)
    draw_text(screen, "Choose a Cultural Challenge", fonts["title"], DARK, 500, 70, center=True)

    festival_button = draw_button(screen, "Pohela Boishakh Prep", fonts["body"], 120, 170, 320, 70, RED, WHITE)
    food_button = draw_button(screen, "Food", fonts["body"], 560, 170, 320, 70, YELLOW)
    river_button = draw_button(screen, "River Journey", fonts["body"], 120, 290, 320, 70, BLUE, WHITE)
    rhythm_button = draw_button(screen, "Village Rhythm", fonts["body"], 560, 290, 320, 70, PURPLE, WHITE)
    symbols_button = draw_button(screen, "Symbols of Bangladesh", fonts["body"], 340, 400, 320, 70, GREEN, WHITE)
    
    quilt_button = draw_button(screen, "View Nokshi Katha", fonts["body"], 340, 490, 320, 70, LIGHT_BROWN)

    completed = sum(1 for value in patches.values() if value)
    draw_text(screen, f"Sections revealed: {completed} / 5", fonts["body"], DARK, 500, 585, center=True)

    final_button = None
    if all(patches.values()):
        final_button = draw_button(screen, "View Completed Quilt", fonts["body"], 340, 580, 320, 60, GREEN, WHITE)

    return {
        
        "festival": festival_button,
        "food": food_button,
        "river": river_button,
        "rhythm": rhythm_button,
        "symbols": symbols_button,
        "quilt": quilt_button,
        "final": final_button,
}
    


def draw_quilt_screen(screen, fonts, patches, reveal_progress, animation_tick):
    """Draw the quilt progress screen."""
    screen.fill(CREAM)
    draw_text(screen, "Nokshi Katha Progress", fonts["title"], DARK, 500, 60, center=True)
    draw_quilt(screen, 215, 120, 190, patches, reveal_progress, fonts, animation_tick)

    completed = sum(1 for value in patches.values() if value)
    draw_text(screen, f"{completed} of 4 memory sections revealed", fonts["body"], DARK, 500, 570, center=True)

    back_button = draw_button(screen, "Back to Map", fonts["body"], 390, 610, 220, 55, GREY)
    return {"back": back_button}


def draw_final_screen(screen, fonts, patches, reveal_progress, animation_tick):
    """Draw the final completed quilt screen."""
    screen.fill(CREAM)
    draw_text(screen, "The Nokshi Katha is Complete", fonts["title"], DARK, 500, 55, center=True)
    draw_quilt(screen, 215, 110, 190, patches, reveal_progress, fonts, animation_tick)

    message = "Identity is stitched memory by memory, just like a Nokshi Katha."
    draw_text(screen, message, fonts["body"], DARK, 500, 555, center=True)

    back_button = draw_button(screen, "Return to Map", fonts["body"], 390, 615, 220, 55, GREY)
    return {"back": back_button}
