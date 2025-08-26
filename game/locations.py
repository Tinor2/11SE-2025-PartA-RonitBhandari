class Location:
    def __init__(self, name: str, description: str) -> None:
        """
        Initialize a new location.
        
        Args:
            name: The name of the location
            description: A description of the location
        """
        self.name = name
        self.description = description
        self.exits = {}  # Maps direction to another Location
        self.has_tool = False
        self.has_crystal = False
        self.droid_present = False
    
    def add_exit(self, direction: str, other_location: 'Location') -> None:
        """
        Add an exit to another location.
        
        Args:
            direction: The direction of the exit (e.g., 'north', 'east')
            other_location: The Location object this exit leads to
        """
        pass
    
    def describe(self) -> str:
        """
        Return a description of this location.
        
        Returns:
            A string describing the location and its exits
        """
        pass
    
    def remove_tool(self) -> bool:
        """
        Remove the tool from this location if present.
        
        Returns:
            bool: True if a tool was removed, False otherwise
        """
        pass
    
    def remove_crystal(self) -> bool:
        """
        Remove the crystal from this location if present.
        
        Returns:
            bool: True if a crystal was removed, False otherwise
        """
        pass
    
    def set_droid_present(self, flag: bool) -> None:
        """
        Set whether a droid is present in this location.
        
        Args:
            flag: Whether a droid should be present
        """
        pass