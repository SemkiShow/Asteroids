from utils import *
import random

NUM_LEVELS = 10
MIN_FILL = 0.1
MAX_FILL = 1.25
BONUSES_K = 0.25
WIDTH = 200
HEIGHT = 200
MIN_DISTANCE = min(WIDTH / 1.5, HEIGHT / 1.5)


def random_pos():
    return IntVec2(random.randint(0, WIDTH), random.randint(0, HEIGHT))


for i in range(NUM_LEVELS):
    asteroids_fill = i / NUM_LEVELS * (MAX_FILL - MIN_FILL) + MIN_FILL
    bonuses_fill = asteroids_fill * BONUSES_K

    level: dict[int, str] = {}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            level[y * WIDTH + x] = " "

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if random.randint(0, 1000) / 10 <= asteroids_fill:
                level[y * WIDTH + x] = "#"

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if random.randint(0, 1000) / 10 <= bonuses_fill:
                pos: int = y * WIDTH + x
                if level[pos] == " ":
                    level[pos] = "+"

    player_pos = random_pos()
    player_pos_int = player_pos.y * WIDTH + player_pos.x
    while level[player_pos_int] != " ":
        player_pos = random_pos()
    level[player_pos_int] = ">"

    end_pos = random_pos()
    end_pos_int = end_pos.y * WIDTH + end_pos.x
    while level[end_pos_int] != " " or end_pos.distance(player_pos) < MIN_DISTANCE:
        end_pos = random_pos()
    level[end_pos_int] = "X"

    with open(f"resources/levels/{i + 1}.ppm", "w") as file:
        file.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pixel = level[y * WIDTH + x]
                if pixel == "#":
                    file.write("0 0 0\n")
                elif pixel == ">":
                    file.write("255 0 0\n")
                elif pixel == "+":
                    file.write("0 255 0\n")
                elif pixel == "X":
                    file.write("0 0 255\n")
                else:
                    file.write("255 255 255\n")
