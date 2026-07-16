import os

# --- Constants ---
GRID_SIZE = 5

# --- Player State ---
# We use (row, col) so (0, 0) means top-left corner
player_pos = [0, 0]


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
        else:
            print("That's not a valid move! Press Enter to continue...")
            input()


if __name__ == "__main__":
    main()
