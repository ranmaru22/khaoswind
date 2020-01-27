"""Some general classes and functions for the game."""

import sys
import time
import random

from items import ContainedItem


class GameData(object):
    def __init__(self, inventory, stack):
        self.inventory = inventory
        self.stack = stack

    def set_loc_list(self, locations):
        self.locations = locations

    def set_item_list(self, items):
        self.items = items

    def set_npc_list(self, npcs):
        self.npcs = npcs

    def set_current_loc(self, location):
        self.current_loc = location

    def get_random_location(self):
        return random.choice(self.locations)

    def get_loc_names(self):
        return [x.name for x in self.locations]

    def get_item_names(self):
        return [x.name for x in self.items]

    def get_npc_names(self):
        return [x.name for x in self.npcs]

    def get_loc_from_name(self, name):
        loc_list = self.get_loc_names()
        return self.locations[loc_list.index(name)] if name in loc_list else None

    def get_item_from_name(self, name):
        item_list = self.get_item_names()
        return self.items[item_list.index(name)] if name in item_list else None

    def get_npc_from_name(self, name):
        npc_list = self.get_npc_names()
        return self.npcs[npc_list.index(name)] if name in npc_list else None

    def get_items_in_location(self, location):
        return [i for i in self.items if i.location == location]

    def get_npcs_in_location(self, location):
        return [n for n in self.npcs if n.location == location]

    def create_map(self):
        x, y = 0, 0
        for loc in self.locations:
            coordinates = [(loc.x, loc.y) for loc in self.locations]
            loc_set = False
            while not loc_set:
                link = random.choice('n')
                if link == 'n' and (x, y+1) not in coordinates:
                    loc.set_coords(x, y+1)
                elif link == 'e' and (x+1, y) not in coordinates:
                    loc.set_coords(x+1, y)
                elif link == 's' and (x, y-1) not in coordinates:
                    loc.set_coords(x, y-1)
                elif link == 'w' and (x-1, y) not in coordinates:
                    loc.set_coords(x-1, y)
                else:
                    continue
                x, y = loc.get_coords()
                loc_set = True

    def distribute_items(self):
        self.add_to_random_location(self.items)

    def distribute_npcs(self):
        self.add_to_random_location(self.npcs)

    def add_to_random_location(self, obj_list):
        for obj in obj_list:
            if isinstance(obj, ContainedItem):
                continue
            obj.location = self.get_random_location()

    def is_in_current_location(self, obj):
        return obj.location == self.current_loc

    def is_in_inventory(self, obj):
        return obj.location == self.inventory

    # @debug
    def draw_map(self):
        coordinates = [(loc.x, loc.y) for loc in self.locations]
        print((self.current_loc.x, self.current_loc.y), end='')
        for y in range(5, -5, -1):
            print()
            for x in range(-9, 9):
                if (x, y) == (self.current_loc.x, self.current_loc.y):
                    print('X', end='')
                elif (x, y) in coordinates:
                    print('#', end='')
                else:
                    print('.', end='')
        print()


def print_speak(text):
    """Print a text character by character, simulating speaking/typing."""
    for c in (text + '\n'):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.025)
