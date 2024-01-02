#!/usr/bin/env python3
from skyjo_game import SkyJoGame
from players.random_player import RandomPlayer
from players.min_max_player import MinMaxPlayer

if __name__ == "__main__":
    players = [
        RandomPlayer("Random Jürgen"),
        MinMaxPlayer("MinMax Joachim"),
        # CustomPlayer("CustomPlayer"), # Add your player here
    ]
    scores = {player.id: 0 for player in players}
    for i in range(1000):
        game = SkyJoGame(players)
        winner = game.play_game()
        scores[winner] += 1

    print(scores)
