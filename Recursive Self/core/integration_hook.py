from memory.subjective_memory_sim import get_subjective_fragment

def inject_subjective_memory(world_state: dict) -> str:
    """
    Determines Bob's current mood from world_state and injects a matching
    subjective memory fragment to enhance realism.
    """
    current_mood = world_state.get("bob_mood", "").lower()
    if not current_mood:
        return ""  # No mood = no subjective memory triggered
    return get_subjective_fragment(current_mood)
