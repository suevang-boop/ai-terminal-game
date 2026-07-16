from unittest.mock import patch

import pytest

import game


@pytest.fixture(autouse=True)
def reset_player():
    """Reset the player to (0, 0) before every test."""
    game.player_pos[0] = 0
    game.player_pos[1] = 0


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


# --- Movement Tests ---


def test_move_right():
    """D should move the player one column to the right."""
    game.move_player("d")
    assert game.player_pos == [0, 1]


def test_move_left():
    """A should move the player one column to the left."""
    game.player_pos[1] = 2
    game.move_player("a")
    assert game.player_pos == [0, 1]


def test_move_down():
    """S should move the player one row down."""
    game.move_player("s")
    assert game.player_pos == [1, 0]


def test_move_up():
    """W should move the player one row up."""
    game.player_pos[0] = 2
    game.move_player("w")
    assert game.player_pos == [1, 0]


def test_cannot_move_past_top_edge():
    """W at row 0 should not change position."""
    game.move_player("w")
    assert game.player_pos == [0, 0]


def test_cannot_move_past_left_edge():
    """A at col 0 should not change position."""
    game.move_player("a")
    assert game.player_pos == [0, 0]


def test_cannot_move_past_bottom_edge():
    """S at the bottom row should not change position."""
    game.player_pos[0] = game.GRID_SIZE - 1
    game.move_player("s")
    assert game.player_pos[0] == game.GRID_SIZE - 1


def test_cannot_move_past_right_edge():
    """D at the rightmost column should not change position."""
    game.player_pos[1] = game.GRID_SIZE - 1
    game.move_player("d")
    assert game.player_pos[1] == game.GRID_SIZE - 1
