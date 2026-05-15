from camera import camera
import time
import os

if __name__ == "__main__":
    # Enable ANSI codes on PowerShell and CMD
    os.system("")

    x = 0
    while True:
        camera.clear()
        camera.draw_char(x, x, "\x1b[31mt\x1b[0m")
        camera.flush()

        x += 1
        x %= len(camera.buf)
        time.sleep(0.1)
