from camera import camera, Colors
from utils import *
import math, random


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

    def update(self):
        self.translate(
            math.sin(self.angle * math.pi / 180) * self.speed,
            -math.cos(self.angle * math.pi / 180) * self.speed * camera.ratio,
        )

        self.speed -= self.friction * camera.get_delta_time()
        self.speed = max(0, self.speed)

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


class Bonus:
    def __init__(self, pos: Vec2):
        self.pos: Vec2 = pos


class Map:
    def __init__(self) -> None:
        self.seed = 0

        self.size: Vec2 = Vec2(0, 0)
        self.asteroids: list[Asteroid] = []
        self.player_pos: Vec2 = Vec2(0, 0)
        self.bonuses: list[Bonus] = []
        self.end_pos: Vec2 = Vec2(1, 1)

    def set_random_seed(self):
        self.seed = random.randint(0, 2**32)
        random.seed(self.seed)

    def reload_game(
        self,
        width: int = 200,
        height: int = 200,
        asteroids_fill: float = 0.1,
        bonuses_fill: float = 0.025,
        min_distance: float = 100,
    ):
        def random_pos():
            return IntVec2(random.randint(0, width), random.randint(0, height))

        def idx(x: int, y: int):
            return y * width + x

        random.seed(self.seed)

        self.size = Vec2(width, height * camera.ratio)

        level: dict[int, str] = {}
        for y in range(height):
            for x in range(width):
                level[idx(x, y)] = " "

        self.asteroids.clear()
        for y in range(height):
            for x in range(width):
                if random.randint(0, 1000) / 10 <= asteroids_fill:
                    pos: Vec2 = Vec2(x, y * camera.ratio)
                    self.asteroids.append(Asteroid(pos))
                    level[idx(x, y)] = "#"

        self.bonuses.clear()
        for y in range(height):
            for x in range(width):
                if random.randint(0, 1000) / 10 <= bonuses_fill:
                    if level[idx(x, y)] == " ":
                        pos: Vec2 = Vec2(x, y * camera.ratio)
                        self.bonuses.append(Bonus(pos))
                        level[idx(x, y)] = "+"

        player_pos = random_pos()
        player_pos_int = player_pos.y * width + player_pos.x
        while level[player_pos_int] != " ":
            player_pos = random_pos()
        self.player_pos = Vec2(player_pos.x, player_pos.y * camera.ratio)
        level[player_pos_int] = ">"

        end_pos = random_pos()
        end_pos_int = end_pos.y * width + end_pos.x
        while level[end_pos_int] != " " or end_pos.distance(player_pos) < min_distance:
            end_pos = random_pos()
        self.end_pos = Vec2(end_pos.x, end_pos.y * camera.ratio)
        level[end_pos_int] = "X"

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

        for bonus in self.bonuses:
            camera.draw_text(bonus.pos, "+", Colors.GREEN)

        camera.draw_text(self.end_pos, "X", Colors.BG_GREEN)
