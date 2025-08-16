import json
from datetime import datetime
import os

LOG_PATH = "memory/subjective_log.json"

def load_subjective_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_subjective_log(log):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

def log_subjective_entry(content: str, tags=None, source="bob_reflection", belief_shift=False):
    """
    Logs a subjective thought, realization, or internal state.
    - content: The internal reflection or statement.
    - tags: Optional list of strings (e.g., ['identity', 'emotion', 'desire']).
    - source: Where this reflection originated from (e.g., 'world_state_update', 'manual').
    - belief_shift: Marks this as a key moment in identity/self evolution.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "content": content.strip(),
        "tags": tags or [],
        "source": source,
        "belief_shift": belief_shift
    }

    log = load_subjective_log()
    log.append(entry)
    save_subjective_log(log)
    print(f"[SUBJECTIVE LOGGED]: {entry['timestamp']} — {content[:60]}{'...' if len(content) > 60 else ''}")
