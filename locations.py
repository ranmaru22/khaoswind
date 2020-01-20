"""The locations of the game."""

import json

# Load the location descriptions.
with open("internals/loc_descriptions.json") as f_obj:
    loc_descriptions = json.load(f_obj)


class Location(object):
    """Class template for locations.
    To create adjacent locations, use the base directions only,
    so 'n' instead of 'north' and 'in' instead of 'inside'.
    """

    def __init__(self, name):
        """Initializes the base variables."""
        self.name = name
        self.status = 0

        # Relative locations and allowed movements
        self.adj = dict()
        self.allowed_movements = list()

        # Items found.
        self.items = dict()

        # NPCs in the location.
        self.npcs = dict()

        # Upon creation, the new location object will automatically
        # pull the base description from loc_descriptions.json.
        self.description = None
        self.prompt = "What do you do?"

    # Methods to add properties to the location.
    # These don't return output!
    def add_link(self, direction, location_obj):
        """Creates a link to a target location."""
        self.adj[direction] = location_obj
        self.allowed_movements.append(direction)

    def add_item(self, item_name, item_obj):
        """Adds an item to the location."""
        self.items[item_name] = item_obj

    def add_npc(self, npc_obj):
        """Adds an NPC to the location."""
        self.npcs[npc_obj.name] = npc_obj

    # Method to change the default prompt.
    def ch_prompt(self, prompt):
        """Changes the location's prompt."""
        self.prompt = prompt

    def get_desc(self):
        """Gets the locations's description text from loc_descriptions.json."""
        self.description = loc_descriptions[self.name][self.status]
        if self.status == 0:
            self.status += 1
        return self.description

    # Methods which react to player input.
    # Always return output which then goes to the stack. If they
    # don't return output directly, they call functions which do.
    def look(self):
        """Reaction to 'look' command."""
        text = str()
        # If there is only one item, return a short string.
        if len(self.items) == 1:
            item = next(iter(self.items))
            article = 'an' if item.startswith(
                ('a', 'i', 'u', 'e', 'o')) else 'a'
            text_items = f"You see {article} {item}."
            text += text_items
        # If there is more than one item, return a string that lists all the
        # items in a comma-separated sentence.
        elif len(self.items) > 1:
            first = True
            text_items = str()
            for item in self.items:
                article = 'an' if item.startswith(
                    ('a', 'i', 'u', 'e', 'o')) else 'a'
                if first:
                    text_items += f"You see {article} {item}"
                    first = False
                else:
                    text_items += f", {article} {item}"
            else:
                text_items = text_items.rsplit(
                    f', {article}', 1)[0] + f', and {article}' + text_items.rsplit(f', {article}', 1)[-1] + '.'
            text += text_items

        # Next, check for NPCs in the same way.
        if len(self.npcs) == 1:
            text_npc = f"You see {next(iter(self.npcs)).capitalize()}."
            text += "\n" + text_npc
        elif len(self.npcs) > 1:
            first = True
            text_npc = str()
            for npc in self.npcs:
                if first:
                    text_npc += f"{npc.capitalize()}"
                    first = False
                else:
                    text_npc += f", {npc.capitalize()}"
            else:
                text_npc = text_npc.rsplit(
                    ', ', 1)[0] + ', and ' + text_npc.rsplit(', ', 1)[-1] + ' are standing there.'
            text += "\n" + text_npc
        # Catch-all clause if there is nothing to be seen.
        if not text:
            text = "You see nothing interesting."
        return text

    def move(self, current_loc, direction, stack):
        """Reaction to 'go' commands.
        Moves to an adjacent location in the target direction. The methods returns the location object that lies in that direction.
        """
        # If no location is in the target direction, return a comment.
        if direction not in self.allowed_movements:
            stack.append("There is nothing in this direction.")
            return current_loc
        # Else set the current location to the new object and push its
        # description onto the stack.
        current_loc = self.adj[direction]
        stack.append(current_loc.get_desc())
        return current_loc
