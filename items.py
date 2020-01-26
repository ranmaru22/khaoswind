"""The items of the game."""

import json

# Load the item descriptions.
with open("internals/item_descriptions.json") as f_obj:
    item_descriptions = json.load(f_obj)


class Item(object):
    """Template class for items."""

    _instances = list()

    def __init__(self, name, location, allow_pickup=False, is_usable=False, usable_with=[]):
        self.name = name
        self.location = location
        self.allow_pickup = allow_pickup
        self.is_usable = is_usable
        self.usable_with = usable_with
        self.used = False

        # Upon creation, the new location object will automatically
        # pull the base description from loc_descriptions.json.
        self.description = None
        self._get_desc()

        self._instances.append(self)

    @classmethod
    def list_items(cls):
        """A list of all item objects."""
        return cls._instances

    def _get_desc(self):
        """Gets the items's description text from item_descriptions.json."""
        self.adjectives = item_descriptions[self.name][0]
        self.description = item_descriptions[self.name][1]

    def set_usable(self, other_item):
        """Sets the item to be usable with another item."""
        self.usable_with.append(other_item)

    def use(self, other_item):
        if not self.is_usable:
            return f"You cannot use that."
        if len(self.usable_with) > 0:
            if other_item is None:
                return f"You need a tool for that."
            elif other_item not in self.usable_with:
                return f"That didn't work."
            else:
                self.used = True
                return f"You used the {self.name} with the {other_item.name}."
        self.used = True
        return f"You used the {self.name}."


class Container(Item):
    """Subblass for items which contains other items."""

    def __init__(self, name, location, allow_pickup=False, is_usable=False, usable_with=[], contains=[]):
        super().__init__(name, location, allow_pickup, is_usable, usable_with)
        self.contains = contains

    def add(self, other_item):
        """Adds an item to the container."""
        new_content = [item for item in self.list_items() if item ==
                       other_item]
        if len(new_content) > 1:
            raise Exception("More than one item with the same name ...")
        self.contains.append(new_content[0])

    def use(self, other_item, inventory, stack):
        """Opens the items and adds the contents to the player's inventory."""
        if self.used:
            return f"The {self.name} is already open."
        if other_item is None:
            return f"You need a tool for that."
        elif other_item not in self.usable_with:
            return f"That cannot use the {other_item.name} here."
        text = str()
        self.used = True
        stack.append(
            f"You unlocked the {self.name} with the {other_item.name}.")
        for item in self.contains:
            inventory.add(item, None, stack)
            text += f"\nYou take the {item.name} from the {self.name}."
        return text


class Blocker(Item):
    """Subclass for items which block the way."""

    def __init__(self, name, location, allow_pickup=False, is_usable=False, usable_with=[], blocks=[]):
        super().__init__(name, location, allow_pickup, is_usable, usable_with)
        self.blocks = blocks

    def block_dir(self, direction):
        """Sets the blocker to block access to target direction."""
        self.blocks.append(direction)

    def _resolve(self):
        """Removes the blocker and opens the way."""
        self.blocks.clear()
        self.location = None

    def use(self, other_item, inventory, stack):
        """Uses an item to resolve the blocker."""
        if self.used:
            return None
        if other_item is None:
            return f"You need a tool for that."
        elif other_item not in self.usable_with:
            return f"That cannot use the {other_item.name} here."
        self.used = True
        self._resolve()
        return f"You unlocked the {self.name} with the {other_item.name}."
