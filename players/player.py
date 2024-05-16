from card import Card


class Player:
    def __init__(self, id: str, settings: dict = None):
        self.id = id
        self._cards: list[Card | None] = (
            []
        )  # list of cards, starting from top left corner
        self._card_in_hand: Card | None = None
        self._score = 0
        self._settings = settings

    def give_cards(self, cards: list[int]):
        # receive cards from dealer
        self._cards = cards.copy()

    def remove_all_cards(self):
        # receive cards from dealer
        self._cards = []

    def get_cards(self) -> list[Card | None]:
        return self._cards

    def flip_card(self, index: int):
        self._cards[index].flip()

    def are_all_cards_visible(self) -> bool:
        return all(
            card.get_value() is not None for card in self._cards if card is not None
        )

    def print_cards(self):
        print(f"{self.id} has cards:")
        for index, card in enumerate(self._cards):
            print(card if card is not None else "X ", end=" ")
            if index % 4 == 3 and index != 11:
                print()
        print()

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
                    card is not None
                    and card.get_value() == column_cards[0].get_value()
                    and card.get_value() is not None
                )
                for card in column_cards
            ):
                discarded_cards.extend(column_cards)
                self._cards[i] = None
                self._cards[i + 4] = None
                self._cards[i + 8] = None
        # if len(discarded_cards) > 0:
        #     print("Full Column, Discarded cards:", discarded_cards)
        return discarded_cards

    def sum_of_uncovered_cards(self) -> int:
        return sum(
            card.get_value()
            for card in self._cards
            if card is not None and card.get_value() is not None
        )

    def get_score(self):
        return self._score

    def sum_up_score(self):
        for card in self._cards:
            if card is not None and card.get_value() is None:
                card.flip()

        self._score += self.sum_of_uncovered_cards()

    def add_penalty(self):
        self._score += self.sum_of_uncovered_cards()

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
