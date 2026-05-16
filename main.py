from camera import camera, Colors
from player import Player
from input import get_key, restore_terminal
from utils import *
import time, os, math


def loop():
    global x

    player.update()

    camera.clear()

    # Draw world border
    terminal_size = camera.get_terminal_size()
    camera.draw_rec(Rec(0, 0, terminal_size.x, terminal_size.y), Colors.BG_RED, world_pos=False)
    camera.draw_rec(Rec(-map_size.x / 2, -map_size.y / 2, map_size.x, map_size.y), Colors.RESET)

    camera.draw_char(Vec2(x, x * camera.character_ratio), "t", Colors.BLUE)

    pos_text = (
        "Position: " + str(math.floor(player.position.x)) + " " + str(math.floor(player.position.y))
    )
    camera.draw_text(
        Vec2(0, 0),
        pos_text,
        Colors.YELLOW,
        world_pos=False,
    )

    player.draw()

    for key in keys:
        # Make Ctrl+C terminate the program
        if key == "\x03":
            raise KeyboardInterrupt

        if key == "a" or key == "LEFT":
            player.angle -= 45
        if key == "d" or key == "RIGHT":
            player.angle += 45
        if key == " ":
            player.speed += 0.5

    keys.clear()

    camera.flush()

    x += 1
    x %= map_size.x // 2


if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")
    camera.hide_cursor()

    player = Player()
    x = 0
    map_size = Vec2(80, 40)
    keys: list[str] = []

    timer = time.time()

    try:
        while True:
            key = get_key()
            while key:
                keys.append(key)
                key = get_key()

            if time.time() - timer >= camera.tick_time:
                loop()
                timer = time.time()

    finally:
        restore_terminal()
        camera.show_cursor()
