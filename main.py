from camera import camera
from input import is_key_pressed, poll_events, prepare_terminal, reset_events, restore_terminal
from menus import *
from tui import *
import time


if __name__ == "__main__":
    timer = time.time()

    app: Application = Application()
    app.add_window(game_menu)
    app.add_window(game_over_menu)
    app.add_window(victory_menu)
    app.add_window(notification_menu)
    game_menu.visible = True

    try:
        prepare_terminal()
        while True:
            poll_events()
            # Make Ctrl+C terminate the program
            if is_key_pressed("\x03"):
                raise KeyboardInterrupt

            if time.time() - timer >= camera.tick_time:
                camera.clear()
                app.frame()
                camera.flush()

                reset_events()
                timer = time.time()

    finally:
        restore_terminal()
