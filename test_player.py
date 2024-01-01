#!/usr/bin/env python3

import unittest.mock
from players.player import Player
from card import Card


class TestPlayerMainClass(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")
        self.cardDeck = [Card(x) for x in range(-2, 13)]

    def test_init(self):
        self.assertEqual(self.player.id, "TestPlayer")
        self.assertEqual(self.player._cards, [])
        self.assertIsNone(self.player._card_in_hand)
        self.assertEqual(self.player._score, 0)

    def test_give_cards(self):
        self.player.give_cards(self.cardDeck[2:6])
        self.assertEqual(self.player._cards, self.cardDeck[2:6])

    def test_remove_all_cards(self):
        self.player.give_cards(self.cardDeck[2:6])
        self.player.remove_all_cards()
        self.assertEqual(self.player._cards, [])

    def test_get_cards(self):
        self.player.give_cards(self.cardDeck[2:6])
        self.assertEqual(self.player.get_cards(), self.cardDeck[2:6])

    def test_flip_card(self):
        self.player.give_cards(self.cardDeck[2:6])
        self.player.flip_card(0)
        self.assertEqual(self.player.get_cards()[0].get_value(), 0)

    def test_are_all_cards_visible(self):
        self.player.give_cards(self.cardDeck[2:6])
        self.assertFalse(self.player.are_all_cards_visible())
        self.player.flip_card(0)
        self.player.flip_card(1)
        self.player.flip_card(2)
        self.player.flip_card(3)
        self.assertTrue(self.player.are_all_cards_visible())

    def test_print_cards(self):
        pass
        # self.player.give_cards(self.cardDeck[:12])
        # with unittest.mock.patch("builtins.print") as mock_print:
        #     self.player.print_cards()
        #     mock_print.assert_called_with("X 0 1 2 \n3 4 5 6 \n7 8 9 10 \n")

    def test_discard_filled_column(self):
        cards = [Card(x) if x % 4 != 0 else Card(4) for x in range(12)]
        cards_to_discard = [x for x in cards if x.peak() == 4]

        self.player.give_cards(cards)
        self.player.flip_card(0)
        self.player.flip_card(4)
        self.player.flip_card(8)
        self.assertEqual(self.player.discard_filled_column(), cards_to_discard)
        for i in range(12):
            if i % 4 == 0:
                self.assertIsNone(self.player._cards[i])
            else:
                self.assertEqual(self.player._cards[i], cards[i])


if __name__ == "__main__":
    unittest.main()
