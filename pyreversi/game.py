"""reversi game"""
from __future__ import annotations

from typing import Optional, cast

from pyreversi import logic
from pyreversi.models import Board, Disk, Position


class Game:
    """Game class"""

    def __init__(self, board: Board, disk: Disk):
        self.current_disk = disk
        self.board = board
        self._legal_actions = logic.obtain_legal_actions(board, self.current_disk)
        self._game_over = not self._legal_actions and not logic.obtain_legal_actions(
            board, cast(Disk, self.current_disk.reverse())
        )

    @staticmethod
    def init_game(length: int) -> Game:
        board = logic.init_board(length)
        return Game(board, Disk.DARK)

    def is_game_over(self) -> bool:
        return self._game_over

    def get_legal_actions(self) -> frozenset[Position]:
        return self._legal_actions

    def execute_action(self, action: Optional[Position]) -> None:
        """execute action

        Args:
            action (Optional[Position]): 石を置く場所，Noneならパス

        Raises:
            IllegalActionError: 石を置けるのにパスした場合，石を置けない場所を指定した場合
        """
        if not self.is_legal_action(action):
            raise IllegalActionError("不正な操作です．")
        # Noneならパスなので，boardは変わらない
        if isinstance(action, Position):
            self.board = logic.execute_action(self.board, self.current_disk, action)
        self.current_disk = cast(Disk, self.current_disk.reverse())
        self._legal_actions = logic.obtain_legal_actions(self.board, self.current_disk)
        # 自分も相手も石を置ける場所がないなら，ゲーム終了
        self._game_over = not self._legal_actions and not logic.obtain_legal_actions(
            self.board, cast(Disk, self.current_disk.reverse())
        )

    def is_legal_action(self, action: Optional[Position]) -> bool:
        """is legal action

        パスできるのはlegal_actionsがない場合のみ，石を置く場合は，legalな場所のみTrue

        Args:
            action (Optional[Position]): 石を置く場所，Noneならパス

        Returns:
            bool: True if legal action, False if illegal action
        """
        return (action is None and not self._legal_actions) or (
            isinstance(action, Position) and action in self._legal_actions
        )

    def count_disk(self, disk: logic.Disk) -> int:
        return logic.count_disk(self.board, disk)


class IllegalActionError(ValueError):
    pass
