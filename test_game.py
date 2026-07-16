from unittest.mock import patch

import pytest

import game


@pytest.fixture(autouse=True)
def reset_game_state():
    """Reset all game state before every test."""
    game.player_pos[0] = 0
    game.player_pos[1] = 0
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 0
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 0
    game.score = 0


def test_grid_size():
    """The grid should be 5x5."""
    assert game.GRID_SIZE == 5


def test_player_starts_at_origin():
    """Player should start at position (0, 0)."""
    assert game.player_pos == [0, 0]


@patch("game.os.system")
def test_draw_grid_contains_player(mock_system):
    """draw_grid() should place the player icon on the grid."""
    with patch("builtins.print") as mock_print:
        game.draw_grid()

    # Grab every string that was printed
    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )

    # The player icon must appear in the output
    assert game.PLAYER_ICON in all_output


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


# --- Collectible Tests ---


def test_spawn_collectible_not_on_player():
    """spawn_collectible() must never place the collectible on the player."""
    game.spawn_collectible()
    assert game.collectible_pos != game.player_pos


def test_spawn_collectible_within_grid():
    """spawn_collectible() must place the collectible within grid bounds."""
    game.spawn_collectible()
    row, col = game.collectible_pos
    assert 0 <= row < game.GRID_SIZE
    assert 0 <= col < game.GRID_SIZE


def test_draw_grid_shows_collectible():
    """draw_grid() should display the collectible icon on the grid."""
    game.collectible_pos[0] = 3
    game.collectible_pos[1] = 3

    with patch("game.os.system"):
        with patch("builtins.print") as mock_print:
            game.draw_grid()

    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )
    assert game.COLLECTIBLE_ICON in all_output


def test_collect_increments_score():
    """Moving onto the collectible should increase the score by 1."""
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1

    game.move_player("d")
    if game.player_pos == game.collectible_pos:
        game.score += 1

    assert game.score == 1


def test_collect_does_not_trigger_when_missed():
    """Score should not change if the player is not on the collectible."""
    game.collectible_pos[0] = 4
    game.collectible_pos[1] = 4

    game.move_player("d")
    if game.player_pos == game.collectible_pos:
        game.score += 1

    assert game.score == 0


def test_win_condition():
    """Reaching WIN_SCORE should mark the game as won."""
    game.score = game.WIN_SCORE
    assert game.score >= game.WIN_SCORE


# --- Hazard Tests ---


def test_spawn_hazard_not_on_player():
    """spawn_hazard() must never place the hazard on the player."""
    game.spawn_hazard()
    assert game.hazard_pos != game.player_pos


def test_spawn_hazard_not_on_collectible():
    """spawn_hazard() must never overlap the collectible."""
    game.collectible_pos[0] = 2
    game.collectible_pos[1] = 3
    game.spawn_hazard()
    assert game.hazard_pos != game.collectible_pos


def test_spawn_hazard_within_grid():
    """spawn_hazard() must stay within grid bounds."""
    game.spawn_hazard()
    row, col = game.hazard_pos
    assert 0 <= row < game.GRID_SIZE
    assert 0 <= col < game.GRID_SIZE


@patch("game.os.system")
def test_draw_grid_shows_hazard(mock_system):
    """draw_grid() should display the hazard icon on the grid."""
    game.hazard_pos[0] = 2
    game.hazard_pos[1] = 2

    with patch("builtins.print") as mock_print:
        game.draw_grid()

    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )
    assert game.HAZARD_ICON in all_output


def test_hazard_terminates_round():
    """Moving onto the hazard should end the round (hazard check triggers)."""
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 1

    game.move_player("d")
    assert game.player_pos == game.hazard_pos


# --- Reset Tests ---


def test_reset_game_resets_player():
    """reset_game() should move the player back to (0, 0)."""
    game.player_pos[0] = 3
    game.player_pos[1] = 4
    game.reset_game()
    assert game.player_pos == [0, 0]


def test_reset_game_resets_score():
    """reset_game() should set the score back to 0."""
    game.score = 99
    game.reset_game()
    assert game.score == 0


def test_reset_game_spawns_items():
    """reset_game() should place collectible and hazard on valid, non-overlapping positions."""
    game.reset_game()

    cr, cc = game.collectible_pos
    hr, hc = game.hazard_pos

    # Both within grid
    assert 0 <= cr < game.GRID_SIZE and 0 <= cc < game.GRID_SIZE
    assert 0 <= hr < game.GRID_SIZE and 0 <= hc < game.GRID_SIZE

    # None overlap with each other or the player
    assert game.collectible_pos != game.hazard_pos
    assert game.collectible_pos != game.player_pos
    assert game.hazard_pos != game.player_pos


# --- Theme Tests ---


def test_game_name():
    """The game name should be set."""
    assert game.GAME_NAME == "Space Rocks"


def test_story_intro():
    """The story intro should describe the game."""
    assert "Spaceship" in game.STORY_INTRO


def test_win_message():
    """Win message should mention samples."""
    assert "samples" in game.WIN_MESSAGE


def test_lose_message():
    """Lose message should mention the spaceship."""
    assert "spaceship" in game.LOSE_MESSAGE.lower()


@patch("game.os.system")
@patch("builtins.print")
@patch("builtins.input", return_value="")
def test_show_intro_displays_game_name(mock_input, mock_print, mock_system):
    """show_intro() should print the game name."""
    game.show_intro()

    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )
    assert game.GAME_NAME in all_output


@patch("game.os.system")
@patch("builtins.print")
@patch("builtins.input", return_value="")
def test_show_intro_displays_story(mock_input, mock_print, mock_system):
    """show_intro() should print the story intro."""
    game.show_intro()

    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )
    assert game.STORY_INTRO in all_output


@patch("game.os.system")
def test_draw_grid_shows_game_name(mock_system):
    """draw_grid() should display the game name header."""
    with patch("builtins.print") as mock_print:
        game.draw_grid()

    all_output = "\n".join(
        call.args[0] for call in mock_print.call_args_list
    )
    assert game.GAME_NAME in all_output
