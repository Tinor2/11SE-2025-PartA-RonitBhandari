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
    output = [
        f"\n{location.name}",
        "=" * len(location.name),
        location.description,
        ""
    ]
    
    # Show items in the location
    if location.items:
        output.append("You see:")
        for item in location.items:
            output.append(f"- {item.name}: {item.description}")
    else:
        output.append("There are no items of interest here.")
    
    # Show obstacles
    if location.droid_present:
        output.append("\nA damaged maintenance droid blocks the way east, sparking erratically.")
    
    # Show exits
    exits = ", ".join(location.exits.keys())
    output.append(f"\nExits: [{exits}]")
    
    return "\n".join(output)


def main():
    """Main game loop."""
    print(get_text('ui.welcome'))
    
    # Initialize game state
    state = initialize_game()
    
    # Main game loop
    while not state.game_over:
        # Display current location and status
        print(display_location(state))
        print(f"\nScore: {state.score} | Hazards: {state.hazards}")
        
        # Get player input
        try:
            command = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n" + get_text('ui.goodbye'))
            break
            
        if not command:
            continue
            
        # Process command
        result = state.command_registry.execute_command(command, state.player)
        if result:
            print(result.message)
            
            # Check for game over conditions
            if result.end_game:
                state.game_over = True
                state.player_won = result.success
                
                if state.player_won:
                    print(get_text('ui.you_win').format(score=state.score))
                else:
                    print(get_text('ui.game_over'))
    
    print("\nThanks for playing Orbital Station Escape!")


if __name__ == "__main__":
    main()
