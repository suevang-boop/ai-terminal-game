import os
import random

# --- Constants ---
GRID_SIZE = 5
WIN_SCORE = 10

# --- Theme ---
GAME_NAME = "Space Rocks"
STORY_INTRO = "Your Spaceship is flying through space collecting rock samples"
PLAYER_ICON = "\U0001f680"     # 🚀
COLLECTIBLE_ICON = "\U0001faa8"  # 🪨
HAZARD_ICON = "\u2604\ufe0f"    # ☄️
WIN_MESSAGE = "You have collected all the samples!"
LOSE_MESSAGE = "Your spaceship is damaged and unable to continue!"

# --- Game State ---
player_pos = [0, 0]
collectible_pos = [0, 0]
hazard_pos = [0, 0]
score = 0


def show_intro():
    """Display the game title and story intro at startup."""
    os.system("clear")
    print(f"\n  === {GAME_NAME} ===\n")
    print(f"  {STORY_INTRO}\n")
    print(f"  Collect {WIN_SCORE} {COLLECTIBLE_ICON} while avoiding {HAZARD_ICON}")
    print(f"  Use WASD to move, Q to quit\n")
    input("  Press Enter to start... ")


def reset_game():
    """Reset all game state for a fresh round."""
    global score
    player_pos[0] = 0
    player_pos[1] = 0
    score = 0
    spawn_collectible()
    spawn_hazard()


def spawn_collectible():
    """Place the collectible at a random position that is not the player's."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if [row, col] != player_pos and [row, col] != hazard_pos:
            collectible_pos[0] = row
            collectible_pos[1] = col
            break


def spawn_hazard():
    """Place the hazard at a random empty position on the grid."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if [row, col] != player_pos and [row, col] != collectible_pos:
            hazard_pos[0] = row
            hazard_pos[1] = col
            break


def move_player(direction: str):
    """Move the player one cell in the given direction, respecting grid boundaries."""
    row, col = player_pos

    if direction == "w" and row > 0:
        player_pos[0] = row - 1
    elif direction == "s" and row < GRID_SIZE - 1:
        player_pos[0] = row + 1
    elif direction == "a" and col > 0:
        player_pos[1] = col - 1
    elif direction == "d" and col < GRID_SIZE - 1:
        player_pos[1] = col + 1


def move_hazard():
    """Move the hazard one cell in a random valid direction, or stay put."""
    row, col = hazard_pos
    directions = []

    if row > 0:
        directions.append((-1, 0))
    if row < GRID_SIZE - 1:
        directions.append((1, 0))
    if col > 0:
        directions.append((0, -1))
    if col < GRID_SIZE - 1:
        directions.append((0, 1))

    # Include staying put as an option
    directions.append((0, 0))

    dr, dc = random.choice(directions)
    new_row, new_col = row + dr, col + dc

    # Only move if the target is not occupied by the player or collectible
    if [new_row, new_col] != player_pos and [new_row, new_col] != collectible_pos:
        hazard_pos[0] = new_row
        hazard_pos[1] = new_col


def draw_grid():
    """Draw the 5x5 grid with themed icons."""
    os.system("clear")

    print(f"  --- {GAME_NAME} ---\n")

    print("    " + "  ".join(str(i) for i in range(GRID_SIZE)))

    for row in range(GRID_SIZE):
        print(f" {row} ", end="")

        cells = []
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                cells.append(PLAYER_ICON)
            elif row == collectible_pos[0] and col == collectible_pos[1]:
                cells.append(COLLECTIBLE_ICON)
            elif row == hazard_pos[0] and col == hazard_pos[1]:
                cells.append(HAZARD_ICON)
            else:
                cells.append("·")
        print("  ".join(cells))


def play_round():
    """Run a single round. Returns True if the player wants to play again."""
    global score
    reset_game()

    while True:
        draw_grid()
        print(f"\n  Score: {score}/{WIN_SCORE}")
        print("  W (up)  A (left)  S (down)  D (right)  Q (quit)")

        action = input("\n  Your move: ").strip().lower()

        if action == "q":
            return False

        if action in ("w", "a", "s", "d"):
            move_player(action)
            move_hazard()

            if player_pos == hazard_pos:
                draw_grid()
                print(f"\n  {LOSE_MESSAGE}")
                break

            if player_pos == collectible_pos:
                score += 1
                if score >= WIN_SCORE:
                    draw_grid()
                    print(f"\n  Score: {score}/{WIN_SCORE}")
                    print(f"\n  {WIN_MESSAGE}")
                    break
                spawn_collectible()

    print("\n  Play again? (y/n)")
    return input("  > ").strip().lower() == "y"


def main():
    """Top-level game loop: keeps starting new rounds until the player quits."""
    show_intro()
    while play_round():
        pass
    print(f"\n  Thanks for playing {GAME_NAME}!\n")


if __name__ == "__main__":
    main()
