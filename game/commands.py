"""
Command pattern implementation for handling player actions in the game.
"""
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, List
from dataclasses import dataclass

from utils import get_text

@dataclass
class CommandResult:
    """Container for command execution results."""
    success: bool
    message: str
    score_change: int = 0
    end_game: bool = False

class Command(ABC):
    """Abstract base class for all game commands."""
    
    @abstractmethod
    def execute(self, player, *args) -> CommandResult:
        """Execute the command and return the result."""
        pass
    
    @abstractmethod
    def get_help_text(self) -> str:
        """Return help text for this command."""
        pass

class MoveCommand(Command):
    """Command for moving between locations."""
    
    def execute(self, player, direction: str = None) -> CommandResult:
        if not direction:
            return CommandResult(False, get_text('ui.move_where'))
            
        result = player.move(direction)
        return CommandResult(
            success=not result.startswith(get_text('ui.no_exit')),
            message=result
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_move')

class TakeCommand(Command):
    """Command for picking up items."""
    
    def execute(self, player, item_name: str = None) -> CommandResult:
        if not item_name:
            return CommandResult(False, get_text('ui.take_what'))
            
        result = player.take_item(item_name)
        score_change = 10 if "tool" in item_name.lower() else 15 if "crystal" in item_name.lower() else 0
        return CommandResult(
            success=not result.startswith(get_text('ui.item_not_here')),
            message=result,
            score_change=score_change if not result.startswith(get_text('ui.item_not_here')) else 0
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_take')

class UseCommand(Command):
    """Command for using items."""
    
    def execute(self, player, item_name: str = None) -> CommandResult:
        if not item_name:
            return CommandResult(False, get_text('ui.use_what'))
            
        result = player.use_item(item_name)
        score_change = 20 if "droid" in result else 0
        return CommandResult(
            success=not result.startswith(get_text('ui.cant_use_item').split('{')[0]) and 
                   not result.startswith(get_text('game.nothing_to_repair')),
            message=result,
            score_change=score_change
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_use')

class ExamineCommand(Command):
    """Command for examining items or the current location."""
    
    def execute(self, player, target: str = None) -> CommandResult:
        if not target:
            return CommandResult(
                success=True,
                message=player.current_location.describe()
            )
            
        # Check inventory first
        item = player.get_item(target)
        if item:
            return CommandResult(
                success=True,
                message=item.examine()
            )
            
        # Check location items
        if ("tool" in target.lower() and player.current_location.has_tool) or \
           ("crystal" in target.lower() and player.current_location.has_crystal):
            item_type = "diagnostic tool" if "tool" in target.lower() else "energy crystal"
            return CommandResult(
                success=True,
                message=get_text('ui.item_seen', item=item_type)
            )
            
        return CommandResult(
            success=False,
            message=get_text('ui.item_not_seen', item=target)
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_examine')

class InventoryCommand(Command):
    """Command for viewing inventory."""
    
    def execute(self, player, *args) -> CommandResult:
        items = player.get_inventory()
        if not items:
            return CommandResult(
                success=True,
                message=get_text('ui.inventory_empty')
            )
            
        return CommandResult(
            success=True,
            message=get_text('ui.inventory_items', items=", ".join(items))
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_inventory')

class HelpCommand(Command):
    """Command for displaying help information."""
    
    def __init__(self, command_registry: 'CommandRegistry'):
        self.command_registry = command_registry
    
    def execute(self, player, *args) -> CommandResult:
        help_text = [get_text('ui.help_header')]
        for name, cmd in self.command_registry.commands.items():
            help_text.append(f"{name}: {cmd.get_help_text()}")
        return CommandResult(
            success=True,
            message="\n".join(help_text)
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_help')

class QuitCommand(Command):
    """Command for quitting the game."""
    
    def execute(self, player, *args) -> CommandResult:
        return CommandResult(
            success=True,
            message=get_text('ui.goodbye'),
            end_game=True
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_quit')


class WinCommand(Command):
    """Command for winning the game."""
    
    def execute(self, player, *args) -> CommandResult:
        # Check if player is in the escape pod with the crystal
        if (hasattr(player.location, 'is_escape_pod') and 
            player.location.is_escape_pod and
            any(isinstance(item, EnergyCrystal) for item in player.inventory)):
            return CommandResult(
                success=True,
                message=get_text('ui.you_win').format(score=player.score + 100),  # Bonus points for winning
                score_change=100,
                end_game=True
            )
        return CommandResult(
            success=False,
            message=get_text('ui.cant_win_yet')
        )
    
    def get_help_text(self) -> str:
        return get_text('ui.help_win')

class CommandRegistry:
    """Manages available commands and their execution."""
    
    def __init__(self):
        # Initialize all commands
        self.commands: Dict[str, Command] = {
            'go': MoveCommand(),
            'take': TakeCommand(),
            'use': UseCommand(),
            'examine': ExamineCommand(),
            'inventory': InventoryCommand(),
            'help': HelpCommand(self),
            'quit': QuitCommand(),
            'win': WinCommand()
        }
        
        # Add movement aliases
        self.commands['north'] = self.commands['go']
        self.commands['south'] = self.commands['go']
        self.commands['east'] = self.commands['go']
        self.commands['west'] = self.commands['go']
        
        # Add other aliases
        self.commands['get'] = self.commands['take']
        self.commands['look'] = self.commands['examine']
        self.commands['exit'] = self.commands['quit']
        self.commands['q'] = self.commands['quit']
        self.commands['h'] = self.commands['help']
        self.commands['i'] = self.commands['inventory']
        self.commands['l'] = self.commands['look']
    
    def execute_command(self, command_str: str, player) -> CommandResult:
        """Parse and execute a command string."""
        parts = command_str.lower().split()
        if not parts:
            return CommandResult(False, get_text('ui.enter_command'))
            
        cmd_name = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd_name not in self.commands:
            return CommandResult(
                False, 
                get_text('ui.unknown_command', command=cmd_name)
            )
            
        # Special case for movement commands
        if cmd_name in ['north', 'south', 'east', 'west']:
            return self.commands[cmd_name].execute(player, cmd_name)
            
        # Execute the command with any provided arguments
        return self.commands[cmd_name].execute(player, *args)


def test_commands() -> None:
    """
    Test function to verify that the command system works as expected.
    This function runs only when commands.py is executed directly.
    """
    try:
        from .locations import Location
        from .player import Player
    except ImportError:
        from locations import Location
        from player import Player
    
    print("\n" + "="*50)
    print("TESTING COMMAND SYSTEM")
    print("="*50)
    
    # Set up test environment
    room1 = Location("Test Room", "A test room with various items.")
    room1.has_tool = True
    player = Player(room1)
    registry = CommandRegistry()
    
    def run_test(test_name: str, command: str, expected_contains: str = None) -> CommandResult:
        print(f"\n[TEST] {test_name}")
        print(f"  Command: {command}")
        result = registry.execute_command(command, player)
        print(f"  Result: {result.message}")
        if expected_contains and expected_contains not in result.message:
            print(f"  [WARNING] Expected to contain: {expected_contains}")
        return result
    
    # Test help command
    result = run_test("Help Command", "help")
    
    # Test move command
    result = run_test("Move Command - Invalid Direction", "go north", "can't go that way")
    
    # Test examine command
    result = run_test("Examine Command", "examine", "Test Room")
    
    # Test take command
    result = run_test("Take Command - Valid Item", "take tool", "You take the diagnostic tool")
    
    # Test inventory command
    result = run_test("Inventory Command", "inventory", "You are carrying: Diagnostic Tool")
    
    # Test use command
    result = run_test("Use Command - Invalid Item", "use crystal", "don't have")
    
    # Test quit command
    result = run_test("Quit Command", "quit", "Thanks for playing")
    print(f"  End game flag: {result.end_game} (expected: True)")
    
    print("\n" + "="*50)
    print("ALL TESTS COMPLETED")
    print("="*50)


if __name__ == "__main__":
    # This block will only execute when commands.py is run directly
    test_commands()
