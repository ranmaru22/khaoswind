"""Some general functions for the game."""

import sys
import time


def print_speak(text):
    """Print a text character by character, simulating speaking/typing."""
    for c in (text + '\n'):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(3/50)
