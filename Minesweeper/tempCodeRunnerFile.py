SE_COLOR)

        arcade.finish_render()

    def draw_text(self, text, color):
        arcade.draw_text(text, start_x=300, start_y=300, color=color,
                         font_size=32, align="center", anchor_x="center", anchor_y="center")


def main():
    window = Minesweeper(10)
    arcade.run()


if __name__ == "__main__":
    main()
