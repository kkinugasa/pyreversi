"""Test players module"""
import numpy as np

from pyreversi.game import Game
from pyreversi.models import Board, Disk, Position, Square
from pyreversi.players import GreedyPlayer


def test_greedy_player() -> None:
    config = np.array(
        [
            [Square.NULL, Square.LIGHT, Square.DARK],
            [Square.NULL, Square.LIGHT, Square.DARK],
            [Square.NULL, Square.DARK, Square.DARK],
        ],
        dtype=np.int8,
    )
    game = Game(Board(config), Disk.DARK)
    assert GreedyPlayer().play(game) == Position(0, 0)
    game.execute_action(Position(0, 0))
    assert GreedyPlayer().play(game) is None
