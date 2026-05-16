from utils import *
import os


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
    position = IntVec2(0, 0)
    buf: list[list[str]] = []
    last_terminal_size = IntVec2(0, 0)
    character_ratio: float = 13 / 29

    def __init__(self):
        self.last_terminal_size = self.get_terminal_size()
        self.clear()

    def get_terminal_size(self):
        terminal_size = os.get_terminal_size()
        return IntVec2(terminal_size.columns, terminal_size.lines)

    def clear(self):
        terminal_size = self.get_terminal_size()

        # Clear the terminal only if the size has changed
        # flush() returns cursor to home, so clear isn't necessary if the terminal size stays the same
        if self.last_terminal_size != terminal_size:
            print("\x1b[H\x1b[J", end="")

        # Reset the internal buffer
        self.buf = [[" " for x in range(terminal_size.x)] for y in range(terminal_size.y)]

        self.last_terminal_size = terminal_size

    def hide_cursor(self):
        print("\x1b[?25l")

    def show_cursor(self):
        print("\x1b[?25h")

    def draw_char(self, pos: Vec2, val: str, color: str = Colors.RESET, world_pos: bool = True):
        # Calculate the offset positions
        if world_pos:
            nx = round(pos.x - self.position.x)
            ny = round(pos.y - self.position.y)
        else:
            nx = round(pos.x)
            ny = round(pos.y)

        # Ignore pixels that are out of screen
        if ny < 0 or ny >= len(self.buf) or nx < 0 or nx >= len(self.buf[ny]):
            return

        if color != Colors.RESET:
            self.buf[ny][nx] = color + val + Colors.RESET
        else:
            self.buf[ny][nx] = val

    def draw_text(self, pos: Vec2, text: str, color: str = Colors.RESET, world_pos: bool = True):
        # Calculate the offset positions
        if world_pos:
            nx = round(pos.x - self.position.x)
            ny = round(pos.y - self.position.y)
        else:
            nx = round(pos.x)
            ny = round(pos.y)

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
        rec: Rec,
        color: str = Colors.BG_WHITE,
        world_pos: bool = True,
    ):
        # Calculate the offset positions
        if world_pos:
            nx = round(rec.x - self.position.x)
            ny = round(rec.y - self.position.y)
        else:
            nx = round(rec.x)
            ny = round(rec.y)

        for dy in range(rec.height):
            for dx in range(rec.width):
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
        print("\x1b[H" + "\n".join("".join(row) for row in self.buf), end="")


camera = Camera()
