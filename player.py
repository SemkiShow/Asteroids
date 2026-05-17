from camera import camera, Colors
from utils import *
import math


class Player:
    def __init__(self):
        self.pos: Vec2 = Vec2(0, 0)
        self.speed: float = 0
        self.angle: float = 90
        self.friction: float = 0.3
        self.directions: str = "↑↗→↘↓↙←↖"

    def translate(self, x: float, y: float):
        self.pos.x += x
        self.pos.y += y

    def update(self):
        self.translate(
            math.sin(self.angle * math.pi / 180) * self.speed,
            -math.cos(self.angle * math.pi / 180) * self.speed * camera.ratio,
        )

        self.speed -= self.friction * camera.get_delta_time()
        self.speed = max(0, self.speed)

        # Set camera position so the player is in the center of the screen
        terminal_size = camera.get_terminal_size()
        camera.pos.x = math.floor(self.pos.x) - terminal_size.x // 2
        camera.pos.y = math.floor(self.pos.y) - terminal_size.y // 2

    def get_draw_pos(self):
        return Vec2(math.floor(self.pos.x), math.floor(self.pos.y))

    def draw(self):
        angle = mod(self.angle, 360)
        char = self.directions[round(angle / 360 * len(self.directions)) % len(self.directions)]
        camera.draw_text(self.get_draw_pos(), char, Colors.MAGENTA)
