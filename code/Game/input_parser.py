from typing import Optional, Tuple, Dict, Any, Type
from commands import Command, MoveCommand, LookCommand, PickupCommand, UseCommand, InventoryCommand, HelpCommand, QuitCommand

class InputParser:
    """Handles parsing of user input into game commands."""
    
    def __init__(self):
        # Command help text
        self.command_help = {
            "north/south/east/west": "Move in the specified direction",
            "look [item]": "Look around or examine an item",
            "take <item>": "Pick up an item",
            "use <item>": "Use an item from your inventory",
            "inventory": "Check your inventory",
            "help": "Show this help message",
            "quit": "Quit the game"
        }
        
        # Command mappings
        self.commands: Dict[str, Type[Command]] = {
            # Movement commands
            'north': MoveCommand,
            'south': MoveCommand,
            'east': MoveCommand,
            'west': MoveCommand,
            'go': MoveCommand,
            'move': MoveCommand,
            
            # Interaction commands
            'look': LookCommand,
            'examine': LookCommand,
            'take': PickupCommand,
            'pickup': PickupCommand,
            'get': PickupCommand,
            'use': UseCommand,
            'inventory': InventoryCommand,
            'inv': InventoryCommand,
            'i': InventoryCommand,
            'help': HelpCommand,
            '?': HelpCommand,
            'quit': QuitCommand,
            'exit': QuitCommand,
            'q': QuitCommand
        }
        
        # Initialize commands that need special parameters
        self.initialized_commands = {
            'help': HelpCommand(self.command_help),
            '?': HelpCommand(self.command_help)
        }
    
    def parse(self, input_str: str) -> Tuple[Optional[Command], list]:
        """Parse a string input into a command and arguments.
        
        Args:
            input_str: The raw input string from the user
            
        Returns:
            Tuple of (command_instance, args_list)
        """
        if not input_str:
            return None, []
            
        # Split input into parts
        parts = input_str.lower().strip().split()
        if not parts:
            return None, []
            
        # Check for single-word direction commands (e.g., 'north' instead of 'go north')
        if parts[0] in ['north', 'south', 'east', 'west']:
            cmd_class = self.commands[parts[0]]
            return cmd_class(), parts[0:1]  # Return the direction as an argument
            
        # Handle multi-word commands
        verb = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Check if it's a known command
        if verb in self.commands:
            # Check if it's a pre-initialized command
            if verb in self.initialized_commands:
                return self.initialized_commands[verb], args
            # Otherwise create a new instance
            return self.commands[verb](), args
            
        return None, []
