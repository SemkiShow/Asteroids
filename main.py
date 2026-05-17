from camera import camera
from input import is_key_pressed, poll_events, reset_events, restore_terminal
from menus import *
from widgets import *
import time, os


if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")

    timer = time.time()

    app: Application = Application()
    app.add_window(game_menu)
    app.add_window(notification_menu)
    game_menu.visible = True

    try:
        camera.hide_cursor()
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
