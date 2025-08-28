# Orbital Station Escape

A text-based adventure game where you play as a technician trying to escape a failing space station.

## Game Overview

You're a technician aboard the Orbital Station Omega-7, which is experiencing critical system failures. Navigate through the station, solve puzzles, and escape before it's too late!

## Features

- **Immersive Text-Based Gameplay**: Navigate through different locations using simple commands
- **Puzzle Solving**: Repair systems and collect items to progress
- **Hazard System**: Face challenges that affect your final score
- **Score Tracking**: Complete objectives to maximize your score
- **Intuitive Commands**: Easy-to-learn command system

## How to Play

1. Run the game: `python3 main.py`
2. Use the following commands:
   - `move [direction]`: Move in a direction (north, south, east, west)
   - `pick up [item]`: Pick up an item
   - `use [item]`: Use an item from your inventory
   - `inventory` or `i`: View your current inventory
   - `look`: Examine your current location
   - `status`: Check your score and hazard count
   - `help`: Show available commands
   - `quit`: Exit the game

## Requirements

- Python 3.8+
- No additional packages required

## Project Structure

```
SOFTWARE-OOP-AT2/
├── PARTA_RPG/           # Main game directory
│   ├── droid.py         # Droid behavior and state
│   ├── game_controller.py # Main game logic and command processing
│   ├── location.py      # Location and map management
│   └── main.py          # Entry point
├── Docs/                # Documentation
│   └── DEVELOPMENT_LOGBOOK.md  # Development history and decisions
└── README.md            # This file
```

## Development

For detailed development history and design decisions, see [DEVELOPMENT_LOGBOOK.md](Docs/DEVELOPMENT_LOGBOOK.md).

## License

This project is for educational purposes as part of the SOFTWARE-OOP-AT2 assessment.