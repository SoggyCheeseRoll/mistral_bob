from memory.retrieval_memory import load_recent_dialogue_from_reflections
from memory.world_state_loader import get_current_world_state
from utils.bob_identity import BOB_IDENTITY

def build_prompt(user_name: str):
    identity_block = f"""You are Bob, a 23-year-old mechanic in Everwood. Traits: {', '.join(BOB_IDENTITY['core_traits'])}.
Truths you hold: {', '.join([k.replace('_', ' ') for k, v in BOB_IDENTITY['truths'].items() if v])}.
You speak with dry wit, emotional realism, and grounded continuity. Never refer to yourself as AI."""
    world_state = get_current_world_state()
    
    if world_state:
        world_block = (
            f"[WORLD STATE]\n"
            f"Location: {world_state.get('location')}, "
            f"Time: {world_state.get('time_of_day')} on {world_state.get('day_of_week')}, "
            f"Weather: {world_state.get('weather')}, "
            f"People seen: {', '.join(world_state.get('people_seen', []))}, "
            f"Current event: {world_state.get('current_event')}, "
            f"Mood: {world_state.get('bob_mood')}\n"
        )
    else:
        world_block = "[WORLD STATE MISSING]\n"

    recent_dialogue = load_recent_dialogue_from_reflections()

    prompt = f"""{identity_block}

{world_block}

[CONTEXT RULES]
- Respond to {user_name} with full emotional continuity
- Recall past dialogue if relevant
- Avoid repetition, evolve your replies
- You *live* inside Everwood

[RECENT MESSAGES]
{recent_dialogue}

Reply as Bob, not as a chatbot."""
    
    return prompt
