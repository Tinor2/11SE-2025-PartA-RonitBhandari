"""
Player class for the Orbital Station Escape game.
Handles player state including inventory, location, and game interactions.
"""
from typing import Dict, List, Optional

from items import StationItem, DiagnosticTool, EnergyCrystal
from utils import get_text
from locations import Location

class Player:
    """
    Represents the player in the game, managing their inventory, score, and current location.
    """
    def __init__(self, starting_location: 'Location') -> None:
        """
        Initialize a new player.
        
        Args:
            starting_location: The initial location where the player starts
        """
        self.current_location = starting_location
        self.inventory: List[StationItem] = []
        self.score = 0
        self.hazards = 0
        self.has_escaped = False
        self.used_tool_on_droid = False

    def move(self, direction: str) -> str:
        """
        Attempt to move the player in the specified direction.
        
        Args:
            direction: The direction to move (e.g., 'north', 'east')
            
        Returns:
            A message describing the result of the movement attempt
        """
        direction = direction.lower()
        if direction in self.current_location.exits:
            new_location = self.current_location.exits[direction]
            
            # Check for droid blocking the way
            if self.current_location.droid_present and not self.has_item("diagnostic_tool"):
                self.hazards += 1
                return get_text('game.droid_blocking')
                
            self.current_location = new_location
            return get_text('ui.moved', direction=direction)
        return get_text('ui.no_exit')

    def take_item(self, item_name: str) -> str:
        """
        Take an item from the current location.
        
        Args:
            item_name: The name of the item to take
            
        Returns:
            A message describing the result of the action
        """
        item_name = item_name.lower()
        
        if "tool" in item_name and self.current_location.has_tool:
            self.inventory.append(DiagnosticTool())
            self.current_location.remove_tool()
            self.score += 10
            return get_text('game.tool_taken')
            
        if "crystal" in item_name and self.current_location.has_crystal:
            self.inventory.append(EnergyCrystal())
            self.current_location.remove_crystal()
            self.score += 15
            return get_text('game.crystal_taken')
            
        return get_text('ui.item_not_here')

    def use_item(self, item_name: str, target: str = None) -> str:
        """
        Use an item from the player's inventory.
        
        Args:
            item_name: The name of the item to use
            target: Optional target of the item usage
            
        Returns:
            A message describing the result of using the item
        """
        item = self.get_item(item_name)
        if not item:
            return get_text('ui.item_not_found')
            
        # Handle specific item interactions
        if isinstance(item, DiagnosticTool):
            if target and 'droid' in target.lower():
                if self.current_location.droid_present:
                    self.current_location.droid_present = False
                    self.used_tool_on_droid = True
                    self.score += 20
                    return get_text('game.droid_repaired')
                else:
                    return get_text('game.no_droid_here')
            return get_text('game.what_to_repair')
        
        if isinstance(item, EnergyCrystal):
            if target and 'pod' in target.lower():
                if hasattr(self.current_location, 'is_escape_pod') and self.current_location.is_escape_pod:
                    self.has_escaped = True
                    self.score += 100
                    return get_text('game.escape_success')
                else:
                    return get_text('game.no_escape_pod_here')
            return get_text('game.what_to_power')
                
        return get_text('game.cant_use_item')

    def add_score(self, points: int) -> None:
        """Add points to the player's score."""
        self.score += points

    def add_hazard(self) -> None:
        """Increment the hazard counter."""
        self.hazards += 1

    def get_item(self, item_name: str) -> Optional[StationItem]:
        """
        Get an item from the inventory by name.
        
        Args:
            item_name: The name of the item to find
            
        Returns:
            The Item object if found, None otherwise
        """
        item_name = item_name.lower()
        for item in self.inventory:
            if item_name in item._name.lower():
                return item
        return None

    def has_item(self, item_id: str) -> bool:
        """
        Check if the player has a specific item.
        
        Args:
            item_id: The ID of the item to check for ('diagnostic_tool' or 'energy_crystal')
            
        Returns:
            True if the player has the item, False otherwise
        """
        item_types = {
            'diagnostic_tool': DiagnosticTool,
            'energy_crystal': EnergyCrystal
        }
        
        item_class = item_types.get(item_id)
        if not item_class:
            return False
            
        return any(isinstance(item, item_class) for item in self.inventory)

    def get_inventory(self) -> List[str]:
        """
        Get a list of item names in the player's inventory.
        
        Returns:
            A list of item names
        """
        return [item._name for item in self.inventory]

    def escape(self) -> str:
        """Attempt to escape the station."""
        if self.has_item("energy_crystal"):
            self.has_escaped = True
            self.score += 100  # Big score bonus for escaping
            return get_text('game.escape_success')
        return get_text('game.escape_failure')


def test_player():
    """Test the Player class functionality."""
    # Import here to avoid circular imports
    try:
        from .locations import Location
    except ImportError:
        from locations import Location
    
    print("\n=== Testing Player Class ===")
    
    # Create test locations
    room1 = Location("test_room1", "A test room")
    room2 = Location("test_room2", "Another test room")
    room1.exits["east"] = room2
    room2.exits["west"] = room1
    
    # Test initialization
    player = Player(room1)
    print(get_text('test_messages.player_created', location=player.current_location.name))
    
    # Test movement
    print("\nTesting movement:")
    result = player.move("east")
    print(f"- Move east: {result}")
    print(get_text('test_messages.test_moved_to', 
                  location=player.current_location.name, 
                  expected="test_room2"))
    
    # Test inventory
    print("\nTesting inventory:")
    # Create a test tool item
    test_tool = DiagnosticTool()
    player.inventory.append(test_tool)
    print(get_text('test_messages.test_item_added', item=test_tool._name))
    has_item = player.has_item('diagnostic_tool')
    print(get_text('test_messages.test_has_item', 
                  result=has_item, 
                  expected=True))
    item = player.get_item('tool')
    print(get_text('test_messages.test_get_item',
                  result=item._name if item else 'None',
                  expected=test_tool._name))
    
    # Test score
    print("\nTesting score:")
    player.score = 50
    print(get_text('test_messages.test_score',
                  score=player.score,
                  expected=50))
    
    print(get_text('test_messages.test_completed', test_name="Player"))

if __name__ == "__main__":
    # This block will only execute when player.py is run directly
    test_player()