""" This application is a Minesweeper game created using the library Arcade. (http://arcade.academy)

    Minesweeper is a single-player puzzle video game. 
    The objective of the game is to clear a rectangular board containing 
    hidden "mines" or bombs without detonating any of them, with help from clues about 
    the number of neighboring mines in each field.
"""

from board import Board
from view import View

import arcade
import os


class Minesweeper(arcade.Window):
    TITLE = 'Minesweeper'

    def __init__(self, size: int):
        window_size = size * View.PIXELS_PER_FIELD
        super().__init__(window_size, window_size, Minesweeper.TITLE)
        self.set_update_rate(1)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.board = Board(size)
        self.view = View(size, os.getcwd() + "\\assets\\")

        self.view.update_all_sprites(self.board.play_board)
        self.on_draw()

    def on_draw(self):
        self.view.draw(self.board.game_state)

    def on_mouse_press(self, px, py, button, modifires):
        if self.board.game_state != Board.GS_IN_PROGRESS:
            self.board.new_game()
            self.view.update_all_sprites(self.board.play_board)
            self.on_draw()
            return
        x = self.pixels_to_coordinates(px)
        y = self.pixels_to_coordinates(py)
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.board.uncover(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.board.mark_mine(x, y)

        self.view.update_all_sprites(self.board.play_board)
        self.on_draw()

    def pixels_to_coordinates(self, pixels):
        return int(pixels / View.PIXELS_PER_FIELD)


def main():
    window = Minesweeper(20)
    arcade.run()


if __name__ == "__main__":
    main()
