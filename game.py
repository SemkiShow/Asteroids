from camera import camera, Colors
from utils import *
import math


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


class Image:
    def __init__(self) -> None:
        self.pixels: list[IntVec3] = []
        self.width = 0
        self.height = 0

    def load_ppm(self, file_name: str):
        file = open(file_name, "r")
        if not file:
            print(f"Error: failed to open {file_name}")
            return

        magic_number = None
        size = None
        depth = None

        self.pixels.clear()
        self.width = 0
        self.height = 0

        # Read data before the pixels
        line = file.readline()
        while line:
            if line.strip()[0] == "#":
                line = file.readline()
                continue

            if not magic_number:
                magic_number = line
                if magic_number != "P3\n":
                    print("Error: invalid file given")
                    return
            elif not size:
                size = line.split(" ")
                self.width, self.height = int(size[0]), int(size[1])
            elif not depth:
                depth = int(line)
                if depth != 255:
                    print("Error: invalid color depth in file")
                    return
            else:
                break
            line = file.readline()

        # Read the rest of the file
        values = (line + "\n" + file.read()).split()
        for i in range(0, len(values), 3):
            self.pixels.append(IntVec3(int(values[i + 0]), int(values[i + 1]), int(values[i + 2])))

        file.close()


class Asteroid:
    def __init__(self, pos: Vec2):
        self.pos: Vec2 = pos


class Bonus:
    def __init__(self, pos: Vec2):
        self.pos: Vec2 = pos


class Map:
    def __init__(self) -> None:
        self.size: Vec2 = Vec2(0, 0)
        self.asteroids: list[Asteroid] = []
        self.player_pos: Vec2 = Vec2(0, 0)
        self.bonuses: list[Bonus] = []
        self.end_pos: Vec2 = Vec2(1, 1)

    def load(self, file_name: str):
        image: Image = Image()
        image.load_ppm(file_name)
        self.size = Vec2(image.width, image.height * camera.ratio)
        self.asteroids.clear()
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.pixels[y * image.width + x]
                pos: Vec2 = Vec2(x, y * camera.ratio)
                if pixel == IntVec3(0, 0, 0):
                    self.asteroids.append(Asteroid(pos))
                elif pixel == IntVec3(255, 0, 0):
                    self.player_pos = pos
                elif pixel == IntVec3(0, 255, 0):
                    self.bonuses.append(Bonus(pos))
                elif pixel == IntVec3(0, 0, 255):
                    self.end_pos = pos

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
