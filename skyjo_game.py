import random
from player_interface import PlayerInterface

FIRST_ROUND_INDEX = 0


class SkyJoGame:
    def __init__(self, players: list[PlayerInterface]):
        self.players = players
        self.current_player = 0
        self.round = FIRST_ROUND_INDEX
        self.winner = None
        self.player_cards = []
        self.player_scores = []
        self.cards = []
        self.discard_pile = []

    def start_round(self, index_of_last_player_to_end_round=-1):
        self.round += 1
        self._reset_cards()
        self.deal_cards()
        self.discard_pile.append(self.cards.pop())
        self.player_scores = [0 for _ in range(self.no_of_players)]

        for player in self.players:
            player.start_round()

        self.players = self._get_players_ordered(index_of_last_player_to_end_round)
        self.current_player = 0

    # Sorts players for a new round,
    def _get_players_ordered(self, index_of_last_player_to_end_round=-1):
        # Sort players by their index to reset
        sorted_players = sorted(self.players, key=lambda x: x.index)
        start_index = 0
        if index_of_last_player_to_end_round == -1:
            # If first round, player with highest sum of uncovered cards starts
            start_index = sorted_players.index(
                max(sorted_players, key=lambda x: x.sum_of_uncovered_cards)
            )
        else:
            # If not first round, player who ended last round starts
            start_index = sorted_players.index(
                self.players[index_of_last_player_to_end_round]
            )
        # Rotate list so that starting player is first
        return sorted_players[start_index:] + sorted_players[:start_index]

    def _reset_cards(self):
        self.cards = [
            *[-2 for x in range(5)],
            *[0 for x in range(15)],
            *[x for x in range(-1, 13) if x != 0 for _ in range(10)],
        ]
        self.discard_pile = []
        self.player_cards = []

    def deal_cards(self):
        random.shuffle(self.cards)
        # Each player gets 12 cards
        self.player_cards = [
            [self.cards.pop() for _ in range(12)] for _ in range(self.no_of_players)
        ]

        print(self.player_cards)
