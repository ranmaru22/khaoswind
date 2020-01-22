"""This file handles the player's inventory."""


class Inventory(object):
    """Base class for the inventory object."""

    def __init__(self):
        self.items = dict()

    def add(self, item_obj, location_obj, stack):
        """Adds an item to the player's inventory, removes it from the location
        and pushes a message to the stack.
        If the location is None, the item is added covertly (i.e no message is
        pushed onto the stack).
        """
        self.items[item_obj.name] = item_obj
        item_obj.location = self
        if location_obj is not None:
            del location_obj.items[item_obj.name]
            stack.append(f"You picked up the {item_obj.name}.")

    def check(self):
        """Executes when the player enters the inv command."""
        if len(self.items) == 1:
            item = next(iter(self.items))
            article = 'an' if item.startswith(
                ('a', 'i', 'u', 'e', 'o')) else 'a'
            text = f"You carried {article} {item}."
        # If there is more than one item, return a string that lists all the
        # items in a comma-separated sentence.
        elif len(self.items) > 1:
            first = True
            text = str()
            for item in self.items:
                article = 'an' if item.name.startswith(
                    ('a', 'i', 'u', 'e', 'o')) else 'a'
                if first:
                    text += f"You had {article} {item.name}"
                    first = False
                else:
                    text += f", {article} {item.name}"
            else:
                text = text.rsplit(
                    f', {article}', 1)[0] + f', and {article}' + text.rsplit(f', {article}', 1)[-1] + ' on you.'
        # Catch-all clause if inventory is empty.
        else:
            text = "Your pockets were empty."
        return text
