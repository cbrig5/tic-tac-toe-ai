# build a tic tac to game

class TicTacToe:
    def __init__(self):
        self.board = [''] * 9
        self.current_player = 'X'

    def reset(self):
        self.board = [''] * 9
        self.current_player = 'X'
        return self.board.copy()
    
    def get_valid_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == '']

    def make_move(self, index):
        if index in self.get_valid_moves():
            self.board[index] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for i,j,k in winning_combinations:
            if self.board[i] == self.board[j] == self.board[k] and self.board[k] != '':
                return self.board[i]
        if '' not in self.board:
            return 'Cats Game'
        return None