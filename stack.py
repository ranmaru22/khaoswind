"""Functions related to the print stack."""

import textwrap as tw

import game_functions as gf


class Stack(object):
    """The main print stack for the game.
    Every round through the main loop, the stack will be emptied and
    everyting that has been stacked will be printed to output in the
    reverse order it has been added. As soon as the stack is empty,
    the game prompts the player for another command.
    """

    def __init__(self):
        # Start with an empty stack.
        self.items = list()
        self.item_types = list()

        # Initialize the TextWrapper object.
        self.wrapper = tw.TextWrapper(width=80, replace_whitespace=False)

    def append(self, item, type_=0):
        """Add an item to the stack.
        If no type is specified, the item is added as normal text (type 0).
        Type 1 is spoken text which will be printed slowly."""
        self.items.append(item)
        self.item_types.append(type_)

    def pop(self):
        """Pops the last item off the stack and returns it."""
        last = self.items.pop()
        _ = self.item_types.pop()
        return last

    def print_stack(self):
        """Empties the stack and prints all the items on it."""
        self.items.reverse()
        self.item_types.reverse()
        while self.items:
            item = self.items.pop()
            type_ = self.item_types.pop()
            for line in self.wrapper.wrap(item):
                if type_ == 1:
                    gf.print_speak(line)
                else:
                    print(line)
            print('')
