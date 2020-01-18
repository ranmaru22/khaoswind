"""The main file for running the game."""


import os
import datetime
import textwrap as tw

import commands as c
import locations as loc

from internals import loc_descriptions as ld
from internals import logo


class TransparentBlue(object):
    """The main class containing the init and run methods."""

    def __init__(self):
        self.current_loc = None
        self.inventory = None
        self.prompt = None
        self.logo = logo.logo
        self.print_stack = list()
        
        self.t = tw.TextWrapper()

        # Set the start time
        self.time = datetime.time(20, 0)

        # Create the first location
        # Put this into another file later!
        main_street = loc.Location()
        main_street.name = 'South Main Street'
        main_street.ch_desc(ld.loc_main_street_start)
        # Change None to item obj for those!
        main_street.add_item('stick', None)
        main_street.add_item('pen', None)
        main_street.add_item('pair of headphones', None)
        self.current_loc = main_street
        
        self.wrapper = tw.TextWrapper(width=80)

        # Set the prompt
        self.prompt = "Press Enter so start the game ..."

    def show_header(self, time_obj, location_obj):
        """Shows the current location and time at the top."""
        header = "{:<} {:>{width}}".format(location_obj.name.upper(),
                                           time_obj.strftime("%l:%M %p"),
                                           width=80 - len(location_obj.name))
        return header

    def run_game(self):
        """The main loop for the game."""

        # Show the title screen
        print(self.logo)
        input(self.prompt)

        # Start the loop
        while True:
        # Clear the screen and show the header
            os.system('clear')
            print(self.show_header(self.time, self.current_loc) + '\r\n')
            
            # Print the current location's description.
            for line in self.wrapper.wrap(self.current_loc.description):
                print(line)
            
            # Print all info from the stack.
            for _ in self.print_stack:
                output = self.print_stack.pop()
                print('\r\n' + output)
                
            # Print the prompt and wait for player input
            self.prompt = self.current_loc.prompt
            print()
            cmd = input(self.prompt)
            
            # Process the player's input and add the response to the stack
            nxt = c.parse_command(cmd, self.current_loc)
            if nxt is None:
                print("Unknown command.")
                continue
            self.print_stack.append(nxt)


if __name__ == '__main__':
    game = TransparentBlue()
    game.run_game()
