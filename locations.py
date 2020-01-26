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
        """Initializes the base variables."""
        self.name = name
        self.status = 0
        self.x = 0
        self.y = 0

        # Upon creation, the new location object will automatically
        # pull the base description from loc_descriptions.json.
        self.description = None

        self._instances.append(self)

    @classmethod
    def list_locations(cls):
        """A list of all location objects."""
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
        """Sets the location coordinates."""
        self.x = x
        self.y = y

    def get_desc(self):
        """Gets the locations's description text from loc_descriptions.json."""
        self.description = loc_descriptions[self.name]
        if self.status == 0:
            self.status = 1
            return self.description

    # Methods which react to player input.
    # Always return output which then goes to the stack. If they
    # don't return output directly, they call functions which do.

    def look(self, items, npcs):
        """Reaction to 'look' command."""
        items_here = list()
        npcs_here = list()
        for item in items:
            if item.location == self:
                items_here.append(item)
        for npc in npcs:
            if npc.location == self:
                npcs_here.append(npc)
        text = str()

        # First, list items.
        for item in items_here:
            article = 'an' if item.adjectives.startswith(
                ('a', 'i', 'u', 'e', 'o')) else 'a'
            text += f"\nThere is {article} {item.adjectives} {item.name} {random.choice(['here', 'nearby', 'close by'])}."

        # Next, list NPCs.
        for npc in npcs_here:
            text += f"\nYou see {npc.name.capitalize()} {random.choice(['standing there', 'walking around', 'nearby'])}."

        # Catch-all clause if there is nothing to be seen.
        if not text:
            text = "You see nothing interesting."
        return text

    def move(self, loc_map, items, direction, stack):
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
