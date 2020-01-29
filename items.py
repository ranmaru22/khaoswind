"""The items of the game."""

import json


class Item(object):
    """Template class for items."""

    _instances = list()
    with open("internals/item_descriptions.json") as f_obj:
        item_descriptions = json.load(f_obj)

    def __init__(self, name):
        self.name = name
        self.location = None
        self.allow_pickup = False
        self.is_usable = False
        self.usable_with = list()
        self.used = False

        # Unique commands which tigger the item's use method.
        self.unique_verb = str()

        self.description = None
        self._get_desc()

        self._instances.append(self)

    @classmethod
    def list_items(cls):
        """A list of all item objects."""
        return cls._instances

    def _get_desc(self):
        self.adjectives = self.item_descriptions[self.name][0]
        self.description = self.item_descriptions[self.name][1]

    def set_pickup_allowed(self):
        self.allow_pickup = True

    def set_usable(self):
        self.is_usable = True

    def set_usable_with(self, other_item):
        self.usable_with.append(other_item)
        if not self.is_usable:
            self.is_usable = True

    def set_unique_verb(self, verb):
        self.unique_verb = verb

    def use(self, data_object, other_item):
        if not self.is_usable:
            return f"You cannot use that."
        if len(self.usable_with) > 0:
            if other_item is None:
                return f"You need a tool for that."
            elif other_item not in self.usable_with:
                return f"That didn't work."
            else:
                self.used = True
                return self.trigger_interaction()
        self.used = True
        return self.trigger_interaction()

    def set_interaction(self, func):
        """Wrapper function for unique item interactions."""
        self.interaction = func

    def trigger_interaction(self, *args):
        return self.interaction(*args)


class ContainedItem(Item):
    """Subclass for items found inside containers."""

    def __init__(self, name):
        super().__init__(name)


class Container(Item):
    """Subblass for items which contain other items."""

    def __init__(self, name):
        super().__init__(name)
        self.is_usable = True
        self.contains = list()

    def add_contents(self, item):
        self.contains.append(item)

    def use(self, data_object, item):
        """Opens the items and adds the contents to the player's inventory."""
        if self.used:
            return f"The {self.name} is already open."
        if item is None:
            return f"You need a tool for that."
        elif item not in self.usable_with:
            return f"That cannot use the {item.name} here."

        text = str()
        data_object.stack.append(
            f"You unlocked the {self.name} with the {item.name}.")
        for new_item in self.contains:
            data_object.inventory.add(data_object, new_item)
            text += f"\nYou take the {new_item.name} from the {self.name}."
        self.used = True
        return text


class Blocker(Item):
    """Subclass for items which block directions."""

    def __init__(self, name):
        super().__init__(name)
        self.is_usable = True
        self.blocked_directions = list()
        self.clear_msg = self.item_descriptions[self.name][2]

    def set_block_dir(self, direction):
        self.blocked_directions.append(direction)

    def _resolve(self):
        self.blocked_directions.clear()
        self.location = None
        self.used = True

    def use(self, data_object, item):
        if self.used:
            return None
        if item is None:
            return "You need a tool for that."
        elif not data_object.is_in_inventory(item):
            return "You don't have anything like that."
        elif item not in self.usable_with:
            return f"That cannot use the {item.name} here."
        self._resolve()
        return f"You {self.clear_msg} the {self.name} with the {item.name}."
