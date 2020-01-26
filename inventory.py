"""This file handles the player's inventory."""


class Inventory(object):
    """Base class for the inventory object."""

    def __init__(self):
        self.items = list()
        self.name = "Inventory"

    def add(self, item_obj, location_obj, stack):
        """Adds an item to the player's inventory, removes it from the location
        and pushes a message to the stack.
        If the location is None, the item is added covertly (i.e no message is
        pushed onto the stack).
        """
        self.items.append(item_obj)
        item_obj.location = self
        if location_obj is not None:
            stack.append(f"You pick up the {item_obj.name}.")

    def check(self):
        """Executes when the player enters the inv command."""
        # Catch-all clause if inventory is empty.
        if len(self.items) == 0:
            return "Your pockets are empty."

        text = "You carry:"
        for item in self.items:
            text += f"\n- {item.name}"
        return text
