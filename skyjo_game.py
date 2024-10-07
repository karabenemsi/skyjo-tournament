import random
from players.player import Player
from card import Card


class SkyJoGame:
    def __init__(self, players: list[Player]):
        # Max number of players
        if len(players) > 8:
            raise ValueError("Too many players")
        # New turn order every game
        random.shuffle(players)
        self.players: list[Player] = players
        self.round = 0
        self._round_closer_id: str = None
        self._cards: list[Card] = []
        self._discard_pile: list[Card] = []

    def play_game(self) -> str:
        # Reset players
        for player in self.players:
            player.reset_game_score()

        # Play rounds until a player has 100 points
        winner_id = None
        while winner_id is None:
            self._play_round(self._round_closer_id)
            winner_id = self._check_for_winner()
        # print(f"Player {winner_id} won after {self.round} rounds!")
        return winner_id

    def _play_round(self, id_of_last_player_to_end_round: str = None):
        self.round += 1
        self._reset_cards()
        self._deal_cards()

        # print("Round no.", self.round)
        for player in self.players:
            player.start_round()

        self.players = self._get_players_ordered(id_of_last_player_to_end_round)

        # Run turns until final round
        round_finished = False
        while not round_finished:
            for player in self.players:
                self.player_turn(player)
                if player.are_all_cards_visible():
                    self._final_turn(player.id)
                    round_finished = True
                    break
        for player in self.players:
            player.add_round_to_game_score()
            player.reset_round_score()

    # Sorts players for a new round,
    def _get_players_ordered(self, id_of_last_player_to_end_round: str = None):
        if id_of_last_player_to_end_round is None:
            # If no player ended the round, start with player with highest sum of uncovered cards
            start_index = self.players.index(
                max(self.players, key=lambda x: x.sum_of_uncovered_cards())
            )
            return self.players[start_index:] + self.players[:start_index]
        else:
            # If player ended the round, start with player who ended the round
            start_index = self.players.index(
                [
                    player
                    for player in self.players
                    if player.id == id_of_last_player_to_end_round
                ][0]
            )
            return self.players[start_index:] + self.players[:start_index]

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
        # Put top card of deck on discard pile
        self._put_on_discard(self.pop_top_card())

    def get_top_discard_card(self):
        return self._discard_pile[-1]

    def pop_top_discard_card(self):
        return self._discard_pile.pop()

    def _put_on_discard(self, card: Card | list[Card]):
        if isinstance(card, list):
            for card in card:
                self._put_on_discard(card)
            return
        if card.get_value() is None:
            card.flip()
        self._discard_pile.append(card)

    def _fill_deck_from_discard(self):
        # Move all cards from discard pile to deck, except the top card
        while len(self._discard_pile) > 1:
            temp_card = self._discard_pile.pop()
            temp_card.flip()  # Flip card before adding to deck (to make it invisible again)
            self._cards.append(temp_card)
        # Shuffle the deck
        random.shuffle(self._cards)

    def pop_top_card(self):
        if len(self._cards) == 0:
            self._fill_deck_from_discard()
        card = self._cards.pop()
        card.flip()
        return card

    def _check_for_winner(self) -> str | None:
        # for player in self.players:
        #     print(f"{player.id} has {player.get_score()} points")
        for player in self.players:
            if player.get_game_score() >= 100:
                # Find player with lowest score
                lowest_id = min(self.players, key=lambda x: x.get_game_score()).id
                return [player.id for player in self.players if player.id == lowest_id][
                    0
                ]
        return None

    def _final_turn(self, closing_player_id: str):
        # Reorder players so that current player is first
        self.players = self._get_players_ordered(closing_player_id)
        self._round_closer_id = closing_player_id
        # print(f"{closing_player_id} ended the round!")
        # All players except current player get one more turn
        for player in self.players[1:]:
            self.player_turn(player)
        # Sum up score for each player
        for player in self.players:
            player.sum_up_round()
        # If current player has not lowest score, add penalty by adding card sum to score
        if min(self.players, key=lambda x: x.get_round_score()).id != closing_player_id:
            # print(f"{closing_player_id} has not lowest score, adding penalty")
            self.players[0].add_penalty()

    def player_turn(self, player: Player):
        # TODO: Check if player is doing a valid turn
        game_cards = len(self._cards) + len(self._discard_pile)
        player.draw_card(self)
        discarded_cards_count = len(self._discard_pile)
        # print("Number of cards in game (not in players decks):", game_cards)
        # Check if player poped on and only one card from discard or deck
        # print(
        #     "Number of cards after player draws card",
        #     len(self._cards) + len(self._discard_pile),
        #     len(self._cards),
        #     len(self._discard_pile),
        # )
        if len(self._cards) + len(self._discard_pile) != game_cards - 1:
            raise ValueError(f"{player.id} did not draw one card")
        discarded_card = player.discard_card(self)
        if discarded_card == None:
            raise ValueError("Player Discarded empty")
        self._put_on_discard(discarded_card)
        # for p in self.players:
        #     p.hook_card_discarded(self, player.id, [discarded_card])
        # Check if player put on one card on discard pile
        if len(self._discard_pile) != discarded_cards_count + 1:
            raise ValueError(f"{player.id} did not discard one card")
        # Check if player has 3 same cards in column
        discarded_column = player.discard_filled_column()
        if len(discarded_column) > 0:
            self._put_on_discard(discarded_column)
            # for p in self.players:
            #     p.hook_card_discarded(
            #         player.id, [x.get_value() for x in discarded_column]
            #     )

    def get_card_infos():
        return {
            "available_cards": range(-2, 13),
            "distribution": {
                -2: 5,
                -1: 10,
                0: 15,
                1: 10,
                2: 10,
                3: 10,
                4: 10,
                5: 10,
                6: 10,
                7: 10,
                8: 10,
                9: 10,
                10: 10,
                11: 10,
                12: 10,
            },
            "card_count": 150,
            "card_sum": 760,
        }
