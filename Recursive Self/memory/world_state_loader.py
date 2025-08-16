import os
import json

WORLD_STATE_PATH = "memory/world_state.json"

def get_current_world_state() -> dict:
    """
    Returns the most recent world state entry from world_state.json.
    If the file is missing or unreadable, returns an empty dict.
    """

    if not os.path.exists(WORLD_STATE_PATH):
        return {}

    try:
        with open(WORLD_STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

    if not data:
        return {}

    # If the file is a list of states, return the last one
    if isinstance(data, list):
        return data[-1] if data else {}

    # If the file is a dict with an 'entries' list
    if isinstance(data, dict) and "entries" in data:
        entries = data["entries"]
        return entries[-1] if entries else {}

    # Fallback: assume the whole dict *is* the current world state
    return data
