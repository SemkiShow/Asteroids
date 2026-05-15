from camera import camera, Colors
from player import Player
from input import get_key, restore_terminal
import time, os, math


def loop():
    global x

    player.update()

    camera.clear()

    # Draw world border
    terminal_size = camera.get_terminal_size()
    camera.draw_rec(
        (0, 0), terminal_size.columns, terminal_size.lines, Colors.BG_RED, world_pos=False
    )
    camera.draw_rec((-map_size[0] // 2, -map_size[1] // 2), map_size[0], map_size[1], Colors.RESET)

    camera.draw_char((x, x), "t", Colors.BLUE)

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

        if key == "w" or key == "UP":
            camera.draw_char((1, 1), "W", Colors.MAGENTA, world_pos=False)
            player.translate(0, -1)
        if key == "a" or key == "LEFT":
            camera.draw_char((0, 2), "A", Colors.MAGENTA, world_pos=False)
            player.translate(-1, 0)
        if key == "s" or key == "DOWN":
            camera.draw_char((1, 2), "S", Colors.MAGENTA, world_pos=False)
            player.translate(0, 1)
        if key == "d" or key == "RIGHT":
            camera.draw_char((2, 2), "D", Colors.MAGENTA, world_pos=False)
            player.translate(1, 0)

        key = get_key()

    camera.flush()

    # x += 1
    x %= len(camera.buf) // 2

    time.sleep(0.1)


if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")

    player = Player()
    x = 0
    map_size: tuple[int, ...] = (80, 40)

    try:
        while True:
            loop()

    finally:
        restore_terminal()
