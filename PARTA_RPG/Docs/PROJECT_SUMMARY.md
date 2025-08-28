# Orbital Station Escape - Project Summary

## Game Overview
A text-based RPG where the player must escape from a damaged space station by following a specific sequence of actions. The game features a fixed "golden path" with specific scoring and hazard mechanics.

## Core Requirements

### Game Flow (Golden Path)
1. **Maintenance Tunnels (Starting Location)**
   - Find and pick up the Diagnostic Tool (+10 points)
   - Use the tool on the Damaged Maintenance Droid (+20 points)
   - Move to Docking Bay
   - Pick up the Energy Crystal (+50 points)
   - Type "win" to complete the mission (+30 points)

### Hazard System
- Attempting to move east while the droid is blocking increments the hazard counter
- Each hazard attempt adds +1 to the hazard count
- Hazards affect the final score

## Class Structure

### 1. StationItem (Abstract Base Class)
- **Attributes**:
  - `_name`: Name of the item
  - `_description`: Description of the item
- **Methods**:
  - `examine()`: Returns item description (to be implemented by subclasses)

### 2. DiagnosticTool (inherits from StationItem)
- **Methods**:
  - `examine()`: Returns a hint about the tool's purpose

### 3. EnergyCrystal (inherits from StationItem)
- **Methods**:
  - `examine()`: Describes the crystal's appearance

### 4. Location
- **Attributes**:
  - `name`: Location name
  - `description`: Location description
  - `exits`: Dictionary of available exits
  - `has_tool`: Boolean for tool presence
  - `has_crystal`: Boolean for crystal presence
  - `droid_present`: Boolean for droid presence
- **Methods**:
  - `__init__(name, description)`
  - `add_exit(direction, other_location)`
  - `describe()`: Returns formatted location description
  - `remove_tool()`: Removes tool from location
  - `remove_crystal()`: Removes crystal from location
  - `set_droid_present(flag)`: Sets droid presence

### 5. DamagedMaintenanceDroid
- **Attributes**:
  - `blocking`: Boolean indicating if droid is blocking
- **Methods**:
  - `__init__()`: Sets blocking to True
  - `repair()`: Sets blocking to False
  - `is_blocking()`: Returns blocking status

### 6. Player
- **Attributes**:
  - `current_location`: Current location object
  - `has_tool`: Boolean for tool possession
  - `has_crystal`: Boolean for crystal possession
  - `score`: Current score
  - `hazard_count`: Number of hazards encountered
- **Methods**:
  - `__init__(starting_location)`
  - `move(direction)`: Attempt to move in direction
  - `pick_up_tool()`: Pick up diagnostic tool
  - `use_tool_on_droid()`: Use tool on droid
  - `pick_up_crystal()`: Pick up energy crystal
  - `get_status()`: Return score and hazard count

### 7. GameController
- **Attributes**:
  - `maintenance_tunnels`: Location instance
  - `docking_bay`: Location instance
  - `droid`: DamagedMaintenanceDroid instance
  - `player`: Player instance
  - `diagnostic_tool`: DiagnosticTool instance
  - `energy_crystal`: EnergyCrystal instance
- **Methods**:
  - `__init__()`: Initialize game world
  - `setup_world()`: Create and connect locations
  - `start_game()`: Main game loop
  - `process_input(command)`: Process player commands
  - `check_win_condition()`: Check if win conditions are met

## Command Structure
- `move <direction>`: Move in specified direction (north, south, east, west)
- `pick up tool`: Pick up diagnostic tool
- `use tool`: Use tool on droid
- `pick up crystal`: Pick up energy crystal
- `status`: Show current score and hazards
- `win`: Complete the mission (only works in Docking Bay with crystal)

## Scoring System
- Pick up diagnostic tool: +10 points
- Use tool on droid: +20 points
- Pick up energy crystal: +50 points
- Complete mission: +30 points
- Hazards: Tracked but don't directly affect score

## UI/Display Format
1. **Location Display**:
```
╔════════════════════════════════════════════╗
   LOCATION NAME  
   Description text...
   << ITEMS: Item descriptions or ~No items available~
   << OBSTACLE: Obstacle description or ~No obstacles~
   << HINT: Helpful hint (when applicable)
   << EXITS: [list of available exits]
╚════════════════════════════════════════════╝
```

2. **Action Feedback**:
```
Action result text...
(SCORE: X | HAZARDS: Y)
```

3. **Status Display**:
```
(SCORE: X | HAZARDS: Y)
```

4. **Win Screen**:
```
🚀 MISSION COMPLETE!  
FINAL SCORE: XXX
HAZARDS ENCOUNTERED: Y  
"Orbital Station saved. Well done, Engineer."
```

## Project Structure
```
PARTA_RPG/
├── main.py              # Main game entry point
├── player.py            # Player class
├── items.py             # Item classes
├── location.py          # Location class
├── droid.py             # DamagedMaintenanceDroid class
├── game_controller.py   # Main game controller
└── PROJECT_SUMMARY.md   # This file
```

## Implementation Notes
- All code will be in a single directory with no subpackages
- Each class will be in its own file
- No `__init__.py` files will be used

## Implementation Notes
- Follow object-oriented design principles
- Use Python type hints
- Implement proper error handling
- Keep game logic separate from UI
- Write docstrings for all classes and methods
- Follow PEP 8 style guide
