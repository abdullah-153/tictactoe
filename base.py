import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class TicTacToeAI:
    def __init__(self):
        self.reset_board()

    def reset_board(self):
        self.board = ['' for _ in range(9)]

    def make_move(self, index, symbol):
        if self.board[index] == '':
            self.board[index] = symbol
            return True
        return False

    def available_moves(self):
        return [i for i, val in enumerate(self.board) if val == '']

    def check_winner(self, symbol):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for a, b, c in lines:
            if self.board[a] == self.board[b] == self.board[c] == symbol:
                return True
        return False

    def get_winner(self):
        for symbol in ['X', 'O']:
            if self.check_winner(symbol):
                return symbol
        return None

    def is_full(self):
        return '' not in self.board

    def minimax(self, is_maximizing, player, ai):
        winner = self.get_winner()
        if winner == ai:
            return 1
        elif winner == player:
            return -1
        elif self.is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves():
                self.board[move] = ai
                score = self.minimax(False, player, ai)
                self.board[move] = ''
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.board[move] = player
                score = self.minimax(True, player, ai)
                self.board[move] = ''
                best_score = min(score, best_score)
            return best_score

    def best_move(self, player, ai):
        best_score = -float('inf')
        move = None
        for i in self.available_moves():
            self.board[i] = ai
            score = self.minimax(False, player, ai)
            self.board[i] = ''
            if score > best_score:
                best_score = score
                move = i
        return move
