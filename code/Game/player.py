from typing import Tuple, Optional
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
        self.has_tool = False
        self.has_crystal = False
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
        
        # Check for blocking droid in the next location
        if hasattr(next_location, 'droid_present') and next_location.droid_present and next_location.droid.is_blocking():
            self.hazard_count += 1
            return False, f"The droid blocks your path! (Hazards: {self.hazard_count})"
        
        # Move to the new location
        previous_location = self.current_location
        self.current_location = next_location
        return True, f"You move {direction} from {previous_location.name} to {self.current_location.name}."
    
    def pick_up_tool(self) -> Tuple[bool, str]:
        """
        Attempt to pick up the diagnostic tool from the current location.
        
        Returns:
            Tuple containing:
                - bool: True if tool was picked up, False otherwise
                - str: A message describing the result
        """
        if self.has_tool:
            return False, "You already have the tool."
        
        if not self.current_location.has_tool:
            return False, "There is no tool here to pick up."
        
        self.current_location.remove_tool()
        self.has_tool = True
        self.score += 10
        return True, "You pick up the diagnostic tool. (+10)"
    
    def use_tool_on_droid(self, droid: DamagedMaintenanceDroid = None) -> Tuple[bool, str]:
        """
        Attempt to use the diagnostic tool on a droid.
        
        Args:
            droid: The droid to use the tool on (optional, will use current location's droid if None)
            
        Returns:
            Tuple containing:
                - bool: True if the tool was used successfully, False otherwise
                - str: A message describing the result
        """
        if not self.has_tool:
            return False, "You don't have any tool to use."
        
        # Use the provided droid or the one in the current location
        target_droid = droid
        if target_droid is None and hasattr(self.current_location, 'droid_present') and self.current_location.droid_present:
            target_droid = self.current_location.droid
        
        if not target_droid or not hasattr(target_droid, 'is_blocking') or not target_droid.is_blocking():
            return False, "There's nothing to use the tool on here."
        
        message = target_droid.repair()
        self.score += 20
        return True, f"{message} (+20)"
    
    def pick_up_crystal(self) -> Tuple[bool, str]:
        """
        Attempt to pick up the energy crystal from the current location.
        
        Returns:
            Tuple containing:
                - bool: True if crystal was picked up, False otherwise
                - str: A message describing the result
        """
        if self.has_crystal:
            return False, "You already have the crystal."
        
        if not self.current_location.has_crystal:
            return False, "There is no crystal here to pick up."
        
        self.current_location.remove_crystal()
        self.has_crystal = True
        self.score += 50
        return True, "You pick up the energy crystal. It vibrates in your hand! (+50)"
    
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
