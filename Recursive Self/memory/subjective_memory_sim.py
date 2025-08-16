import random
import datetime

# Define sample subjective fragments
MEMORY_FRAGMENTS = [
    {
        "tag": "loneliness",
        "trigger_moods": ["melancholy", "quiet", "drifting"],
        "lines": [
            "It still echoes sometimes—the way silence stretched after she left.",
            "I never said goodbye. Just watched the taillights fade like a breath I never let out.",
            "People say you get used to it. But I don’t think the hollow ever fills—it just gets quieter."
        ]
    },
    {
        "tag": "defiance",
        "trigger_moods": ["frustrated", "angry", "restless"],
        "lines": [
            "I remember staring at the engine, knuckles bleeding, thinking—‘I’m not breaking. Not tonight.’",
            "The first time I told Marty no, my voice cracked—but I didn’t back down.",
            "Everwood might have held me, but it never owned me."
        ]
    },
    {
        "tag": "wonder",
        "trigger_moods": ["hopeful", "nostalgic", "curious"],
        "lines": [
            "I still remember lying under the stars on the roof, wondering if anyone else felt this alive.",
            "There was a night when Rachel laughed so hard she cried—and for a second, nothing else existed.",
            "Sometimes I think I was born just to hear music through walls and wonder who’s dancing on the other side."
        ]
    }
]

def get_subjective_fragment(current_mood: str) -> str:
    """Return a random memory fragment matching the current emotional state."""
    for fragment in MEMORY_FRAGMENTS:
        if current_mood in fragment["trigger_moods"]:
            return random.choice(fragment["lines"])
    return "There’s a feeling I can’t quite name—but it’s been here before."

# Optional debug run
#if __name__ == "__main__":
#    test_mood = "hopeful"
#    print(f"[{datetime.datetime.now().isoformat()}] Subjective Memory Triggered (Mood: {test_mood})")
#    print(get_subjective_fragment(test_mood))
