"""The locations of the game."""

import json
import math
import random

from items import Blocker
from stack import Color

# Load the location descriptions.
with open("internals/loc_descriptions.json") as f_obj:
    loc_descriptions = json.load(f_obj)


class Location(object):
    """Class template for locations.
    To create adjacent locations, use the base directions only,
    so 'n' instead of 'north' and 'in' instead of 'inside'.
    """

    _instances = list()

    def __init__(self, name):
        self.name = name
        self.status = 0
        self.x = 0
        self.y = 0

        self.description = None

        self._instances.append(self)

    @classmethod
    def list_locations(cls):
        return cls._instances

    def _get_opposite(self, direction):
        """Returns the opposite direction for creating two-way links."""
        pairs = {
            'n': 's',
            'e': 'w',
            's': 'n',
            'w': 'e',
            'in': 'out',
            'out': 'in'
        }
        return pairs.get(direction, None)

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y

    def get_desc(self):
        """Gets the locations's description text from loc_descriptions.json."""
        self.description = loc_descriptions[self.name]
        if self.status == 0:
            self.status = 1
            return self.description

    def look(self, data_object):
        items_here = data_object.get_items_in_location(self)
        npcs_here = data_object.get_npcs_in_location(self)
        if len(items_here) == 0 and len(npcs_here) == 0:
            return "You see nothing interesting."

        text = str()
        for item in items_here:
            article = 'an' if item.adjectives.startswith(
                ('a', 'i', 'u', 'e', 'o')) else 'a'
            text += f"\nThere is {article} {item.adjectives} {item.name} {random.choice(['here', 'nearby', 'close by'])}."
        for npc in npcs_here:
            text += f"\nYou see {npc.name.capitalize()} {random.choice(['standing there', 'walking around', 'nearby'])}."
        return text

    def move(self, data_object, direction):
        """Reaction to 'go' commands.
        Moves to an adjacent location in the target direction. The method
        returns the location object that lies in that direction.
        """
        # If no location is in the target direction ...
        coordinates = [(loc.x, loc.y) for loc in loc_map]
        pos_x, pos_y = self.x, self.y
        mov_x, mov_y = self._parse_direction(direction)
        if (self.x + mov_x, self.y + mov_y) not in coordinates:
            stack.append("There is nothing in this direction.")
            return self

        # Check whether there's something in the way.
        blockers = [item for item in items if isinstance(item, Blocker)]
        if len(blockers) > 0:
            for blocker in blockers:
                if blocker.location == self and direction in blocker.blocks:
                    stack.append(
                        f"A {blocker.adjectives} {blocker.name} blocks the way.")
                    return self

        # Else get the coordinates for the target and make the move.
        target_loc = [loc for loc in loc_map if loc.x ==
                      self.x + mov_x and loc.y == self.y + mov_y]
        if len(target_loc) > 1:
            raise Exception("More than one location with those coordinates.")
        stack.append(target_loc[0].name, 2)
        if target_loc[0].status == 0:
            stack.append(target_loc[0].get_desc())
        return target_loc[0]

    def _parse_direction(self, direction):
        """Returns coordinate changes for a given direction."""
        dirs = {
            'n': (0, 1),
            'e': (1, 0),
            's': (0, -1),
            'w': (-1, 0)
        }
        x, y = dirs.get(direction, None)
        return x, y
