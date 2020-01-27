"""This file handles the player's inventory."""


class Inventory(object):
    """Base class for the inventory object."""

    def __init__(self):
        self.items = list()
        self.name = "Inventory"

    def add(self, data_object, item):
        if item.location is not None:
            data_object.stack.append(f"You pick up the {item.name}.")
        item.location = self
        self.items.append(item)

    def check(self):
        if self.is_empty():
            return "Your pockets are empty."
        text = "You carry:"
        for item in self.items:
            text += f"\n- {item.name}"
        return text

    def is_empty(self):
        return len(self.items) == 0
