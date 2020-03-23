from board import Board
from math import floor
import arcade


class View:
    TEXTURE_SIZE = 100
    TEXTURE_SCALE = .5
    PIXELS_PER_FIELD = int(TEXTURE_SIZE * TEXTURE_SCALE)

    MESSAGE_WIN = "You win!"
    MESSAGE_WIN_COLOR = arcade.color.GREEN
    MESSAGE_LOSE = "You lose..."
    MESSAGE_LOSE_COLOR = arcade.color.RED

    texture_names = [
        "0.png",
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
        "6.png",
        "7.png",
        "mine_triggered.png",
        "flag.png",
        "hidden_field.png"
    ]

    def __init__(self, size, asset_dir):
        self.sprite_list = arcade.SpriteList()
        self.size = size
        self.textures = self.create_textures(asset_dir)
        self.fill_sprite_list()

    @staticmethod
    def create_textures(asset_dir):
        textures = []
        for name in View.texture_names:
            path = asset_dir + name
            texture = arcade.load_texture(path, scale=View.TEXTURE_SCALE)
            textures.append(texture)
        return textures

    def update_all_sprites(self, play_board):
        for i, sprite in enumerate(self.sprite_list):
            x, y = self.map_coordinates(i)
            current_state = play_board[x][y]
            if sprite.state != current_state:
                sprite.set_texture(current_state)

    def map_coordinates(self, i):
        if not i:
            return 0, 0
        return int(floor(i / self.size)), int(i % self.size)

    def fill_sprite_list(self):
        for x in range(self.size):
            for y in range(self.size):
                new_sprite = arcade.Sprite()
                for texture in self.textures:
                    new_sprite.append_texture(texture)
                new_sprite.state = None
                px = (x + .5) * View.PIXELS_PER_FIELD
                py = (y + .5) * View.PIXELS_PER_FIELD
                new_sprite._set_center_x(px)
                new_sprite._set_center_y(py)
                self.sprite_list.append(new_sprite)

    def draw(self, game_state):
        arcade.start_render()
        self.sprite_list.draw()
        if game_state == Board.GS_WON:
            self.draw_text(View.MESSAGE_WIN, View.MESSAGE_WIN_COLOR)
        elif game_state == Board.GS_LOST:
            self.draw_text(View.MESSAGE_LOSE, View.MESSAGE_LOSE_COLOR)

        arcade.finish_render()

    def draw_text(self, text, color):
        window_center = self.size * self.PIXELS_PER_FIELD / 2
        arcade.draw_text(text, start_x=window_center, start_y=window_center, color=color,
                         font_size=32, align="center", anchor_x="center", anchor_y="center")
