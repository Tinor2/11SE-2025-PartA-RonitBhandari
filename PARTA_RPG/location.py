"""
Location module for Orbital Station Escape.

This module contains the Location class which represents a location in the game world.
"""
from typing import Dict, Optional, List


class Location:
    """Represents a location in the game world.
    
    Attributes:
        name (str): The name of the location.
        description (str): A description of the location.
        exits (Dict[str, 'Location']): Available exits from this location.
        has_tool (bool): Whether this location contains the diagnostic tool.
        has_crystal (bool): Whether this location contains the energy crystal.
        droid_present (bool): Whether the damaged maintenance droid is present.
        hint (Optional[str]): Optional hint for the player.
    """
    
    def __init__(self, name: str, description: str, 
                 has_tool: bool = False, 
                 has_crystal: bool = False, 
                 droid_present: bool = False):
        """Initialize the location.
        
        Args:
            name: The name of the location.
            description: A description of the location.
            has_tool: Whether this location has a diagnostic tool.
            has_crystal: Whether this location has an energy crystal.
            droid_present: Whether the droid is present in this location.
        """
        self.name = name
        self.description = description
        self.exits: Dict[str, 'Location'] = {}
        self.has_tool = has_tool
        self.has_crystal = has_crystal
        self.droid_present = droid_present
        self.hint: Optional[str] = None
    
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
            Matches the exact format from the storyboard
        """
        # Build the location description
        lines = [
            f"╔{'=' * 50}╗",
            f"   {self.name.upper()}",
            f"   {self.description}"
        ]
        
        # Add items if present
        if self.has_tool:
            lines.append("   << ITEMS: Diagnostic Tool glows on the floor")
        elif self.has_crystal:
            lines.append("   << ITEMS: A glowing ENERGY CRYSTAL is lodged in the wall...")
        else:
            lines.append("   << ITEMS: ~No items available~")
            
        # Add obstacles if present
        if self.droid_present:
            lines.append("    << OBSTACLE:   Droid beeps angrily")
        elif self.name.upper() == "MAINTENANCE TUNNELS" and not self.droid_present:
            lines.append("    << OBSTACLE: ~No obstacles~")
            
        # Add hint if available
        if hasattr(self, 'hint') and self.hint:
            lines.append(f"    << HINT: {self.hint}")
            
        # Add available exits
        if self.exits:
            exit_dirs = [f"{dir}" for dir in self.exits.keys()]
            lines.append(f"    <<  EXITS: {exit_dirs}")
            
        lines.append(f"╚{'=' * 50}╝")
        return "\n".join(lines)
    
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
        
        # Add appropriate hint based on droid state
        if is_present:
            self.hint = "use tool to fix it."
        else:
            self.hint = None
