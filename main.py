from camera import camera, Colors
from player import Player
from input import is_key_pressed, poll_events, reset_events, restore_terminal
from utils import *
from widgets import *
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

    if is_key_pressed("a") or is_key_pressed("LEFT"):
        player.angle -= 45
    if is_key_pressed("d") or is_key_pressed("RIGHT"):
        player.angle += 45
    if is_key_pressed(" "):
        player.speed += 0.5

    camera.flush()

    x += 1
    x %= map_size.x // 2


if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")
    camera.hide_cursor()

    player: Player = Player()
    x: float = 0
    map_size: Vec2 = Vec2(80, 40)

    timer = time.time()

    app: Application = Application()

    window: Window = Window()
    layout = VBoxLayout()
    window.set_widget(layout)
    layout.add_widget(Label("a"))
    layout.add_widget(Label("b"))
    layout.add_widget(Label("c"))
    window.connect(lambda: is_key_pressed("w"), lambda: camera.draw_char(Vec2(1, 1), "D"))

    app.add_window(window)

    try:
        while True:
            poll_events()
            # Make Ctrl+C terminate the program
            if is_key_pressed("\x03"):
                raise KeyboardInterrupt

            if time.time() - timer >= camera.tick_time:
                camera.clear()
                app.update()
                app.draw()
                camera.flush()

                reset_events()
                timer = time.time()

    finally:
        restore_terminal()
        camera.show_cursor()
