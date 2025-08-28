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
        self.current_turn = 0
        self._initialize_game_world()
        
    def _get_status(self) -> str:
        """Get the current status string."""
        return f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
    
    def _initialize_game_world(self) -> None:
        """Set up the game world, locations, and initial state.
        
        Follows the exact locations and descriptions from the storyboard.
        """
        # Initialize locations
        self.locations = {
            'maintenance_tunnels': Location(
                name="MAINTENANCE TUNNELS",
                description=(
                    "Flickering lights reveal a sparking droid blocking the east tunnel."
                ),
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
            ),
            'launch_pad': Location(
                name="LAUNCH PAD",
                description=(
                    "The escape pod is ready to launch!"
                )
            )
        }
        
        # Set up initial location connections (east exit from docking bay will be added after crystal pickup)
        self.locations['maintenance_tunnels'].add_exit("east", self.locations['docking_bay'])
        self.locations['docking_bay'].add_exit("west", self.locations['maintenance_tunnels'])
        
        # Add hints
        self.locations['maintenance_tunnels'].hint = "use tool to fix it"
        self.locations['docking_bay'].hint = "Find a way to restore gravity"
        
        # Track if the crystal has been picked up
        self.crystal_picked_up = False
        
        # Initialize player and droid
        self.player = Player(self.locations['maintenance_tunnels'])
        self.droid = DamagedMaintenanceDroid()
    
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
        elif command in ["north", "south", "east", "west"]:
            # For backward compatibility, but this should be removed eventually
            return "Please use 'move <direction>' format.\nExample: 'move east'"
            
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
            
        if command in ["inventory", "i"]:
            return self._show_inventory()
            
        if command == "look":
            return self.player.current_location.describe()
            
        if command == "win":
            return self._process_win()
            
        if command in ["quit", "exit"]:
            self.game_over = True
            return "Thanks for playing!"
            
        return "I don't understand that command. Type 'help' for a list of commands."
    
    def _process_movement(self, direction: str) -> str:
        """Process a movement command."""
        current_location = self.player.current_location
        
        # Check if path is blocked by droid
        if (direction == 'east' and 
            hasattr(current_location, 'droid_present') and 
            current_location.droid_present):
            # Trigger hazard event
            self.player.hazard_count += 1
            return (
                f"The droid SHOVES you back! (+1 HAZARD)\n"
                f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
            )
            
        # Handle movement to Docking Bay from Maintenance Tunnels
        if (direction == 'east' and 
            current_location.name.upper() == 'MAINTENANCE TUNNELS' and 
            not current_location.droid_present):
            # Find the Docking Bay location
            for location in self.locations.values():
                if location.name.upper() == 'DOCKING BAY':
                    self.player.current_location = location
                    return (
                        "You enter the DOCKING BAY.\n"
                        f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
                    )
                    
        # Handle movement to Launch Pad from Docking Bay (only after getting crystal)
        if (direction == 'east' and 
            current_location.name.upper() == 'DOCKING BAY' and
            self.crystal_picked_up):
            # Find the Launch Pad location
            for location in self.locations.values():
                if location.name.upper() == 'LAUNCH PAD':
                    self.player.current_location = location
                    return (
                        "You enter the LAUNCH PAD. The escape pod awaits!\n"
                        "Type 'win' to launch and complete your mission.\n"
                        f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
                    )
                    
        # Handle movement back to Docking Bay
        if (direction == 'west' and 
            current_location.name.upper() == 'LAUNCH PAD'):
            # Find the Docking Bay location
            for location in self.locations.values():
                if location.name.upper() == 'DOCKING BAY':
                    self.player.current_location = location
                    return "You return to the DOCKING BAY."
        
        # Handle movement back to Maintenance Tunnels
        if (direction == 'west' and 
            current_location.name.upper() == 'DOCKING BAY'):
            # Find the Maintenance Tunnels location
            for location in self.locations.values():
                if location.name.upper() == 'MAINTENANCE TUNNELS':
                    self.player.current_location = location
                    return "You return to the MAINTENANCE TUNNELS."
        
        # Handle invalid movement
        if direction in current_location.exits:
            self.player.current_location = current_location.exits[direction]
            return f"You move {direction}."
            
        return "You can't go that way."
    
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
        """Handle picking up the energy crystal."""
        if not hasattr(self.player.current_location, 'has_crystal') or not self.player.current_location.has_crystal:
            return "There's no crystal here to pick up."
            
        self.player.score += 50
        self.player.has_crystal = True
        self.player.current_location.has_crystal = False
        self.crystal_picked_up = True
        
        # Update location description and add exit to launch pad
        self.player.current_location.description = (
            "The escape pod hatch glows green - Almost there"
        )
        self.locations['docking_bay'].add_exit("east", self.locations['launch_pad'])
        self.locations['docking_bay'].hint = "Your exit is wide open!"
        
        return (
            "The crystal vibrates in your palm. You drop to the ground as the gravity resets! [+50]\n"
            f"(SCORE: {self.player.score} | HAZARDS: {self.player.hazard_count})"
        )
    
    def _show_inventory(self) -> str:
        """Get the player's current inventory.
        
        Returns:
            A string listing the items in the player's inventory.
        """
        inventory = self.player.get_inventory()
        if not inventory:
            return "You're not carrying anything."
        return "You are carrying: " + ", ".join(inventory).replace("_", " ").title()
    
    def _show_inventory(self) -> str:
        """Show the player's inventory."""
        items = []
        if self.player.has_tool:
            items.append("Diagnostic Tool")
        if self.player.has_crystal:
            items.append("Energy Crystal")
            
        if not items:
            return "You're not carrying anything."
            
        return "You are carrying: " + ", ".join(items)
    
    def _process_win(self) -> str:
        """Handle the win command."""
        if self.player.current_location.name.upper() != "LAUNCH PAD":
            return "You can't win from here! You need to be at the launch pad."
            
        if not self.player.has_crystal:
            return "You need the energy crystal to power the escape pod!"
            
        self.game_over = True
        self.game_won = True
        return (
            "You place the crystal into the escape pod's power core. "
            "The engines roar to life as the pod's systems come online.\n\n"
            "🚀 MISSION COMPLETE!\n"
            f"FINAL SCORE: {self.player.score + 30} (including 30-point bonus)\n"
            f"HAZARDS ENCOUNTERED: {self.player.hazard_count}\n"
            "\"Orbital Station saved. Well done, Engineer.\""
        )
        
    def _show_help(self) -> str:
        """Return a help message with available commands."""
        help_text = """
Available Commands:
  move <direction> - Move in a direction (north, south, east, or west)
  pick up tool / pickup tool - Pick up the diagnostic tool
  use tool - Use the diagnostic tool on the droid
  pick up crystal / pickup crystal - Pick up the energy crystal
  status - Show your current score and hazard count
  inventory/i - Show items in your inventory
  look - Look around the current location
  help - Show this help message
  quit/exit - Quit the game
"""
        if self.player.current_location.name.upper() == "LAUNCH PAD" and self.player.has_crystal:
            help_text += "  win - Launch the escape pod and win the game!\n"
        return help_text
    
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
