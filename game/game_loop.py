"""
Main game loop for Orbital Station Escape.
Handles the core game mechanics and flow.
"""
from typing import Dict, Any
from player import Player
from locations import Location
from commands import CommandRegistry
from items import DiagnosticTool, EnergyCrystal
from utils import get_text

class GameState:
    """Manages the current state of the game."""
    
    def __init__(self):
        self.game_over = False
        self.player_won = False
        self.score = 0
        self.hazards = 0
        self.player = None
        self.current_location = None
        self.locations: Dict[str, Location] = {}
        self.command_registry = None

    def update_score(self, points: int):
        """Update the player's score."""
        self.score += points
        return f"Score updated: {self.score}"

    def add_hazard(self):
        """Increment the hazard counter."""
        self.hazards += 1
        return f"Hazards encountered: {self.hazards}"


def initialize_game() -> GameState:
    """Initialize the game state and set up the game world."""
    state = GameState()
    
    # Create locations
    maintenance_tunnels = Location("Maintenance Tunnels", get_text('locations.maintenance_tunnels'))
    docking_bay = Location("Docking Bay", get_text('locations.docking_bay'))
    
    # Set up exits
    maintenance_tunnels.add_exit("east", docking_bay)
    docking_bay.add_exit("west", maintenance_tunnels)
    
    # Add items and obstacles
    maintenance_tunnels.add_item('tool')  # Add diagnostic tool
    maintenance_tunnels.add_item('droid')  # Add broken droid
    
    # Set initial state
    state.current_location = maintenance_tunnels
    state.player = Player(maintenance_tunnels)
    
    # Initialize command registry
    state.command_registry = CommandRegistry()
    
    return state


def display_location(state: GameState) -> str:
    """Generate the location description for display."""
    location = state.current_location
    # Get the appropriate description text based on game state
    if isinstance(location.description, dict):
        if hasattr(location, 'droid_present') and location.droid_present:
            description = location.description.get('initial', 'A mysterious location.')
        else:
            description = location.description.get('after_droid_fix', 'The corridor is now clear.')
    else:
        description = str(location.description)
        
    output = [
        f"\n╔{'═' * (len(location.name) + 4)}╗",
        f"║  {location.name}  ║",
        f"╚{'═' * (len(location.name) + 4)}╝",
        description,
        ""
    ]
    
    # Show items in the location
    if location.items and len(location.items) > 0:
        items_text = ", ".join([str(item.name) for item in location.items])
        output.append(f"You see: {items_text}")
    else:
        output.append("There are no items of interest here.")
    
    # Show obstacles
    if hasattr(location, 'droid_present') and location.droid_present:
        output.append("\nA damaged maintenance droid blocks the way east, sparking erratically.")
    
    # Show exits
    exits = ", ".join([f"[{exit}]" for exit in location.exits.keys()])
    output.append(f"\nExits: {exits}")
    
    # Add score and hazards
    output.append(f"\n(SCORE: {state.score} | HAZARDS: {state.hazards})")
    
    # Ensure all items are strings before joining
    return "\n".join(str(item) for item in output)


def main():
    """Main game loop."""
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 50 + "║")
    print("║" + "ORBITAL STATION ESCAPE".center(50) + "║")
    print("║" + " " * 50 + "║")
    print("╚" + "═" * 50 + "╝\n")
    print(get_text('ui.welcome'))
    print("Type 'help' for a list of commands.\n")
    
    # Initialize game state
    state = initialize_game()
    
    # Main game loop
    while not state.game_over:
        # Display current location and status
        print(display_location(state))
        
        # Get player input
        try:
            command = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n" + get_text('ui.goodbye'))
            break
            
        if not command:
            print(get_text('ui.empty_command'))
            continue
            
        # Process command
        result = state.command_registry.execute_command(command, state.player)
        if result:
            if result.message:
                print("\n" + result.message)
            
            # Update game state if needed
            if hasattr(result, 'update_score') and result.update_score:
                state.score += result.update_score
            if hasattr(result, 'add_hazard') and result.add_hazard:
                state.hazards += 1
            
            # Check for game over conditions
            if result.end_game:
                state.game_over = True
                state.player_won = result.success
                
                if state.player_won:
                    base_score = state.score
                    bonus = max(0, 30 - (state.hazards * 2))  # Bonus decreases with hazards
                    final_score = base_score + bonus
                    print("\n" + get_text('game.escape_success', 
                                       score=final_score, 
                                       base=base_score, 
                                       bonus=bonus,
                                       hazards=state.hazards))
                else:
                    print("\n" + get_text('ui.game_over'))
                    print(f"Final Score: {state.score} | Hazards: {state.hazards}")
                
                print("\n" + get_text('ui.goodbye'))
                break


if __name__ == "__main__":
    main()
