"""
Damaged Maintenance Droid module for Orbital Station Escape.

This module contains the DamagedMaintenanceDroid class which represents the
malfunctioning droid that blocks the player's path in the game.
"""


class DamagedMaintenanceDroid:
    """Represents a malfunctioning maintenance droid in the game.
    
    The droid blocks the player's path until it is repaired using the diagnostic tool.
    
    Attributes:
        is_repaired (bool): Whether the droid has been repaired.
        is_active (bool): Whether the droid is currently blocking the path.
        description (str): Description of the droid's current state.
    """
    
    def __init__(self):
        """Droid starts in a damaged state."""
        self.is_repaired = False
        self.is_active = True
        self.description = (
            "A damaged MAINTENANCE DROID blocks your path. "
            "Its eyes flicker with erratic energy. It shoves you back "
            "when you try to pass!"
        )
    
    def repair(self) -> str:
        """Repair the droid using the diagnostic tool.
        
        Returns:
            str: A message describing the result of the repair attempt.
        """
        if self.is_repaired:
            return "The droid is already functioning properly."
            
        self.is_repaired = True
        self.is_active = False
        self.description = (
            "The droid powers down, its eyes dimming as it enters "
            "maintenance mode. The path is now clear."
        )
        return (
            "DROID REBOOT SEQUENCE INITIATED...\n"
            "The droid shudders as its systems reset. Its eyes flash blue "
            "and it stands aside, allowing you to pass.\n"
            "The droid gives you a mechanical salute as you pass."
        )
    
    def block_path(self) -> bool:
        """Determine if the droid is blocking the path.
        Example of encapsulation
        """
        return self.is_active and not self.is_repaired
    
    def get_description(self) -> str:
        """Get the current description of the droid.
        
        Returns:
            str: The droid's current description.
        """
        return self.description
    
    def reset(self) -> None:
        """Reset the droid to its initial damaged state."""
        self.is_repaired = False
        self.is_active = True
        self.description = (
            "A damaged MAINTENANCE DROID blocks your path. "
            "Its eyes flicker with erratic energy. It shoves you back "
            "when you try to pass!"
        )
