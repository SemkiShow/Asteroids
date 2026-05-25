"""The program entry point"""

from camera import camera
from input import *
from menus import *
from tui import *
import time


if __name__ == "__main__":
    timer = time.time()

    app: Application = Application()
    app.add_window(main_menu)
    app.add_window(settings_menu)
    app.add_window(game_menu)
    app.add_window(pause_menu)
    app.add_window(game_over_menu)
    app.add_window(victory_menu)
    app.add_window(notification_menu)
    main_menu.set_visible(True)

    try:
        prepare_terminal()
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
    except ExitSuccess:
        # Clear the terminal on successful exit
        print("\x1b[0m\x1b[J", end="")
    finally:
        restore_terminal()
        settings_menu.save()
