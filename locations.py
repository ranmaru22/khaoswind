"""The locations of the game."""

import json
import random

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
        """Loads the locations's description text from loc_descriptions.json."""
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
            text += f"There is {article} {item.adjectives} {item.name} {random.choice(['here', 'nearby', 'close by'])}.\n"
        for npc in npcs_here:
            text += f"You see {npc.name.capitalize()} {random.choice(['standing there', 'walking around', 'nearby'])}.\n"
        return text.rstrip()

    def move(self, data_object, direction):
        delta_x, delta_y = self._parse_direction(direction)
        target_loc = data_object.get_loc_from_coordinates(
            self.x + delta_x, self.y + delta_y)
        if target_loc is None:
            data_object.stack.append("There is nothing in this direction.")
            return self

        # Check for blockers.
        opposite_dir = self._get_opposite(direction)
        if data_object.is_blocked(direction):
            blockers = set([b for b in data_object.get_blockers()
                            if direction in b.blocked_directions])
        elif data_object.is_blocked(opposite_dir, target_loc):
            blockers = set([b for b in data_object.get_blockers(target_loc)
                            if opposite_dir in b.blocked_directions])
        else:
            blockers = None
        if blockers:
            text = str()
            for blocker in blockers:
                text += f"A {blocker.adjectives} {blocker.name} blocks the way.\n"
            data_object.stack.append(text.rstrip())
            return self

        data_object.stack.append(target_loc.name, 2)
        if target_loc.status == 0:
            data_object.stack.append(target_loc.get_desc())
        data_object.set_current_loc(target_loc)
        return target_loc

    def _parse_direction(self, direction):
        vectors = {
            'n': (0, 1),
            'e': (1, 0),
            's': (0, -1),
            'w': (-1, 0)
        }
        x, y = vectors.get(direction, None)
        return x, y
