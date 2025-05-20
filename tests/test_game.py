import unittest
from game.game import TicTacToe

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_initialization(self):
        self.assertEqual(self.game.board, [''] * 9)
        self.assertEqual(self.game.current_player, 'X')

    def test_reset(self):
        self.game.make_move(0)
        self.game.reset()
        self.assertEqual(self.game.board, [''] * 9)
        self.assertEqual(self.game.current_player, 'X')

    def test_get_valid_moves(self):
        self.game.make_move(0)
        valid_moves = self.game.get_valid_moves()
        self.assertIn(1, valid_moves)
        self.assertIn(2, valid_moves)
        self.assertIn(3, valid_moves)
        self.assertIn(4, valid_moves)
        self.assertIn(5, valid_moves)
        self.assertIn(6, valid_moves)
        self.assertIn(7, valid_moves)
        self.assertIn(8, valid_moves)

    def check_winner(self):
        self.game.make_move(0)
        self.game.make_move(1)
        self.game.make_move(3)
        self.game.make_move(4)
        self.game.make_move(6)
        winner = self.game.check_winner()
        self.assertEqual(winner, 'X')

    def test_draw(self):
        moves = [
            0, 1, 2,
            5, 3, 6,
            4, 8, 7,
        ]
        for move in moves:
            self.game.make_move(move)
        winner = self.game.check_winner()
        self.assertEqual(winner, 'Cats Game')

if __name__ == '__main__':
    unittest.main()