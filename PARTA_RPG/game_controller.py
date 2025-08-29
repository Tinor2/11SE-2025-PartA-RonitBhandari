"""
Game Controller module - SPECIFICATION COMPLIANT ONLY.

Contains ONLY the classes, attributes, and methods specified in the requirements.
NO additional features, methods, or functionality.
"""
from player import Player
from location import Location
from droid import DamagedMaintenanceDroid
from items import DiagnosticTool, EnergyCrystal


class GameController:
    """Manages the overall game state and coordinates game components.
    
    Attributes (EXACT SPECIFICATION):
        maintenance_tunnels: The maintenance tunnels location
        docking_bay: The docking bay location  
        droid: The damaged maintenance droid
        player: The player object
        diagnostic_tool: The diagnostic tool item
        energy_crystal: The energy crystal item
    """
    
    def __init__(self):
        """Build the world (all locations, the droid, the two items, and the player)."""
        self.setup_world()
    
    def setup_world(self):
        """Create two Location instances and set up the game world exactly as specified."""
        # Instantiate the droid first
        self.droid = DamagedMaintenanceDroid()
        
        # Create two Location instances
        self.maintenance_tunnels = Location(
            name="Maintenance Tunnels",
            description="Flickering lights reveal a sparking droid blocking the east tunnel.",
            has_tool=True,
            droid_present=True,
            droid=self.droid
        )
        
        self.docking_bay = Location(
            name="Docking Bay", 
            description="Debris floats with no gravity, near a shattered window.",
            has_crystal=True
        )
        
        # Link the two locations
        self.maintenance_tunnels.add_exit("east", self.docking_bay)
        self.docking_bay.add_exit("west", self.maintenance_tunnels)
        
        # Instantiate one DiagnosticTool and one EnergyCrystal
        self.diagnostic_tool = DiagnosticTool()
        self.energy_crystal = EnergyCrystal()
        
        # Instantiate a Player whose starting location is Maintenance Tunnels
        self.player = Player(self.maintenance_tunnels)
        
        # Track last command for win condition
        self.last_command = ""
    
    def start_game(self):
        """Print a welcome message and run the main game loop."""
        print("Welcome to Orbital Station Escape!")
        
        try:
            while True:
                # Show current_location.describe()
                print("\n" + self.player.current_location.describe())
                
                try:
                    # Read a single line of input
                    command = input("\n> ").strip()
                    
                    # Call process_input(command)
                    self.process_input(command)
                    
                    # Call check_win_condition(). If True, break and end.
                    if self.check_win_condition():
                        break
                        
                except KeyboardInterrupt:
                    # Handle Ctrl+C during command input
                    print("\n\nUse 'quit' or 'exit' to leave the game, or 'help' for commands.")
                    
        except KeyboardInterrupt:
            # Handle Ctrl+C during game loop
            print("\n\nThanks for playing!")
            exit(0)
    
    def process_input(self, command):
        """Recognise exactly these commands (case-insensitive) and call appropriate methods."""
        command = command.lower().strip()
        self.last_command = command
        
        # Parse move command
        if command.startswith("move "):
            direction = command[5:].strip()
            result = self.player.move(direction)
            if result == "success":
                print("You moved successfully.")
                self._show_status()
            elif result == "failure - no exit":
                print("You can't go that way.")
                self._show_status()
            elif result == "failure - droid blocking":
                print("The droid blocks your path!")
                self._show_status()
        
        # "pick up tool" → call player.pick_up_tool() and print success or "no tool here."
        elif command == "pick up tool":
            result = self.player.pick_up_tool()
            if result == "success":
                print("Tool picked up successfully.")
            else:
                print("No tool here.")
            self._show_status()
        
        # "use tool" → call player.use_tool_on_droid() and print success or "nothing happens."  
        elif command == "use tool":
            result = self.player.use_tool_on_droid()
            if result == "success":
                print("Tool used successfully.")
            else:
                print("Nothing happens.")
            self._show_status()
        
        # "pick up crystal" → call player.pick_up_crystal() and print success or "no crystal here."
        elif command == "pick up crystal":
            result = self.player.pick_up_crystal()
            if result == "success":
                print("Crystal picked up successfully.")
            else:
                print("No crystal here.")
            self._show_status()
        
        # "status" → call player.get_status() and print "Score: <score> Hazards: <hazard_count>".
        elif command == "status":
            self._show_status()
        
        # "win" – handled in check_win_condition.
        elif command == "win":
            pass
        
        # Help command
        elif command == "help":
            print("\nAvailable commands:")
            print("  move <direction>   - Move in a direction (north, south, east, west)")
            print("  pick up tool      - Pick up the diagnostic tool")
            print("  use tool          - Use the diagnostic tool on the droid")
            print("  pick up crystal   - Pick up the energy crystal")
            print("  status            - Show your current score and hazard count")
            print("  help              - Show this help message")
            print("  quit/exit         - Exit the game\n")
        
        # Quit command
        elif command in ("quit", "exit"):
            print("Thanks for playing!")
            exit(0)
        
        # Anything else → invalid.
        else:
            print("Invalid command. Type 'help' for a list of commands.")
    
    def _show_status(self):
        """Display the player's current status."""
        print(f"\nStatus: {self.player.get_status()}")
    
    def check_win_condition(self):
        """Check if player has won and add 30 points if so."""
        # If all of these are true:
        # - player.current_location is Docking Bay
        # - player.has_crystal is True  
        # - the last command was "win"
        if (self.player.current_location == self.docking_bay and
            self.player.has_crystal and 
            self.last_command == "win"):
            
            # Then add 30 to player.score
            self.player.score += 30
            
            # Print mission complete message
            print(f"Mission complete! Final Score: {self.player.score} Total Hazards: {self.player.hazard_count}")
            
            return True
        
        return False