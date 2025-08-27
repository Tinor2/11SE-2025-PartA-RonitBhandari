#!/usr/bin/env python3
"""
Test runner for the Orbital Station Escape game.
Run all tests with: python3 run_tests.py
"""
import unittest
import sys
import os

# Add the game directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """Run all test modules."""
    # Import test modules
    from game.player import test_player
    from game.locations import test_locations
    from game.commands import test_commands
    from game.items import test_items
    
    # Run tests
    print("Running Player tests...")
    test_player()
    
    print("\n" + "="*50 + "\n")
    
    print("Running Location tests...")
    test_locations()
    
    print("\n" + "="*50 + "\n")
    
    print("Running Command tests...")
    test_commands()
    
    print("\n" + "="*50 + "\n")
    
    print("Running Item tests...")
    test_items()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_tests()
