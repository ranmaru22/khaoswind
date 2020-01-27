"""This file handles all non-player characters in the game."""

import json

import game_functions as gf

# Load the conversations and descriptions.
with open("internals/conversations.json") as f_obj:
    conversations = json.load(f_obj)
with open("internals/npc_descriptions.json") as f_obj:
    npc_descriptions = json.load(f_obj)


class NPC(object):
    """Base class for NPC objects."""

    _instances = list()

    def __init__(self, name):
        self.name = name
        self.location = None
        self.description = None
        self._get_desc()

        self._instances.append(self)

    @classmethod
    def list_npcs(cls):
        """A list of all NPC objects."""
        return cls._instances

    def _get_desc(self):
        """Gets the NPC's description text from npc_descriptions.json."""
        self.description = npc_descriptions[self.name]

    def trigger_conv(self, keyword, stack):
        """Triggers a conversation. Loads the lines from conversations.json and
        pushes them onto the stack.
        """
        if keyword not in conversations[self.name]:
            stack.append("\"I don't know anything about that ...\"", 1)
            return
        for line in conversations[self.name][keyword]:
            stack.append(f'"{line}"', 1)

    def move(self, loc_map):
        """Moves the NPC to an adjacent location."""
        x, y = self.location.x, self.location.y
        targets = [loc for loc in loc_map if loc.x ==
                   x + mov_x and loc.y == self.y + mov_y]
