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
import game_functions as gf
import settings as stt


class TransparentBlue(object):
    """The main class containing the init and run methods."""

    def __init__(self):
        # Initalize the base variables.
        self.settings = stt.Settings()
        self.inventory = inv.Inventory()
        self.current_loc = None

        # Set the prompt for the title screen.
        self.prompt = "Press Enter so start the game ..."

        # Load the logo.
        with open("internals/logo.txt") as f_obj:
            self.logo = f_obj.read()

        # Initialize the stack.
        self.stack = st.Stack()

        # Initialize locations, items, and NPCs
        self.init_locations()
        # self.locations = loc.Location.list_locations()
        self.init_items()
        self.items = itm.Item.list_items()
        self.init_npcs()
        self.npcs = npc.NPC.list_npcs()

    def init_locations(self):
        """Initializes the game's location objects."""

        # room_grid_size = 2  # TODO: Variable grid sizes.
        # with open('internals/loc_descriptions.json') as f_obj:
        #     all_rooms = json.load(f_obj)
        #     for room in all_rooms:
        #         x_room = loc.Location(room)
        #         room_grid_size -= 1
        #         if room_grid_size == 0:
        #             break
        room1 = loc.Location("Entrance Room")
        room2 = loc.Location("Large Foyer")
        self.current_loc = room1
        self.locations = loc.Location.list_locations()

        # Creating random links between rooms.
        x, y = 0, 0
        for room in self.locations:
            all_links = [(r.x, r.y) for r in self.locations]
            loc_set = False
            while not loc_set:
                link = random.choice('n')
                if link == 'n' and (x, y+1) not in all_links:
                    room.set_coords(x, y+1)
                elif link == 'e' and (x+1, y) not in all_links:
                    room.set_coords(x+1, y)
                elif link == 's' and (x, y-1) not in all_links:
                    room.set_coords(x, y-1)
                elif link == 'w' and (x-1, y) not in all_links:
                    room.set_coords(x-1, y)
                else:
                    continue
                x, y = room.x, room.y
                loc_set = True

    def init_items(self):
        """Initializes items at random locations."""
        stick = itm.Item('stick', random.choice(self.locations), True)
        keys = itm.Item('keys', random.choice(self.locations), True, False)
        chest = itm.Container('chest', random.choice(
            self.locations), False, True)
        gold = itm.Item('gold', None)
        rubble = itm.Blocker('rubble', random.choice(
            self.locations), False, True)

        chest.add(gold)
        chest.set_usable(keys)
        rubble.set_usable(stick)
        rubble.block_dir('n')

    def init_npcs(self):
        """Initializes NPCs at random locations."""
        all_loc = list(self.locations)
        sample = npc.NPC('sample', random.choice(all_loc))

    def main(self):
        """The main method for running the game."""
        # Show the title screen the first time the game starts.
        os.system('clear')
        print(self.logo)
        input(self.prompt)

        # Push the start location's description to the stack.
        self.stack.append(self.current_loc.name, 2)
        self.stack.append(self.current_loc.get_desc())

        # Start the main loop
        os.system('clear')
        print(self.locations)
        print(self.items)
        while True:
            # Print all info from the stack.
            print()
            self.stack.print_stack()

            # Wait for player input.
            cmd = input("> ")

            # Process the player's input and add the response to the stack
            self.current_loc = com.parser(cmd, self.current_loc,
                                          self.inventory, self.locations, self.items, self.npcs, self.stack)


if __name__ == '__main__':
    game = TransparentBlue()
    game.main()
