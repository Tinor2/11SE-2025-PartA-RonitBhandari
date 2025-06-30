class Location:
    """
    Represents a location in the game world where the player can be.
    
    Locations can contain items, have exits to other locations, and may contain
    obstacles like the damaged maintenance droid.
    """
    
    def __init__(self, name, description):
        """
        Initialize a new location.
        
        Args:
            name (str): The name of the location
            description (str): A description of the location
        """
        self.name = name
        self.description = description
        self.exits = {}  # Maps direction to another Location
        self.has_tool = False
        self.has_crystal = False
        self.droid = None
        self.droid_present = False
    
    def add_exit(self, direction, other_location):
        """
        Add an exit to another location.
        
        Args:
            direction (str): The direction of the exit (e.g., 'east')
            other_location (Location): The location this exit leads to
        """
        self.exits[direction.lower()] = other_location
    
    def describe(self):
        """
        Generate a description of this location.
        
        Returns:
            str: A formatted description including items and exits
        """
        description = [f"=== {self.name} ===", self.description, ""]
        
        # Add item descriptions
        if self.has_tool:
            description.append("A diagnostic tool lies on the floor.")
        if self.has_crystal:
            description.append("An energy crystal is lodged in the wall, pulsing with light.")
            
        # Add droid description if present
        if self.droid_present and self.droid:
            description.append(self.droid.examine())
        
        # Add exit information
        if self.exits:
            exits = ", ".join(self.exits.keys())
            description.append(f"\nExits: {exits}.")
        
        return "\n".join(description)
    
    def remove_tool(self):
        """
        Remove the diagnostic tool from this location.
        
        Returns:
            bool: True if the tool was present and removed, False otherwise
        """
        if self.has_tool:
            self.has_tool = False
            return True
        return False
    
    def remove_crystal(self):
        """
        Remove the energy crystal from this location.
        
        Returns:
            bool: True if the crystal was present and removed, False otherwise
        """
        if self.has_crystal:
            self.has_crystal = False
            return True
        return False
    
    def set_droid_present(self, flag, droid=None):
        """
        Set whether a droid is present in this location.
        
        Args:
            flag (bool): Whether a droid should be present
            droid (DamagedMaintenanceDroid, optional): The droid to place here
        """
        self.droid_present = flag
        if flag and droid:
            self.droid = droid
