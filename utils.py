"""Vector and rectangle types, helper functions"""

from typing import Self
import math


class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: Self):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class IntVec2:
    def __init__(self, x: float, y: float):
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other: object):
        if not isinstance(other, IntVec2):
            return NotImplemented
        return (self.x == other.x) and (self.y == other.y)

    def distance(self, other: Self):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Rec:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = round(width)
        self.height = round(height)

    def set_pos(self, val: Vec2):
        self.x = round(val.x)
        self.y = round(val.y)

    def get_pos(self):
        return Vec2(self.x, self.y)

    def set_size(self, val: Vec2):
        self.width = round(val.x)
        self.height = round(val.y)

    def get_size(self):
        return Vec2(self.width, self.height)


def mod(a: float, b: float):
    return ((a % b) + b) % b


def clamp(val: int, min_val: int, max_val: int) -> int:
    return min(max(val, min_val), max_val)


def measure_text(text: str):
    size = Vec2(0, 0)
    for line in text.split("\n"):
        size.x = max(size.x, len(line))
    size.y = text.count("\n") + 1
    return size
