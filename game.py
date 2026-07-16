import os
import random

# --- Constants ---
GRID_SIZE = 5
WIN_SCORE = 10

# --- Game State ---
player_pos = [0, 0]
collectible_pos = [0, 0]
hazard_pos = [0, 0]
score = 0


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


def draw_grid():
    """Draw the 5x5 grid with player (@), collectible (*), and hazard (X)."""
    os.system("clear")

    print("    " + "  ".join(str(i) for i in range(GRID_SIZE)))

    for row in range(GRID_SIZE):
        print(f" {row} ", end="")

        cells = []
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                cells.append("@")
            elif row == collectible_pos[0] and col == collectible_pos[1]:
                cells.append("*")
            elif row == hazard_pos[0] and col == hazard_pos[1]:
                cells.append("X")
            else:
                cells.append(".")
        print("  ".join(cells))


def play_round():
    """Run a single round. Returns True if the player wants to play again."""
    global score
    reset_game()

    while True:
        draw_grid()
        print(f"\nScore: {score}/{WIN_SCORE}")
        print("Moves: W (up), A (left), S (down), D (right), Q (quit)")

        action = input("Your move: ").strip().lower()

        if action == "q":
            return False

        if action in ("w", "a", "s", "d"):
            move_player(action)

            if player_pos == hazard_pos:
                draw_grid()
                print("\nGame Over!")
                break

            if player_pos == collectible_pos:
                score += 1
                if score >= WIN_SCORE:
                    draw_grid()
                    print(f"\nScore: {score}/{WIN_SCORE}")
                    print("You win!")
                    break
                spawn_collectible()

    print("\nPlay again? (y/n)")
    return input("> ").strip().lower() == "y"


def main():
    """Top-level game loop: keeps starting new rounds until the player quits."""
    while play_round():
        pass
    print("Goodbye!")


if __name__ == "__main__":
    main()
