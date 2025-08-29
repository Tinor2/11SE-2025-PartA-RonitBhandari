"""
Game Controller module for Orbital Station Escape.

This module manages the overall game state and handles all game commands.
"""
from typing import Dict, Tuple, Optional, List
from player import Player
from location import Location
from droid import DamagedMaintenanceDroid


class GameController:
    """Manages the overall game state and coordinates game components.
    
    This class is responsible for initializing the game world, tracking the
    game state, and processing player commands.
    """
    
    def __init__(self):
        """Initialize the game controller and set up the initial game state."""
        self.game_over = False
        self.game_won = False
        self._initialize_game_world()
        
    def _get_status(self) -> str:
        """Get the current status string."""
        return f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
    
    def _initialize_game_world(self) -> None:
        """Set up the game world, locations, and initial state.
        
        Follows the exact locations and descriptions from the storyboard.
        """
        # Initialize ONLY the two specified locations
        self.locations = {
            'maintenance_tunnels': Location(
                name="MAINTENANCE TUNNELS",
                description="Flickering lights reveal a sparking droid blocking the east tunnel.",
                has_tool=True,
                droid_present=True
            ),
            'docking_bay': Location(
                name="DOCKING BAY",
                description=(
                    "Debris floats with no gravity, near a shattered window.\n"
                    "The escape pod's hatch is lodged shut, thanks to the broken gravity generators."
                ),
                has_crystal=True
            )
        }
        
        # Set up bidirectional exits
        self.locations['maintenance_tunnels'].add_exit("east", self.locations['docking_bay'])
        self.locations['docking_bay'].add_exit("west", self.locations['maintenance_tunnels'])
        
        # Initialize player and droid
        self.player = Player(self.locations['maintenance_tunnels'])
        self.droid = DamagedMaintenanceDroid()

        # Track crystal state for help display
        self.crystal_picked = False
    
    def process_command(self, command: str) -> str:
        """Process a player command and return the game's response.
        
        Args:
            command: The raw input string from the player.
            
        Returns:
            A string containing the game's response to the command.
        """
        if not command.strip():
            return ""
            
        command = command.strip().lower()
        parts = command.split()
        
        # Handle movement commands
        if len(parts) == 2 and parts[0] == 'move' and parts[1] in ["north", "south", "east", "west"]:
            return self._process_movement(parts[1])
            
        # Handle specific commands
        if command == "pick up tool" or command == "pickup tool":
            return self._process_pick_up_tool()
            
        if command == "use tool":
            return self._process_use_tool()
            
        if command == "pick up crystal" or command == "pickup crystal":
            return self._process_pick_up_crystal()
            
        if command == "status":
            return self._get_status()

        if command == "help":
            return self._show_help()

        if command == "win":
            return self._process_win()
            
        if command in ["quit", "exit"]:
            self.game_over = True
            return "Thanks for playing!"
            
        return "I don't understand that command. Type 'help' for a list of commands."
    
    def _process_movement(self, direction: str) -> str:
        """Delegate movement handling to the Player class."""
        return self.player.move(direction)
    
    def _process_pick_up_tool(self) -> str:
        """Handle picking up the diagnostic tool."""
        if not self.player.current_location.has_tool:
            return "There's no tool here to pick up."            
        self.player.score += 10
        self.player.has_tool = True
        self.player.current_location.has_tool = False
        return f"You grab the diagnostic tool. [+10]\n{self._get_status()}"
    
    def _process_use_tool(self) -> str:
        """Handle using the diagnostic tool on the droid."""
        if not self.player.has_tool:
            return "You don't have a tool to use."
            
        current_location = self.player.current_location
        if not hasattr(current_location, 'droid_present') or not current_location.droid_present:
            return "There's nothing to use the tool on here."
            
        # Update droid status and location description
        current_location.droid_present = False
        self.player.score += 20
        
        # Update the location's description to remove the droid
        current_location.description = (
            "The corridor to the Docking Bay is now clear."
        )
        
        return (
            "Droid reboots! It salutes and shuffles aside. [+20]\n"
            f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
        )
        
    def _process_pick_up_crystal(self) -> str:
        """Handle picking up the energy crystal using Player method."""
        self.crystal_picked = True
        # Update Docking Bay description to signal mission completion possibility
        self.player.current_location.description = (
            "The escape pod hatch slides open, ready for launch. Type 'win' to escape!"
        )
        return self.player.pick_up_crystal() + "\n(The escape pod is now ready. Type 'win' to complete your mission!)"
    
    def _process_win(self) -> str:
        """Handle the win command when in Docking Bay with crystal."""
        if self.player.current_location.name.upper() != "DOCKING BAY":
            return "You can't win from here! You need to be at the Docking Bay."
        if not self.player.has_crystal:
            return "You need the energy crystal to power the escape pod!"
        self.game_over = True
        self.game_won = True
        self.player.score += 30  # mission completion bonus
        return (
            " MISSION COMPLETE!\n"
            f"FINAL SCORE: {self.player.score}\n"
            f"HAZARDS ENCOUNTERED: {self.player.hazard_count}\n"
            "\"Orbital Station saved. Well done, Engineer.\""
        )
        
    def _show_help(self) -> str:
        """Return a help message with available commands."""
        base = (
            "Available Commands:\n"
            "  move <direction> - Move north, south, east, or west\n"
            "  pick up tool / pickup tool - Pick up the diagnostic tool\n"
            "  use tool - Use the diagnostic tool on the droid\n"
            "  pick up crystal / pickup crystal - Pick up the energy crystal\n"
            "  status - Show score and hazards\n"
        )
        if self.crystal_picked:
            base += "  win - Complete the mission\n"
        base += "  quit/exit - Quit the game\n"
        return base
    
    def check_game_state(self) -> Tuple[bool, str]:
        """Check if the game has been won or lost.
        
        Returns:
            A tuple of (game_over, message) where game_over is a boolean
            indicating if the game has ended, and message is a string
            describing the end game state.
        """
        if self.player.hazards_encountered >= 3:
            return (True, "TOO MANY HAZARDS! The station's systems fail catastrophically.\nGAME OVER!")
            
        if (self.player.current_location.name.lower() == "docking bay" and 
            "energy_crystal" in self.player.inventory):
            return (True, "You place the crystal in the escape pod and blast off!\nYOU ESCAPED!")
            
        return (False, "")
