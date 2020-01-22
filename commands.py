"""Contains commands and command-related functions."""

import unicodedata


def parser(cmd, location, inventory, locations, items, npcs, stack):
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
        return _look(location, items, npcs, stack, target)
    if func in ['go']:
        return _change_loc(location, target, stack)
    if func in ['take']:
        return _take(location, items, inventory, stack, target)
    if func in ['talk', 'talk to']:
        return _talk(location, npcs, stack, target)

    if func.startswith('use'):
        item = None
        if len(func.split()) == 3:
            func, item, _ = func.split()
        return _use(location, items, inventory, stack, item, target)

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
    # TODO: Add a save/load function.
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


def _show_inventory(location, inventory, stack):
    """Shows the player's inventory."""
    stack.append(inventory.check())
    return location


def _look(location, items, npcs, stack, *args):
    """Looks at an item or the location."""
    if args[0] is not None:
        target = args[0]
        # Check whether the player actually named an item.
        if target == 'at':
            stack.append("What did you want to look at?")
            return location
        # Check whether the item is actually there.
        item_names = [x.name for x in items]
        if target in item_names:
            item = items[item_names.index(target)]
            stack.append(item.description)
            return location
        stack.append(f"There's no {target} in sight.")
        return location
    # If no argument was sent, inspect the location itself.
    location.get_desc()
    stack.append(location.description)
    stack.append(location.look(items, npcs))
    return location


def _take(location, items, inventory, stack, *args):
    """Picks up an item."""
    print(items)
    if args[0] is None:
        stack.append("What did you want to take again?")
        return location
    target = args[0]
    item_names = [x.name for x in items]
    if target not in item_names:
        stack.append("Whatever you wanted to take, it was not there ...")
        return location
    item = items[item_names.index(target)]
    if not item.allow_pickup:
        stack.append("You could not pick that up.")
        return location
    inventory.add(item, location, stack)
    return location


def _change_loc(location, direction, stack):
    """Invokes a location change."""
    if direction is None:
        stack.append("Where did you want to go again?")
        return location
    direction = _shorten_direction(direction)
    return location.move(location, direction, stack)


def _talk(location, npcs, stack, *args):
    """Talks to an NPC."""
    if args[0] is None:
        stack.append("Did you often talk to yourself?")
        return location
    target = args[0]
    # Check whether that NPC is at the player's location.
    npc_names = [x.name for x in npcs]
    if target not in npc_names:
        stack.append("No, there's no one there ...")
        return location
    # Ask for a keyword and trigger a conversation.
    keyword = input("\nWhat was it you asked them?\n> ")
    keyword = unicodedata.normalize("NFKD", keyword.casefold().strip())
    npc = npcs[npc_names.index(target)]
    npc.trigger_conv(keyword, stack)
    return location


def _use(location, items, inventory, stack, *args):
    """Uses an item, or interacts with something at the location."""
    if args == (None, None):
        stack.append("You wanted to use something, didn't you?")
        return location
    else:
        item, target = args[1], args[0]
    try:
        item_names = [x.name for x in items]
        item_obj = items[item_names.index(item)]
    except KeyError:
        stack.append(f"There was no {item} in sight.")
        return location
    if not item_obj.is_usable:
        stack.append("There was no way you could do that.")
        return location
    if item_obj.used:
        stack.append("You remembered that you already did that.")
        return location
    if target is None:
        if len(item_obj.usable_with) > 0:
            stack.append(
                f"You were sure that there was something you could do with the {item_obj.name}, but you needed a different tool.")
            return location
        stack.append(f"You used the {item_obj.name}.")
        item_obj.used = True
        return location
    try:
        target_obj = items[item_names.index(target)]
    except KeyError:
        stack.append(f"You didn't have anything like that.")
        return location
    if target_obj.location.name != "Inventory":
        stack.append(f"You didn't have anything like that.")
        return location
    # ? Does the order matter?
    if target_obj.name not in item_obj.usable_with:
        stack.append(
            f"You tried using your {target_obj.name}, but it didn't work.")
        return location
    item_obj.used = True
    stack.append(f"You used your {target_obj.name} with the {item_obj.name}.")
    return location
