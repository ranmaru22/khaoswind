"""The main file for running the game."""


import os
import datetime

import commands as c
import locations as loc
import stack as s


class TransparentBlue(object):
    """The main class containing the init and run methods."""

    def __init__(self):
        # Initalize location objects and set the start location
        # to South Main Street.
        self.init_locations()
        self.current_loc = self.south_main_street
        
        # Start with an empty inventory.
        self.inventory = None
        
        # Set the prompt for the title screen.
        self.prompt = "Press Enter so start the game ..."
        
        # Load the logo.
        with open("internals/logo.txt") as f_obj:
            self.logo = f_obj.read()
        
        # Initialize the stack.
        self.stack = s.Stack()

        # Set the start time to 8 PM.
        # Time has no effect yet, so this is just fluff for now.
        self.time = datetime.time(20, 0)

    def init_locations(self):
        """Initializes the game's location objects."""
        # Main Locations
        # South Main Street
        self.south_main_street = loc.Location('South Main Street')
        # Add some sample items. No item objects for now!
        self.south_main_street.add_item('stick', None)
        self.south_main_street.add_item('pen', None)
        self.south_main_street.add_item('pair of headphones', None)

    def show_header(self, time_obj, location_obj):
        """Shows the current location and time at the top.
        This will always be printed before the stack.
        """
        header = "{:<} {:>{width}}".format(location_obj.name.upper(),
                                           time_obj.strftime("%l:%M %p"),
                                           width=80 - len(location_obj.name))
        return header

    def run_game(self):
        """The main method for running the game."""

        # Show the title screen the first time the game starts.
        print(self.logo)
        input(self.prompt)
        
        # Push the start location's description to the stack.
        self.stack.append(self.current_loc.description)

        # Start the main loop
        while True:
        # Clear the screen and show the header
            os.system('clear')
            print(self.show_header(self.time, self.current_loc) + '\r\n')
            
            # Print all info from the stack.
            self.stack.print_stack()
                
            # Print the prompt and wait for player input
            self.prompt = self.current_loc.prompt
            cmd = input(self.prompt)
            
            # Process the player's input and add the response to the stack
            c.parse_command(cmd, self.current_loc, self.stack)


if __name__ == '__main__':
    game = TransparentBlue()
    game.run_game()
    # print(game.current_loc.description)
