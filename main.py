"""Main entry point for Threads of Home."""

import pygame
import sys

from settings import (
    WIDTH, HEIGHT, FPS,
    MENU, INTRO, MAP, FESTIVAL, FOOD, RIVER, RHYTHM, SYMBOLS, QUILT, FINAL
)
from quilt import update_reveal_progress
from screens import draw_menu, draw_intro, draw_map, draw_quilt_screen, draw_final_screen
from challenges.festival import FestivalChallenge
from challenges.placeholder import draw_placeholder_challenge
from challenges.food import FoodChallenge

def create_fonts():
    """Create and return all fonts used by the game."""

    def choose_font(candidates, size, bold=False, italic=False):
        available = {name.lower().replace(" ", "") for name in pygame.font.get_fonts()}

        for name in candidates:
            key = name.lower().replace(" ", "")
            if key in available:
                return pygame.font.SysFont(name, size, bold=bold, italic=italic)

        return pygame.font.SysFont("arial", size, bold=bold, italic=italic)

    return {
        "title": choose_font(["Gabriola", "Palatino Linotype", "Book Antiqua", "Georgia"], 58, bold=True),
        "heading": choose_font(["Palatino Linotype", "Book Antiqua", "Georgia"], 36, bold=True),
        "map_label": choose_font(["Palatino Linotype", "Book Antiqua", "Georgia"], 28, bold=True),
        "body": choose_font(["Cambria", "Trebuchet MS", "Arial"], 24),
        "small": choose_font(["Cambria", "Trebuchet MS", "Arial"], 18),
        "tiny": choose_font(["Cambria", "Trebuchet MS", "Arial"], 15),
    }


def main():
    """Run the main game loop."""
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Threads of Home: Stitching a Nokshi Katha")
    clock = pygame.time.Clock()
    fonts = create_fonts()

    current_state = MENU
    animation_tick = 0

    patches = {
        "festival": False,
        "food": False,
        "river": False,
        "rhythm": False,
        "symbols": False,
    }

    reveal_progress = {
        "festival": 0.0,
        "food": 0.0,
        "river": 0.0,
        "rhythm": 0.0,
        "symbols": 0.0,
    }

    festival_challenge = FestivalChallenge()
    food_challenge = FoodChallenge()
    buttons = {}
    running = True

    while running:
        # -----------------------------
        # Draw current screen
        # -----------------------------
        if current_state == MENU:
            buttons = draw_menu(screen, fonts)

        elif current_state == INTRO:
            buttons = draw_intro(screen, fonts)

        elif current_state == MAP:
            buttons = draw_map(screen, fonts, patches)

        elif current_state == FESTIVAL:
            festival_challenge.update()
            buttons = festival_challenge.draw(screen, fonts)

        elif current_state == FOOD:
             food_challenge.update()
             buttons = food_challenge.draw(screen, fonts)

        elif current_state == RIVER:
            buttons = draw_placeholder_challenge(
                screen,
                fonts,
                "River Journey",
                "Travel by boat and discover how rivers shape life in Bangladesh.",
            )

        elif current_state == RHYTHM:
            buttons = draw_placeholder_challenge(
                screen,
                fonts,
                "Village Rhythm",
                "Follow the rhythm of a village gathering and unlock a music section.",
            )
        
        elif current_state == SYMBOLS:
            buttons = draw_placeholder_challenge(
             screen,
             fonts,
            "Symbols of Bangladesh",
            "Learn about the Shapla, Royal Bengal Tiger, and other national symbols.",
            )

        elif current_state == QUILT:
            buttons = draw_quilt_screen(screen, fonts, patches, reveal_progress, animation_tick)

        elif current_state == FINAL:
            buttons = draw_final_screen(screen, fonts, patches, reveal_progress, animation_tick)

        # -----------------------------
        # Event handling
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if current_state == MENU:
                    if buttons["start"].collidepoint(mouse_pos):
                        current_state = INTRO
                    elif buttons["quit"].collidepoint(mouse_pos):
                        running = False

                elif current_state == INTRO:
                    if buttons["continue"].collidepoint(mouse_pos):
                        current_state = MAP

                elif current_state == MAP:
                    if buttons["festival"].collidepoint(mouse_pos):
                        festival_challenge.reset()
                        current_state = FESTIVAL
                    elif buttons["food"].collidepoint(mouse_pos):
                        food_challenge.reset()
                        current_state = FOOD
                    elif buttons["river"].collidepoint(mouse_pos):
                        current_state = RIVER
                    elif buttons["rhythm"].collidepoint(mouse_pos):
                        current_state = RHYTHM
                    elif buttons["symbols"].collidepoint(mouse_pos):
                         current_state = SYMBOLS
                    elif buttons["quilt"].collidepoint(mouse_pos):
                        current_state = QUILT
                    elif buttons["final"] is not None and buttons["final"].collidepoint(mouse_pos):
                        current_state = FINAL

                elif current_state == FESTIVAL:
                    result = festival_challenge.handle_click(mouse_pos, buttons)
                    if result == "back":
                        current_state = MAP
                    elif result == "complete":
                        patches["festival"] = True
                        reveal_progress["festival"] = 0.0
                        current_state = QUILT

                elif current_state == FOOD:
                    result = food_challenge.handle_click(mouse_pos, buttons)
                    if result == "back":
                        current_state = MAP
                    elif result == "complete":
                        patches["food"] = True
                        reveal_progress["food"] = 0.0
                        current_state = QUILT

                elif current_state in [RIVER, RHYTHM, SYMBOLS]:
                    if buttons["complete"].collidepoint(mouse_pos):
                        if current_state == RIVER:
                            key = "river"
                        elif current_state == RHYTHM:
                            key = "rhythm"
                        else:
                            key = "symbols"

                        patches[key] = True
                        reveal_progress[key] = 0.0
                        current_state = QUILT

                    elif buttons["back"].collidepoint(mouse_pos):
                        current_state = MAP

                elif current_state == QUILT:
                    if buttons["back"].collidepoint(mouse_pos):
                        current_state = MAP

                elif current_state == FINAL:
                    if buttons["back"].collidepoint(mouse_pos):
                        current_state = MAP

        update_reveal_progress(patches, reveal_progress)

        animation_tick += 1
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
