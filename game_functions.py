"""Some general functions for the game."""

import sys
import time


def print_speak(text):
    """Print a text character by character, simulating speaking/typing."""
    for c in (text + '\n'):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.025)


# @debug
def draw_map(current_loc, loc_map):
    """Draws a map based on a list of RG locations."""
    coordinates = [(loc.x, loc.y) for loc in loc_map]
    print(coordinates, end='')
    for y in range(5, -5, -1):
        print()
        for x in range(-9, 9):
            if (x, y) == (current_loc.x, current_loc.y):
                print('X', end='')
            elif (x, y) in coordinates:
                print('#', end='')
            else:
                print('.', end='')
    print()
