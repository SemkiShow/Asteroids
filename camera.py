import os
from typing import List


# https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
class Colors:
    RESET: str = "\x1b[0m"

    RED: str = "\x1b[31m"
    GREEN: str = "\x1b[32m"
    YELLOW: str = "\x1b[33m"
    BLUE: str = "\x1b[34m"
    MAGENTA: str = "\x1b[35m"
    CYAN: str = "\x1b[36m"
    WHITE: str = "\x1b[37m"
    DEFAULT: str = "\x1b[39m"

    BG_RED: str = "\x1b[41m"
    BG_GREEN: str = "\x1b[42m"
    BG_YELLOW: str = "\x1b[43m"
    BG_BLUE: str = "\x1b[44m"
    BG_MAGENTA: str = "\x1b[45m"
    BG_CYAN: str = "\x1b[46m"
    BG_WHITE: str = "\x1b[47m"
    BG_DEFAULT: str = "\x1b[49m"


class Camera:
    position: tuple[int, ...] = (0, 0)
    buf: List[List[str]] = []
    last_terminal_size: tuple[int, ...] = (0, 0)

    def __init__(self):
        self.last_terminal_size = self.get_terminal_size()
        self.clear()

    def get_terminal_size(self):
        return os.get_terminal_size()

    def clear(self):
        terminal_size = self.get_terminal_size()

        # Clear the terminal only if the size has changed
        # flush() returns cursor to home, so clear isn't necessary if the terminal size stays the same
        if self.last_terminal_size != terminal_size:
            print("\033[H\033[J", end="")

        # Reset the internal buffer
        self.buf = [
            [" " for x in range(terminal_size.columns)] for y in range(terminal_size.lines - 1)
        ]

        self.last_terminal_size = terminal_size

    def draw_char(
        self, pos: tuple[int, ...], val: str, color: str = Colors.RESET, world_pos: bool = True
    ):
        # Calculate the offset positions
        if world_pos:
            nx = round(pos[0] - self.position[0])
            ny = round(pos[1] - self.position[1])
        else:
            nx = round(pos[0])
            ny = round(pos[1])

        # Ignore pixels that are out of screen
        if ny < 0 or ny >= len(self.buf) or nx < 0 or nx >= len(self.buf[ny]):
            return

        if color != Colors.RESET:
            self.buf[ny][nx] = color + val + Colors.RESET
        else:
            self.buf[ny][nx] = val

    def draw_text(
        self, pos: tuple[int, ...], text: str, color: str = Colors.RESET, world_pos: bool = True
    ):
        # Calculate the offset positions
        if world_pos:
            nx = round(pos[0] - self.position[0])
            ny = round(pos[1] - self.position[1])
        else:
            nx = round(pos[0])
            ny = round(pos[1])

        for char in text:
            # Ignore pixels that are out of screen
            if ny < 0 or ny >= len(self.buf) or nx < 0 or nx >= len(self.buf[ny]):
                nx += 1
                continue

            if color != Colors.RESET:
                self.buf[ny][nx] = color + char + Colors.RESET
            else:
                self.buf[ny][nx] = char

            nx += 1

    def draw_rec(
        self,
        pos: tuple[int, ...],
        width: int,
        height: int,
        color: str = Colors.BG_WHITE,
        world_pos: bool = True,
    ):
        # Calculate the offset positions
        if world_pos:
            nx = round(pos[0] - self.position[0])
            ny = round(pos[1] - self.position[1])
        else:
            nx = round(pos[0])
            ny = round(pos[1])

        for dy in range(height):
            for dx in range(width):
                x = nx + dx
                y = ny + dy

                # Ignore pixels that are out of screen
                if y < 0 or y >= len(self.buf) or x < 0 or x >= len(self.buf[y]):
                    continue

                if color != Colors.RESET:
                    self.buf[y][x] = color + " " + Colors.RESET
                else:
                    self.buf[y][x] = " "

    def flush(self):
        print("\x1b[H" + "\n".join("".join(row) for row in self.buf))


camera = Camera()
