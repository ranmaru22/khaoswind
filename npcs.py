"""This file handles all non-player characters in the game."""

import json

import game_functions as gf

# Load the conversations..
with open("internals/conversations.json") as f_obj:
    conversations = json.load(f_obj)


class NPC(object):
    """Base class for NPC objects."""

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def trigger_conv(self, keyword, stack):
        """Triggers a conversation. Loads the lines from conversations.json and
        pushes them onto the stack.
        """
        if keyword not in conversations[self.name]:
            stack.append("\"I don't know anything about that ...\"", 1)
            return
        for line in conversations[self.name][keyword]:
            stack.append(f'"{line}"', 1)
