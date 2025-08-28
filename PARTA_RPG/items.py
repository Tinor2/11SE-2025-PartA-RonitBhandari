"""
Game items module.

This module contains the base Item class and all item implementations.
"""
from abc import ABC, abstractmethod
from typing import Optional


class StationItem(ABC):
    """Base class for all items in the game.
    
    Attributes:
        _name (str): The name of the item.
        _description (str): A description of the item.
    """
    
    def __init__(self, name: str, description: str):
        """Initialize the item with a name and description.
        Args:
            name: The name of the item.
            description: A description of the item.
        """
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        """
        Returns:
            The name of the item.
        """
        return self._name
    
    @property
    def description(self) -> str:
        """
        Returns:
            The description of the item.
        """
        return self._description
    
    @abstractmethod
    def examine(self) -> str:
        """Examine the item to get more information.  
        Returns:
            A detailed description of the item.
        """
        pass


class DiagnosticTool(StationItem):
    """A tool used to repair the damaged maintenance droid."""
    
    def __init__(self):
        """Initialize the diagnostic tool with default values."""
        super().__init__(
            name="Diagnostic Tool",
            description="A handheld device with various probes and readouts."
        )
    
    def examine(self) -> str:
        """Examine the diagnostic tool.
        
        Returns:
            A description of the tool and its purpose.
        """
        return (
            "This diagnostic tool seems designed to interface with maintenance droids. "
            "It has several probes and a small display showing system diagnostics."
        )


class EnergyCrystal(StationItem):
    """A volatile energy source needed to power the escape pod."""
    
    def __init__(self):
        """Initialize the energy crystal with default values."""
        super().__init__(
            name="Energy Crystal",
            description="A glowing crystal pulsing with unstable energy."
        )
    
    def examine(self) -> str:
        """Examine the energy crystal.
        
        Returns:
            A description of the crystal's appearance and behavior.
        """
        return (
            "The crystal pulses with an unstable, vibrant energy. It feels warm to the touch "
            "and occasionally emits small sparks. This must be what powers the station's "
            "critical systems."
        )
