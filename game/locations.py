from typing import Dict, List, Optional

try:
    from .utils import get_text
except ImportError:
    from utils import get_text


class Location:
    def __init__(self, name: str, description: str) -> None:
        """
        Initialize a new location.
        
        Args:
            name: The name of the location
            description: A description of the location
        """
        self.name = name
        self.description = description
        self.exits = {}  # Maps direction to another Location
        self.has_tool = False
        self.has_crystal = False
        self.droid_present = False
    
    def add_exit(self, direction: str, other_location: 'Location') -> None:
        """
        Add an exit to another location.
        
        Args:
            direction: The direction of the exit (e.g., 'north', 'east')
            other_location: The Location object this exit leads to
        """
        self.exits[direction.lower()] = other_location
    
    def describe(self) -> str:
        """
        Return a description of this location.
        
        Returns:
            A string describing the location and its exits
        """
        # Create the header with name and description
        description = [get_text('ui.location_header', 
                              name=self.name, 
                              divider='-' * len(self.name))]
        description.append(self.description)
        
        # Add items in the location
        items = []
        if self.has_tool:
            items.append("a diagnostic tool")
        if self.has_crystal:
            items.append("an energy crystal")
        if self.droid_present:
            items.append("a damaged maintenance droid")
            
        if items:
            description.append(get_text('game.location_items', items=", ".join(items)))
            
        # Add available exits
        if self.exits:
            exits = ", ".join(sorted(self.exits.keys()))
            description.append(get_text('game.location_exits', exits=exits))
            
        return "\n".join(description)
    
    def remove_tool(self) -> bool:
        """
        Remove the tool from this location if present.
        
        Returns:
            bool: True if a tool was removed, False otherwise
        """
        if self.has_tool:
            self.has_tool = False
            return True
        return False
    
    def remove_crystal(self) -> bool:
        """
        Remove the crystal from this location if present.
        
        Returns:
            bool: True if a crystal was removed, False otherwise
        """
        if self.has_crystal:
            self.has_crystal = False
            return True
        return False
    
    def set_droid_present(self, present: bool) -> None:
        """Set whether a droid is present in this location."""
        self.droid_present = present


def test_locations() -> None:
    """
    Test function to verify that the Location class works as expected.
    This function runs only when locations.py is executed directly.
    """
    print("\n=== Testing Location Class ===")
    
    # Create test locations
    room1 = Location("Test Room 1", "A small testing room")
    room2 = Location("Test Room 2", "Another testing room")
    
    # Test basic properties
    print("\nTesting basic properties:")
    print(f"- Room 1 name: {room1.name} (expected: Test Room 1)")
    print(f"- Room 1 description: {room1.description[:20]}... (expected: A small testing room...)")
    
    # Test adding exits
    print("\nTesting exits:")
    room1.add_exit("east", room2)
    room2.add_exit("west", room1)
    print(f"- Room 1 exits: {list(room1.exits.keys())} (expected: ['east'])")
    print(f"- Room 2 exits: {list(room2.exits.keys())} (expected: ['west'])")
    
    # Test item and droid presence
    print("\nTesting item and droid presence:")
    room1.has_tool = True
    room2.has_crystal = True
    room1.set_droid_present(True)
    
    print(f"- Room 1 has tool: {room1.has_tool} (expected: True)")
    print(f"- Room 2 has crystal: {room2.has_crystal} (expected: True)")
    print(f"- Room 1 has droid: {room1.droid_present} (expected: True)")
    
    # Test describe method
    print("\nTesting describe method:")
    room1_desc = room1.describe()
    print("Room 1 description contains items and droid:")
    print(f"- 'diagnostic tool' in description: {'diagnostic tool' in room1_desc}")
    print(f"- 'damaged maintenance droid' in description: {'damaged maintenance droid' in room1_desc}")
    
    print("\n✓ All Location tests completed!")


if __name__ == "__main__":
    # This block will only execute when locations.py is run directly
    test_locations()