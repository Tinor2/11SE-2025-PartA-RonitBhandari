"""
Player module for Orbital Station Escape.

This module contains the Player class which represents the player in the game.
"""
from typing import Any  # 'Any' currently unused but kept if needed for type hints
from location import Location
from items import DiagnosticTool, EnergyCrystal


class Player:
    """Represents the player.

    Attributes:
        current_location (Location): Where the player is.
        has_tool (bool): Whether the player carries the diagnostic tool.
        has_crystal (bool): Whether the player carries the energy crystal.
        score (int): Current score.
        hazard_count (int): Number of hazards encountered.
    """
    
    def __init__(self, starting_location: Location):
        """Initialize the player with a starting location.
        
        Args:
            starting_location: The initial Location object where the player begins.
        """
        self.current_location = starting_location
        self.has_tool = False
        self.has_crystal = False
        self.score = 0
        self.hazard_count = 0
    
    def move(self, direction: str) -> str:
        """Attempt to move in a direction.
        
        Args:
            direction: The direction to move in.
            
        Returns:
            A message describing the result of the movement attempt.
        """
        direction = direction.lower()

        if direction not in self.current_location.exits:
            return "You can't go that way."

        # Droid hazard check (only east from Maintenance Tunnels in spec)
        if self.current_location.droid_present and direction == "east":
            self.hazard_count += 1
            return (
                "The droid SHOVES you back! (+1 HAZARD)\n"
                f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
            )

        self.current_location = self.current_location.exits[direction]
        return f"You enter the {self.current_location.name}.\n{self.get_status()}"
    
    # --- Item interactions ---
    def pick_up_tool(self) -> str:
        """Pick up the diagnostic tool if present.

        Returns:
            str: Result message.
        """
        if not self.current_location.has_tool:
            return "There's no tool here to pick up."
        self.current_location.remove_tool()
        self.has_tool = True
        self.score += 10
        return (
            "You grab the diagnostic tool. [+10]\n"
            f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
        )
            
    
    def use_tool_on_droid(self) -> str:
        """Use the diagnostic tool on the droid if possible.

        Returns:
            str: Result message.
        """
        if not self.has_tool:
            return "You don't have a tool to use."
        if not self.current_location.droid_present:
            return "There's nothing to use the tool on here."
        self.current_location.set_droid_present(False)
        self.score += 20
        return (
            "Droid reboots! It salutes and shuffles aside. [+20]\n"
            f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
        )
    
    def pick_up_crystal(self) -> str:
        """Pick up the energy crystal if present.

        Returns:
            str: Result message.
        """
        if not self.current_location.has_crystal:
            return "There's no crystal here to pick up."
        self.current_location.remove_crystal()
        self.has_crystal = True
        self.score += 50
        return (
            "The crystal vibrates in your palm. You drop to the ground as the gravity resets! [+50]\n"
            f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"
        )
    
    def get_status(self) -> str:
        """Return a formatted status string showing current score and hazards."""
        return f"(SCORE: {self.score} | HAZARDS: {self.hazard_count})"

    # Temporary method kept for compatibility with GameController; will be removed during refactor
    def get_inventory(self):
        """Return list of carried item names (non-spec). Will be removed soon."""
        items = []
        if self.has_tool:
            items.append("Diagnostic Tool")
        if self.has_crystal:
            items.append("Energy Crystal")
        return items
    
