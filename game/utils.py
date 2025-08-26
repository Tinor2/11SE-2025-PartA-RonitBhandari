"""Utility functions for the game."""
import json
from pathlib import Path
from typing import Dict, Any

def load_game_data() -> Dict[str, Any]:
    """
    Load game data from the JSON file.
    
    Returns:
        Dictionary containing all game data
    """
    data_path = Path(__file__).parent / 'data' / 'game_data.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_item_data(item_id: str) -> Dict[str, str]:
    """
    Get data for a specific item.
    
    Args:
        item_id: The ID of the item to retrieve
        
    Returns:
        Dictionary containing the item's data
    """
    data = load_game_data()
    return data['items'][item_id]
