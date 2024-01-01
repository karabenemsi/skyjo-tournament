from players.player import Player
from card import Card
import random
from skyjo_game import SkyJoGame


class RandomPlayer(Player):
    def start_round(self):
        # flip 2 random cards
        cards_to_flip = random.sample(range(0, len(self._cards)), 2)
        for card_index in cards_to_flip:
            self._cards[card_index].flip()

    def draw_card(self, game: SkyJoGame):
        if random.randint(0, 1) == 0:
            self._card_in_hand = game.pop_top_card()
        else:
            self._card_in_hand = game.pop_top_discard_card()

    def discard_card(self, game: SkyJoGame) -> Card:
        if self._card_in_hand is None:
            raise ValueError("No card in hand")
        for index, card in enumerate(self._cards):
            if (
                card is None
                or card.get_value() is None
                or self._card_in_hand.get_value() is None
            ):
                continue
            if card.get_value() <= self._card_in_hand.get_value():
                self._cards[index] = self._card_in_hand
                self._card_in_hand = None
                return card

        # If no card is smaller than the card in hand, discard the card in hand or switch with uncovered card
        if random.randint(0, 1) == 0:
            return self._card_in_hand
        else:
            # Indeces of all invisible cards
            invisible_cards_indices = [
                index
                for index, card in enumerate(self._cards)
                if card.get_value() is None
            ]

            if len(invisible_cards_indices) == 0:
                raise ValueError("No invisible cards")
            # Select random invisible card to switch with
            index_of_card_to_switch = random.choice(invisible_cards_indices)
            temp = self._cards[index_of_card_to_switch]
            self._cards[index_of_card_to_switch] = self._card_in_hand
            return temp
