"""Some general functions for the game."""

import sys
import time


def print_speak(text):
    """Print a text character by character, simulating speaking/typing."""
    for c in (text + '\n'):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.025)


def draw_map(loc_map):
    """Draws a map based on a list of RG locations."""
    coordinates = [(loc.x, loc.y) for loc in loc_map]
    x_coords = [x for x, y in coordinates]
    y_coords = [y for x, y in coordinates]
    x_max, y_max = max(x_coords), max(y_coords)
    x_min, y_min = min(x_coords), min(y_coords)
    abs_max = max(map(abs, (x_max, y_max, x_min, y_min)))
    abs_min = -abs_max

    print(coordinates)
    print(abs_max, abs_min)

    for y in range(abs_max, abs_min, -1):
        print()
        for x in range(abs_min, abs_max):
            if (x, y) == (0, 0):
                print('X', end='')
            elif (x, y) in coordinates:
                print('#', end='')
            else:
                print('.', end='')
    print()
