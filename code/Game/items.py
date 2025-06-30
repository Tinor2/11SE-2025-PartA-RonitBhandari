from abc import ABC, abstractmethod

class StationItem(ABC):
    """Base class for all items in the game."""
    def __init__(self, name, description):
        self._name = name
        self._description = description
    
    @abstractmethod
    def examine(self):
        """Return a description of the item."""
        pass

class DiagnosticTool(StationItem):
    """Tool used to repair the maintenance droid."""
    def __init__(self):
        super().__init__(
            "Diagnostic Tool",
            "A handheld device for repairing electronic systems."
        )
    
    def examine(self):
        return "This diagnostic tool seems designed to interface with maintenance droids."

class EnergyCrystal(StationItem):
    """Volatile crystal that the player must collect."""
    def __init__(self):
        super().__init__(
            "Energy Crystal",
            "A glowing crystal pulsing with unstable energy."
        )
    
    def examine(self):
        return "The crystal pulses with an unstable, vibrant energy."
