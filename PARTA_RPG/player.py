"""
Player module for Orbital Station Escape.

This module contains the Player class which represents the player in the game.
"""
from typing import List, Optional, Dict, Any
from location import Location
from items import DiagnosticTool, EnergyCrystal


class Player:
    """Represents the player in the game.
    
    Attributes:
        current_location (Location): The player's current location.
        inventory (Dict[str, Any]): Items the player is carrying.
    """
    
    def __init__(self, starting_location):
        """Initialize the player with a starting location.
        
        Args:
            starting_location: The initial Location object where the player begins.
        """
        self.current_location = starting_location
        self.inventory = []
        self.score = 0
        self.hazards_encountered = 0
        self.hazard_count = 0  # Track number of hazards encountered
        self.has_tool = False
        self.has_crystal = False
        self.moved_this_turn = False
    
    def move(self, direction: str) -> str:
        """Attempt to move in a direction.
        
        Args:
            direction: The direction to move in.
            
        Returns:
            A message describing the result of the movement attempt.
        """
        direction = direction.lower()
        
        # Check if the direction is valid
        if direction not in self.current_location.exits:
            return "You can't go that way."
        
        # Check for droid blocking the way
        if self.current_location.droid_present and direction == "east":
            self.hazard_count += 1
            return (
                "The droid SHOVES you back! (+1 HAZARD)\n"
                f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
            )
        
        # Move to the new location
        self.current_location = self.current_location.exits[direction]
        return f"You move {direction}."
    
    def pick_up_item(self, item_name: str) -> str:
        """Attempt to pick up an item from the current location.
        
        Args:
            item_name: The name of the item to pick up.
            
        Returns:
            A message describing the result of the pickup attempt.
        """
        item_name = item_name.lower()
        
        # Check for diagnostic tool
        if "tool" in item_name and self.current_location.has_tool:
            self.current_location.remove_tool()
            self.inventory["diagnostic_tool"] = DiagnosticTool()
            self.score += 10
            return (
                f"You grab the diagnostic tool. [+10]\n"
                f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
            )
            
        # Check for energy crystal
        if "crystal" in item_name and self.current_location.has_crystal:
            self.current_location.remove_crystal()
            self.inventory["energy_crystal"] = EnergyCrystal()
            self.score += 50
            return (
                "The crystal vibrates in your palm. You drop to the ground as the gravity resets! [+50]\n"
                f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
            )
            
        return "You don't see that here."
    
    def use_item(self, item_name: str) -> str:
        """Attempt to use an item from the inventory.
        
        Args:
            item_name: The name of the item to use.
            
        Returns:
            A message describing the result of using the item.
        """
        item_name = item_name.lower()
        
        # Using the diagnostic tool on the droid
        if "tool" in item_name and "diagnostic_tool" in self.inventory:
            if self.current_location.droid_present:
                self.current_location.set_droid_present(False)
                self.has_used_tool = True
                self.score += 20
                return (
                    "Droid reboots! It salutes and shuffles aside. [+20]\n"
                    f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
                )
            return "Nothing happens."
            
        return "You don't have that item."
    
    def get_status(self) -> str:
        """Get the player's current status.
        
        Returns:
            A string showing the current score and hazard count.
        """
        return f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
    
    def has_won(self) -> bool:
        """Check if the player has met the win conditions.
        
        Returns:
            bool: True if the player has won, False otherwise.
        """
        return (
            self.current_location.name.lower() == "docking bay"
            and "energy_crystal" in self.inventory
        )
    
    def get_inventory(self) -> List[str]:
        """Get a list of items in the player's inventory.
        
        Returns:
            A list of item names in the inventory.
        """
        return list(self.inventory.keys())
