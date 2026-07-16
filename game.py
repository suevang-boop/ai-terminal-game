import os
import random

# --- Constants ---
GRID_SIZE = 5
WIN_SCORE = 10

# --- Player State ---
# We use (row, col) so (0, 0) means top-left corner
player_pos = [0, 0]
collectible_pos = [0, 0]
score = 0


def spawn_collectible():
    """Place the collectible at a random position that is not the player's."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if [row, col] != player_pos:
            collectible_pos[0] = row
            collectible_pos[1] = col
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
    """Draws a 5x5 grid with the player marked as @."""
    os.system("clear")  # Clears the terminal so the grid redraws fresh

    # Print column numbers across the top for reference
    print("    " + "  ".join(str(i) for i in range(GRID_SIZE)))

    for row in range(GRID_SIZE):
        # Print row number on the left side
        print(f" {row} ", end="")

        cells = []
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                cells.append("@")
            elif row == collectible_pos[0] and col == collectible_pos[1]:
                cells.append("*")
            else:
                cells.append(".")
        print("  ".join(cells))


def main():
    """Main game loop."""
    global score

    spawn_collectible()

    while True:
        draw_grid()
        print(f"\nScore: {score}/{WIN_SCORE}")
        print("Moves: W (up), A (left), S (down), D (right), Q (quit)")

        action = input("Your move: ").strip().lower()

        if action == "q":
            print("Goodbye!")
            break
        elif action in ("w", "a", "s", "d"):
            move_player(action)

            if player_pos == collectible_pos:
                score += 1
                if score >= WIN_SCORE:
                    draw_grid()
                    print(f"\nScore: {score}/{WIN_SCORE}")
                    print("You win!")
                    break
                spawn_collectible()


if __name__ == "__main__":
    main()
