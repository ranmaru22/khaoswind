"""The main file for running the game."""


import os
import time
import random
import json

import commands as com
import locations as loc
import stack
import inventory as inv
import items
import npcs
import game_functions as gf
import settings


class Main(object):
    """The main class containing the init and run methods."""

    def __init__(self):
        self.settings = settings.Settings()
        self.game_data = gf.GameData(inv.Inventory(), stack.Stack())

        self.game_data.set_loc_list(self.init_locations())
        self.game_data.set_item_list(self.init_items())
        self.game_data.set_npc_list(self.init_npcs())
        self.game_data.set_current_loc(self.game_data.get_random_location())

        self.game_data.get_item_from_name('stick').set_pickup_allowed()
        self.game_data.get_item_from_name('keys').set_pickup_allowed()
        self.game_data.get_item_from_name('chest').add_contents(
            self.game_data.get_item_from_name('gold'))
        self.game_data.get_item_from_name('chest').set_usable_with(
            self.game_data.get_item_from_name('keys'))
        self.game_data.get_item_from_name('rubble').set_usable_with(
            self.game_data.get_item_from_name('stick'))
        self.game_data.get_item_from_name('rubble').set_block_dir('n')

        self.game_data.create_map()
        self.game_data.distribute_items()
        self.game_data.distribute_npcs()

        with open("internals/logo.txt") as f_obj:
            self.logo = f_obj.read()

    def init_locations(self):
        loc_list = [loc.Location("Entrance Room"),
                    loc.Location("Large Foyer")
                    ]
        return loc_list

    def init_items(self):
        item_list = [items.Item('stick'),
                     items.Item('keys'),
                     items.Container('chest'),
                     items.ContainedItem('gold'),
                     items.Blocker('rubble')
                     ]
        return item_list

    def init_npcs(self):
        npc_list = [npcs.NPC('sample')]
        return npc_list

    def main(self):
        # Show the title screen the first time the game starts.
        os.system('clear')
        print(self.logo)
        input("Press Enter so start the game ...")

        self.game_data.stack.append(self.game_data.current_loc.name, 2)
        self.game_data.stack.append(self.game_data.current_loc.get_desc())

        os.system('clear')
        print(self.game_data.locations)
        print(self.game_data.items)

        while True:
            print()
            self.game_data.stack.print_stack()
            cmd = input("> ")
            self.game_data.set_current_loc(com.parser(cmd, self.game_data))


if __name__ == '__main__':
    game = Main()
    game.main()
