from camera import camera, Colors
from utils import *
import math


class Player:
    position: Vec2 = Vec2(0, 0)
    speed: float = 0
    angle: float = 123
    friction: float = 0.1
    directions: str = "↑↗→↘↓↙←↖"

    def translate(self, x: float, y: float):
        self.position.x += x
        self.position.y += y

    def update(self):
        self.translate(
            math.sin(self.angle * math.pi / 180) * self.speed,
            -math.cos(self.angle * math.pi / 180) * self.speed * camera.character_ratio,
        )

        self.speed -= self.friction * camera.get_delta_time()
        self.speed = max(0, self.speed)

        # Set camera position so the player is in the center of the screen
        terminal_size = camera.get_terminal_size()
        camera.position.x = math.floor(self.position.x) - terminal_size.x // 2
        camera.position.y = math.floor(self.position.y) - terminal_size.y // 2

    def draw(self):
        draw_pos = Vec2(math.floor(self.position.x), math.floor(self.position.y))
        angle = mod(self.angle, 360)
        char = self.directions[math.floor(angle / 360 * len(self.directions))]
        camera.draw_char(draw_pos, char, Colors.RED)
