"""The locations of the game."""


class Location(object):
    """Class template for locations."""

    def __init__(self):
        """Initializes empty variables."""
        self.name = None

        # Relative locations
        self.adj = dict()

        # Description returned when looking around.
        self.description = None
        self.prompt = "What do you do? "

        # Items found.
        self.items = dict()

    def add_loc(self, direction, location_obj):
        """Create links to other locations."""
        self.adj[direction] = location_obj

    def ch_desc(self, desc):
        """Sets the locations's description text."""
        self.description = desc

    def add_item(self, item_name, item_obj):
        """Adds an item to a location."""
        self.items[item_name] = item_obj

    def look(self):
        """Output for looking around."""
        if len(self.items) == 1:
            text = f"You see a {next(iter(self.items))}."
        elif len(self.items) > 1:
            text = f"You see {len(self.items)} things.\r\n"
            first = True
            item_str = str()
            for item in self.items:
                if first:
                    item_str += f"A {item}"
                    first = False
                else:
                    item_str += f", a {item}"
            else:
                item_str = item_str.rsplit(
                    ', a', 1)[0] + ', and a' + item_str.rsplit(', a', 1)[-1] + '.'
                text += item_str
        else:
            text = "You see nothing interesting."
        return text

    def ch_prompt(self, prompt):
        """Changes the location's prompt."""
        self.prompt = prompt
