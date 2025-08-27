#!/usr/bin/env python3
"""
Orbital Station Escape - Main Entry Point

A text-based adventure game where you must escape from a damaged space station.
"""
import sys

def main():
    """Main entry point for the game."""
    try:
        from game.game_loop import main as game_main
        game_main()
    except ImportError as e:
        print(f"Error: {e}")
        print("Could not start the game. Make sure to run this from the project root directory.")
        print("Try: python main.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
