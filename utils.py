class Vec2:
    x: float = 0
    y: float = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class IntVec2:
    x: int = 0
    y: int = 0

    def __init__(self, x: float, y: float):
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


class Rec:
    x: float = 0
    y: float = 0
    width: int = 0
    height: int = 0

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = round(width)
        self.height = round(height)
