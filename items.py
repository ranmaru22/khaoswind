"""The items of the game."""

import json

# Load the item descriptions.
with open("internals/item_descriptions.json") as f_obj:
    item_descriptions = json.load(f_obj)


class Item(object):
    """Template class for items."""

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

    def _get_desc(self):
        """Gets the items's description text from item_descriptions.json."""
        self.adjectives = item_descriptions[self.name][0]
        self.description = item_descriptions[self.name][1]

    def pick_up(self, inventory, location, stack):
        """Adds the item to the player's inventory and removes it from the
        location's inventory.
        """
        inventory.add(self)
