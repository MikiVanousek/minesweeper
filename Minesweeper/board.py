from random import random
import numpy as np


class Board:
    """ Model class for the Minesweeper game. """
    # How many cells are there for one mine. The higher the number, the emptier the board, the easier the game is.
    MINE_SPARSITY = 4

    # play_board special values
    PB_HIDDEN_FIELD = -1
    PB_MARKED_FIELD = -2
    PB_TRIGGERED_MINE = -3

    GS_IN_PROGRESS = 0
    GS_WON = 1
    GS_LOST = -1

    def __init__(self, size: int):
        self.size = size
        # 1 for a won game, 0 for game in progress, -1 for loss; also true if game is finished
        self.game_state = None
        # Matrix storing the mines' location. 0 for empty location, 1 for a mine.
        self.mines = None
        self.play_board = None
        """Player-visible data. It a special Value (hidden)"""
        self.new_game()

    def new_game(self):
        self.game_state = Board.GS_IN_PROGRESS
        self.populate_mines()
        self.init_play_board()

    # Randomly populates board with mines. Edges left empty.
    def populate_mines(self):
        self.mines = np.zeros(shape=(self.size,)*2, dtype=int)
        fields_left = (self.size - 2)**2
        mines_left = int(fields_left / self.MINE_SPARSITY)

        # Everywhere, execpt the edges
        rng = range(1, self.size - 1)
        for row_index in rng:
            for item_index in rng:
                # propability with which we want to insert mine
                propability = mines_left / fields_left
                if random() < propability:
                    self.mines[row_index, item_index] = 1
                    mines_left -= 1
                fields_left -= 1

    def init_play_board(self):
        """Sets playboard to be size**2 array of hidden fields."""
        self.play_board = [[Board.PB_HIDDEN_FIELD for _ in range(
            self.size)] for _ in range(self.size)]

    def uncover(self, x, y):
        """ Uncovers a hidden field in play_board, setting its value to the number of surrounding mines if no mine is present.
        Retruns true if a mine was triggerd.
         """
        # Checks if we are uncovering valid hidden field.
        if not self.are_valid_coordinates((x, y)) or self.play_board[x][y] != Board.PB_HIDDEN_FIELD:
            return False
        # If tring to uncover bomb, triggers it, else counts surrounding mines.
        if self.mines[x][y]:
            self.play_board[x][y] = Board.PB_TRIGGERED_MINE
            self.game_state = Board.GS_LOST
            return True

        surrounding_mines = self.do_for_surrounding_fields(
            x, y, lambda x, y: self.mines[x][y])

        self.play_board[x][y] = surrounding_mines
        # If there are no surrouding mines, uncovers all surrounding fields.
        if not surrounding_mines:
            self.do_for_surrounding_fields(x, y, self.uncover)
        self.check_for_win()

        return False

    def check_for_win(self):
        if not any(Board.PB_HIDDEN_FIELD in row for row in self.play_board):
            self.game_state = Board.GS_WON

    def do_for_surrounding_fields(self, x, y, function):
        result = 0
        surrounding_range = range(-1, 2)
        for sx in surrounding_range:
            for sy in surrounding_range:
                alt_x = x + sx
                alt_y = y + sy
                if self.are_valid_coordinates((alt_x, alt_y)):
                    result += function(alt_x, alt_y)
        return result

    def is_mine(self, x, y):
        return self.mines[x][y]

    def are_valid_coordinates(self, coordinates):
        is_valid = True
        for c in coordinates:
            is_valid &= 0 <= c < self.size
        return is_valid

    def mark_mine(self, x, y):
        if self.play_board[x][y] == Board.PB_HIDDEN_FIELD:
            self.play_board[x][y] = Board.PB_MARKED_FIELD
            self.check_for_win()
        elif self.play_board[x][y] == Board.PB_MARKED_FIELD:
            self.play_board[x][y] = Board.PB_HIDDEN_FIELD
