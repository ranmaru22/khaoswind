"""Contains commands and command-related functions."""

import unicodedata

# Command lists
look_cmds = ['look', 'look at']
go_cmds = ['go', 'go to', 'walk', 'move']
directions = ['n', 'e', 's', 'w', 'north', 'east', 'south', 'west', 'left',
              'right', 'up', 'down', 'inside', 'in', 'outside', 'out']
take_cmds = ['take', 'get']
talk_cmds = ['talk', 'talk to', 'ask']


def _consolidate_directions(cmd):
    """Matches equivalent movement commands."""
    if cmd == 'north':
        return 'n'
    elif cmd == 'east':
        return 'e'
    elif cmd == 'south':
        return 's'
    elif cmd == 'west':
        return 'w'
    elif cmd == 'outside':
        return 'out'
    elif cmd == 'inside':
        return 'in'
    return cmd


# ! All public functions must return a location object.

def parse_command(cmd, location, inventory, stack):
    """Interprets latest user input."""

    # Ignore case and tailing whitespace
    cmd = unicodedata.normalize("NFKD", cmd.casefold().strip())

    # Quit clause
    if cmd in ['q', 'quit']:
        # TODO: ADD ALL THIS BACK IN LATER
        # r = input("Are you sure? ([y]es/[n]o) ").lower()
        # if r.startswith('y'):
        print('Thank you for playing!')
        raise SystemExit
        # return

    # Help command
    elif cmd in ['h', 'help']:
        print(
            "Available commands: LOOK (AT), GO, TAKE, TALK (TO), I[NVENTORY], Q[UIT]")
        print("You can also just enter a direction to go there.")
        return location

    # Check inventory command
    elif cmd in ['i', 'inv', 'inventory']:
        stack.append(inventory.check())
        return location

    # If player enters a direction without a keyword
    elif cmd in directions:
        direction = _consolidate_directions(cmd)
        return _change_loc(location, direction, stack)

    # If player enters a go command
    elif cmd.startswith('go'):
        direction = _consolidate_directions(cmd.rsplit(' ', 1)[-1])
        return _change_loc(location, direction, stack)

    # If player enters a look command
    elif cmd.startswith('look'):
        if len(cmd.split(' ')) > 1:
            target = cmd.rsplit(' ', 1)[-1]
            # If the player does not specify a target ...
            if target == 'at':
                stack.append("What do you want to look at?")
                return location
            # Check whether the item is actually there.
            # If yes, return its description.
            if target in location.items.keys():
                stack.append(location.items[target].description)
                return location
            stack.append(f"There's no {target} here ...")
            return location
        # If the player just types 'look,' return the location's
        # description plus items instead.
        location.get_desc()
        stack.append(location.description)
        stack.append(location.look())
        return location

    # If player enters a take command
    elif cmd.startswith('take'):
        item = location.items[cmd.rsplit(' ', 1)[1]]
        _take_item(item, location, inventory, stack)
        return location

    # If player enters a talk command
    elif cmd.startswith('talk'):
        if len(cmd.split(' ')) <= 2:
            stack.append("Who do you want to talk to?")
            return location
        target = cmd.rsplit(' ', 1)[-1]
        # Check whether that NPC is at the player's location.
        if target not in location.npcs:
            stack.append("There's no one there ...")
            return location
        # Ask for a keyword and trigger a conversation.
        keyword = input("\nWhat did you want to talk about again?\n> ")
        keyword = unicodedata.normalize("NFKD", keyword.casefold().strip())
        npc = location.npcs[target]
        npc.trigger_conv(keyword, stack)
        return location

    # Catch unrecognized commands
    else:
        stack.append("Hmm, that didn't work out.")
        return location


def _take_item(item, location, inventory, stack):
    """Picks up an item."""
    # Check whether the player can pick up the item.
    if not item.allow_pickup:
        stack.append("You cannot pick that up.")
        return location
    inventory.add(item, location, stack)
    return location


def _change_loc(location, direction, stack):
    """Invokes a location change."""
    return location.move(location, direction, stack)
