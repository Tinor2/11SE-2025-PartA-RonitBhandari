"""Utility functions for the game."""
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union


def get_text(key_path: str, **format_args) -> str:
    """
    Get a text string from the game data, with optional string formatting.
    
    Args:
        key_path: Dot-separated path to the text (e.g., 'ui.welcome' or 'game.droid_repaired')
        **format_args: Format arguments for the string
        
    Returns:
        The formatted text string
    """
    data = load_game_data()
    keys = key_path.split('.')
    
    # Navigate through the nested dictionaries
    current = data
    for key in keys:
        if key not in current:
            return f"[MISSING TEXT: {key_path}]"
        current = current[key]
    
    # Format the string if we have format arguments
    if format_args and isinstance(current, str):
        try:
            return current.format(**format_args)
        except (KeyError, IndexError):
            return f"[INVALID FORMAT: {key_path}]"
    
    return current


def load_game_data() -> Dict[str, Any]:
    """
    Load the game data from the JSON file.
    
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
    return data['items'].get(item_id, {})
