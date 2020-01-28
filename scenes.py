"""File containing scenes which play out during the game."""

import json
import textwrap as tw

import game_functions as gf


class Scene(object):
    """A template class for scenes."""

    _instances = list()
    _wrapper = tw.TextWrapper(width=80, replace_whitespace=False)

    def __init__(self, name, location):
        self.name = name
        self.location = location

        with open(f"scenes/scene_{self.name}.json") as f_obj:
            self.contents = json.load(f_obj)

        self._instances.append(self)

    @classmethod
    def list_scenes(cls):
        return cls._instances

    def play(self):
        for paragraph in self.contents.values():
            if paragraph.startswith("***"):
                for line in self._wrapper.wrap(paragraph.lstrip('*')):
                    gf.print_speak(line)
            else:
                for line in self._wrapper.wrap(paragraph):
                    print(line)
            input("...")
