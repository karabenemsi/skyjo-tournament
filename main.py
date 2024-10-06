#!/usr/bin/env python3
from skyjo_game import SkyJoGame
from players.random_player import RandomPlayer
from players.min_max_player import MinMaxPlayer
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    players = [
        # RandomPlayer("Random Jürgen"),
        MinMaxPlayer("MinMax Joachim 1", {"take_threshold": 5}),
        MinMaxPlayer("MinMax Joachim 2", {"take_threshold": 5}),
        MinMaxPlayer("MinMax Joachim 3", {"take_threshold": 5}),
        # MinMaxPlayer("MinMax Joachim 4", {"take_threshold": 5}),
        # MinMaxPlayer("MinMax Joachim 5", {"take_threshold": 5}),
        # MinMaxPlayer("MinMax Joachim 6", {"take_threshold": 5}),
        # MinMaxPlayer("MinMax Joachim 7", {"take_threshold":7}),
        # MinMaxPlayer("MinMax Joachim 8", {"take_threshold":8}),
        # CustomPlayer("CustomPlayer"), # Add your player here
    ]
    scores = {player.id: 0 for player in players}
    for i in range(2):
        game = SkyJoGame(players)
        winner = game.play_game()
        scores[winner]["wins"] += 1
    logger.info(scores)
