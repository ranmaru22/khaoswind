"""Contains commands and command-related functions."""

# Command lists
look_cmds = ['look', 'look at', 'watch', 'observe']
go_cmds = ['go', 'go to', 'walk', 'run', 'move']
directions = ['n', 'e', 's', 'w', 'north', 'east', 'south', 'west', 'left',
              'right', 'up', 'down', 'inside', 'in', 'outside', 'out']
take_cmds = ['take', 'pick up', 'get']


def consolidate_directions(cmd):
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


def parse_command(cmd, location, inventory, stack):
    """Interprets latest user input."""

    # Ignore case and tailing whitespace
    cmd = cmd.lower().strip()

    # Quit clause
    if cmd in ['q', 'quit']:
        # ADD ALL THIS BACK IN LATER
        # r = input("Are you sure? ([y]es/[n]o) ").lower()
        # if r.startswith('y'):
            print('Thank you for playing!')
            raise SystemExit
        # return

    # Help command
    elif cmd in ['h', 'help']:
        print("Available commands: LOOK, GO, TAKE, INVENTORY, QUIT")
        print("You can also just enter a direction to go there.")
        return

    # Check inventory command
    elif cmd in ['i', 'inv', 'inventory']:
        stack.append(inventory.check())
        return

    # If player enters a direction without a keyword
    elif cmd in directions:
        target = consolidate_directions(cmd)
        # Check whether there's anything in that direction at the current location
        if target not in location.adj:
            stack.append("There is nothing in that direction.")
            return
        change_loc(location, target)
        return

    # If player enters a look command
    elif cmd.rsplit(' ', 1)[0] in look_cmds:
        location.get_desc()
        stack.append(location.description)
        stack.append(location.look())
        return

    # If player enters a go command
    elif cmd.rsplit(' ', 1)[0] in go_cmds:
        target = consolidate_directions(cmd.rsplit(' ', 1)[-1])
        # Check whether there's anything in that direction at the current location
        if target not in location.adj:
            stack.append("There is nothing in that direction.")
            return
        change_loc(location, target)
        return

    # If player enters a take command
    elif cmd.rsplit(' ', 1)[0] in take_cmds:
        item = location.items[cmd.rsplit(' ', 1)[1]]
        take_item(item, location, inventory, stack)
        return

    # Catch unrecognized commands
    else:
        stack.append("Hmm, that didn't work out.")


def take_item(item, location, inventory, stack):
    """Picks up an item."""
    # Check whether the player can pick up the item.
    if not item.allow_pickup:
        stack.append("You cannot pick that up.")
        return
    inventory.add(item, location, stack)


def change_loc(old_location, new_location):
    """Invokes a location change."""
    old_location = new_location
    # old_location.move(new_location)
