from players.player import Player
from card import Card
import random
from skyjo_game import SkyJoGame
import questionary


class HumanPlayer(Player):
    def start_round(self):
        print("Your cards are:")
        self.print_cards()
        questionary.checkbox
        print("Which two cards do you want to flip?")
        card_index= input()
            self._cards[card_index].flip()
        # flip 2 random cards
        cards_to_flip = random.sample(range(0, len(self._cards)), 2)
        for card_index in cards_to_flip:

    def draw_card(self, game: SkyJoGame):
        if random.randint(0, 1) == 0:
            self._card_in_hand = game.pop_top_card()
        else:
            self._card_in_hand = game.pop_top_discard_card()

    def discard_card(self, game: SkyJoGame) -> Card:
        if self._card_in_hand is None:
            raise ValueError("No card in hand")

        # Three options: keep card in hand and trade for uncovered card, keep card in hand and trade for covered card, discard card in hand

        card_indices_with_higher_value = [
            index
            for index, card in enumerate(self._cards)
            if card is not None
            and card.get_value() is not None
            and card.get_value() >= self._card_in_hand.get_value()
        ]
        if len(card_indices_with_higher_value) > 0:
            index = random.choice(card_indices_with_higher_value)
            temp = self._cards[index]
            self._cards[index] = self._card_in_hand
            self._card_in_hand = None
            return temp

        # If no card is with value {temp.get_value()}smaller than the card in hand, discard the card in hand or switch with uncovered card
        # Indeces of all invisible cards
        invisible_cards_indices = [
            index
            for index, card in enumerate(self._cards)
            if card is not None and card.get_value() is None
        ]
        if random.randint(0, 1) == 0:
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
