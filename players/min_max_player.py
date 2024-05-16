from players.player import Player
from card import Card
import random
from skyjo_game import SkyJoGame


class MinMaxPlayer(Player):
    def start_round(self):
        # flip 2 random cards
        cards_to_flip = random.sample(range(0, len(self._cards)), 2)
        for card_index in cards_to_flip:
            self._cards[card_index].flip()

    def draw_card(self, game: SkyJoGame):
        highest_card_value = max(
            [r.get_value() or -10 for r in self._cards if r is not None]
        )
        if highest_card_value > game.get_top_discard_card().get_value():
            print("Taking from discard pile")
            self._card_in_hand = game.pop_top_discard_card()
        else:
            print("Taking from deck")
            self._card_in_hand = game.pop_top_card()

    def discard_card(self, game: SkyJoGame) -> Card:
        if self._card_in_hand is None:
            raise ValueError("No card in hand")

        # Find card with highest value on table, if card is not visible then value is -20 (not None to avoid errors)
        card_index_with_hightest_value = self._cards.index(
            max(
                self._cards,
                key=lambda c: c.get_value(-20) if c is not None else -20,
            )
        )

        print("Index with highest value:", card_index_with_hightest_value)
        if self._cards[card_index_with_hightest_value] is None:
            self.print_cards()
        print("Card in hand:", self._card_in_hand)
        print("Highest card on table:", self._cards[card_index_with_hightest_value])
        # If the highest card on table is higher than the card in hand, switch them and discard the card in hand
        if (
            self._card_in_hand.get_value()
            < self._cards[card_index_with_hightest_value].get_value()
        ):
            temp = self._cards[card_index_with_hightest_value]
            self._cards[card_index_with_hightest_value] = self._card_in_hand
            self._card_in_hand = None
            return temp

        # # There must be a card with the hightest value
        # if card_index_with_hightest_value:
        #     # print(card_index_with_hightest_value)
        #     temp = self._cards[card_index_with_hightest_value]
        #     self._cards[card_index_with_hightest_value] = self._card_in_hand
        #     self._card_in_hand = None
        #     return temp

        # card_indices_with_higher_value = [
        #     index
        #     for index, card in enumerate(self._cards)
        #     if card is not None
        #     and card.get_value() is not None
        #     and card.get_value() >= self._card_in_hand.get_value()
        # ]
        # if len(card_indices_with_higher_value) > 0:
        #     index = random.choice(card_indices_with_higher_value)
        #     temp = self._cards[index]
        #     self._cards[index] = self._card_in_hand
        #     self._card_in_hand = None
        #     return temp

        # If no card is with value higher than the card in hand, discard the card in hand or switch with uncovered card
        # Indeces of all invisible cards
        invisible_cards_indices = [
            index
            for index, card in enumerate(self._cards)
            if card is not None and card.get_value() is None
        ]

        # If the card in hand is higher than the threshold, flip a random invisible card and discard the card in hand
        if self._card_in_hand.get_value() >= self._settings["take_threshold"]:
            # Flip a random invisible card and discard the card in hand
            self._cards[random.choice(invisible_cards_indices)].flip()
            return self._card_in_hand
        else:
            if len(invisible_cards_indices) == 0:
                raise ValueError("No invisible cards")
            # Select random invisible card to switch with
            index_of_card_to_switch = random.choice(invisible_cards_indices)
            temp = self._cards[index_of_card_to_switch]
            self._cards[index_of_card_to_switch] = self._card_in_hand
            return temp
