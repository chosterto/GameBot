from random import choice
from math import inf

class TicTacToe:
    def __init__(self):
        self.grid = [
            [":black_large_square:", ":black_large_square:", ":black_large_square:"], 
            [":black_large_square:", ":black_large_square:", ":black_large_square:"], 
            [":black_large_square:", ":black_large_square:", ":black_large_square:"]
            ]
        self.winner = None


    def display(self):
        fancy_grid = [
            ["", ":red_square:", "", ":red_square:", ""], 
            [":red_square:", ":red_square:", ":red_square:", ":red_square:", ":red_square:"],
            ["", ":red_square:", "", ":red_square:", ""],
            [":red_square:", ":red_square:", ":red_square:", ":red_square:", ":red_square:"],
            ["", ":red_square:", "", ":red_square:", ""]
            ]
        for r in range(3):
            for c in range(3):
                fancy_grid[r * 2][c * 2] = self.grid[r][c]
        final_gameboard = "".join(j for i in fancy_grid for j in i + ["\n"])
        return final_gameboard


    def is_space_unoccupied(self, space):
        row = (space - 1) // 3
        col = (space - 1) % 3
        return self.grid[row][col] == ":black_large_square:"


    def mark_space(self, space):
        row = (space - 1) // 3
        col = (space - 1) % 3
        self.grid[row][col] = ":regional_indicator_x:"


    def bot_random(self):
        options = []
        for a, b in enumerate(self.grid):
            ind = [x for x, y in enumerate(b) if y == ":black_large_square:"]
            for i in ind:
                options.append((a, i))
        r_row, r_col = choice(options)
        self.grid[r_row][r_col] = ":regional_indicator_o:"
    

    def bot_smart(self):
        best_score = -inf
        best_row = None
        best_col = None
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] != ":black_large_square:":
                    continue 
                self.grid[r][c] = ":regional_indicator_o:"
                score = self._minimax(self.grid, 0, False)
                self.grid[r][c] = ":black_large_square:"
                if score > best_score:
                    best_score = score
                    best_row, best_col = r, c
        self.grid[best_row][best_col] = ":regional_indicator_o:"


    def is_finished(self):
        rows = self.grid
        cols = list(zip(*self.grid))
        diagonal_r = [[self.grid[i][i] for i in range(3)]]
        diagonal_l = [[self.grid[i][-i-1] for i in range(3)]]
        for markings in [rows, cols, diagonal_r, diagonal_l]:
            for m in markings:
                if ":black_large_square:" in m:
                    continue
                if len(set(m)) == 1:
                    self.winner = m[0]
                    return True
        return all(":black_large_square:" not in row for row in self.grid)
    

    def _find_winner(self, board):
        rows = board
        cols = list(zip(*board))
        diagonal_r = [[board[i][i] for i in range(3)]]
        diagonal_l = [[board[i][-i-1] for i in range(3)]]
        for markings in [rows, cols, diagonal_r, diagonal_l]:
            for m in markings:
                if ":black_large_square:" in m:
                    continue
                if len(set(m)) == 1:
                    return m[0]
        if all(":black_large_square:" not in row for row in board):
            return "tie"
        return None
    

    def _minimax(self, board, depth, maximizing_player):
        winner_ = self._find_winner(board)
        if winner_ == ":regional_indicator_o:":
            return 10 
        if winner_ == ":regional_indicator_x:":
            return -10 
        if winner_ == "tie":
            return 0
        if maximizing_player:
            best_score = -inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ":black_large_square:":
                        board[r][c] = ":regional_indicator_o:"
                        score = self._minimax(board, depth + 1, False)
                        board[r][c] = ":black_large_square:"
                        best_score = max(score, best_score)
            return best_score
        # Minimizing player 
        else: 
            best_score = inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ":black_large_square:":
                        board[r][c] = ":regional_indicator_x:"
                        score = self._minimax(board, depth + 1, True)
                        board[r][c] = ":black_large_square:"
                        best_score = min(score, best_score)
            return best_score
