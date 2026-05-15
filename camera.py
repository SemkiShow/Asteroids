import os
from typing import List
import math


class Colors:
    RESET: str = "\x1b[0m"
    RED: str = "\x1b[31m"
    GREEN: str = "\x1b[32m"
    YELLOW: str = "\x1b[33m"
    BLUE: str = "\x1b[34m"
    MAGENTA: str = "\x1b[35m"


class Camera:
    position: tuple[int] = (0, 0)
    buf: List[List[int]] = []
    last_terminal_size: tuple[int] = (0, 0)

    def __init__(self):
        self.last_terminal_size = self.get_terminal_size()
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

        self.last_terminal_size = terminal_size

    def draw_char(
        self, pos: tuple(int), val: str, color: str = Colors.RESET, world_pos: bool = True
    ):
        # Calculate the offset positions
        if world_pos:
            nx = math.floor(pos[0] - self.position[0])
            ny = math.floor(pos[1] - self.position[1])
        else:
            nx = math.floor(pos[0])
            ny = math.floor(pos[1])

        # Ignore pixels that are out of screen
        if ny < 0 or ny >= len(self.buf) or nx < 0 or nx >= len(self.buf[ny]):
            return

        if color != Colors.RESET:
            self.buf[ny][nx] = color + val + Colors.RESET
        else:
            self.buf[ny][nx] = val

    def draw_text(
        self, pos: tuple(int), text: str, color: str = Colors.RESET, world_pos: bool = True
    ):
        # Calculate the offset positions
        if world_pos:
            nx = math.floor(pos[0] - self.position[0])
            ny = math.floor(pos[1] - self.position[1])
        else:
            nx = math.floor(pos[0])
            ny = math.floor(pos[1])

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

    def flush(self):
        for row in self.buf:
            for cell in row:
                print(cell, end="")
            print()


camera = Camera()
