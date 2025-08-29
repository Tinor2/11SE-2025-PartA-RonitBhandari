"""
Location module for Orbital Station Escape.

This module contains the Location class which represents a location in the game world.
"""
from typing import Dict, List


class Location:
    """Represents a location in the game world.
    
    Attributes:
        name (str): The name of the location.
        description (str): A description of the location.
        exits (Dict[str, 'Location']): Available exits from this location.
        has_tool (bool): Whether this location contains the diagnostic tool.
        has_crystal (bool): Whether this location contains the energy crystal.
        droid_present (bool): Whether the damaged maintenance droid is present.
    """
    
    def __init__(self, name: str, description: str, 
                 has_tool: bool = False, 
                 has_crystal: bool = False, 
                 droid_present: bool = False,
                 droid: 'DamagedMaintenanceDroid' = None):
        """Initialize the location.
        
        Args:
            name: The name of the location.
            description: A description of the location.
            has_tool: Whether this location has a diagnostic tool.
            has_crystal: Whether this location has an energy crystal.
            droid_present: Whether the droid is present in this location.
            droid: Reference to the droid in this location, if any.
        """
        self.name = name
        self.description = description
        self.exits: Dict[str, 'Location'] = {}
        self.has_tool = has_tool
        self.has_crystal = has_crystal
        self.droid_present = droid_present
        self.droid = droid
    
    def add_exit(self, direction: str, other_location: 'Location') -> None:
        """Add an exit to another location.
        
        Args:
            direction: The direction of the exit (e.g., 'north', 'east').
            other_location: The Location object this exit leads to.
        """
        self.exits[direction.lower()] = other_location
    
    def describe(self) -> str:
        """Generate a description of the location.
        
        Returns:
            A formatted string describing the location and its contents.
            Matches the exact format from the storyboard.
        """
        item_desc = "~No items available~"
        if self.has_tool:
            item_desc = "Diagnostic Tool"
        elif self.has_crystal:
            item_desc = "Energy Crystal"

        obstacle_desc = "~No obstacles~"
        if self.droid_present:
            obstacle_desc = "A damaged maintenance droid is blocking the path."

        exit_list = list(self.exits.keys())

        return (
            f"╔══════════════════════════════════════════════════╗\n"
            f"   {self.name.upper()}\n"
            f"   {self.description}\n"
            f"   << ITEMS: {item_desc}\n"
            f"   << OBSTACLE: {obstacle_desc}\n"
            f"   << EXITS: {exit_list}\n"
            f"╚══════════════════════════════════════════════════╝"
        )
    
    def remove_tool(self) -> bool:
        """Remove the diagnostic tool from this location.
        
        Returns:
            bool: True if the tool was removed, False if there was no tool.
        """
        if self.has_tool:
            self.has_tool = False
            return True
        return False
    
    def remove_crystal(self) -> bool:
        """Remove the energy crystal from this location.
        
        Returns:
            bool: True if the crystal was removed, False if there was no crystal.
        """
        if self.has_crystal:
            self.has_crystal = False
            return True
        return False
    
    def set_droid_present(self, is_present: bool) -> None:
        """Set whether the droid is present in this location.
        
        Args:
            is_present: Whether the droid should be present.
        """
        self.droid_present = is_present
        if not is_present:
            self.droid = None
