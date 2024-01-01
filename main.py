#!/usr/bin/env python3
from skyjo_game import SkyJoGame
from players.random_player import RandomPlayer

if __name__ == "__main__":
    players = [RandomPlayer(0), RandomPlayer(1)]
    game = SkyJoGame(players)
    game.play_game()
