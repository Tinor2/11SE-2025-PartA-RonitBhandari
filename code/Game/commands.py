from typing import Optional, Tuple, List, Dict, Any
from player import Player

class Command:
    """Base command class that all commands inherit from."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        """Execute the command.
        
        Args:
            player: The player executing the command
            *args: Arguments for the command
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        raise NotImplementedError("Subclasses must implement execute()")

class MoveCommand(Command):
    """Command to move the player in a direction."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        if not args:
            return False, "Please specify a direction (north, south, east, west)."
        return player.move(args[0])

class LookCommand(Command):
    """Command to look around the current location or examine an object."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        if not args:
            return True, player.current_location.describe()
        # TODO: Implement examining specific objects
        return False, f"You don't see a {args[0]} here."

class PickupCommand(Command):
    """Command to pick up an item."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        if not args:
            return False, "Please specify an item to pick up."
        return player.pick_up(' '.join(args))

class UseCommand(Command):
    """Command to use an item."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        if not args:
            return False, "Please specify an item to use."
        return player.use(' '.join(args))

class InventoryCommand(Command):
    """Command to show player's inventory."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        return player.check_inventory()

class HelpCommand(Command):
    """Command to show help information."""
    def __init__(self, command_help: Dict[str, str]):
        self.command_help = command_help
    
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        help_text = ["Available commands:"]
        for cmd, desc in self.command_help.items():
            help_text.append(f"  {cmd}: {desc}")
        return True, "\n".join(help_text)

class QuitCommand(Command):
    """Command to quit the game."""
    def execute(self, player: 'Player', *args: List[str]) -> Tuple[bool, str]:
        return False, "Thanks for playing!"
