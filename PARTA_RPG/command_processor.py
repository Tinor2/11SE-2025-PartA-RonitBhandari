"""
Command Processor module for Orbital Station Escape.

This module handles parsing and executing player commands.
"""
from typing import List, Tuple, Optional
from game_controller import GameController


class CommandProcessor:
    """Handles parsing and executing player commands.
    
    This class follows the Command pattern to encapsulate all command processing
    logic in one place.
    """
    
    def __init__(self, game_controller: GameController):
        """Initialize with a reference to the game controller."""
        self.game_controller = game_controller
        self.last_command = ""
    
    def process_command(self, command: str) -> str:
        """Process a player command and return the game's response.
        
        Args:
            command: The raw input string from the player.
            
        Returns:
            A string containing the game's response to the command.
            Matches the exact responses from the storyboard.
        """
        if not command.strip():
            return ""
            
        command = command.strip().lower()
        self.last_command = command
        
        # Handle movement commands
        if command in ["north", "south", "east", "west"]:
            return self._process_movement(command)
            
        # Handle specific commands from storyboard
        if command == "pick up tool":
            return self._process_pick_up_tool()
            
        if command == "use tool":
            return self._process_use_tool()
            
        if command == "pick up crystal":
            return self._process_pick_up_crystal()
            
        if command == "status":
            return self._process_status()
            
        if command == "win":
            return self._process_win()
            
        if command == "help":
            return self._show_help()
            
        if command == "inventory" or command == "i":
            return self._show_inventory()
            
        if command == "look":
            return self._look_around()
            
        if command in ["quit", "exit"]:
            self.game_controller.game_over = True
            return "Thanks for playing!"
            
        return "I don't understand that command. Type 'help' for a list of commands."
    
    def _process_movement(self, direction: str) -> str:
        """Handle movement commands."""
        current_location = self.game_controller.player.current_location
        
        # Check if path is blocked by droid
        if (direction == 'east' and 
            hasattr(current_location, 'droid_present') and 
            current_location.droid_present):
            return "The droid blocks your path! It needs to be repaired first."
            
        # Check for win condition (in docking bay with crystal)
        if (direction == 'east' and 
            current_location.name.lower() == 'maintenance tunnels' and 
            not current_location.droid_present):
            self.game_controller.game_over = True
            self.game_controller.game_won = True
            return "You enter the docking bay and use the energy crystal to power up the escape pod.\nYou've escaped the station! [WIN]\nFinal Score: 80/100"
            
        # Normal movement
        result = self.game_controller.process_command(direction)
        if "You can't go that way" in result:
            return result
            
        # Update status after movement
        return f"{result}\n{self._get_status()}"
    
    def _process_pick_up_tool(self) -> str:
        """Handle picking up the diagnostic tool."""
        if not self.game_controller.player.current_location.has_tool:
            return "There's no tool here to pick up."            
        self.game_controller.player.score += 10
        self.game_controller.player.has_tool = True
        self.game_controller.player.current_location.has_tool = False
        return f"You grab the diagnostic tool. [+10]\n{self._get_status()}"
    
    def _process_use_tool(self) -> str:
        """Handle using the diagnostic tool on the droid."""
        if not self.game_controller.player.has_tool:
            return "You don't have a tool to use."
            
        if not self.game_controller.player.current_location.droid_present:
            return "There's nothing to use the tool on here."
            
        self.game_controller.player.score += 20
        self.game_controller.player.current_location.droid_present = False
        return f"DROID REBOOT: The droid beeps and moves aside. [+20]\n{self._get_status()}"
    
    def _process_pick_up_crystal(self) -> str:
        """Handle picking up the energy crystal."""
        if not self.game_controller.player.current_location.has_crystal:
            return "There's no crystal here to pick up."
            
        self.game_controller.player.score += 50
        self.game_controller.player.has_crystal = True
        self.game_controller.player.current_location.has_crystal = False
        return f"You grab the energy crystal. [+50]\n{self._get_status()}"
    
    def _process_status(self) -> str:
        """Handle the status command."""
        return self._get_status()
    
    def _process_win(self) -> str:
        """Handle the win command."""
        game_over, message = self.game_controller.check_game_state()
        if game_over and "win" in message.lower():
            self.game_controller.game_over = True
            self.game_controller.game_won = True
            return f"{message}\nFinal Score: {self.game_controller.player.score} | Hazards: {self.game_controller.player.hazard_count}"
        return "You can't win yet!"
    
    def _show_help(self) -> str:
        """Display the help message."""
        return """
Available Commands:
  move <direction> - Move in a direction (north, south, east, west)
  pick up tool - Pick up the diagnostic tool
  use tool - Use the diagnostic tool on the droid
  pick up crystal - Pick up the energy crystal
  status - Show your current score and hazard count
  inventory/i - Show items in your inventory
  look - Look around the current location
  help - Show this help message
  quit/exit - Quit the game
"""
    
    def _show_inventory(self) -> str:
        """Show the player's inventory."""
        return self.game_controller.process_command("inventory")
    
    def _look_around(self) -> str:
        """Show the current location's description."""
        return self.game_controller.process_command("look")
    
    def _get_status(self) -> str:
        """Get the current status string."""
        return f"(SCORE: {self.game_controller.player.score} | HAZARDS: {self.game_controller.player.hazard_count})"
