"""Contains commands and command-related verbtions."""

import unicodedata

import game_functions as gf


def parser(cmd, location, inventory, locations, items, npcs, stack):
    """Parses user commands."""

    directions = ['n', 'e', 's', 'w', 'north', 'east',
                  'south', 'west', 'inside', 'in', 'outside', 'out']
    # Ignore case and whitespace.
    cmd = unicodedata.normalize("NFKD", cmd.casefold().strip())

    # Catch system functions.
    if cmd in ['q', 'quit']:
        _system_exit()
    if cmd in ['h', 'help']:
        return _print_help(location)
    if cmd in ['i', 'inv', 'inventory']:
        return _show_inventory(location, inventory, stack)
    if cmd in ['m', ',map']:
        return _print_map(location, locations)
    if cmd in directions:
        return _change_loc(location, locations, items, cmd, stack)

    # Split player's input into command and argument.
    cmd_split = cmd.rsplit(' ', 1)
    if len(cmd_split) == 2:
        verb, obj1 = cmd_split
    else:
        verb, obj1 = cmd_split[0], None

    # Call the appropriate verbtion.
    if verb in ['look', 'look at']:
        return _look(location, items, npcs, stack, obj1)
    if verb in ['go', 'go to']:
        return _change_loc(location, locations, obj1, stack)
    if verb in ['take', 'get']:
        return _take(location, items, inventory, stack, obj1)
    if verb in ['talk', 'talk to']:
        return _talk(location, npcs, stack, obj1)

    # Further split the input for the two-argument use command.
    if verb.startswith('use'):
        obj2 = None
        if len(verb.split()) == 3:
            verb, obj2, _ = verb.split()
        return _use(location, items, inventory, stack, obj1, obj2)

    # If the player's input matches none of the commands:
    stack.append("Hmm, that didn't work out.")
    return location


def _shorten_direction(cmd):
    """Matches equivalent movement commands."""
    shorts = {
        'north': 'n',
        'east': 'e',
        'south': 's',
        'west': 'w',
        'outside': 'out',
        'inside': 'in'
    }
    return shorts.get(cmd, cmd)


def _system_exit():
    """Quits the game."""
    # TODO: ADD ALL THIS BACK IN LATER
    # TODO: Add a save/load verbtion.
    # r = input("Are you sure? ([y]es/[n]o) ").lower()
    # if r.startswith('y'):
    print('Thank you for playing!')
    raise SystemExit
    # return??


def _print_help(location):
    """Prints available commands."""
    print(
        "Available commands: LOOK (AT), GO, TAKE, TALK TO, I[NVENTORY], Q[UIT]")
    print("You can also just enter a direction to go there.")
    return location


def _print_map(location, locations):
    """DEBUG METHOD: Shows the room map."""
    gf.draw_map(location, locations)
    return location


def _show_inventory(location, inventory, stack):
    """Shows the player's inventory."""
    stack.append(inventory.check())
    return location


def _look(location, items, npcs, stack, *args):
    """Looks at an item or the location."""
    if args[0] is not None:
        obj1 = args[0]
        # Check whether the player actually named an item.
        if obj1 == 'at':
            stack.append("What did you want to look at?")
            return location
        # Check whether the item is actually there.
        item_names = [x.name for x in items]
        if obj1 in item_names:
            item = items[item_names.index(obj1)]
            if item.location == location:
                stack.append(item.description)
                return location
        npc_names = [x.name for x in npcs]
        if obj1 in npc_names:
            npc = npcs[npc_names.index(obj1)]
            if npc.location == location:
                stack.append(npc.description)
                return location
        stack.append(f"There's no {obj1} in sight.")
        return location
    # If no argument was sent, inspect the location itself.
    location.get_desc()
    stack.append(location.description)
    stack.append(location.look(items, npcs))
    return location


def _take(location, items, inventory, stack, *args):
    """Picks up an item."""
    if args[0] is None:
        stack.append("What do you want to pick up?")
        return location
    obj1 = args[0]
    item_names = [x.name for x in items]
    if obj1 not in item_names:
        stack.append("You don't see that anywhere.")
        return location
    item = items[item_names.index(obj1)]
    if item.location != location:
        stack.append("You don't see that anywhere.")
        return location
    if not item.allow_pickup:
        stack.append("You cannot pick that up.")
        return location
    inventory.add(item, location, stack)
    return location


def _change_loc(location, loc_map, items, direction, stack):
    """Invokes a location change."""
    if direction is None:
        stack.append("Where do you want to go?")
        return location
    direction = _shorten_direction(direction)
    return location.move(loc_map, items, direction, stack)


def _talk(location, npcs, stack, *args):
    """Talks to an NPC."""
    if args[0] is None:
        stack.append("Did you often talk to yourself?")
        return location
    obj1 = args[0]
    # Check whether that NPC is at the player's location.
    npc_names = [x.name for x in npcs]
    if obj1 not in npc_names:
        stack.append("No, there's no one there ...")
        return location
    # Ask for a keyword and trigger a conversation.
    keyword = input("\nWhat was it you asked them?\n> ")
    keyword = unicodedata.normalize("NFKD", keyword.casefold().strip())
    npc = npcs[npc_names.index(obj1)]
    npc.trigger_conv(keyword, stack)
    return location


def _use(location, items, inventory, stack, *args):
    """Uses an item, or interacts with something at the location."""
    if args == (None, None):
        stack.append("What do you want to use?")
        return location
    else:
        obj1, obj2 = args[0], args[1]
    try:
        item_names = [x.name for x in items]
        obj1_obj = items[item_names.index(obj1)]
    except ValueError:
        stack.append(f"There is no {obj1} here.")
        return location
    try:
        obj2_obj = items[item_names.index(obj2)]
    except ValueError:
        obj2_obj = None
    if obj2_obj and obj2_obj.location.name != "Inventory":
        stack.append(f"You don't have anything like that.")
        return location
    stack.append(obj1_obj.use(obj2_obj, inventory, stack))
    return location
