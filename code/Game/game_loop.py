"""
Main game loop for the Orbital Station Escape game.
Handles the game state, player input, and game flow.
"""
import json
import os
from typing import Dict, Any, Optional

from location import Location
from player import Player
from damaged_droid import DamagedMaintenanceDroid

class Game:
    """Main game class that manages the game state and loop."""
    
    def __init__(self):
        """Initialize the game with all necessary components."""
        self.game_active = False
        self.messages = self._load_messages()
        self.locations: Dict[str, Location] = {}
        self.player: Optional[Player] = None
        self._setup_game()
    
    def _load_messages(self) -> Dict[str, Any]:
        """Load game messages from JSON file."""
        try:
            with open('game_messages.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: game_messages.json not found. Using default messages.")
            return {}
    
    def _setup_game(self):
        """Set up the initial game state."""
        # Initialize locations with descriptions from game_messages.json or defaults
        maintenance_desc = self.messages.get("locations", {}).get("maintenance_tunnels", {}).get(
            "initial_description",
            "Flickering lights reveal a sparking droid blocking the east tunnel."
        )
        
        docking_bay_desc = self.messages.get("locations", {}).get("docking_bay", {}).get(
            "initial_description",
            "Debris floats with no gravity, near a shattered window. An energy crystal is lodged in the wall."
        )
        
        # Create locations
        maintenance_tunnels = Location("MAINTENANCE TUNNELS", maintenance_desc)
        docking_bay = Location("DOCKING BAY", docking_bay_desc)
        
        # Set up items in locations
        maintenance_tunnels.has_tool = True
        docking_bay.has_crystal = True  # Add energy crystal to docking bay
        
        # Create and configure the droid
        droid = DamagedMaintenanceDroid()
        maintenance_tunnels.droid = droid
        maintenance_tunnels.droid_present = True
        
        # Set up location connections
        # The droid blocks the east exit from maintenance tunnels
        maintenance_tunnels.add_exit("east", docking_bay)
        # No droid blocking the return path
        docking_bay.add_exit("west", maintenance_tunnels)
        
        # Store locations for reference
        self.locations = {
            "maintenance_tunnels": maintenance_tunnels,
            "docking_bay": docking_bay
        }
        
        # Initialize player in the maintenance tunnels
        self.player = Player(maintenance_tunnels)
        self.player.score = 0  # Ensure score is initialized
        self.player.hazard_count = 0  # Reset hazard count
    
    def _display_location(self):
        """Display the current location and its description."""
        if not self.player or not self.player.current_location:
            return
            
        location = self.player.current_location
        print(f"\n=== {location.name} ===")
        
        # Get the location description
        description = location.describe()
        if description:
            print(description)
        
        # Show available exits
        if location.exits:
            exits = ", ".join(direction for direction in location.exits.keys())
            print(f"\nExits: {exits}")
    
    def _process_command(self, command: str) -> bool:
        """Process a player command."""
        if not self.player or not self.player.current_location:
            return True
            
        command = command.lower().strip()
        current_loc = self.player.current_location
        
        # Handle movement
        if command in ["north", "south", "east", "west"]:
            # Check if the exit is blocked by a droid
            target_loc = current_loc.exits.get(command)
            if target_loc and hasattr(target_loc, 'droid_present') and target_loc.droid_present and target_loc.droid:
                if target_loc.droid.is_blocking():
                    self.player.hazard_count += 1
                    print(f"The droid blocks your path! (Hazards: {self.player.hazard_count})")
                    return True
            
            success, message = self.player.move(command)
            print(message)
            return True
            
        # Handle item interactions
        elif command in ["get tool", "take tool"]:
            if not self.player.has_tool and hasattr(current_loc, 'has_tool') and current_loc.has_tool:
                success, message = self.player.pick_up_tool()
                if success:
                    current_loc.has_tool = False
                    print(message)
                return True
            print("There's no tool to take here.")
            return True
            
        # Handle crystal pickup
        elif command in ["get crystal", "take crystal"]:
            if not self.player.has_crystal and hasattr(current_loc, 'has_crystal') and current_loc.has_crystal:
                self.player.has_crystal = True
                current_loc.has_crystal = False
                print("You carefully extract the energy crystal. The gravity suddenly restores!")
                # Update docking bay description
                if current_loc.name == "DOCKING BAY":
                    current_loc.description = self.messages.get("locations", {}).get("docking_bay", {}).get(
                        "after_gravity_restore",
                        "The escape pod hatch glows green - Almost there."
                    )
                return True
            print("There's no crystal to take here.")
            return True
                
        # Handle droid repair
        elif command in ["use tool on droid", "fix droid"]:
            if not self.player.has_tool:
                print("You don't have a tool to use!")
                return True
                
            if not (hasattr(current_loc, 'droid_present') and 
                   current_loc.droid_present and 
                   current_loc.droid):
                print("There's no droid here to fix!")
                return True
                
            success, message = self.player.use_tool_on_droid()
            print(message)
            
            # If successful, update the location description
            if success and current_loc.name == "MAINTENANCE TUNNELS":
                current_loc.description = self.messages.get("locations", {}).get("maintenance_tunnels", {}).get(
                    "after_droid_fix",
                    "The corridor to the Docking Bay is now clear."
                )
            return True
            
        # Game state commands
        elif command == "look":
            self._display_location()
            return True
            
        elif command == "inventory" or command == "i":
            print("\n=== INVENTORY ===")
            if self.player.has_tool:
                print("- Diagnostic Tool")
            if self.player.has_crystal:
                print("- Energy Crystal")
            if not self.player.has_tool and not self.player.has_crystal:
                print("You're not carrying anything.")
            return True
            
        elif command == "score":
            print(f"\nScore: {self.player.score}")
            print(f"Hazards: {self.player.hazard_count}/10")
            return True
            
        elif command == "help" or command == "?":
            self._show_help()
            return True
            
        elif command == "quit" or command == "exit":
            print("Thanks for playing!")
            return False
            
        else:
            print("I don't understand that command. Type 'help' for a list of commands.")
            return True
    
    def _show_help(self):
        """Display the help menu."""
        print("\n=== HELP ===")
        print("Commands:")
        print("- north/south/east/west: Move in that direction")
        print("- get/take tool: Pick up the diagnostic tool")
        print("- get/take crystal: Pick up the energy crystal (in Docking Bay)")
        print("- use tool on droid/fix droid: Use the tool on a droid")
        print("- look: Look around the current location")
        print("- inventory/i: Check your inventory")
        print("- score: Check your score and hazards")
        print("- help/?: Show this help")
        print("- quit/exit: Quit the game")
    
    def _check_game_state(self) -> bool:
        """Check if the game should end."""
        if not self.player:
            return False
            
        # Check win condition: Player is in docking bay with crystal and no droid blocking
        if (hasattr(self.player, 'current_location') and 
            self.player.current_location and 
            self.player.current_location.name == "DOCKING BAY" and 
            hasattr(self.player, 'has_crystal') and 
            self.player.has_crystal):
            print("\n=== YOU WIN! ===")
            print("You've successfully restored power and escaped the station!")
            print(f"Final Score: {getattr(self.player, 'score', 0)}")
            return False
            
        # Check lose condition: Too many hazards
        if hasattr(self.player, 'hazard_count') and self.player.hazard_count >= 10:
            print("\n=== GAME OVER ===")
            print("You've encountered too many hazards and have been overwhelmed!")
            return False
            
        return True
    
    def run(self):
        """Run the main game loop."""
        print("\n=== ORBITAL STATION ESCAPE ===")
        print("Type 'help' for a list of commands.\n")
        
        self.game_active = True
        self._display_location()
        
        while self.game_active:
            if not self._check_game_state():
                break
                
            try:
                command = input("\n> ").strip()
                self.game_active = self._process_command(command)
            except (EOFError, KeyboardInterrupt):
                print("\nGame interrupted. Type 'quit' to exit.")
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                self.game_active = False


if __name__ == "__main__":
    game = Game()
    game.run()
