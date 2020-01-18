"""Contains commands and command-related functions."""

# Command lists
look_cmds = ['look', 'look at', 'watch', 'observe', 'stare at']
go_cmds = ['go', 'walk', 'run', 'move']
directions = ['n', 'e', 's', 'w', 'north', 'east', 'south', 'west', 'left',
              'right', 'up', 'down', 'inside', 'in', 'outside', 'out']


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


def parse_command(cmd, location):
    """Interprets latest user input."""

    # Ignore case and tailing whitespace
    cmd = cmd.lower().strip()

    # Quit clause
    if cmd == 'q':
        # ADD ALL THIS BACK IN LATER
        # r = input("Are you sure? ([y]es/[n]o) ").lower()
        # if r.startswith('y'):
            print('Thank you for playing!')
            raise SystemExit
        # return

    # If player enters a direction without a keyword
    if cmd in directions:
        target = consolidate_directions(cmd)
        # Check whether there's anything in that direction at the current location
        if target not in location.adj:
            return "There is nothing in that direction."
        return change_loc(location, target)

    # If player enters a look command
    if cmd.rsplit(' ', 1)[0] in look_cmds:
        return location.look()

    # If player enters a go command
    if cmd.rsplit(' ', 1)[0] in go_cmds:
        target = consolidate_directions(cmd.rsplit(' ', 1)[-1])
        # Check whether there's anything in that direction at the current location
        if target not in location.adj:
            return "There is nothing in that direction."
        return change_loc(location, target)


def change_loc(old_location, new_location):
    """Invokes a location change."""
    pass  # tdb
