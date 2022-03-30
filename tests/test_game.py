"""Test game module"""
import numpy as np
import numpy.typing as npt
import pytest

from pyreversi.game import Game, IllegalActionError
from pyreversi.logic import init_board, obtain_legal_actions
from pyreversi.models import Board, Disk, Position


def test_init_game() -> None:
    game = Game.init_game(8)
    assert game.current_disk == Disk.DARK
    assert game.board == init_board(8)
    assert game.get_legal_actions() == obtain_legal_actions(init_board(8), Disk.DARK)
    assert game.is_game_over() is False


def test_game_over() -> None:
    board = Board(np.zeros((8, 8), dtype=np.int8))
    game = Game(board, Disk.LIGHT)
    assert game.is_game_over() is True


def test_execute_action() -> None:
    game = Game.init_game(4)
    game.execute_action(Position(0, 1))
    config: npt.NDArray[np.int8] = np.array(
        [
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 1, -1, 0],
            [0, 0, 0, 0],
        ],
        dtype=np.int8,
    )
    assert game.board == Board(config)
    assert game.current_disk == Disk.LIGHT
    assert game.get_legal_actions() == frozenset(
        [Position(0, 0), Position(0, 2), Position(2, 0)]
    )
    assert game.is_game_over() is False

    config = np.array(
        [
            [1, -1, -1, 1],
            [0, -1, -1, 1],
            [1, -1, -1, 1],
            [1, -1, 1, 1],
        ],
        dtype=np.int8,
    )
    game = Game(Board(config), Disk.LIGHT)
    assert game.get_legal_actions() == frozenset()
    with pytest.raises(IllegalActionError):
        game.execute_action(Position(0, 0))
    with pytest.raises(IllegalActionError):
        game.execute_action(Position(1, 0))
    game.execute_action(None)
    assert game.current_disk == Disk.DARK
    assert game.board == Board(config)
    with pytest.raises(IllegalActionError):
        game.execute_action(None)
    game.execute_action(Position(1, 0))
    after_config = np.array(
        [
            [1, -1, -1, 1],
            [1, 1, 1, 1],
            [1, 1, -1, 1],
            [1, -1, 1, 1],
        ],
        dtype=np.int8,
    )
    assert game.board == Board(after_config)
    assert game.get_legal_actions() == frozenset()
    assert game.is_game_over() is True
