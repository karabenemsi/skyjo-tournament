from typing import List, Literal
from players.player import Player
from card import Card
import random
from skyjo_game import SkyJoGame
import logging

logger = logging.getLogger(__name__)


class TrackerPlayer(Player):

    def __init__(self, id: str, settings: dict = None):
        super().__init__(id, settings)
        self._average_hidden_card_value: int = 5.066666

    def start_round(self):
        # Reset discard_pile at start of game
        self._discard_pile = []
        # flip 2 random cards
        cards_to_flip = random.sample(range(0, len(self._cards)), 2)
        for card_index in cards_to_flip:
            self._cards[card_index].flip()

    def draw_card(self, game: SkyJoGame):
        self.recalculate_average()
        discard_potentials = self._get_card_potential(game.get_top_discard_card())
        top_card_potentials = self._get_card_potential(None)

        if max([x for x in discard_potentials if x is not None]) > max(
            [x for x in top_card_potentials if x is not None]
        ):
            logger.debug("Taking from discard pile")
            self._card_in_hand = game.pop_top_discard_card()
        else:
            logger.debug("Taking from deck")
            self._card_in_hand = game.pop_top_card()

    def discard_card(self, game: SkyJoGame) -> Card:
        if self._card_in_hand is None:
            raise ValueError("No card in hand")

        self.recalculate_average()

        # Find card with highest value on table, if card is not visible then value is the average value of a card
        card_index_with_hightest_value = self._cards.index(
            max(
                self._cards,
                # 5 is the average value of a card in the game
                # TODO: This could be adjusted according to what we know about uncovered cards)
                key=lambda c: (
                    c.get_value(self._average_hidden_card_value)
                    if c is not None
                    else -30
                ),
            )
        )

        # If the card with higest value is None, we have no cards left, this is not allowed (or is it?)
        if self._cards[card_index_with_hightest_value] is None:
            self.print_cards()
            raise ValueError("We have an empty spot on our table")

        # If the highest card on table is higher than the card in hand, switch them and discard the card in hand
        if (
            self._cards[card_index_with_hightest_value].get_value() is not None
            and self._card_in_hand.get_value()
            <= self._cards[card_index_with_hightest_value].get_value()
        ):
            logger.debug(
                f"Switching card in hand ({self._card_in_hand.get_value()}) with card from deck ({self._cards[card_index_with_hightest_value].get_value()})"
            )
            temp = self._cards[card_index_with_hightest_value]

            improvement = (
                self._cards[card_index_with_hightest_value].get_value()
                - self._card_in_hand.get_value()
            )
            logger.debug(f"Improved by {improvement}, keep hand, switch with higher")

            self._cards[card_index_with_hightest_value] = self._card_in_hand
            self._card_in_hand = None
            return temp

        # If no card is with value higher than the card in hand, discard the card in hand or switch with uncovered card
        # Indeces of all invisible cards
        invisible_cards_indices = [
            index
            for index, card in enumerate(self._cards)
            if card is not None and card.get_value() is None
        ]

        # If the card in hand is higher than the threshold, flip a random invisible card and discard the card in hand
        if self._card_in_hand.get_value() >= 2.5:
            random_card = self._cards[random.choice(invisible_cards_indices)]
            # Flip a random invisible card and discard the card in hand
            random_card.flip()
            logger.debug(
                f"Improved by {random_card.get_value() - self._average_hidden_card_value}, could have been {random_card.get_value() - self._card_in_hand.get_value()}, discard hand"
            )
            temp = self._card_in_hand
            self._card_in_hand = None
            return temp
        else:
            if len(invisible_cards_indices) == 0:
                raise ValueError("No invisible cards")
            # Select random invisible card to switch with
            index_of_card_to_switch = random.choice(invisible_cards_indices)
            temp = self._cards[index_of_card_to_switch]
            logger.debug(
                f"Improved by {self._card_in_hand.get_value() - temp.peak()}, could have been {self._card_in_hand.get_value() - self._average_hidden_card_value}, keep hand, flip random"
            )
            self._cards[index_of_card_to_switch] = self._card_in_hand
            self._card_in_hand = None
            return temp

    # def hook_card_discarded(self, game, player_id, card_value: List[int]):

    #     self._discard_pile.extend(card_value)

    def recalculate_average(self):
        # We know all cards in the game, number of cards is 150
        # Get visible cards of all players
        # Get uncovered cards from discard_pile
        # TODO: handle case when discard_pile gets shuffled
        self._average_hidden_card_value = 5

    def get_chances_for_hidden_cards(
        self,
        game,
    ):
        chances = {value: 0 for value in range(-2, 13)}
        return chances

    """ Returns the cards potential for each position
        Returns a list of potential in the following placement
        0  1  2  3
        4  5  6  7
        8  9  10 11 
    """

    def _get_card_potential(self, card: Card | None):
        card_value = (
            card.get_value() if card is not None else self._average_hidden_card_value
        )
        if card_value == None:
            raise ValueError("Trying to asses potential of a hidden card")

        potentialmap = []
        cards_hidden = [c is not None and c.get_value() is None for c in self._cards]
        only_one_left = sum(cards_hidden) == 1
        for pos, t_card in enumerate(self._cards):
            value = 0

            # If this position is empty, we can not place anything here
            if t_card == None:
                value = None
                potentialmap.append(value)
                continue

            # If this position is the last

            # If the card in the current position is hidden, we use the average value
            if t_card.get_value() == None:
                value = self._average_hidden_card_value - card_value
            # If the other cards in this column have the same value as this one,
            # The the potential includes eliminating them
            row_size = 4
            num_rows = 3
            # Get neighboring card values by adjusting the position based on row
            other_card_values = [
                self._cards[pos + offset]
                for offset in (-row_size, row_size)
                if 0 <= pos + offset < row_size * num_rows
            ]

            # If both other cards have the same value, we would eliminate a row
            if all(v is not None and v == card_value for v in other_card_values):
                value -= other_card_values[0]
            elif card_value in other_card_values and None in other_card_values:
                # TODO if only one other card has the same value and the other is hidden,
                # We could calculate the chance for the hidden card to be the card we want, for now do the default thing
                if t_card.is_visible():
                    value = t_card.get_value() - card_value
                else:
                    value = self._average_hidden_card_value - card_value
            else:
                # Default case: we would replace the current card
                if t_card.is_visible():
                    value = t_card.get_value() - card_value
                else:
                    value = self._average_hidden_card_value - card_value

            # if this position is the last uncovered card, we might want to wait with
            # uncovering to avoid a penalty, we need to look at the potential of other
            # players to do this, so we will skip it for not and just assume we get a
            # penalty any other time
            if only_one_left and cards_hidden[pos] == True:
                value += (
                    self.sum_of_uncovered_cards() + self._average_hidden_card_value
                ) / 3
            potentialmap.append(value)
        return potentialmap
