import os

# --- Constants ---
GRID_SIZE = 5

# --- Player State ---
# We use (row, col) so (0, 0) means top-left corner
player_pos = [0, 0]


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
            else:
                cells.append(".")
        print("  ".join(cells))


def main():
    """Main game loop."""
    while True:
        draw_grid()
        print("\nMoves: W (up), A (left), S (down), D (right), Q (quit)")

        action = input("Your move: ").strip().lower()

        if action == "q":
            print("Goodbye!")
            break
        elif action in ("w", "a", "s", "d"):
            move_player(action)


if __name__ == "__main__":
    main()
