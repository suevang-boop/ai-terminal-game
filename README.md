# Space Rocks

A terminal-based Python game where you pilot a spaceship through a 5x5 grid, collecting rock samples while dodging deadly meteors.

## Story

Your Spaceship is flying through space collecting rock samples. Navigate the stars, gather 10 samples to complete your mission, and avoid the meteors that threaten your ship.

## Features

- **WASD Movement** — Navigate the grid with W (up), A (left), S (down), and D (right)
- **Collectible Scoring** — Pick up rock samples (🪨) to increase your score
- **Hazard Avoidance** — Dodge meteors (☄️) or face immediate game over
- **Win & Lose Conditions** — Collect 10 samples to win, or get hit by a meteor and lose
- **Play Again** — After each round, choose to play again or exit cleanly
- **Themed Interface** — Custom intro screen, emoji icons, and narrative messages

## How to Run

### Play the Game

```bash
python game.py
```

### Run the Tests

```bash
pytest
```

To run tests with verbose output:

```bash
pytest -v
```

## Controls

| Key | Action |
|-----|--------|
| W | Move up |
| A | Move left |
| S | Move down |
| D | Move right |
| Q | Quit |

## What I Learned

- **Iterative Development** — Building the game in small, testable steps (grid → movement → collectibles → hazards → theming) made each feature easy to understand and verify before moving on.

- **Engineering Prompts to Prevent Regression** — Adding new features like hazards or theming could easily break existing logic. Writing pytest tests after each change caught issues early and kept the game stable across iterations.

- **Automated Testing** — pytest became a safety net. Every feature was backed by tests for grid rendering, movement boundaries, spawning logic, scoring, and win/lose conditions — giving confidence that nothing broke when refactoring.

## Project Structure

```
ai-terminal-game/
├── game.py          # Main game logic and loop
├── test_game.py     # Pytest test suite (33 tests)
├── .gitignore       # Ignores __pycache__ and .opencode
└── README.md        # This file
```

## Tech Stack

- **Python 3.11** — Core language
- **pytest** — Test framework
- **Unicode Emojis** — 🚀 🪨 ☄️ for themed grid visuals
