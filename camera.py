import os


class Colors:
    RESET: str = "\x1b[0m"
    RED: str = "\x1b[31m"
    GREEN: str = "\x1b[32m"
    YELLOW: str = "\x1b[33m"
    BLUE: str = "\x1b[34m"
    MAGENTA: str = "\x1b[35m"


class Camera:
    position = (0, 0)
    buf = []
    last_terminal_size = (0, 0)

    def __init__(self):
        self.clear()

    def get_terminal_size(self):
        return os.get_terminal_size()

    def clear(self):
        terminal_size = self.get_terminal_size()

        # Use fast terminal clear if the size hasn't changed
        if self.last_terminal_size == terminal_size:
            print(f"\033[{terminal_size.lines}A\033[{terminal_size.columns}D")
        else:
            print("\033[H\033[J", end="")

        # Reset the internal buffer
        self.buf = [
            [" " for x in range(terminal_size.columns)] for y in range(terminal_size.lines - 1)
        ]

    def draw_char(self, x: int, y: int, val: str, color: str = Colors.RESET):
        # Calculate the offset positions
        nx = x + self.position[0]
        ny = y + self.position[1]
        terminal_size = self.get_terminal_size()

        # Ignore pixels that are out of screen
        if ny < 0 or ny >= len(self.buf) or nx < 0 or nx >= len(self.buf[ny]):
            return

        self.buf[ny][nx] = color + val + Colors.RESET

    def flush(self):
        for row in self.buf:
            for cell in row:
                print(cell, end="")
            print()


camera = Camera()
