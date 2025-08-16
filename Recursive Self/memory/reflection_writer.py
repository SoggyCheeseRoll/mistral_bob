import os
import json
from datetime import datetime

REFLECTION_FILE = "memory/bob_reflection.json"

def write_reflection_entry(dialogue: str, summary: str, source: str = "main_loop"):
    """
    Stores a reflection into bob_reflection.json with:
    - date-based sorting
    - full dialogue block (user + Bob)
    - emotional summary
    - source label
    - timestamp
    """

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().isoformat()

    entry = {
        "timestamp": timestamp,
        "dialogue": dialogue.strip(),
        "emotional_summary": summary.strip(),
        "source": source
    }

    if not os.path.exists(REFLECTION_FILE):
        data = {today: [entry]}
    else:
        with open(REFLECTION_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        if today not in data:
            data[today] = []

        data[today].append(entry)

    with open(REFLECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    #print(f"[Reflection Entry Written] {timestamp} → {source}") 
