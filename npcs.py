"""This file handles all non-player characters in the game."""

import json

import game_functions as gf

# Load the conversations..
with open("internals/conversations.json") as f_obj:
    conversations = json.load(f_obj)


class NPC(object):
    """Base class for NPC objects."""

    def __init__(self, name, location_obj):
        self.name = name
        self.location = location_obj
        self.finished_convs = list()

        # Add NPC to the location.
        location_obj.add_npc(self)

    def finish_conv(self, keyword):
        """Adds a conversation to the NPC's stack of finished conversations."""
        self.finished_convs.append(keyword)

    def trigger_conv(self, keyword, stack):
        """Triggers a conversation. Loads the lines from conversations.json and
        pushes them onto the stack.
        """
        if keyword not in conversations[self.name]:
            stack.append("\"I don't know anything about that ...\"", 1)
            return
        for line in conversations[self.name][keyword]:
            stack.append(line, 1)
        # Add the conversation to the list of finished ones.
        # This might be useful in the future ...
        self.finish_conv(keyword)
