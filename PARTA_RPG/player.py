"""
Player module - SPECIFICATION COMPLIANT ONLY.

Contains ONLY the Player class with exact specification requirements.
"""
from location import Location


class Player:
    """Tracks the player's current location, which items they hold, and their score/hazard counts.
    
    Attributes (EXACT SPECIFICATION):
        current_location: Player's current location
        has_tool: Whether player has the diagnostic tool  
        has_crystal: Whether player has the energy crystal
        score: Current score
        hazard_count: Number of hazards encountered
    """
    
    def __init__(self, starting_location):
        """Initialise the player.
        
        Args:
            starting_location (Location): Where the player starts.
        """
        self.current_location = starting_location
        self.has_tool = False
        self.has_crystal = False
        self.score = 0
        self.hazard_count = 0
    
    def move(self, direction):
        """Attempt to change current_location in the given direction.
        
        • If no such exit exists, return failure.
        • If the droid is still blocking, increment hazard_count, return failure.  
        • Otherwise update current_location and return success.
        """
        direction = direction.lower()
        
        # If no such exit exists, return failure
        if direction not in self.current_location.exits:
            return "failure - no exit"
        
        # If the droid is still blocking, increment hazard_count, return failure
        if self.current_location.droid_present and direction == "east":
            self.hazard_count += 1
            return "failure - droid blocking"
        
        # Otherwise update current_location and return success
        self.current_location = self.current_location.exits[direction]
        return "success"
    
    def pick_up_tool(self):
        """If current_location.has_tool is True, clear that flag, set has_tool to True, add 10 to score, and return success; otherwise return failure."""
        if self.current_location.has_tool:
            self.current_location.remove_tool()  # Clear that flag
            self.has_tool = True  # Set has_tool to True
            self.score += 10  # Add 10 to score
            return "success"
        else:
            return "failure - no tool here"
    
    def use_tool_on_droid(self):
        """Attempt to repair the droid using the diagnostic tool.
        
        Returns:
            str: "success" if the droid was repaired, else a failure code.
        """
        if self.has_tool and self.current_location.droid and self.current_location.droid.is_blocking():
            # Call the droid's repair logic through the location
            self.current_location.droid.repair()
            self.current_location.set_droid_present(False)
            self.score += 20
            return "success"
        return "failure - cannot use tool"
    
    def pick_up_crystal(self):
        """If current_location.has_crystal is True, clear that flag, set has_crystal to True, add 50 to score, and return success; otherwise return failure."""
        if self.current_location.has_crystal:
            self.current_location.remove_crystal()  # Clear that flag
            self.has_crystal = True  # Set has_crystal to True  
            self.score += 50  # Add 50 to score
            return "success"
        else:
            return "failure - no crystal here"
    
    def get_status(self):
        """Return the current score and hazard count (students decide how to format)."""
        return f"Score: {self.score}, Hazards: {self.hazard_count}"