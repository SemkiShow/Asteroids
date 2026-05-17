from camera import camera, Colors
from utils import *


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
        self.pos = pos


class Map:
    def __init__(self) -> None:
        self.asteroids: list[Asteroid] = []
        self.size: Vec2 = Vec2(0, 0)

    def load(self, file_name: str):
        image: Image = Image()
        image.load_ppm(file_name)
        self.size = Vec2(image.width, image.height * camera.ratio)
        self.asteroids.clear()
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.pixels[y * image.width + x]
                r, g, b = pixel.x, pixel.y, pixel.z
                if r != 255 or g != 255 or b != 255:
                    self.asteroids.append(
                        Asteroid(Vec2(x - image.width / 2, (y - image.height / 2) * camera.ratio))
                    )

    def draw(self):
        # Draw world border
        terminal_size = camera.get_terminal_size()
        camera.draw_rec(Rec(0, 0, terminal_size.x, terminal_size.y), Colors.BG_RED, world_pos=False)
        camera.draw_rec(
            Rec(-self.size.x / 2, -self.size.y / 2, self.size.x, self.size.y),
            Colors.RESET,
        )

        for asteroid in self.asteroids:
            camera.draw_text(asteroid.pos, "#", Colors.RED)
