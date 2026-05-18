from input import is_key_pressed
from map import Map
from player import Player
from utils import *
from widgets import *
import time


class GameMenu(Window):
    def __init__(self):
        super().__init__()

        self.player: Player = Player()
        self.map: Map = Map()

        self.load_map("resources/levels/gimp.ppm")

        layout = VBoxLayout()
        layout.set_padding(0)
        self.set_widget(layout)

        self.position_label = Label("")
        self.position_label.color = Colors.YELLOW
        layout.add_widget(self.position_label)

        self.speed_label = Label("")
        self.speed_label.color = Colors.YELLOW
        layout.add_widget(self.speed_label)

    def load_map(self, file_name: str):
        self.map.load(file_name)
        self.player.pos = self.map.player_pos

    def game_over(self):
        self.player.speed = 0
        notification_menu.show("Game Over!")
        # end_game_menu.visible = True

    def update(self):
        super().update()

        self.position_label.set_text(
            "Position: " + str(round(self.player.pos.x, 1)) + " " + str(round(self.player.pos.y, 1))
        )
        self.speed_label.set_text("Speed: " + str(round(self.player.speed, 1)))

        # Don't run game update if the game is over
        if end_game_menu.visible:
            return

        if is_key_pressed("a") or is_key_pressed("LEFT"):
            self.player.angle -= 45
        if is_key_pressed("d") or is_key_pressed("RIGHT"):
            self.player.angle += 45
        if is_key_pressed(" "):
            self.player.speed += 0.5

        self.player.update()

        player_pos = self.player.get_draw_pos()
        if (
            player_pos.x < 0
            or player_pos.x >= self.map.size.x
            or player_pos.y < 0
            or player_pos.y >= self.map.size.y
        ):
            self.game_over()
            return

        player_pos = camera.get_draw_pos(self.player.get_draw_pos())
        for asteroid in self.map.asteroids:
            asteroid_pos = camera.get_draw_pos(asteroid.pos)
            if asteroid_pos == player_pos:
                self.game_over()
                return

    def draw(self):
        self.map.draw()
        self.player.draw()

        return super().draw()


class EndGameMenu(Window):
    def __init__(self):
        super().__init__()

        layout = VBoxLayout()
        self.set_widget(layout)

        layout.add_widget(Label("Game Over!"))


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
        new_message = self.message_label.get_text()
        if len(new_message) > 0:
            new_message += "\n"
        new_message += message
        self.message_label.set_text(new_message)
        self.open_time = open_time
        self.timer = time.time()
        self.visible = True

    def update(self):
        if time.time() - self.timer >= self.open_time:
            self.message_label.set_text("")
            self.visible = False
        return super().update()


game_menu = GameMenu()
end_game_menu = EndGameMenu()
notification_menu = NotificationMenu()
