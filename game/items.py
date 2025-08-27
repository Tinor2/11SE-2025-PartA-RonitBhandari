from abc import ABC, abstractmethod
try:
    from .utils import get_item_data
except ImportError:
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
        super().__init__("diagnostic_tool")

class EnergyCrystal(Item):
    """
    An energy crystal that powers the escape pod.
    """
    def __init__(self) -> None:
        """
        Initialize a new energy crystal.
        """
        super().__init__("energy_crystal")

def test_items() -> None:
    """
    Test function to verify that all item classes work as expected.
    This function runs only when items.py is executed directly.
    """
    print("Testing items...\n")
    
    # Test DiagnosticTool
    print("Creating DiagnosticTool...")
    tool = DiagnosticTool()
    print(f"Name: {tool._name}")
    print(f"Description: {tool._description}")
    print(f"Examine: {tool.examine()}")
    
    print("\nCreating EnergyCrystal...")
    crystal = EnergyCrystal()
    print(f"Name: {crystal._name}")
    print(f"Description: {crystal._description}")
    print(f"Examine: {crystal.examine()}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    # This block will only execute when items.py is run directly
    test_items()