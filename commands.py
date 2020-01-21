"""Contains commands and command-related functions."""

import unicodedata


def parser(cmd, location, inventory, stack):
    """New version."""
    # TODO: Run some tests on this before pushing it to master.
    directions = ['n', 'e', 's', 'w', 'north', 'east', 'south', 'west', 'left',
                  'right', 'up', 'down', 'inside', 'in', 'outside', 'out']
    # Ignore case and whitespace.
    cmd = unicodedata.normalize("NFKD", cmd.casefold().strip())

    # Carch system functions.
    if cmd in ['q', 'quit']:
        _system_exit()
    if cmd in ['h', 'help']:
        return _print_help(location)
    if cmd in ['i', 'inv', 'inventory']:
        return _show_inventory(location, inventory, stack)
    if cmd in directions:
        return _change_loc(location, cmd, stack)

    # Split player's input into command and argument.
    cmd_split = cmd.rsplit(' ', 1)
    if len(cmd_split) == 2:
        func, target = cmd_split
    else:
        func, target = cmd_split[0], None

    # Call the appropriate function.
    if func in ['look', 'look at']:
        return _look(location, stack, target)
    if func in ['go']:
        return _change_loc(location, target, stack)
    if func in ['take']:
        return _take(location, inventory, stack, target)
    if func in ['talk', 'talk to']:
        return _talk(location, stack, target)

    # If the player's input matches none of the commands:
    stack.append("Hmm, that didn't work out.")
    return location


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


def _system_exit():
    """Quits the game."""
    # TODO: ADD ALL THIS BACK IN LATER
    # TODO: Add a save/load function.
    # r = input("Are you sure? ([y]es/[n]o) ").lower()
    # if r.startswith('y'):
    print('Thank you for playing!')
    raise SystemExit
    # return??


def _print_help(location):
    """Prints available commands."""
    print(
        "Available commands: LOOK (AT), GO, TAKE, TALK (TO), I[NVENTORY], Q[UIT]")
    print("You can also just enter a direction to go there.")
    return location


def _show_inventory(location, inventory, stack):
    """Shows the player's inventory."""
    stack.append(inventory.check())
    return location


def _look(location, stack, *args):
    """Looks at an item or the location."""
    if args[0] is not None:
        target = args[0]
        # Check whether the player actually named an item.
        if target == 'at':
            stack.append("What did you want to look at?")
            return location
        # Check whether the item is actually there.
        if target in location.items.keys():
            stack.append(location.items[target].description)
            return location
        stack.append(f"There's no {target} in sight.")
        return location
    # If no argument was sent, inspect the location itself.
    location.get_desc()
    stack.append(location.description)
    stack.append(location.look())
    return location


def _take(location, inventory, stack, *args):
    """Picks up an item."""
    if args[0] is None:
        stack.append("What did you want to take again?")
        return location
    target = args[0]
    if target not in location.items:
        stack.append("There is nothing there ...")
        return location
    item = location.items[target]
    if not item.allow_pickup:
        stack.append("You cannot pick that up.")
        return location
    inventory.add(item, location, stack)
    return location


def _change_loc(location, direction, stack):
    """Invokes a location change."""
    if direction is None:
        stack.append("Where did you want to go again?")
        return location
    direction = _consolidate_directions(direction)
    return location.move(location, direction, stack)


def _talk(location, stack, *args):
    if args[0] is None:
        stack.append("Did you often talk to yourself?")
        return location
    target = args[0]
    # Check whether that NPC is at the player's location.
    if target not in location.npcs:
        stack.append("No, there's no one there ...")
        return location
    # Ask for a keyword and trigger a conversation.
    keyword = input("\nWhat did you mean to ask them?\n> ")
    keyword = unicodedata.normalize("NFKD", keyword.casefold().strip())
    npc = location.npcs[target]
    npc.trigger_conv(keyword, stack)
    return location
