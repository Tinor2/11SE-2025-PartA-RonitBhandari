from abc import ABC, abstractmethod
from utils import get_item_data

class Item(ABC):
    """
    Abstract base class for all items in the game.
    """
    def __init__(self, item_id: str) -> None:
        """
        Initialize a new item using data from game_data.json
        
        Args:
            item_id: The ID of the item from game_data.json
        """
        item_data = get_item_data(item_id)
        self._name = item_data['name']
        self._description = item_data['description']
        self._examine_text = item_data['examine']
    
    @abstractmethod
    def examine(self) -> str:
        """
        Return the examine text for the item.
        
        Returns:
            A string describing the item when examined
        """
        return self._examine_text


class DiagnosticTool(Item):
    """
    A diagnostic tool that can be used to repair the droid.
    """
    def __init__(self) -> None:
        """
        Initialize a new diagnostic tool.
        """
        super().__init__("diagnostic_tool")
    pass


class EnergyCrystal(Item):
    """
    An energy crystal that powers the escape pod.
    """
    def __init__(self) -> None:
        """
        Initialize a new energy crystal.
        """
        super().__init__("energy_crystal")
    
    pass