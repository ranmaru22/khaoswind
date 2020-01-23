"""The main file for running the game."""


import os
import time
import random
import json

import commands as com
import locations as loc
import stack as st
import inventory as inv
import items as itm
import npcs as npc


class TransparentBlue(object):
    """The main class containing the init and run methods."""

    def __init__(self):
        # Initalize the base variables.
        self.locations = self.init_locations()
        self.items = self.init_items()
        self.npcs = self.init_npcs()
        self.inventory = inv.Inventory()
        self.current_loc = self.locations[0]  # random.choice(self.locations)

        # Fill the map.
        for room in self.locations:
            room.generate_links(self.locations)

        # Set the prompt for the title screen.
        self.prompt = "Press Enter so start the game ..."

        # Load the logo.
        with open("internals/logo.txt") as f_obj:
            self.logo = f_obj.read()

        # Initialize the stack.
        self.stack = st.Stack()

    def init_locations(self):
        """Initializes the game's location objects."""
        # Main Locations
        room_grid_size = 9  # TODO: Variable grid sizes.
        rooms = list()
        with open('internals/loc_descriptions.json') as f_obj:
            all_rooms = json.load(f_obj)
            for room in all_rooms:
                rooms.append(loc.Location(room[0]))
        # Creating random links between rooms.
        for i, room in enumerate(rooms):
            link = random.choice([l for l in 'nesw' if l not in room.adj])
            try:
                room.add_link(link, rooms[i+1])
            except IndexError:
                continue
            x, y = room.x, room.y
            if link == 'n':
                rooms[i+1].set_coords(x, y+1)
            elif link == 'e':
                rooms[i+1].set_coords(x+1, y)
            elif link == 's':
                rooms[i+1].set_coords(x, y-1)
            elif link == 'w':
                rooms[i+1].set_coords(x-1, y)
        return rooms

    def init_items(self):
        """Initializes items at random locations."""
        items = [
            itm.Item('stick', random.choice(self.locations), True),
            itm.Item('foo', random.choice(self.locations), False, True),
            itm.Item('oogie', random.choice(
                self.locations), False, True, ['stick'])
        ]
        return items

    def init_npcs(self):
        """Initializes NPCs at random locations."""
        npcs = [
            npc.NPC('sample', random.choice(self.locations))
        ]
        return npcs

    def intro(self):
        """Plays the intro sequence of the game and gets input."""
        # self.stack.append

    def main(self):
        """The main method for running the game."""
        # Show the title screen the first time the game starts.
        # ! DEBUG MODE: Skipping title screen
        # os.system('clear')
        # print(self.logo)
        # input(self.prompt)

        # Push the start location's description to the stack.
        self.stack.append(self.current_loc.get_desc())

        # Start the main loop
        os.system('clear')
        while True:
            # Print all info from the stack.
            print()
            print("DEBUG: Initialized rooms:", [
                  l.name for l in self.locations])
            print(self.current_loc.x, self.current_loc.y)
            self.stack.print_stack()

            # Print the prompt and wait for player input
            self.prompt = self.current_loc.prompt
            print(self.prompt)
            cmd = input("> ")

            # Process the player's input and add the response to the stack
            self.current_loc = com.parser(cmd, self.current_loc,
                                          self.inventory, self.locations, self.items, self.npcs, self.stack)


if __name__ == '__main__':
    game = TransparentBlue()
    game.main()
    # print(game.current_loc.items)
