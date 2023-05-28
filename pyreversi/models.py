"""reversi models"""
from __future__ import annotations

from enum import IntEnum
from typing import Iterator, NamedTuple

import numpy as np
import numpy.typing as npt


class Reversible(IntEnum):
    """Reversible object class"""

    def reverse(self) -> Reversible:
        """Return a reversed object

        Returns:
            Reversible: reversed object
        """
        return self.__class__(-self.value)

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Reversible) and self.value == obj.value


class Disk(Reversible):
    """Reversi disk"""

    DARK = 1
    LIGHT = -1


class Square(Reversible):
    """State of each piece of a board

    NULL means piece is empty.
    """

    DARK = Disk.DARK
    LIGHT = Disk.LIGHT
    NULL = 0

    def __str__(self) -> str:
        if self == self.DARK:
            return "x"
        if self == self.LIGHT:
            return "o"
        return "-"


class Direction(NamedTuple):
    row: int
    col: int


_DIRECTIONS: tuple[Direction, ...] = (
    Direction(-1, -1),
    Direction(-1, 0),
    Direction(-1, 1),
    Direction(0, -1),
    Direction(0, 1),
    Direction(1, -1),
    Direction(1, 0),
    Direction(1, 1),
)


class Position(NamedTuple):
    """Position on the game board"""

    row: int
    col: int

    def __lt__(self, position: object) -> bool:
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row < position.row and self.col < position.col

    def __le__(self, position: object) -> bool:
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row <= position.row and self.col <= position.col

    def __gt__(self, position: object) -> bool:
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row > position.row and self.col > position.col

    def __ge__(self, position: object) -> bool:
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        return self.row >= position.row and self.col >= position.col

    def __add__(self, direction: object) -> Position:
        if not isinstance(direction, Direction):
            raise TypeError(f"{direction} is not 'Direction'")
        return Position(self.row + direction.row, self.col + direction.col)


class Board:
    """Reversi board

    This is supposed to be immutable
    """

    def __init__(self, config: npt.NDArray[np.int8]):
        """init

        config must be a squire matrix. elements of config must be -1, 0, or 1.
        上記の条件はチェックしないから，外部から呼ぶ場合は注意すること．

        Args:
            config (np.ndarray): configuration of the board
        """
        self._config: npt.NDArray[np.int8] = config.copy()
        self._config.setflags(write=False)

    def __eq__(self, board: object) -> bool:
        return isinstance(board, Board) and np.array_equal(self._config, board._config)

    def __ne__(self, board: object) -> bool:
        return not self.__eq__(board)

    def __getitem__(self, position: object) -> Square:
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not 'Position'")
        if not self.is_in_range(position):
            raise IndexError(f"{position} is out of range")
        return Square(self._config[position])

    def __str__(self) -> str:
        board_str = ""
        for line in self._config:
            for elem in line:
                board_str += str(Square(elem))
            board_str += "\n"
        # remove last new line
        return board_str[:-1]

    def __repr__(self) -> str:
        return f"Board(\n{repr(self._config)})"

    def __iter__(self) -> Iterator[Position]:
        return iter([Position(*index) for index in np.ndindex(*self.config.shape)])

    @property
    def config(self) -> npt.NDArray[np.int8]:
        return self._config

    def is_in_range(self, position: Position) -> bool:
        return Position(0, 0) <= position < Position(*self._config.shape)
