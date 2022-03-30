"""Entry point"""
import pyreversi.game
import pyreversi.players
from pyreversi.logic import Disk

game = pyreversi.game.Game.init_game(6)
# player1 = pyreversi.players.HumanPlayer()
player1 = pyreversi.players.RandomPlayer()
player2 = pyreversi.players.GreedyPlayer()

players_list = [player1, player2]
turn = 0
print(game.board)
print()
while not game.is_game_over():
    action = players_list[turn % 2].play(game)
    if not game.is_legal_action(action):
        print("無効な操作です．")
        continue
    game.execute_action(action)
    print(game.board)
    print()
    turn += 1
print("turn", turn)
print(Disk.DARK, game.count_disk(Disk.DARK))
print(Disk.LIGHT, game.count_disk(Disk.LIGHT))
