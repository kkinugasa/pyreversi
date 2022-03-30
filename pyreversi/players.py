"""reversi players"""
import random
from typing import Dict, List, Optional

from pyreversi.game import Game
from pyreversi.logic import count_disk, execute_action
from pyreversi.models import Disk, Position


class Player:
    """Player class"""

    disk: Disk

    def set_disk(self, disk: Disk) -> None:
        """set player's disk"""
        self.disk = disk

    def play(self, game: Game) -> Optional[Position]:
        pass


class RandomPlayer(Player):
    """Random player

    可能な行動の中からランダムに実行するプレイヤー
    """

    def play(self, game: Game) -> Optional[Position]:
        legal_actions = game.get_legal_actions()
        if not legal_actions:
            return None
        return random.choice(list(legal_actions))


class GreedyPlayer(Player):
    """Greedy player

    常に自分の石が一番多くなる行動をするプレイヤー
    """

    def play(self, game: Game) -> Optional[Position]:
        legal_actions = game.get_legal_actions()
        if not legal_actions:
            return None
        flip_num_action: Dict[int, List[Position]] = {}
        current_disk_num = count_disk(game.board, game.current_disk)
        for action in legal_actions:
            next_disk_num = count_disk(
                execute_action(game.board, game.current_disk, action), game.current_disk
            )
            if flip_num_action.get(next_disk_num - current_disk_num) is None:
                flip_num_action[next_disk_num - current_disk_num] = [action]
            else:
                flip_num_action[next_disk_num - current_disk_num].append(action)
        return random.choice(flip_num_action[max(flip_num_action.keys())])


class HumanPlayer(Player):
    """Human player"""

    def play(self, game: Game) -> Optional[Position]:
        legal_actions = game.get_legal_actions()
        for position in legal_actions:
            print("[", position.row, position.col, end=" ] ")
        action: Optional[Position]
        while True:
            input_action = input()
            if input_action == "pass" and not legal_actions:
                action = None
                break
            input_a = input_action.split(" ")
            if len(input_a) == 2:
                try:
                    row, col = [int(i) for i in input_a]
                    if Position(row, col) in legal_actions:
                        action = Position(row, col)
                        break
                except ValueError:
                    # Input needs to be an integer
                    print("Invalid integer")
            print("Invalid action")
        return action
