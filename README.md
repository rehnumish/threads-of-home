# Threads of Home: Stitching a Nokshi Katha

A small Pygame cultural adventure game about Bangladeshi heritage and diaspora identity.

## Current features

- Main menu
- Story intro
- Challenge selection map
- Playable Pohela Boishakh item-selection challenge
- Placeholder screens for food, river, and rhythm challenges
- Continuous Nokshi Katha quilt
- Animated section reveal
- Code-generated visuals using Pygame shapes

## How to run

```bash
pip install pygame
python main.py
```

## File structure

```text
main.py
settings.py
ui.py
screens.py
quilt.py
challenges/
    __init__.py
    festival.py
    placeholder.py
```

## Design idea

The game uses a continuous Nokshi Katha as a visual progress system. Each completed cultural challenge reveals one section of the quilt. Unrevealed sections are covered by a soft blurred fabric overlay, symbolising memories that have not yet been rediscovered.
