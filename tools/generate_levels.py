import random

NUM_LEVELS = 10
MIN_FILL = 0.1
MAX_FILL = 1.25
WIDTH = 200
HEIGHT = 200

for i in range(NUM_LEVELS):
    fill = i / NUM_LEVELS * (MAX_FILL - MIN_FILL) + MIN_FILL

    with open(f"resources/levels/{i + 1}.ppm", "w") as file:
        file.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")
        for j in range(WIDTH * HEIGHT):
            if random.randint(0, 1000) / 10 <= fill:
                file.write("0 0 0\n")
            else:
                file.write("255 255 255\n")
