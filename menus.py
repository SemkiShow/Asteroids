from input import is_key_pressed
from player import Player
from utils import *
from widgets import *
import time


class GameMenu(Window):
    def __init__(self):
        super().__init__()
        self.visible = True

        self.map_size: Vec2 = Vec2(80, 80 * camera.character_ratio)
        self.player: Player = Player()
        self.x: float = 0

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

        self.connect(
            lambda: is_key_pressed("w"), lambda: notification_menu.show("Notification\nSecond line")
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

        camera.draw_text(Vec2(self.x, self.x * camera.character_ratio), "t", Colors.BLUE)

        self.player.draw()

        return super().draw()


class NotificationMenu(Window):
    def __init__(self):
        super().__init__()

        self.open_time: float = 2
        self.timer: float = time.time()

        layout = VBoxLayout()
        self.set_widget(layout)

        self.message_label = Label("")
        layout.add_widget(self.message_label)

        def move_layout():
            layout.bounds.x = camera.get_terminal_size().x - self.message_label.bounds.width

        self.connect(lambda: True, move_layout)

    def show(self, message: str, open_time: float = 2):
        self.message_label.set_text(message)
        self.open_time = open_time
        self.timer = time.time()
        self.visible = True

    def update(self):
        if time.time() - self.timer >= self.open_time:
            self.visible = False
        return super().update()


game_menu = GameMenu()
notification_menu = NotificationMenu()
