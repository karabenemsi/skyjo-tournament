import random
from players.player import Player
from card import Card


class SkyJoGame:
    def __init__(self, players: list[Player]):
        self.players = players
        self.round = 0
        self.winner = None
        self._cards: list[Card] = []
        self._discard_pile: list[Card] = []

    def play_game(self):
        # Play rounds until a player has 100 points
        while self.winner is None:
            self._play_round()
            self.winner = self._check_for_winner()
        print(f"Player {self.winner} won after {self.round} rounds!")

    def _play_round(self, index_of_last_player_to_end_round=-1):
        self.round += 1
        self._reset_cards()
        self._deal_cards()
        self._discard_pile.append(self._cards.pop())
        self.player_scores = [0 for _ in range(len(self.players))]

        for player in self.players:
            player.start_round()

        self.players = self._get_players_ordered(index_of_last_player_to_end_round)

        # Run turns until final round
        round_finished = False
        while not round_finished:
            for player in self.players:
                player.draw_card(self)
                self.put_on_discard(player.discard_card(self))
                # Check if player has 3 same cards in column
                self.put_on_discard(player.discard_filled_column())
                if player.are_all_cards_visible():
                    self._final_turn(player.id)
                    round_finished = True
                    print(f"Round {self.round} finished!")
                    break

    # Sorts players for a new round,
    def _get_players_ordered(self, index_of_last_player_to_end_round=-1):
        # Sort players by their index to reset
        sorted_players = sorted(self.players, key=lambda x: x.id)
        start_index = 0
        if index_of_last_player_to_end_round == -1:
            # If fi: list[Card]rst round, player with highest sum of uncovered cards starts
            start_index = sorted_players.index(
                max(sorted_players, key=lambda x: x.sum_of_uncovered_cards())
            )
        else:
            # If not first round, player who closed last round starts
            start_index = sorted_players.index(
                self.players[index_of_last_player_to_end_round]
            )
        # Rotate list so that starting player is first
        return sorted_players[start_index:] + sorted_players[:start_index]

    def _reset_cards(self):
        self._cards = [
            *[Card(-2) for x in range(5)],
            *[Card(0) for x in range(15)],
            *[Card(x) for x in range(-1, 13) if x != 0 for _ in range(10)],
        ]
        self._discard_pile = []
        for player in self.players:
            player.remove_all_cards()

    def _deal_cards(self):
        random.shuffle(self._cards)
        # Each player gets 12 cards
        for player in self.players:
            player.give_cards([self._cards.pop() for _ in range(12)])

    def get_top_discard_card(self):
        return self._discard_pile[-1]

    def pop_top_discard_card(self):
        return self._discard_pile.pop()

    def put_on_discard(self, card: Card | list[Card]):
        if isinstance(card, list):
            for card in card:
                self._put_on_discard(card)
            return
        if card.get_value() is None:
            card.flip()
        self._discard_pile.append(card)

    def pop_top_card(self):
        card = self._cards.pop()
        card.flip()
        return card

    def _check_for_winner(self) -> Player | None:
        for player in self.players:
            if player.get_score() >= 100:
                # Find player with lowest score
                lowest_id = min(self.players, key=lambda x: x.get_score()).id
                return [player.id for player in self.players if player.id == lowest_id][
                    0
                ]
        return None

    def _final_turn(self, closing_player_index: int):
        # Reorder players so that current player is first
        self.players = self._get_players_ordered(closing_player_index)
        # All players except current player get one more turn
        for player in self.players[1:]:
            player.draw_card(self)
            self.put_on_discard(player.discard_card(self))
            # Check if player has 3 same cards in column
            self.put_on_discard(player.discard_filled_column())
            # Flip all remaining cards of player and sum up score
            player.sum_up_score()
        # TODO: check if other player has less points and maybe double score if so
