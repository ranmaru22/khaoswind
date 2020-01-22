"""The items of the game."""

import json

# Load the item descriptions.
with open("internals/item_descriptions.json") as f_obj:
    item_descriptions = json.load(f_obj)


class Item(object):
    """Template class for items."""

    def __init__(self, name, allow_pickup, is_usable, location):
        self.name = name
        self.status = 0
        self.allow_pickup = allow_pickup
        self.is_usable = is_usable
        self.usable_with = list()
        self.location = location

        # Upon creation, the new location object will automatically
        # pull the base description from loc_descriptions.json.
        self.description = None
        self._get_desc()

        # Add it to the location
        self._add_to_loc(location)

    def _get_desc(self):
        """Gets the items's description text from item_descriptions.json."""
        self.description = item_descriptions[self.name][self.status]

    def _add_to_loc(self, location):
        """Adds the item to the location's inventory."""
        location.add_item(self.name, self)

    def pick_up(self, inventory, location, stack):
        """Adds the item to the player's inventory and removes it from the
        location's inventory.
        """
        inventory.add(self)
