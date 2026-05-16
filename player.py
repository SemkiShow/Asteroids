from camera import camera, Colors
from utils import *
import math


class Player:
    position = Vec2(0, 0)
    speed: float = 0
    angle: float = 123

    def translate(self, x: float, y: float):
        self.position.x += x
        self.position.y += y

    def update(self):
        self.translate(
            math.sin(self.angle * math.pi / 180) * self.speed,
            -math.cos(self.angle * math.pi / 180) * self.speed,
        )

        # Set camera position so the player is in the center of the screen
        terminal_size = camera.get_terminal_size()
        camera.position.x = math.floor(self.position.x) - terminal_size.x // 2
        camera.position.y = math.floor(self.position.y) - terminal_size.y // 2

    def draw(self):
        camera.draw_char(self.position, "X", Colors.RED)
