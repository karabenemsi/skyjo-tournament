from card import Card


class Player:
    def __init__(self, id: int):
        self.id = id
        self._cards: list[
            Card | None
        ] = []  # list of cards, starting from top left corner
        self._card_in_hand: Card | None = None
        self._score = 0

    def give_cards(self, cards: list[int]):
        # receive cards from dealer
        self._cards = cards

    def remove_all_cards(self):
        # receive cards from dealer
        self._cards = []

    def get_cards(self) -> list[Card | None]:
        return self._cards

    def flip_card(self, index: int):
        self.card[index].flip()

    def are_all_cards_visible(self) -> bool:
        return all(
            card.get_value() is not None for card in self._cards if card is not None
        )

    def discard_filled_column(self) -> list[Card]:
        # Cards indexes are ordered like this:
        # 0 1 2 3
        # 4 5 6 7
        # 8 9 10 11
        # if three cards in a column have the same value, discard them
        discarded_cards = []
        for i in range(4):
            column_cards = [self._cards[i], self._cards[i + 4], self._cards[i + 8]]
            if all(
                (
                    card.get_value() == column_cards[0].get_value()
                    and card.get_value() is not None
                )
                for card in column_cards
            ):
                discarded_cards.extend(column_cards)
                self._cards[i] = None
                self._cards[i + 4] = None
                self._cards[i + 8] = None
        self._cards = [card for card in self._cards if card is not None]
        return discarded_cards

    def sum_of_uncovered_cards(self) -> int:
        return sum(
            card.get_value() for card in self._cards if card.get_value() is not None
        )

    def get_score(self):
        return self._score

    def sum_up_score(self):
        for card in self._cards:
            if card.get_value() is None:
                card.flip()

        self._score += sum(card.get_value() for card in self._cards)

    # These functions have to be implemented by the player
    def start_round(self):
        # uncover 2 cards
        # Put in some clever logic here, must flip 2 cards
        pass

    def draw_card(self, game):
        # do turn
        pass

    def discard_card(self, game) -> Card:
        # do turn
        pass
