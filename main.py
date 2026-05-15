from camera import *
from player import Player
import time
import os

if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")

    x = 0
    player = Player()
    while True:
        player.update()

        camera.clear()

        camera.draw_char((x, x), "t", Colors.BLUE)
        camera.draw_char((3, 3), "W", Colors.GREEN, world_pos=False)

        pos_text = (
            "Position: "
            + str(math.floor(player.position[0]))
            + " "
            + str(math.floor(player.position[1]))
        )
        camera.draw_text(
            (0, 0),
            pos_text,
            Colors.YELLOW,
            world_pos=False,
        )

        player.draw()

        camera.flush()

        x += 1
        x %= len(camera.buf) // 2
        time.sleep(0.1)
