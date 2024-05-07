import unittest
from unittest.mock import MagicMock

import numpy as np
from skatzero.game.game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game('N')
        self.game.round = MagicMock()
        self.game.round.soloplayer_id = 0
        self.game.round.solo_points = 75
        self.game.round.opponent_points = 0
        self.game.blind_hand = False
        self.game.open_hand = False
        self.game.black_soloplayer = False
        self.game.black_opponent = False

    def test_compute_rewards_null_game(self):
        self.game.black_soloplayer = True
        payoffs = self.game.compute_rewards(is_training=False)
        expected_payoffs = np.array([73, -73/4, -73/4], dtype=float)
        self.assertTrue(np.array_equal(payoffs, expected_payoffs))

    def test_compute_rewards_grand(self):
        self.game.gametype = 'G'
        payoffs = self.game.compute_rewards(is_training=False)
        expected_payoffs = np.array([98, -98/4, -98/4], dtype=float)
        self.assertTrue(np.array_equal(payoffs, expected_payoffs))

    def test_compute_rewards_diamonds(self):
        self.game.gametype = 'D'
        payoffs = self.game.compute_rewards(is_training=False)
        expected_payoffs = np.array([70, -70/4, -70/4], dtype=float)
        self.assertTrue(np.array_equal(payoffs, expected_payoffs))


    def test_check_trick_winner_0(self):
        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1
        player2 = MagicMock()
        player2.player_id = 2
        self.game.round.current_trick = [(player0, 'C7'), (player1, 'C8'), (player2, 'C9')]
        self.game.round.trump = 'D'
        self.game.round.current_suit = 'C'

        # Call the function and check the result
        winner = self.game.check_trick()
        self.assertEqual(winner, 2)
        self.assertEqual(self.game.round.opponent_points, 0)
        self.assertEqual(self.game.round.solo_points, 75)
        self.assertEqual(self.game.done, False)

    def test_check_trick_winner_1(self):
        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1
        player2 = MagicMock()
        player2.player_id = 2
        self.game.round.current_trick = [(player0, 'C7'), (player1, 'DJ'), (player2, 'CT')]
        self.game.round.trump = 'D'
        self.game.round.current_suit = 'C'

        # Call the function and check the result
        winner = self.game.check_trick()
        self.assertEqual(winner, 1)
        self.assertEqual(self.game.round.opponent_points, 12)
        self.assertEqual(self.game.round.solo_points, 75)
        self.assertEqual(self.game.done, False)

    def test_check_trick_winner_2(self):
        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1
        player2 = MagicMock()
        player2.player_id = 2
        self.game.round.current_trick = [(player0, 'C7'), (player1, 'DJ'), (player2, 'CJ')]
        self.game.round.trump = 'D'
        self.game.round.current_suit = 'C'

        # Call the function and check the result
        winner = self.game.check_trick()
        self.assertEqual(winner, 2)
        self.assertEqual(self.game.round.opponent_points, 4)
        self.assertEqual(self.game.round.solo_points, 75)
        self.assertEqual(self.game.done, False)

    def test_check_trick_no_winner(self):
        player0 = MagicMock()
        player0.player_id = 0
        player1 = MagicMock()
        player1.player_id = 1
        player2 = MagicMock()
        player2.player_id = 2
        self.game.round.current_trick = [(player0, 'C7'), (player1, 'DJ')]
        self.game.round.trump = 'D'
        self.game.round.current_suit = 'C'

        # Call the function and check the result
        winner = self.game.check_trick()
        self.assertEqual(winner, -1)
        self.assertEqual(self.game.round.opponent_points, 0)
        self.assertEqual(self.game.round.solo_points, 75)
        self.assertEqual(self.game.done, False)

if __name__ == '__main__':
    unittest.main()
