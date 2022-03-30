"""Test models module"""
import numpy as np
import pytest
from numpy import array

from pyreversi.models import Board, Direction, Disk, Position, Square


def test_disk() -> None:
    """Test Disk class"""
    assert Disk.LIGHT == Disk.DARK.reverse()


def test_square() -> None:
    """Test Square class"""
    assert Square.DARK == Disk.DARK
    assert Square.LIGHT == Disk.LIGHT
    assert Square.NULL.value == 0
    assert str(Square.DARK) == "x"
    assert str(Square.LIGHT) == "o"
    assert str(Square.NULL) == "-"


def test_position() -> None:
    "Test Position class"
    assert Position(0, 0) == Position(0, 0)
    assert Position(0, 0) != Position(0, 1)
    assert Position(0, 1) <= Position(0, 1)
    assert Position(0, 1) <= Position(0, 2)
    assert not Position(1, 1).__le__(Position(0, 2))
    assert not Position(1, 1).__gt__(Position(0, 2))
    assert Position(0, 1) + Direction(0, 1) == Position(0, 2)
    with pytest.raises(TypeError):
        # NOTE: Use the expression "_ =" to avoid expression-not-assigned of pylint
        _ = Position(0, 0) + Position(0, 1)


def test_board() -> None:
    """Test Board class"""
    config = array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    config_str = (
        "--------\n"
        "--------\n"
        "--------\n"
        "---xo---\n"
        "---ox---\n"
        "--------\n"
        "--------\n"
        "--------"
    )
    board = Board(config)
    assert Board(np.zeros((4, 4), dtype=np.int8)) == Board(
        np.zeros((4, 4), dtype=np.int8)
    )
    assert Board(np.zeros((4, 4), dtype=np.int8)) != Board(
        np.ones((4, 4), dtype=np.int8)
    )
    assert str(board) == config_str
    # pylint: disable=eval-used
    assert board == eval(repr(board))
    assert board[Position(0, 0)] == Square.NULL
    # config cannot be replaced.
    with pytest.raises(AttributeError):
        board.config = config
    with pytest.raises(ValueError):
        board.config[0][0] = Square.DARK
    # board cannot be updated
    with pytest.raises(TypeError):
        # pylint: disable=unsupported-assignment-operation
        board[Position(0, 0)] = Square.DARK
    with pytest.raises(IndexError):
        # NOTE: Use the expression "_ =" to avoid expression-not-assigned of pylint
        _ = board[Position(-1, -1)]
