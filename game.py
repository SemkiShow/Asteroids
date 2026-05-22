from camera import camera, Colors
from utils import *
import math, random
from enum import Enum


class Player:
    def __init__(self):
        self.pos: Vec2 = Vec2(0, 0)
        self.speed: float = 0
        self.angle: float = 0
        self.friction: float = 0.3
        self.directions: str = "↑↗→↘↓↙←↖"

    def translate(self, x: float, y: float):
        self.pos.x += x
        self.pos.y += y

    def restart_game(self):
        self.pos = Vec2(0, 0)
        self.speed = 0
        self.angle = 0
        self.fuel: float = 1000

    def update(self):
        self.translate(
            math.sin(self.angle * math.pi / 180) * self.speed,
            -math.cos(self.angle * math.pi / 180) * self.speed * camera.ratio,
        )

        self.speed -= self.friction * camera.get_delta_time()
        self.speed = max(0, self.speed)

        self.fuel -= self.speed
        self.fuel = max(0, self.fuel)

        # Set camera position so the player is in the center of the screen
        terminal_size = camera.get_terminal_size()
        camera.pos.x = math.floor(self.pos.x) - terminal_size.x // 2
        camera.pos.y = math.floor(self.pos.y) - terminal_size.y // 2

    def get_draw_pos(self):
        return Vec2(math.floor(self.pos.x), math.floor(self.pos.y))

    def draw(self):
        angle = mod(self.angle, 360)
        char = self.directions[round(angle / 360 * len(self.directions)) % len(self.directions)]
        camera.draw_text(self.get_draw_pos(), char, Colors.MAGENTA)


class Asteroid:
    def __init__(self, pos: Vec2):
        self.pos: Vec2 = pos


class FieldType(Enum):
    AddPoints = 0
    Time = 1
    Fuel = 2
    Speed = 3
    RemovePoints = 4


class Field:
    def __init__(self, pos: Vec2, field_type: FieldType):
        self.pos: Vec2 = pos
        self.type = field_type


class Map:
    def __init__(self) -> None:
        self.seed = 0

        self.size: Vec2 = Vec2(0, 0)
        self.asteroids: list[Asteroid] = []
        self.player_pos: Vec2 = Vec2(0, 0)
        self.fields: list[Field] = []
        self.end_pos: Vec2 = Vec2(1, 1)

    def set_random_seed(self):
        self.seed = random.randint(0, 2**32)
        random.seed(self.seed)

    def restart_game(
        self,
        width: int = 200,
        height: int = 200,
        asteroids_fill: float = 0.1,
        fields_fill: float = 0.025,
        min_distance: float = 100,
    ):
        def random_pos():
            return Vec2(random.randint(0, width - 1), random.randint(0, height - 1))

        random.seed(self.seed)

        height = math.floor(height * camera.ratio)
        self.size = Vec2(width, height)

        level: list[list[bool]] = [[False for _ in range(width)] for _ in range(height)]

        self.asteroids.clear()
        for y in range(height):
            for x in range(width):
                if random.randint(0, 1000) / 10 <= asteroids_fill and not level[y][x]:
                    pos: Vec2 = Vec2(x, y)
                    self.asteroids.append(Asteroid(pos))
                    level[y][x] = True

        self.fields.clear()
        for y in range(height):
            for x in range(width):
                if random.randint(0, 1000) / 10 <= fields_fill and not level[y][x]:
                    pos: Vec2 = Vec2(x, y)
                    self.fields.append(Field(pos, random.choice(list(FieldType))))
                    level[y][x] = True

        player = Player()
        player.pos = random_pos()
        player_pos = player.get_draw_pos()
        while level[int(player_pos.y)][int(player_pos.x)]:
            player.pos = random_pos()
            player_pos = player.get_draw_pos()
        self.player_pos = Vec2(player.pos.x, player.pos.y)
        level[int(player_pos.y)][int(player_pos.x)] = True

        end_pos = random_pos()
        while level[int(end_pos.y)][int(end_pos.x)] or end_pos.distance(player_pos) < min_distance:
            end_pos = random_pos()
        self.end_pos = Vec2(end_pos.x, end_pos.y)
        level[int(end_pos.y)][int(end_pos.x)] = True

    def draw(self):
        # Draw world border
        terminal_size = camera.get_terminal_size()
        camera.draw_rec(Rec(0, 0, terminal_size.x, terminal_size.y), Colors.BG_RED, world_pos=False)
        camera.draw_rec(
            Rec(0, 0, self.size.x, self.size.y),
            Colors.RESET,
        )

        for asteroid in self.asteroids:
            camera.draw_text(asteroid.pos, "#", Colors.RED)

        for field in self.fields:
            camera.draw_text(field.pos, "?", Colors.BLUE)

        camera.draw_text(self.end_pos, "X", Colors.BG_GREEN)
