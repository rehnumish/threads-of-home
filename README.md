# Threads of Home: Stitching a Nokshi Katha

Threads of Home is a small Pygame cultural adventure game about Bangladeshi heritage, family memory, and diaspora identity. The player learns about different parts of Bangladeshi culture, completes five interactive challenges, and gradually reveals a Nokshi Katha memory quilt.

## What the player does

- Starts from a main menu and reads a short story introduction.
- Chooses challenges from a visual map.
- Learns through short lesson pages before each challenge.
- Uses the mouse to click, drag, drop, reset, and return to the map.
- Opens optional Wikipedia pages from lesson screens for extra learning.
- Completes five cultural challenges to reveal five quilt sections.
- Views the completed Nokshi Katha after every section is stitched.

## How to run

Install Python 3 and Pygame, then run the game from the project folder.

```bash
pip install pygame
python main.py
```

On Windows, if `python` is not mapped to Python 3, use:

```bash
py -m pip install pygame
py main.py
```

The game opens a 1000 by 700 pixel Pygame window and runs at 60 FPS.

## Requirements

- Python 3
- Pygame
- The `assets/` folder included with the project

The game relies on local image assets for the map, challenge cards, symbols, river photos, rhythm photos, and quilt sections. If an asset is missing, some screens show a "Missing" label or a missing quilt file notice instead of crashing.

## Project structure

```text
main.py
settings.py
ui.py
screens.py
quilt.py
README.md
assets/
    festival/
    food/
    map/
    quilt/
    rhythm/
    river/
    symbols/
challenges/
    __init__.py
    festival.py
    food.py
    river.py
    rhythm.py
    symbols.py
```

## Important files

- `main.py` runs the game loop, creates challenge objects, tracks screen state, handles mouse events, and updates quilt reveal progress.
- `settings.py` stores screen size, FPS, game state names, and shared colours.
- `screens.py` draws the menu, story intro, challenge map, progress quilt screen, and final quilt screen.
- `quilt.py` loads and draws the five quilt image sections and handles reveal animation.
- `ui.py` contains shared text, wrapped text, and button drawing helpers.
- `challenges/festival.py` contains the Pohela Boishakh lesson and drag-and-drop scene puzzle.
- `challenges/food.py` contains the Bangladeshi meal lesson and drag-and-drop table puzzle.
- `challenges/river.py` contains the river lesson and river-name matching challenge.
- `challenges/rhythm.py` contains the Bangla music lesson and song-tradition matching challenge.
- `challenges/symbols.py` contains the national symbols lesson and quiz challenge.

## Assets

- `assets/map/` stores the visual challenge map and map icons.
- `assets/quilt/` stores the five final quilt section images.
- `assets/festival/` stores photos for festival puzzle items.
- `assets/food/` stores food challenge images.
- `assets/river/` stores river and river-card images.
- `assets/rhythm/` stores music tradition images.
- `assets/symbols/` stores symbol quiz images.

Keep these folders beside the Python files. The code uses relative paths such as `assets/map/map_background.png`, so running the game from another working directory may prevent images from loading.

## Notes for users and presenters

- Challenge progress is stored only while the game is open. Closing the game resets progress.
- The lesson pages are part of the game flow; each challenge starts after the final lesson page.
- The Wikipedia buttons require a browser and internet connection, but the main game can still run without using them.
- Most interactions are visual and mouse-based, so the game is best played on a screen large enough for the 1000 by 700 window.
- The game is designed as an educational prototype and cultural storytelling experience, not a competitive score-based game.


## Cultural challenges

### Festival: Pohela Boishakh Prep Puzzle

The festival challenge teaches about Pohela Boishakh, the Bengali New Year. The player reads lesson pages about alpana, dhol, Mongol Shovajatra, masks, pitha, and red-white festival clothing. In the puzzle, the player drags festival photos into the correct scene zones:

