from players.player import Player
from card import Card
from skyjo_game import SkyJoGame


# This is a template for your custom player. You can use it as a starting point for your own player.
# Once you have implemented your player, you can run it against the other players in main.py
class CustomPlayer(Player):
    def start_round(self):
        # You need to implement this method
        # This method is called at the beginning of each round and must flip 2 cards
        # You can access the cards with self._cards and flip them with card.flip()
        # e.g. self._cards[0].flip()
        pass

    def draw_card(self, game: SkyJoGame):
        # You need to implement this method
        # This method is called when it is your turn to draw a card
        # You must draw a card from either the deck or the discard pile
        # You can view the top card of the discard pile with game.get_top_discard_card()
        # You can draw the top card of the discard pile with game.pop_top_discard_card()
        # You can draw the top card of the deck with game.pop_top_card()
        # You must store the card you drew in self._card_in_hand
        # e.g. self._card_in_hand = game.pop_top_card()
        pass

    def discard_card(self, game: SkyJoGame) -> Card:
        if self._card_in_hand is None:
            raise ValueError("No card in hand")
        # You need to implement this method
        # This method is called when it is your turn to discard a card
        # You must discard a card
        # You can discard the card in your hand with return self._card_in_hand
        # You can discard another card with return self._cards[0]
        # If you place the card in your hand on the discard pile,
        # you must flip another card of your choice which is not already flipped
        # You must return the card you want to discard, you may return an unflipped/covered card
        # e.g. return self._card_in_hand
        # e.g. temp = self._cards[0]
        #      self._cards[0] = self._card_in_hand
        #      self._card_in_hand = None
        #      return temp
        pass

