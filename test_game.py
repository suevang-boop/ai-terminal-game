from unittest.mock import patch

import game


def test_grid_size():
    """The grid should be 5x5."""
    assert game.GRID_SIZE == 5


def test_player_starts_at_origin():
    """Player should start at position (0, 0)."""
    assert game.player_pos == [0, 0]


@patch("game.os.system")
def test_draw_grid_contains_player(mock_system):
    """draw_grid() should place the player symbol @ at (0, 0)."""
    with patch("builtins.print") as mock_print:
        game.draw_grid()

    # Grab every string that was printed
    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )

    # The @ symbol must appear in the output
    assert "@" in all_output


@patch("game.os.system")
def test_draw_grid_dimensions(mock_system):
    """draw_grid() should produce exactly GRID_SIZE rows of cells."""
    printed_rows = []

    with patch("builtins.print") as mock_print:
        game.draw_grid()

    # Each grid row is printed as two calls:
    #   1) print(f" {row} ", end="")   -> " 0 " (row number, no newline)
    #   2) print("  ".join(cells))     -> "@  .  .  .  ." (the cells)
    # The row-number prints start with a space then a digit, e.g. " 0 "
    for call in mock_print.call_args_list:
        line = call.args[0]
        if isinstance(line, str) and line.strip().isdigit():
            printed_rows.append(line)

    assert len(printed_rows) == game.GRID_SIZE
