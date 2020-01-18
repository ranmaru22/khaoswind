"""Functions related to the print stack."""

import textwrap as tw

class Stack(object):
    """The main print stack for the game.
    Every round through the main loop, the stack will be emptied and
    everyting that has been stacked will be printed to output in the
    reverse order it has been added. As soon as the stack is empty,
    the game prompts the player for another command.
    """
    
    def __init__(self):
        # Start with an empty stack.
        self.items = list()
                
        # Initialize the TextWrapper object.
        self.wrapper = tw.TextWrapper(width=80)
        
    def append(self, item):
        """Add an item to the stack."""
        self.items.append(item)
        
    def pop(self):
        """Pops the last item off the stack and returns it."""
        last = self.items.pop()
        return last
    
    def print_stack(self):
        """Empties the stack and prints all the items on it."""
        for item in self.items:
            for line in self.wrapper.wrap(item):
                print(line)
            print('\n')
    