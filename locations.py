"""The locations of the game."""

import json
import math

# Load the location descriptions.
with open("internals/loc_descriptions.json") as f_obj:
    loc_descriptions = json.load(f_obj)


class Location(object):
    """Class template for locations.
    To create adjacent locations, use the base directions only,
    so 'n' instead of 'north' and 'in' instead of 'inside'.
    """

    def __init__(self, name):
        """Initializes the base variables."""
        self.name = name
        self.status = 0
        self.x = 0
        self.y = 0

        # Upon creation, the new location object will automatically
        # pull the base description from loc_descriptions.json.
        self.description = None
        self.prompt = "What did you do next?"

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

    def ch_prompt(self, prompt):
        """Changes the location's prompt."""
        self.prompt = prompt

    def get_desc(self):
        """Gets the locations's description text from loc_descriptions.json."""
        self.description = loc_descriptions[self.name][self.status]
        if self.status == 0:
            self.status += 1
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
        # If there is only one item, return a short string.
        if len(items_here) == 1:
            item = next(iter(items_here))
            article = 'an' if item.name.startswith(
                ('a', 'i', 'u', 'e', 'o')) else 'a'
            text_items = f"You saw {article} {item.name}. "
            text += text_items
        # If there is more than one item, return a string that lists all the
        # items in a comma-separated sentence.
        elif len(items_here) > 1:
            first = True
            text_items = str()
            for item in items_here:
                article = 'an' if item.name.startswith(
                    ('a', 'i', 'u', 'e', 'o')) else 'a'
                if first:
                    text_items += f"You saw {article} {item.name}"
                    first = False
                else:
                    text_items += f", {article} {item.name}"
            else:
                text_items = text_items.rsplit(
                    f', {article}', 1)[0] + f', and {article}' + text_items.rsplit(f', {article}', 1)[-1] + '. '
            text += text_items

        # Next, check for NPCs in the same way.
        if len(npcs_here) == 1:
            text_npc = f"You saw {next(iter(npcs_here)).name.capitalize()}."
            text += text_npc
        elif len(npcs_here) > 1:
            first = True
            text_npc = str()
            for npc in npcs_here:
                if first:
                    text_npc += f"{npc.name.capitalize()}"
                    first = False
                else:
                    text_npc += f", {npc.name.capitalize()}"
            else:
                text_npc = text_npc.rsplit(
                    ', ', 1)[0] + ', and ' + text_npc.rsplit(', ', 1)[-1] + ' were standing there.'
            text += "\n" + text_npc
        # Catch-all clause if there is nothing to be seen.
        if not text:
            text = "You saw nothing interesting."
        return text

    def move(self, loc_map, direction, stack):
        """Reaction to 'go' commands.
        Moves to an adjacent location in the target direction. The method
        returns the location object that lies in that direction.
        """
        # If no location is in the target direction, return a comment.
        coordinates = [(loc.x, loc.y) for loc in loc_map]
        pos_x, pos_y = self.x, self.y
        mov_x, mov_y = self._parse_direction(direction)
        if (self.x + mov_x, self.y + mov_y) not in coordinates:
            stack.append("There is nothing in this direction.")
            return self
        # Else set the current location to the new object and push its
        # description onto the stack.
        target_loc = [loc for loc in loc_map if loc.x ==
                      self.x + mov_x and loc.y == self.y + mov_y]
        if len(target_loc) > 1:
            raise Exception("More than one location with those coordinates.")
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
