from camera import *
import math


class Player:
    position: tuple[float] = (0, 0)
    speed: float = 0.3
    angle: float = 123

    def __init__(self):
        pass

    def update(self):
        self.position = (
            self.position[0] + math.sin(self.angle * math.pi / 180) * self.speed,
            self.position[1] - math.cos(self.angle * math.pi / 180) * self.speed,
        )

        # Set camera position so the player is in the center of the screen
        terminal_size = camera.get_terminal_size()
        camera.position = (
            math.floor(self.position[0]) - terminal_size[0] // 2,
            math.floor(self.position[1]) - terminal_size[1] // 2,
        )

    def draw(self):
        camera.draw_char(self.position, "X", Colors.RED)
