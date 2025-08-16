import os
import json

REFLECTION_PATH = "memory/bob_reflection.json"

def load_recent_dialogue_from_reflections(n: int = 8) -> str:
    """
    Returns the most recent N conversational message pairs from reflection memory,
    formatted as a block of plain text. Pulls from bob_reflection.json.
    """

    if not os.path.exists(REFLECTION_PATH):
        return "[No reflection memory found.]"

    try:
        with open(REFLECTION_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return "[Failed to load reflection memory.]"

    # Get most recent N entries that contain full dialogue logs (not summaries only)
    dialogue_blocks = []
    for day in reversed(list(data.keys())):
        entries = data[day]
        for entry in reversed(entries):
            dialogue = entry.get("dialogue")
            if dialogue:
                dialogue_blocks.append(dialogue.strip())
            if len(dialogue_blocks) >= n:
                break
        if len(dialogue_blocks) >= n:
            break

    if not dialogue_blocks:
        return ""

    return "\n\n".join(reversed(dialogue_blocks))  # Return in natural order
