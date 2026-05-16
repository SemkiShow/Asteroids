from player import Player
from input import is_key_pressed
from utils import *
from widgets import *


class GameMenu(Window):
    map_size: Vec2 = Vec2(80, 80 * camera.character_ratio)
    player: Player = Player()
    x: float = 0

    def __init__(self):
        super().__init__()
        self.visible = True

        layout = VBoxLayout()
        layout.set_padding(0)
        self.set_widget(layout)

        position_label = Label("")
        position_label.color = Colors.YELLOW
        layout.add_widget(position_label)

        self.connect(
            lambda: True,
            lambda: position_label.set_text(
                "Position: "
                + str(round(self.player.position.x, 1))
                + " "
                + str(round(self.player.position.y, 1))
            ),
        )

        speed_label = Label("")
        speed_label.color = Colors.YELLOW
        layout.add_widget(speed_label)

        self.connect(
            lambda: True,
            lambda: speed_label.set_text("Speed: " + str(round(self.player.speed, 1))),
        )

    def update(self):
        if is_key_pressed("a") or is_key_pressed("LEFT"):
            self.player.angle -= 45
        if is_key_pressed("d") or is_key_pressed("RIGHT"):
            self.player.angle += 45
        if is_key_pressed(" "):
            self.player.speed += 0.5

        self.player.update()

        self.x += 1
        self.x %= self.map_size.x // 2

        return super().update()

    def draw(self):
        # Draw world border
        terminal_size = camera.get_terminal_size()
        camera.draw_rec(Rec(0, 0, terminal_size.x, terminal_size.y), Colors.BG_RED, world_pos=False)
        camera.draw_rec(
            Rec(-self.map_size.x / 2, -self.map_size.y / 2, self.map_size.x, self.map_size.y),
            Colors.RESET,
        )

        camera.draw_char(Vec2(self.x, self.x * camera.character_ratio), "t", Colors.BLUE)

        self.player.draw()

        return super().draw()
