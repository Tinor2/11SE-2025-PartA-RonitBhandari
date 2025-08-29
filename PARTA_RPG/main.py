"""
Orbital Station Escape - Main Game Module

This is the entry point for the Orbital Station Escape text adventure game.
"""
import sys
from game_controller import GameController


def display_welcome() -> None:
    """Display the welcome message and game instructions."""
    print("""
╔══════════════════════════════════════════════════╗
            ORBITAL STATION ESCAPE
╚══════════════════════════════════════════════════╝
You're a technician on a space station experiencing
multiple system failures. Navigate the station,
collect items, and escape before it's too late! 

Type 'help' for a list of commands.
""")


def main() -> None:
    """Entry point matching the simplified GameController interface."""
    display_welcome()
    
    game = GameController()
    # Delegate control to GameController's internal loop
    game.start_game()
    
    print("\nThanks for playing Orbital Station Escape!")


if __name__ == "__main__":
    main()
