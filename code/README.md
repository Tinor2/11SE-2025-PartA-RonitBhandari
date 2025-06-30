# Orbital Station Escape

A text-based adventure game where you play as an engineer trying to escape from an orbital space station.

## How to Play

1. Run the game:
   ```
   python game_controller.py
   ```

2. Available commands:
   - `move <direction>` - Move in a direction (e.g., 'move east')
   - `pick up tool` - Pick up the diagnostic tool
   - `use tool` - Use the tool on the droid
   - `pick up crystal` - Pick up the energy crystal
   - `status` - Show your current score and hazards
   - `win` - Complete the mission (only in Docking Bay with crystal)
   - `help` - Show available commands
   - `quit` - Exit the game

## Game Objective

Follow these steps to escape:
1. Pick up the diagnostic tool in the Maintenance Tunnels
2. Use the tool on the droid to clear your path
3. Move to the Docking Bay
4. Pick up the energy crystal
5. Type 'win' to complete the mission

## Project Structure

- `game_controller.py` - Main game loop and controller
- `player.py` - Player class and actions
- `location.py` - Location and Droid classes
- `items.py` - Item classes (Tool and Crystal)
- `README.md` - This file

## Requirements

- Python 3.6+
- No external dependencies required

## Implementation Notes

- Follows the specified class structure and requirements
- Implements all required functionality from the specification
- Includes error handling and input validation
- Tracks score and hazards as specified

## Testing

To test the game, try these sequences:

1. Golden Path:
   - `pick up tool`
   - `use tool`
   - `move east`
   - `pick up crystal`
   - `win`

2. Try to move past the droid before fixing it to see the hazard counter increase.
