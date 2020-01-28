"""Contains commands and command-related functions."""

import unicodedata

import game_functions as gf


def parser(cmd, data_object):
    """Parses user commands."""

    directions = ['n', 'e', 's', 'w', 'north', 'east',
                  'south', 'west', 'inside', 'in', 'outside', 'out']
    # Ignore case and whitespace.
    cmd = unicodedata.normalize("NFKD", cmd.casefold().strip())

    if cmd in ['q', 'quit']:
        _system_exit()
    if cmd in ['h', 'help']:
        return _print_help(data_object)
    if cmd in ['i', 'inv', 'inventory']:
        return _show_inventory(data_object)
    if cmd in ['m', ',map']:
        return _print_map(data_object)
    if cmd in directions:
        return _change_loc(data_object, cmd)

    # Split player's input into command and argument.
    cmd_split = cmd.rsplit(' ', 1)
    if len(cmd_split) == 2 and cmd_split[0] != 'at':
        verb, obj1 = cmd_split
    else:
        verb, obj1 = cmd_split[0], None

    if verb in ['look', 'look at']:
        return _look(data_object, obj1)
    if verb in ['go', 'go to']:
        return _change_loc(data_object, obj1)
    if verb in ['take', 'get']:
        return _take(data_object, obj1)
    if verb in ['talk', 'talk to']:
        return _talk(data_object, obj1)
    if verb.startswith('use'):
        obj2 = None
        if len(verb.split()) == 3:
            verb, obj2, _ = verb.split()
        return _use(data_object, obj1, obj2)

    data_object.stack.append("Hmm, that didn't work out.")
    return data_object.current_loc


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
    # r = input("Are you sure? ([y]es/[n]o) ").lower()
    # if r.startswith('y'):
    print('Thank you for playing!')
    raise SystemExit


def _print_help(data_object):
    """Prints available commands."""
    print(
        "Available commands: LOOK (AT), GO, TAKE, TALK TO, I[NVENTORY], Q[UIT]")
    print("You can also just enter a direction to go there.")
    return data_object.current_loc


def _print_map(data_object):
    """DEBUG METHOD: Shows the room map."""
    data_object.draw_map()
    return data_object.current_loc


def _show_inventory(data_object):
    """Shows the player's inventory."""
    data_object.stack.append(data_object.inventory.check())
    return data_object.current_loc


def _look(data_object, obj1):
    """Looks at an item or the location."""
    if obj1 is None:
        data_object.current_loc.get_desc()
        data_object.stack.append(data_object.current_loc.description)
        data_object.stack.append(data_object.current_loc.look(data_object))
        return data_object.current_loc

    target_item = data_object.get_item_from_name(obj1)
    if target_item and (data_object.is_in_current_location(target_item) or data_object.is_in_inventory(target_item)):
        data_object.stack.append(target_item.description)
        return data_object.current_loc

    target_npc = data_object.get_npc_from_name(obj1)
    if target_npc and data_object.is_in_current_location(target_npc):
        data_object.stack.append(target_npc.description)
        return data_object.current_loc

    data_object.stack.append(f"There's no {obj1} in sight.")
    return data_object.current_loc


def _take(data_object, obj1):
    """Picks up an item."""
    if obj1 is None:
        data_object.stack.append("What do you want to pick up?")
        return data_object.current_loc
    target_item = data_object.get_item_from_name(obj1)
    if not target_item or not data_object.is_in_current_location(target_item):
        data_object.stack.append("You don't see that anywhere.")
        return data_object.current_loc
    if not target_item.allow_pickup:
        data_object.stack.append("You cannot pick that up.")
        return data_object.current_loc
    data_object.inventory.add(data_object, target_item)
    return data_object.current_loc


def _change_loc(data_object, direction):
    """Invokes a location change."""
    if direction is None:
        data_object.stack.append("Where do you want to go?")
        return data_object.current_loc
    direction = _shorten_direction(direction)
    return data_object.current_loc.move(data_object, direction)


def _talk(data_object, obj1):
    """Talks to an NPC."""
    if obj1 is None:
        data_object.stack.append("Who do you want to talk to?")
        return data_object.current_loc
    target_npc = data_object.get_npc_from_name(obj1)
    if not target_npc or not data_object.is_in_current_location(target_npc):
        data_object.stack.append("There is no one there.")
        return data_object.current_loc
    keyword = input(f"\nWhat will you ask {target_npc.name}?\n> ")
    keyword = unicodedata.normalize("NFKD", keyword.casefold().strip())
    target_npc.trigger_conv(data_object, keyword)
    return data_object.current_loc


def _use(data_object, obj1, obj2):
    """Uses an item, or interacts with something at the location."""
    if obj1 is None and obj2 is None:
        data_object.stack.append("What do you want to use?")
        return data_object.current_loc
    use_item = data_object.get_item_from_name(obj1)
    tool_item = data_object.get_item_from_name(obj2)
    if not use_item or not data_object.is_in_current_location(use_item):
        data_object.stack.append(f"There is no {obj1} here.")
        return data_object.current_loc
    data_object.stack.append(use_item.use(data_object, tool_item))
    return data_object.current_loc
