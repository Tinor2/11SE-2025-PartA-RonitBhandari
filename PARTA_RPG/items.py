"""
Items module for Orbital Station Escape.

Contains the base StationItem class and its subclasses.
"""
from abc import ABC, abstractmethod


class StationItem(ABC):
    """Base class for all items in the game."""
    
    def __init__(self, name: str, description: str):
        """Initialize the item with name and description."""
        self._name = name
        self._description = description
    
    @abstractmethod
    def examine(self) -> str:
        """Return a description of the item when examined."""
        pass


class DiagnosticTool(StationItem):
    """A diagnostic tool used to repair maintenance droids."""
    
    def __init__(self):
        """Initialize the diagnostic tool."""
        super().__init__(
            name="Diagnostic Tool",
            description="A device for interfacing with maintenance droids."
        )
    
    def examine(self) -> str:
        """Return a description of the tool."""
        return "This diagnostic tool seems designed to interface with maintenance droids."


class EnergyCrystal(StationItem):
    """An energy crystal that powers the escape pod."""
    
    def __init__(self):
        """Initialize the energy crystal."""
        super().__init__(
            name="Energy Crystal",
            description="A glowing crystal pulsing with unstable energy."
        )
    
    def examine(self) -> str:
        """Return a description of the crystal."""
        return "The crystal pulses with an unstable, vibrant energy."
