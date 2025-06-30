from typing import Tuple, Optional, List, Dict, Any
from location import Location
from damaged_droid import DamagedMaintenanceDroid

class Player:
    """
    Represents the player in the game, handling all player-related state and actions.
    
    The Player class manages the player's location, inventory, score, and hazard count.
    It provides methods for interacting with the game world and items.
    """
    
    def __init__(self, starting_location: Location):
        """
        Initialize a new player.
        
        Args:
            starting_location: The initial location where the player starts
        """
        self.current_location = starting_location
        self.inventory: List[str] = []
        self.score = 0
        self.hazard_count = 0
        self._max_hazards = 10  # Maximum hazards before game over
    
    def move(self, direction: str) -> Tuple[bool, str]:
        """
        Attempt to move the player in the specified direction.
        
        Args:
            direction: The direction to move (e.g., 'north', 'east')
            
        Returns:
            Tuple containing:
                - bool: True if movement was successful, False otherwise
                - str: A message describing the result of the movement
        """
        direction = direction.lower().strip()
        
        # Check if the direction is valid
        if direction not in self.current_location.exits:
            return False, "There is no exit in that direction."
        
        next_location = self.current_location.exits[direction]
        
        # Check for blocking droid in the current location
        if (hasattr(self.current_location, 'droid_present') and 
            self.current_location.droid_present and 
            self.current_location.droid and 
            self.current_location.droid.is_blocking() and
            hasattr(self.current_location, 'exits') and
            direction in self.current_location.exits and
            self.current_location.exits[direction].name == 'Docking Bay'):
            
            self.hazard_count += 1
            return False, f"The droid blocks your path! (Hazards: {self.hazard_count})"
        
        # Move to the new location
        self.current_location = next_location
        return True, f"You move {direction} to the {self.current_location.name}."
    
    def use(self, item_name: str) -> Tuple[bool, str]:
        """
        Attempt to use an item from the player's inventory.
        
        Args:
            item_name: Name of the item to use
            
        Returns:
            Tuple of (success, message)
        """
        item_name = item_name.lower()
        
        # Check for diagnostic tool
        if 'tool' in item_name and 'diagnostic_tool' in self.inventory:
            if hasattr(self.current_location, 'droid') and self.current_location.droid:
                result = self.current_location.droid.repair()
                self.score += 20
                return True, result
            return False, "There's nothing to use the diagnostic tool on here."
            
        return False, f"You don't have a {item_name} in your inventory."
    
    def pick_up(self, item_name: str) -> Tuple[bool, str]:
        """
        Attempt to pick up an item from the current location.
        
        Args:
            item_name: Name of the item to pick up
            
        Returns:
            Tuple of (success, message)
        """
        item_name = item_name.lower()
        
        # Check for diagnostic tool
        if 'tool' in item_name and hasattr(self.current_location, 'has_tool') and self.current_location.has_tool:
            self.inventory.append('diagnostic_tool')
            self.current_location.has_tool = False
            self.score += 10
            return True, "You pick up the diagnostic tool."
            
        # Check for energy crystal
        if 'crystal' in item_name and hasattr(self.current_location, 'has_crystal') and self.current_location.has_crystal:
            self.inventory.append('energy_crystal')
            self.current_location.has_crystal = False
            self.score += 50
            return True, "You pick up the energy crystal."
            
        return False, f"You don't see a {item_name} here."
    
    def get_status(self) -> str:
        """
        Get the player's current status.
        
        Returns:
            A formatted string showing the player's score and hazard count
        """
        return f"Score: {self.score} | Hazards: {self.hazard_count}/{self._max_hazards}"
    
    def has_won(self) -> bool:
        """
        Check if the player has met the winning conditions.
        
        Returns:
            bool: True if the player has won, False otherwise
        """
        if not hasattr(self, 'current_location') or not self.current_location:
            return False
            
        # Check if current location is a docking bay
        is_in_docking_bay = "docking" in self.current_location.name.lower()
        
        # Check if droid is not blocking (either not present or not blocking)
        droid_not_blocking = True
        if hasattr(self.current_location, 'droid_present') and self.current_location.droid_present:
            if hasattr(self.current_location, 'droid') and self.current_location.droid:
                droid_not_blocking = not self.current_location.droid.is_blocking()
        
        return is_in_docking_bay and self.has_crystal and droid_not_blocking
    
    def has_lost(self) -> bool:
        """
        Check if the player has lost the game.
        
        Returns:
            bool: True if the player has lost, False otherwise
        """
        return self.hazard_count >= self._max_hazards
