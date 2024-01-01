#!/usr/bin/env python3

import unittest.mock
from skyjo_game import SkyJoGame


class TestSkyjoGame(unittest.TestCase):
    def setUp(self):
        self.game = SkyJoGame(4)  # Assuming 4 players for the test

    def test_init(self):
        self.assertEqual(self.game.no_of_players, 4)
        self.assertEqual(self.game.current_player, 0)
        self.assertEqual(self.game.round, 0)
        self.assertIsNone(self.game.winner)
        self.assertIsInstance(self.game.player_cards, list)
        self.assertIsInstance(self.game.player_scores, list)
        self.assertIsInstance(self.game.cards, list)
        self.assertIsInstance(self.game.discard_pile, list)

    def test_player_cards_empty(self):
        self.assertEqual(len(self.game.player_cards), 0)

    def test_player_scores_empty(self):
        self.assertEqual(len(self.game.player_scores), 0)

    def test_cards_empty(self):
        self.assertEqual(len(self.game.cards), 0)

    def test_discard_pile_empty(self):
        self.assertEqual(len(self.game.discard_pile), 0)

    def test_reset_cards(self):
        self.game.reset_cards()
        self.assertEqual(len(self.game.cards), 150)
        self.assertEqual(len(self.game.discard_pile), 0)
        self.assertEqual(len(self.game.player_cards), 0)
        self.assertEqual(len([x for x in self.game.cards if x == -2]), 5)
        self.assertEqual(len([x for x in self.game.cards if x == 0]), 15)
        self.assertEqual(len([x for x in self.game.cards if x >= -1 and x <= 12]), 130)
        self.assertEqual(len([x for x in self.game.cards if x < -2 or x > 12]), 0)
        self.assertEqual(len([x for x in self.game.cards if x == -1]), 10)
        self.assertEqual(len([x for x in self.game.cards if x == 0]), 15)
        self.assertEqual(len([x for x in self.game.cards if x == 1]), 10)
        self.assertEqual(len([x for x in self.game.cards if x == 12]), 10)

    def test_deal_cards(self):
        self.game.reset_cards()
        self.game.deal_cards()
        self.assertEqual(len(self.game.cards), 101)
        self.assertEqual(len(self.game.discard_pile), 1)
        self.assertEqual(len(self.game.player_cards), 4)
        self.assertEqual(len(self.game.player_cards[0]), 12)
        self.assertEqual(len(self.game.player_cards[1]), 12)
        self.assertEqual(len(self.game.player_cards[2]), 12)
        self.assertEqual(len(self.game.player_cards[3]), 12)

    def test_start_round(self):
        self.game.start_round()
        self.assertEqual(len(self.game.player_scores), 4)
        self.assertEqual(self.game.round, 1)


if __name__ == "__main__":
    unittest.main()
