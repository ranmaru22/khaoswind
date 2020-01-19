"""This file handles the player's inventory."""


class Inventory(object):
    """Base class for the inventory object."""

    def __init__(self):
        self.items = []

    def add(self, item_obj, location_obj, stack):
        """Adds an item to the player's inventory, removes it from the location
        and pushes a message to the stack.
        If the location is None, the item is added covertly (i.e no message is
        pushed onto the stack).
        """
        self.items.append(item_obj)
        if location_obj is not None:
            del location_obj.items[item_obj.name]
            stack.append(f"You pick up the {item_obj.name}.")

    def check(self):
        """Executes when the player enters the inv command."""
        if len(self.items) == 1:
            text = f"You carry a {next(iter(self.items)).name}."
        # If there is more than one item, return a string that lists all the
        # items in a comma-separated sentence.
        elif len(self.items) > 1:
            is_first = True
            text = str()
            for item in self.items:
                if is_first:
                    item_str += f"You carry a {item.name}"
                    is_first = False
                else:
                    item_str += f", a {item.name}"
            else:
                item_str = item_str.rsplit(
                    ', a', 1)[0] + ', and a' + item_str.rsplit(', a', 1)[-1] + '.'
        # Catch-all clause if inventory is empty.
        else:
            text = "You don't carry anything."
        return text
