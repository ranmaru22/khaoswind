"""This file handles all non-player characters in the game."""

import json

import game_functions as gf


class NPC(object):
    """Base class for NPC objects."""

    _instances = list()

    with open("internals/conversations.json") as f_obj:
        _conversations = json.load(f_obj)
    with open("internals/npc_descriptions.json") as f_obj:
        _npc_descriptions = json.load(f_obj)

    def __init__(self, name):
        self.name = name
        self.location = None
        self.description = None
        self._get_desc()
        self.finished_convs = 0

        self._instances.append(self)

    @classmethod
    def list_npcs(cls):
        """A list of all NPC objects."""
        return cls._instances

    def _get_desc(self):
        self.description = self._npc_descriptions[self.name]

    def trigger_conv(self, data_object):
        try:
            conv = self._conversations[self.name][str(self.finished_convs + 1)]
            self.finished_convs += 1
        except IndexError:
            conv = self._conversations[self.name][str(self.finished_convs)]
        for line in conv:
            data_object.stack.append(f'"{line}"', 1)
