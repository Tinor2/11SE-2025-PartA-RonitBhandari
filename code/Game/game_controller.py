from location import Location, DamagedMaintenanceDroid
from items import DiagnosticTool, EnergyCrystal
from player import Player

class GameController:
    """Controls the main game loop and manages game state."""
    def __init__(self):
        self.setup_world()
    
    def setup_world(self):
        """Set up the game world with locations, items, and the player."""
        # Create locations
        self.maintenance_tunnels = Location(
            "Maintenance Tunnels",
            "Dark, cramped tunnels filled with flickering lights and the hum of machinery."
        )
        self.docking_bay = Location(
            "Docking Bay",
            "A large open area with a view of space through a massive window. Debris floats in zero-g."
        )
        
        # Set up exits
        self.maintenance_tunnels.add_exit("east", self.docking_bay)
        self.docking_bay.add_exit("west", self.maintenance_tunnels)
        
        # Place items
        self.maintenance_tunnels.has_tool = True
        self.docking_bay.has_crystal = True
        
        # Create and place droid
        self.droid = DamagedMaintenanceDroid()
        self.maintenance_tunnels.droid_present = True
        self.maintenance_tunnels.droid = self.droid  # Reference to the droid
        
        # Create player
        self.player = Player(self.maintenance_tunnels)
        
        # Create items (though mostly handled through location flags)
        self.diagnostic_tool = DiagnosticTool()
        self.energy_crystal = EnergyCrystal()
    
    def start_game(self):
        """Start the main game loop."""
        print("=== ORBITAL STATION ESCAPE ===")
        print("Type 'help' for a list of commands.\n")
        
        while True:
            # Display current location
            print(self.player.current_location.describe())
            
            # Get player input
            command = input("> ").strip().lower()
            
            # Process command
            if command == "quit":
                print("Thanks for playing!")
                break
                
            if self.process_input(command):
                # Check win condition after each command
                if self.check_win_condition():
                    break
    
    def process_input(self, command):
        """Process a player command."""
        if command == "help":
            print("\nAvailable commands:")
            print("  move <direction> - Move in a direction (e.g., 'move east')")
            print("  pick up tool - Pick up the diagnostic tool")
            print("  use tool - Use the tool on the droid")
            print("  pick up crystal - Pick up the energy crystal")
            print("  status - Show your current score and hazards")
            print("  win - Complete the mission (only in Docking Bay with crystal)")
            print("  quit - Exit the game\n")
            return False
            
        elif command.startswith("move "):
            direction = command[5:].strip()
            success, message = self.player.move(direction)
            print(message)
            return success
            
        elif command == "pick up tool":
            success, message = self.player.pick_up_tool()
            print(message)
            return success
            
        elif command == "use tool":
            success, message = self.player.use_tool_on_droid(self.droid)
            if success:
                self.maintenance_tunnels.set_droid_present(False)
            print(message)
            return success
            
        elif command == "pick up crystal":
            success, message = self.player.pick_up_crystal()
            print(message)
            return success
            
        elif command == "status":
            print(self.player.get_status())
            return False
            
        elif command == "win":
            return self.check_win_condition()
            
        else:
            print("Invalid command. Type 'help' for a list of commands.")
            return False
    
    def check_win_condition(self):
        """Check if the player has won the game."""
        if (self.player.current_location == self.docking_bay and 
            self.player.has_crystal and 
            not self.docking_bay.droid_present):
            
            self.player.score += 30  # Bonus points for winning
            print("\n" + "="*50)
            print("MISSION COMPLETE!")
            print(f"Final Score: {self.player.score}")
            print(f"Total Hazards: {self.player.hazard_count}")
            print("Thanks for playing!")
            print("="*50 + "\n")
            return True
        
        print("You can't do that here.")
        return False


def main():
    """Entry point for the game."""
    game = GameController()
    game.start_game()

if __name__ == "__main__":
    main()