- Alpana goes in the courtyard.
- Dhol goes in the music corner.
- Mask goes in the procession.
- Pitha goes on the food table.
- Red-white outfit goes on the outfit stand.
- Barbie is a decoy item and does not complete the scene.

After all five correct items are placed, the player can click "Stitch Quilt Section" to reveal the festival patch.

### Food: Serve the Family

The food challenge teaches that food can carry hospitality, family memory, celebration, and culture. Lesson pages explain Bangladeshi cuisine, rice and fish, balanced meals, sweets, pitha, and achar. In the puzzle, the player drags food photos to matching places on a table:

- Bhaat goes on the main plate.
- Fish goes with the fish side.
- Achar goes in the small bowl.
- Mishti goes on the sweet plate.
- Pitha goes on the snack plate.
- Burger is a decoy item.

After the meal is completed, the food quilt section can be stitched.

### River: River Story Board

The river challenge teaches that rivers shape life, travel, food, land, stories, and songs in Bangladesh. The player learns about the Padma, Jamuna, and Meghna rivers. In the challenge, the player drags each river name to the matching photo card:

- Padma matches the hilsa and food culture card.
- Jamuna matches the wide river and changing land card.
- Meghna matches the waterways to the Bay of Bengal card.

After all three river names are matched, the river quilt section can be stitched.

### Rhythm: Bangla Song Traditions

The rhythm challenge teaches that music carries stories, memory, place, identity, devotion, protest, and emotion. Lesson pages introduce Bangladeshi music, Bhatiyali, Rabindra Sangeet, Nazrul Geeti, and Lalon songs. The player answers one prompt at a time by clicking the matching song tradition:

- Bhatiyali is connected with rivers and boatmen.
- Rabindra Sangeet is connected with Rabindranath Tagore.
- Nazrul Geeti is connected with Kazi Nazrul Islam.
- Lalon Geeti is connected with Lalon Fakir and Baul tradition.

After all prompts are answered, the rhythm quilt section can be stitched.

### Symbols: National Symbols of Bangladesh

The symbols challenge teaches how symbols help people remember a place from far away. Lesson pages introduce national symbols of Bangladesh, including the national flower, animal, fish, bird, and flag. The player answers five quiz pages:

- Shapla or White Water Lily is the national flower.
- Royal Bengal Tiger is the national animal.
- Hilsa or Ilish is the national fish.
- The green flag with a red circle is the flag of Bangladesh.
- Doyel or Oriental Magpie Robin is the national bird.

Correct answers unlock symbols on the board. After all five are unlocked, the symbols quilt section can be stitched.

## Quilt progress system

The game uses a continuous Nokshi Katha as the progress system. Each completed challenge reveals one section of the quilt:

- Festival: top-left quilt section.
- Food: top-right quilt section.
- River: bottom-left quilt section.
- Rhythm: bottom-right quilt section.
- Symbols: tall center quilt section.

Unrevealed sections are covered by a soft fabric-like overlay and labelled as unstitched. When a challenge is completed, that section animates open and sparkles. The map shows a "DONE" badge for completed challenges and a "Revealed: 0 / 5" style counter. When all five sections are complete, the map unlocks the "View Completed Quilt" button.

## Controls

- Use the mouse to click buttons and select map areas.
- Click "Next" through lesson pages.
- Click "Wikipedia" or river-specific wiki buttons to open extra reading in a browser.
- Drag and drop items in the festival, food, and river challenges.
- Click answer cards in the rhythm and symbols challenges.
- Click "Reset" or "Reset Puzzle" to restart the current challenge.
- Click "Back to Map" or "Return to Map" to leave the current screen.
- Close the Pygame window or click "Quit" from the menu to exit.


## Credits

Screens artwork: Suprito Saumik (supritosaumik1@gmail.com)

Final quilt artwork: Renaissa Rahmat Ullah (renaissa.rahmat01@gmail.com)
