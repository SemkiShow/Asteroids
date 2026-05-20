from utils import *
import os


# https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
class Colors:
    RESET: str = "\x1b[0m"

    BLACK: str = "\x1b[30m"
    RED: str = "\x1b[31m"
    GREEN: str = "\x1b[32m"
    YELLOW: str = "\x1b[33m"
    BLUE: str = "\x1b[34m"
    MAGENTA: str = "\x1b[35m"
    CYAN: str = "\x1b[36m"
    WHITE: str = "\x1b[37m"
    DEFAULT: str = "\x1b[39m"

    BG_BLACK: str = "\x1b[40m"
    BG_RED: str = "\x1b[41m"
    BG_GREEN: str = "\x1b[42m"
    BG_YELLOW: str = "\x1b[43m"
    BG_BLUE: str = "\x1b[44m"
    BG_MAGENTA: str = "\x1b[45m"
    BG_CYAN: str = "\x1b[46m"
    BG_WHITE: str = "\x1b[47m"
    BG_DEFAULT: str = "\x1b[49m"


class Camera:
    def __init__(self):
        self.pos: IntVec2 = IntVec2(0, 0)
        self.buf: list[list[str]] = []
        self.ratio: float = 13 / 29
        self.tick_time: float = 0.01

        self.clear()

    def get_terminal_size(self):
        terminal_size = os.get_terminal_size()
        return IntVec2(terminal_size.columns, terminal_size.lines)

    def clear(self):
        print("\x1b[H", end="")
        terminal_size = self.get_terminal_size()
        self.buf = [[" " for _ in range(terminal_size.x)] for _ in range(terminal_size.y)]

    def hide_cursor(self):
        print("\x1b[?25l")

    def show_cursor(self):
        print("\x1b[?25h")

    def get_delta_time(self):
        return self.tick_time

    def get_draw_pos(self, pos: Vec2, world_pos: bool = True):
        if world_pos:
            return IntVec2(
                round(pos.x - self.pos.x),
                round(pos.y - self.pos.y),
            )
        else:
            return IntVec2(
                round(pos.x),
                round(pos.y),
            )

    def draw_text(self, pos: Vec2, text: str, color: str = Colors.RESET, world_pos: bool = True):
        draw_pos = self.get_draw_pos(pos, world_pos)
        nx, ny = draw_pos.x, draw_pos.y

        start_x = nx
        for char in text:
            if char == '\n':
                nx = start_x
                ny += 1
                continue

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
        draw_pos = self.get_draw_pos(rec.get_pos(), world_pos)
        nx, ny = draw_pos.x, draw_pos.y

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
        print("\n".join("".join(row) for row in self.buf), end="")


camera = Camera()
