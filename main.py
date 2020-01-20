"""The main file for running the game."""


import os
import time

import commands as com
import locations as loc
import stack as st
import inventory as inv
import items as itm
import npcs as npc


class TransparentBlue(object):
    """The main class containing the init and run methods."""

    def __init__(self):
        # Initalize location objects, item objects, and set the
        # start location to South Main Street.
        self.init_locations()
        self.init_items()
        self.init_npcs()
        self.current_loc = self.loc_south_main_street

        # Start with an empty inventory.
        self.inventory = inv.Inventory()

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
        # Main Street
        self.loc_south_main_street = loc.Location('South Main Street')
        self.loc_north_main_street = loc.Location('North Main Street')
        # Side Street
        self.loc_east_side_street = loc.Location('East Side Street')
        self.loc_west_side_street = loc.Location('West Side Street')
        # Create links
        self.loc_south_main_street.add_link('n', self.loc_north_main_street)
        self.loc_north_main_street.add_link('s', self.loc_south_main_street)
        self.loc_north_main_street.add_link('e', self.loc_east_side_street)
        self.loc_east_side_street.add_link('w', self.loc_north_main_street)
        self.loc_north_main_street.add_link('w', self.loc_west_side_street)
        self.loc_west_side_street.add_link('e', self.loc_north_main_street)

    def init_items(self):
        """Initializes items at their default locations."""
        item_stick = itm.Item('stick', True, self.loc_south_main_street)
        item_cig = itm.Item('cigarette', True, self.loc_south_main_street)
        item_phone = itm.Item('phone', True, self.loc_south_main_street)
        item_debug = itm.Item('oogie', True, self.loc_south_main_street)

    def init_npcs(self):
        """Initializes NPCs in their locations."""
        npc_sample = npc.NPC('sample', self.loc_east_side_street)

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
            self.stack.print_stack()

            # Print the prompt and wait for player input
            self.prompt = self.current_loc.prompt
            print(self.prompt)
            cmd = input("> ")

            # Process the player's input and add the response to the stack
            self.current_loc = com.parse_command(cmd, self.current_loc,
                                                 self.inventory, self.stack)


if __name__ == '__main__':
    game = TransparentBlue()
    game.main()
    # print(game.current_loc.items)
