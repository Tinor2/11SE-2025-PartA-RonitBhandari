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
    """Main game loop."""
    # Initialize game controller
    game = GameController()
    
    # Display welcome message
    display_welcome()
    
    # Initial game state display
    print("\n" + "="*50)
    print(game.player.current_location.describe())
    print("\nWhat would you like to do?")
    
    # Main game loop
    while not game.game_over:
        try:
            # Get player input
            command = input("\n>> ").strip()
            
            # Process the command
            result = game.process_command(command)
            
            # Display the result of the command
            if result:
                print(f"\n{result}")
                
                # If game over from the command (like 'quit' or win condition)
                if game.game_over:
                    break
            
            # Show location description after each command if game is still going
            if not game.game_over:
                input("\nPress Enter to continue...")
                print("\n" + "="*50)
                print(game.player.current_location.describe())
                print("\nWhat would you like to do?")
                    
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            if input("Do you want to quit? (y/n): ").lower() == 'y':
                break
    
    print("\nThanks for playing Orbital Station Escape!")


if __name__ == "__main__":
    main()
