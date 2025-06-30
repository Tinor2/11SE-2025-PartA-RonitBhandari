from location import Location
from player import Player
from input_parser import InputParser
from commands import QuitCommand
import json

def load_game_world():
    """Load the game world from the JSON file and set up locations."""
    try:
        with open('game_messages.json', 'r') as f:
            game_data = json.load(f)
    except FileNotFoundError:
        print("Error: game_messages.json not found.")
        return None
    
    # Create locations
    locations = {}
    for loc_id, loc_data in game_data['locations'].items():
        locations[loc_id] = Location(
            loc_data['name'],
            loc_data['descriptions']['default']
        )
    
    # Set up exits and obstacles
    for loc_id, loc_data in game_data['locations'].items():
        if 'exits' in loc_data:
            for direction, exit_data in loc_data['exits'].items():
                if exit_data['to'] in locations:
                    locations[loc_id].add_exit(direction, locations[exit_data['to']])
        
        # Set up items and obstacles
        if 'items' in loc_data:
            for item_id in loc_data['items']:
                if item_id == 'diagnostic_tool':
                    locations[loc_id].has_tool = True
                elif item_id == 'energy_crystal':
                    locations[loc_id].has_crystal = True
        
        # Set up droid if present
        if 'obstacles' in loc_data and 'malfunctioning_droid' in loc_data['obstacles']:
            from damaged_droid import DamagedMaintenanceDroid
            locations[loc_id].droid = DamagedMaintenanceDroid()
            locations[loc_id].droid_present = True
    
    return locations

def main():
    """Main game function."""
    # Load the game world
    locations = load_game_world()
    if not locations:
        print("Failed to load game world. Exiting.")
        return
    
    # Initialize player and parser
    player = Player(locations['maintenance_tunnel'])
    parser = InputParser()
    
    # Game loop
    print("=== ORBITAL STATION ESCAPE ===\n")
    print(player.current_location.describe())
    print("\nType 'help' for a list of commands.")
    
    while True:
        # Get player input
        try:
            command_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing!")
            break
            
        if not command_input:
            continue
            
        # Parse and execute command
        command, args = parser.parse(command_input)
        
        if not command:
            print("I don't understand that command. Type 'help' for a list of commands.")
            continue
            
        # Handle quit command
        if isinstance(command, QuitCommand):
            success, message = command.execute(player, *args)
            print(message)
            break
            
        # Execute the command
        success, message = command.execute(player, *args)
        print(message)
        
        # Check for game over conditions
        if player.hazard_count >= player._max_hazards:
            print("\nToo many hazards! You've been overwhelmed by the station's dangers.")
            print("Game Over!")
            break
            
        # Check for win condition (at launch pad with crystal)
        if (hasattr(player.current_location, 'name') and 
            player.current_location.name.lower() == 'launch pad' and 
            'energy_crystal' in player.inventory):
            print("\nYou insert the energy crystal into the escape pod's console.")
            print("The engines roar to life as you strap in. You've done it!")
            print(f"\nFinal Score: {player.score}")
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()