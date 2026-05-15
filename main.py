from camera import *
from player import Player
from input import get_key, restore_terminal
import time, os


def loop():
    global x

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

    key = get_key()
    while key:
        # Make Ctrl+C terminate the program
        if key == "\x03":
            raise KeyboardInterrupt
        if key == "w" or key == "ESC" or key == "ENTER":
            camera.draw_char((2, 2), "D", Colors.MAGENTA, world_pos=False)

        key = get_key()

    camera.flush()

    x += 1
    x %= len(camera.buf) // 2

    time.sleep(0.1)


if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")

    player = Player()
    x = 0

    try:
        while True:
            loop()

    finally:
        restore_terminal()
